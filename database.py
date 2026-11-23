"""
Agent Gatekeeper - Database Layer
Student: Vansh Sharma | Enrolment: PGD202562849
Company: JPMorgan Chase Bank (Academic Simulation)
Subject: AI & Digital Transformation
"""

import sqlite3
from datetime import datetime
import os
from typing import List, Dict, Optional, Tuple

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gatekeeper.db")


def get_connection():
    """Returns a SQLite connection with row factory configured."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(seed_data: bool = True):
    """
    Initializes SQLite tables for agents and audit logs.
    Optionally populates initial academic simulation seed data.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Agents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            agent_id TEXT PRIMARY KEY,
            agent_name TEXT NOT NULL,
            agent_type TEXT NOT NULL,
            assigned_customer_id TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('ACTIVE', 'REVOKED')),
            registered_at TEXT NOT NULL,
            revoked_at TEXT,
            description TEXT
        )
    """)

    # 2. Audit logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            agent_id TEXT NOT NULL,
            agent_name TEXT,
            customer_id TEXT NOT NULL,
            action TEXT NOT NULL,
            amount REAL,
            recipient_or_biller TEXT,
            decision TEXT NOT NULL CHECK(decision IN ('ALLOW', 'ASK CUSTOMER', 'BLOCK')),
            rule_id TEXT NOT NULL,
            rule_description TEXT NOT NULL,
            risk_level TEXT NOT NULL,
            execution_notes TEXT
        )
    """)

    conn.commit()

    if seed_data:
        # Check if table already has data
        cursor.execute("SELECT COUNT(*) as cnt FROM agents")
        row = cursor.fetchone()
        if row["cnt"] == 0:
            seed_initial_data(cursor)
            conn.commit()

    conn.close()


def seed_initial_data(cursor):
    """Inserts initial active and revoked agents for simulation and testing."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sample_agents = [
        (
            "AGENT-JPMC-101",
            "JPMC Concierge Assistant",
            "Customer Support Bot",
            "CUST-88210",
            "ACTIVE",
            now,
            None,
            "Primary automated concierge for day-to-day balance and utility operations."
        ),
        (
            "AGENT-JPMC-102",
            "Chase Wealth Copilot",
            "Wealth Management Agent",
            "CUST-88210",
            "ACTIVE",
            now,
            None,
            "Personalized wealth management assistant authorized for portfolio review."
        ),
        (
            "AGENT-JPMC-103",
            "AutoPay Bill Agent",
            "Recurring Billing Bot",
            "CUST-94102",
            "ACTIVE",
            now,
            None,
            "Dedicated agent for processing routine utility and bill payments up to limits."
        ),
        (
            "AGENT-JPMC-999",
            "Legacy Compromised Bot",
            "Deprecated Agent",
            "CUST-77419",
            "REVOKED",
            "2026-01-10 09:30:00",
            "2026-02-15 14:15:22",
            "Revoked by JPMC Security Operations Center due to abnormal API activity."
        )
    ]

    cursor.executemany("""
        INSERT INTO agents (
            agent_id, agent_name, agent_type, assigned_customer_id, status, registered_at, revoked_at, description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, sample_agents)


def register_agent(
    agent_id: str,
    agent_name: str,
    agent_type: str,
    assigned_customer_id: str,
    description: str = ""
) -> Tuple[bool, str]:
    """
    Registers a new AI agent with ACTIVE status.
    Returns (success, message).
    """
    if not agent_id or not agent_name or not assigned_customer_id:
        return False, "Agent ID, Agent Name, and Customer ID are required."

    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute("""
            INSERT INTO agents (
                agent_id, agent_name, agent_type, assigned_customer_id, status, registered_at, revoked_at, description
            ) VALUES (?, ?, ?, ?, 'ACTIVE', ?, NULL, ?)
        """, (agent_id.strip(), agent_name.strip(), agent_type.strip(), assigned_customer_id.strip(), now, description.strip()))
        conn.commit()
        return True, f"Agent '{agent_id}' successfully registered."
    except sqlite3.IntegrityError:
        return False, f"Agent with ID '{agent_id}' already exists."
    except Exception as e:
        return False, f"Registration failed: {str(e)}"
    finally:
        conn.close()


def revoke_agent(agent_id: str, reason: str = "") -> Tuple[bool, str]:
    """
    Revokes an existing active agent and records revocation timestamp.
    Returns (success, message).
    """
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("SELECT status, agent_name FROM agents WHERE agent_id = ?", (agent_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return False, f"Agent ID '{agent_id}' not found."

    if row["status"] == "REVOKED":
        conn.close()
        return False, f"Agent '{agent_id}' is already REVOKED."

    desc_update = f" [Revoked on {now}: {reason}]" if reason else f" [Revoked on {now}]"

    cursor.execute("""
        UPDATE agents
        SET status = 'REVOKED',
            revoked_at = ?,
            description = COALESCE(description, '') || ?
        WHERE agent_id = ?
    """, (now, desc_update, agent_id))

    conn.commit()
    conn.close()
    return True, f"Agent '{agent_id}' ({row['agent_name']}) has been successfully REVOKED at {now}."


def reactivate_agent(agent_id: str) -> Tuple[bool, str]:
    """Allows reactivating a revoked agent for testing/demonstration purposes."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("SELECT status, agent_name FROM agents WHERE agent_id = ?", (agent_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False, f"Agent ID '{agent_id}' not found."

    cursor.execute("""
        UPDATE agents
        SET status = 'ACTIVE',
            revoked_at = NULL,
            description = COALESCE(description, '') || ?
        WHERE agent_id = ?
    """, (f" [Reactivated on {now}]", agent_id))
    conn.commit()
    conn.close()
    return True, f"Agent '{agent_id}' reactivated."


def get_agent(agent_id: str) -> Optional[Dict]:
    """Fetches a single agent dictionary by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agents WHERE agent_id = ?", (agent_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def list_agents(status_filter: Optional[str] = None) -> List[Dict]:
    """Lists all agents, optionally filtered by status ('ACTIVE' or 'REVOKED')."""
    conn = get_connection()
    cursor = conn.cursor()
    if status_filter:
        cursor.execute("SELECT * FROM agents WHERE status = ? ORDER BY registered_at DESC", (status_filter,))
    else:
        cursor.execute("SELECT * FROM agents ORDER BY registered_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def log_request(
    request_id: str,
    agent_id: str,
    agent_name: Optional[str],
    customer_id: str,
    action: str,
    amount: Optional[float],
    recipient_or_biller: Optional[str],
    decision: str,
    rule_id: str,
    rule_description: str,
    risk_level: str,
    execution_notes: str = ""
) -> int:
    """Logs an authorization evaluation into the immutable audit_logs table."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO audit_logs (
            request_id, timestamp, agent_id, agent_name, customer_id,
            action, amount, recipient_or_biller, decision, rule_id,
            rule_description, risk_level, execution_notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        request_id, now, agent_id, agent_name or "Unknown Agent",
        customer_id, action, amount, recipient_or_biller or "N/A",
        decision, rule_id, rule_description, risk_level, execution_notes
    ))
    log_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return log_id


def get_audit_logs(limit: int = 100, decision_filter: Optional[str] = None) -> List[Dict]:
    """Retrieves recent audit logs."""
    conn = get_connection()
    cursor = conn.cursor()
    if decision_filter and decision_filter != "ALL":
        cursor.execute("""
            SELECT * FROM audit_logs
            WHERE decision = ?
            ORDER BY log_id DESC LIMIT ?
        """, (decision_filter, limit))
    else:
        cursor.execute("""
            SELECT * FROM audit_logs
            ORDER BY log_id DESC LIMIT ?
        """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_dashboard_stats() -> Dict:
    """Calculates aggregated metrics for the executive dashboard."""
    conn = get_connection()
    cursor = conn.cursor()

    # Agent counts
    cursor.execute("SELECT COUNT(*) as total FROM agents")
    total_agents = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as active FROM agents WHERE status = 'ACTIVE'")
    active_agents = cursor.fetchone()["active"]

    cursor.execute("SELECT COUNT(*) as revoked FROM agents WHERE status = 'REVOKED'")
    revoked_agents = cursor.fetchone()["revoked"]

    # Audit log counts
    cursor.execute("SELECT COUNT(*) as total_requests FROM audit_logs")
    total_requests = cursor.fetchone()["total_requests"]

    cursor.execute("SELECT COUNT(*) as allowed FROM audit_logs WHERE decision = 'ALLOW'")
    allowed_count = cursor.fetchone()["allowed"]

    cursor.execute("SELECT COUNT(*) as ask_customer FROM audit_logs WHERE decision = 'ASK CUSTOMER'")
    ask_customer_count = cursor.fetchone()["ask_customer"]

    cursor.execute("SELECT COUNT(*) as blocked FROM audit_logs WHERE decision = 'BLOCK'")
    blocked_count = cursor.fetchone()["blocked"]

    conn.close()

    return {
        "total_agents": total_agents,
        "active_agents": active_agents,
        "revoked_agents": revoked_agents,
        "total_requests": total_requests,
        "allowed_count": allowed_count,
        "ask_customer_count": ask_customer_count,
        "blocked_count": blocked_count,
        "allow_rate": (allowed_count / total_requests * 100) if total_requests > 0 else 0.0,
        "ask_customer_rate": (ask_customer_count / total_requests * 100) if total_requests > 0 else 0.0,
        "block_rate": (blocked_count / total_requests * 100) if total_requests > 0 else 0.0
    }


def reset_database():
    """Resets database and re-initializes with seed data."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db(seed_data=True)


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_PATH)
    print("Dashboard Stats:", get_dashboard_stats())
