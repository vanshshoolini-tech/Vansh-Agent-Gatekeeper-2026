"""
Agent Gatekeeper - Deterministic Authorization Engine
Student: Vansh Sharma | Enrolment: PGD202562849
Company: JPMorgan Chase Bank (Academic Simulation)
Subject: AI & Digital Transformation

Rule Definitions & Evaluation Hierarchy:
R7: Invalid request, unsupported action or invalid amount -> BLOCK (Precedence: Input Validation)
R1: Unknown agent -> BLOCK (Precedence: Identity Verification)
R2: Revoked agent -> BLOCK (Precedence: Lifecycle Status Verification)
R3: Active agent requesting account balance -> ALLOW (Precedence: Low Risk Read Action)
R4: Active agent making a bill payment of <= ₹5,000 -> ALLOW (Precedence: Autonomous Threshold)
R5: Active agent making a bill payment > ₹5,000 -> ASK CUSTOMER (Precedence: Step-Up Auth)
R6: Active agent requesting a money transfer -> ASK CUSTOMER (Precedence: High Risk Asset Transfer)
"""

import uuid
from typing import Dict, Any, Optional
import database as db

# Constants for Supported Actions
ACTION_BALANCE = "View Account Balance"
ACTION_BILL = "Pay a Bill"
ACTION_TRANSFER = "Transfer Money"
SUPPORTED_ACTIONS = [ACTION_BALANCE, ACTION_BILL, ACTION_TRANSFER]

# Autonomous threshold limit
AUTONOMOUS_BILL_PAYMENT_LIMIT = 5000.0


class GatekeeperDecision:
    ALLOW = "ALLOW"
    ASK_CUSTOMER = "ASK CUSTOMER"
    BLOCK = "BLOCK"


def evaluate_authorization_request(
    agent_id: str,
    action: str,
    amount: Optional[float] = None,
    customer_id: Optional[str] = None,
    recipient_or_biller: Optional[str] = None,
    log_to_db: bool = True
) -> Dict[str, Any]:
    """
    Evaluates an authorization request according to strict corporate banking risk rules.

    Evaluation Priority:
    1. Input Validation Check (R7)
    2. Agent Existence & Identity Check (R1)
    3. Agent Lifecycle Status Check (R2)
    4. Action & Policy Rules (R3, R4, R5, R6)

    Returns a comprehensive result dictionary.
    """
    request_id = f"REQ-JPMC-{uuid.uuid4().hex[:8].upper()}"

    # Normalize inputs
    agent_id = str(agent_id).strip() if agent_id else ""
    action = str(action).strip() if action else ""
    cust_id = str(customer_id).strip() if customer_id else "CUST-DEFAULT"
    recipient = str(recipient_or_biller).strip() if recipient_or_biller else "N/A"

    # --- PRIORITY STEP 1: Rule R7 (Input Validation, Unsupported Action, Invalid Amount) ---
    if not agent_id or action not in SUPPORTED_ACTIONS:
        result = {
            "request_id": request_id,
            "agent_id": agent_id or "UNKNOWN",
            "agent_name": "N/A",
            "customer_id": cust_id,
            "action": action or "UNSPECIFIED",
            "amount": amount,
            "recipient_or_biller": recipient,
            "decision": GatekeeperDecision.BLOCK,
            "rule_id": "R7",
            "rule_description": "Invalid request, unsupported action or invalid amount",
            "risk_level": "CRITICAL",
            "reason": f"Request rejected: Action '{action}' is either unsupported or malformed."
        }
        if log_to_db:
            db.log_request(
                request_id=result["request_id"],
                agent_id=result["agent_id"],
                agent_name=result["agent_name"],
                customer_id=result["customer_id"],
                action=result["action"],
                amount=result["amount"],
                recipient_or_biller=result["recipient_or_biller"],
                decision=result["decision"],
                rule_id=result["rule_id"],
                rule_description=result["rule_description"],
                risk_level=result["risk_level"],
                execution_notes=result["reason"]
            )
        return result

    # For transactional actions, validate the numeric amount
    if action in [ACTION_BILL, ACTION_TRANSFER]:
        try:
            if amount is None:
                raise ValueError("Amount is required")
            numeric_amount = float(amount)
            if numeric_amount <= 0:
                raise ValueError("Amount must be strictly greater than 0")
        except (ValueError, TypeError):
            result = {
                "request_id": request_id,
                "agent_id": agent_id,
                "agent_name": "N/A",
                "customer_id": cust_id,
                "action": action,
                "amount": amount,
                "recipient_or_biller": recipient,
                "decision": GatekeeperDecision.BLOCK,
                "rule_id": "R7",
                "rule_description": "Invalid request, unsupported action or invalid amount",
                "risk_level": "CRITICAL",
                "reason": f"Request rejected: Transactional action '{action}' requires a valid positive numeric amount (received: {amount})."
            }
            if log_to_db:
                db.log_request(
                    request_id=result["request_id"],
                    agent_id=result["agent_id"],
                    agent_name=result["agent_name"],
                    customer_id=result["customer_id"],
                    action=result["action"],
                    amount=0.0,
                    recipient_or_biller=result["recipient_or_biller"],
                    decision=result["decision"],
                    rule_id=result["rule_id"],
                    rule_description=result["rule_description"],
                    risk_level=result["risk_level"],
                    execution_notes=result["reason"]
                )
            return result
    else:
        numeric_amount = 0.0

    # --- PRIORITY STEP 2: Rule R1 (Unknown Agent Check) ---
    agent_record = db.get_agent(agent_id)
    if not agent_record:
        result = {
            "request_id": request_id,
            "agent_id": agent_id,
            "agent_name": "Unknown / Unregistered",
            "customer_id": cust_id,
            "action": action,
            "amount": numeric_amount,
            "recipient_or_biller": recipient,
            "decision": GatekeeperDecision.BLOCK,
            "rule_id": "R1",
            "rule_description": "Unknown agent",
            "risk_level": "HIGH",
            "reason": f"Security violation: Agent identifier '{agent_id}' does not exist in the JPMorgan Chase agent registry."
        }
        if log_to_db:
            db.log_request(
                request_id=result["request_id"],
                agent_id=result["agent_id"],
                agent_name=result["agent_name"],
                customer_id=result["customer_id"],
                action=result["action"],
                amount=result["amount"],
                recipient_or_biller=result["recipient_or_biller"],
                decision=result["decision"],
                rule_id=result["rule_id"],
                rule_description=result["rule_description"],
                risk_level=result["risk_level"],
                execution_notes=result["reason"]
            )
        return result

    agent_name = agent_record.get("agent_name", "Unknown Agent")

    # --- PRIORITY STEP 3: Rule R2 (Revoked Agent Check) ---
    if agent_record.get("status") == "REVOKED":
        result = {
            "request_id": request_id,
            "agent_id": agent_id,
            "agent_name": agent_name,
            "customer_id": agent_record.get("assigned_customer_id", cust_id),
            "action": action,
            "amount": numeric_amount,
            "recipient_or_biller": recipient,
            "decision": GatekeeperDecision.BLOCK,
            "rule_id": "R2",
            "rule_description": "Revoked agent",
            "risk_level": "HIGH",
            "reason": f"Authorization denied: Agent '{agent_id}' ({agent_name}) was revoked on {agent_record.get('revoked_at', 'prior date')} and cannot execute any actions."
        }
        if log_to_db:
            db.log_request(
                request_id=result["request_id"],
                agent_id=result["agent_id"],
                agent_name=result["agent_name"],
                customer_id=result["customer_id"],
                action=result["action"],
                amount=result["amount"],
                recipient_or_biller=result["recipient_or_biller"],
                decision=result["decision"],
                rule_id=result["rule_id"],
                rule_description=result["rule_description"],
                risk_level=result["risk_level"],
                execution_notes=result["reason"]
            )
        return result

    # --- PRIORITY STEP 4: Active Agent Action Rules (R3, R4, R5, R6) ---

    # Rule R3: Active agent requesting account balance -> ALLOW
    if action == ACTION_BALANCE:
        result = {
            "request_id": request_id,
            "agent_id": agent_id,
            "agent_name": agent_name,
            "customer_id": agent_record.get("assigned_customer_id", cust_id),
            "action": action,
            "amount": 0.0,
            "recipient_or_biller": recipient,
            "decision": GatekeeperDecision.ALLOW,
            "rule_id": "R3",
            "rule_description": "Active agent requesting account balance",
            "risk_level": "LOW",
            "reason": f"Autonomous read-only action approved for active agent '{agent_name}'. No financial funds are debited."
        }

    # Rule R4 & R5: Bill Payment
    elif action == ACTION_BILL:
        if numeric_amount <= AUTONOMOUS_BILL_PAYMENT_LIMIT:
            # Rule R4: <= ₹5,000 -> ALLOW
            result = {
                "request_id": request_id,
                "agent_id": agent_id,
                "agent_name": agent_name,
                "customer_id": agent_record.get("assigned_customer_id", cust_id),
                "action": action,
                "amount": numeric_amount,
                "recipient_or_biller": recipient,
                "decision": GatekeeperDecision.ALLOW,
                "rule_id": "R4",
                "rule_description": f"Active agent making a bill payment of ₹{AUTONOMOUS_BILL_PAYMENT_LIMIT:,.0f} or less",
                "risk_level": "LOW",
                "reason": f"Autonomous bill payment of ₹{numeric_amount:,.2f} is within the pre-approved autonomous limit of ₹{AUTONOMOUS_BILL_PAYMENT_LIMIT:,.2f}."
            }
        else:
            # Rule R5: > ₹5,000 -> ASK CUSTOMER
            result = {
                "request_id": request_id,
                "agent_id": agent_id,
                "agent_name": agent_name,
                "customer_id": agent_record.get("assigned_customer_id", cust_id),
                "action": action,
                "amount": numeric_amount,
                "recipient_or_biller": recipient,
                "decision": GatekeeperDecision.ASK_CUSTOMER,
                "rule_id": "R5",
                "rule_description": f"Active agent making a bill payment above ₹{AUTONOMOUS_BILL_PAYMENT_LIMIT:,.0f}",
                "risk_level": "MEDIUM",
                "reason": f"Threshold exceeded: Bill payment of ₹{numeric_amount:,.2f} exceeds the autonomous limit of ₹{AUTONOMOUS_BILL_PAYMENT_LIMIT:,.2f}. Step-up human customer authorization required."
            }

    # Rule R6: Active agent requesting a money transfer -> ASK CUSTOMER
    elif action == ACTION_TRANSFER:
        result = {
            "request_id": request_id,
            "agent_id": agent_id,
            "agent_name": agent_name,
            "customer_id": agent_record.get("assigned_customer_id", cust_id),
            "action": action,
            "amount": numeric_amount,
            "recipient_or_biller": recipient,
            "decision": GatekeeperDecision.ASK_CUSTOMER,
            "rule_id": "R6",
            "rule_description": "Active agent requesting a money transfer",
            "risk_level": "HIGH",
            "reason": f"High-risk operation: Peer-to-peer or external money transfers of ₹{numeric_amount:,.2f} require explicit two-factor customer confirmation."
        }

    else:
        # Fallback safeguard (covered by R7)
        result = {
            "request_id": request_id,
            "agent_id": agent_id,
            "agent_name": agent_name,
            "customer_id": cust_id,
            "action": action,
            "amount": numeric_amount,
            "recipient_or_biller": recipient,
            "decision": GatekeeperDecision.BLOCK,
            "rule_id": "R7",
            "rule_description": "Invalid request, unsupported action or invalid amount",
            "risk_level": "CRITICAL",
            "reason": "Unsupported action encountered."
        }

    # Log to audit trail
    if log_to_db:
        db.log_request(
            request_id=result["request_id"],
            agent_id=result["agent_id"],
            agent_name=result["agent_name"],
            customer_id=result["customer_id"],
            action=result["action"],
            amount=result["amount"],
            recipient_or_biller=result["recipient_or_biller"],
            decision=result["decision"],
            rule_id=result["rule_id"],
            rule_description=result["rule_description"],
            risk_level=result["risk_level"],
            execution_notes=result["reason"]
        )

    return result
