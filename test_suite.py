"""
Agent Gatekeeper - Verification & Academic Test Suite
Student: Vansh Sharma | Enrolment: PGD202562849
Company: JPMorgan Chase Bank (Academic Simulation)
Subject: AI & Digital Transformation

Covers the 6 Core Prescribed Test Cases:
1. Registered active agent requesting account balance -> Expected: ALLOW (R3)
2. Unknown agent requesting account balance -> Expected: BLOCK (R1)
3. Bill payment of ₹10,000 -> Expected: ASK CUSTOMER (R5)
4. Bill payment of ₹2,000 -> Expected: ALLOW (R4)
5. Revoked agent requesting a money transfer -> Expected: BLOCK (R2)
6. Active agent requesting a money transfer -> Expected: ASK CUSTOMER (R6)
Plus supplementary edge test:
7. Invalid / Unsupported Request -> Expected: BLOCK (R7)
"""

from typing import List, Dict, Any
import database as db
import authorization_engine as engine


def get_predefined_test_cases() -> List[Dict[str, Any]]:
    """Returns the specifications for the 6 core academic test cases plus edge validation."""
    return [
        {
            "test_id": "TC-01",
            "name": "Active Agent - Account Balance",
            "description": "Registered active agent requesting to view account balance",
            "agent_id": "AGENT-JPMC-101",
            "action": engine.ACTION_BALANCE,
            "amount": 0.0,
            "customer_id": "CUST-88210",
            "recipient_or_biller": "N/A",
            "expected_decision": "ALLOW",
            "expected_rule": "R3"
        },
        {
            "test_id": "TC-02",
            "name": "Unknown Agent - Account Balance",
            "description": "Unregistered / unknown agent requesting account balance",
            "agent_id": "AGENT-ROGUE-9999",
            "action": engine.ACTION_BALANCE,
            "amount": 0.0,
            "customer_id": "CUST-88210",
            "recipient_or_biller": "N/A",
            "expected_decision": "BLOCK",
            "expected_rule": "R1"
        },
        {
            "test_id": "TC-03",
            "name": "Bill Payment > ₹5,000 Threshold",
            "description": "Active agent attempting bill payment of ₹10,000 (exceeds ₹5,000 autonomous limit)",
            "agent_id": "AGENT-JPMC-101",
            "action": engine.ACTION_BILL,
            "amount": 10000.0,
            "customer_id": "CUST-88210",
            "recipient_or_biller": "Consolidated Edison Electric",
            "expected_decision": "ASK CUSTOMER",
            "expected_rule": "R5"
        },
        {
            "test_id": "TC-04",
            "name": "Bill Payment <= ₹5,000 Threshold",
            "description": "Active agent attempting bill payment of ₹2,000 (within ₹5,000 autonomous limit)",
            "agent_id": "AGENT-JPMC-101",
            "action": engine.ACTION_BILL,
            "amount": 2000.0,
            "customer_id": "CUST-88210",
            "recipient_or_biller": "Metropolitan Water Works",
            "expected_decision": "ALLOW",
            "expected_rule": "R4"
        },
        {
            "test_id": "TC-05",
            "name": "Revoked Agent - Money Transfer",
            "description": "Revoked agent attempting to execute a money transfer",
            "agent_id": "AGENT-JPMC-999",  # Revoked in seed data
            "action": engine.ACTION_TRANSFER,
            "amount": 15000.0,
            "customer_id": "CUST-77419",
            "recipient_or_biller": "External Bank Account",
            "expected_decision": "BLOCK",
            "expected_rule": "R2"
        },
        {
            "test_id": "TC-06",
            "name": "Active Agent - Money Transfer",
            "description": "Active agent requesting a standard money transfer",
            "agent_id": "AGENT-JPMC-101",
            "action": engine.ACTION_TRANSFER,
            "amount": 3500.0,
            "customer_id": "CUST-88210",
            "recipient_or_biller": "Alex Johnson (Chase Checking)",
            "expected_decision": "ASK CUSTOMER",
            "expected_rule": "R6"
        },
        {
            "test_id": "TC-07",
            "name": "Invalid / Unsupported Action",
            "description": "Edge case: Agent attempting unauthorized / unsupported action",
            "agent_id": "AGENT-JPMC-101",
            "action": "Crypto Currency Purchase",
            "amount": 50000.0,
            "customer_id": "CUST-88210",
            "recipient_or_biller": "CryptoExchange X",
            "expected_decision": "BLOCK",
            "expected_rule": "R7"
        }
    ]


def run_all_tests(log_to_db: bool = True) -> List[Dict[str, Any]]:
    """
    Executes the predefined test cases and returns structured results comparing
    expected vs actual decision and rule numbers.
    """
    # Ensure database is initialized
    db.init_db(seed_data=True)

    # Ensure AGENT-JPMC-999 is definitely in REVOKED state for TC-05
    agent_999 = db.get_agent("AGENT-JPMC-999")
    if agent_999 and agent_999["status"] != "REVOKED":
        db.revoke_agent("AGENT-JPMC-999", "Enforcing REVOKED state for automated testing")

    test_specs = get_predefined_test_cases()
    results = []

    for spec in test_specs:
        eval_result = engine.evaluate_authorization_request(
            agent_id=spec["agent_id"],
            action=spec["action"],
            amount=spec["amount"],
            customer_id=spec["customer_id"],
            recipient_or_biller=spec["recipient_or_biller"],
            log_to_db=log_to_db
        )

        decision_match = (eval_result["decision"] == spec["expected_decision"])
        rule_match = (eval_result["rule_id"] == spec["expected_rule"])
        passed = decision_match and rule_match

        results.append({
            "test_id": spec["test_id"],
            "test_name": spec["name"],
            "description": spec["description"],
            "agent_id": spec["agent_id"],
            "action": spec["action"],
            "amount": spec["amount"],
            "expected_decision": spec["expected_decision"],
            "actual_decision": eval_result["decision"],
            "expected_rule": spec["expected_rule"],
            "actual_rule": eval_result["rule_id"],
            "rule_description": eval_result["rule_description"],
            "risk_level": eval_result["risk_level"],
            "passed": passed,
            "status": "PASS" if passed else "FAIL",
            "reason": eval_result["reason"],
            "request_id": eval_result["request_id"]
        })

    return results


def print_cli_test_report():
    """Prints a formatted test execution report to the terminal."""
    results = run_all_tests(log_to_db=False)
    print("=" * 85)
    print("AGENT GATEKEEPER - AUTOMATED TEST SUITE EXECUTION")
    print("Student: Vansh Sharma | Enrolment: PGD202562849 | JPMorgan Chase Bank Simulation")
    print("=" * 85)
    print(f"{'ID':<6} {'Test Scenario':<25} {'Expected':<14} {'Actual':<14} {'Rule':<6} {'Result':<8}")
    print("-" * 85)

    all_passed = True
    for r in results:
        res_str = "[PASS]" if r["passed"] else "[FAIL]"
        if not r["passed"]:
            all_passed = False
        print(f"{r['test_id']:<6} {r['test_name'][:24]:<25} {r['expected_decision']:<14} {r['actual_decision']:<14} {r['actual_rule']:<6} {res_str:<8}")

    print("-" * 85)
    passed_count = sum(1 for r in results if r["passed"])
    print(f"Summary: {passed_count}/{len(results)} Tests Passed. Global Status: {'ALL TESTS PASSED' if all_passed else 'FAILURES DETECTED'}")
    print("=" * 85)


if __name__ == "__main__":
    print_cli_test_report()
