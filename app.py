"""
Agent Gatekeeper – AI Agent Authorization & Risk Management System
Student: Vansh Sharma | Enrolment Number: PGD202562849
Company Selected: JPMorgan Chase Bank (Academic Simulation)
Subject: AI & Digital Transformation (MBA Programme)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

import database as db
import authorization_engine as engine
import test_suite

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="Agent Gatekeeper | JPMorgan Chase (Academic Simulation)",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database
db.init_db(seed_data=True)

# Custom Styling (JPMorgan Chase Corporate Palette: Deep Navy, Gold, Crisp Slate)
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #F8FAFC;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    
    /* Top Banner */
    .jpmc-header {
        background: linear-gradient(135deg, #0A2540 0%, #1A365D 50%, #0F172A 100%);
        color: white;
        padding: 24px 30px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.12);
        border-left: 6px solid #D4AF37;
    }
    
    .jpmc-title {
        font-size: 26px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 0;
        color: #FFFFFF;
    }
    
    .jpmc-subtitle {
        font-size: 14px;
        color: #94A3B8;
        margin-top: 6px;
        margin-bottom: 0px;
    }
    
    .student-badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-top: 14px;
    }
    
    .student-pill {
        background-color: rgba(255, 255, 255, 0.12);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        color: #F1F5F9;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .student-pill strong {
        color: #FBBF24;
    }
    
    .disclaimer-box {
        background-color: #FEF3C7;
        border-left: 4px solid #F59E0B;
        padding: 10px 16px;
        border-radius: 6px;
        color: #92400E;
        font-size: 12px;
        margin-top: 12px;
        font-weight: 500;
    }
    
    /* KPI Card */
    .kpi-card {
        background: white;
        padding: 18px 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #E2E8F0;
        border-top: 4px solid #0A2540;
    }
    
    .kpi-label {
        font-size: 12px;
        text-transform: uppercase;
        font-weight: 600;
        color: #64748B;
        letter-spacing: 0.5px;
    }
    
    .kpi-value {
        font-size: 28px;
        font-weight: 700;
        color: #0A2540;
        margin-top: 4px;
    }
    
    .kpi-sub {
        font-size: 12px;
        color: #94A3B8;
        margin-top: 4px;
    }

    /* Decision Result Box */
    .decision-card-allow {
        background: #ECFDF5;
        border: 2px solid #10B981;
        border-radius: 10px;
        padding: 20px;
        color: #065F46;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.15);
    }
    
    .decision-card-ask {
        background: #FFFBEB;
        border: 2px solid #F59E0B;
        border-radius: 10px;
        padding: 20px;
        color: #92400E;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.15);
    }
    
    .decision-card-block {
        background: #FEF2F2;
        border: 2px solid #EF4444;
        border-radius: 10px;
        padding: 20px;
        color: #991B1B;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.15);
    }
</style>
""", unsafe_allow_html=True)

# Top Header Banner with Student and Academic Metadata
st.markdown("""
<div class="jpmc-header">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
        <div>
            <div class="jpmc-title">🛡️ AGENT GATEKEEPER</div>
            <div class="jpmc-subtitle">AI Agent Authorization & Risk Management Gateway | Autonomous Banking Governance</div>
        </div>
        <div style="text-align: right; margin-top: 4px;">
            <span style="background: #D4AF37; color: #0A2540; font-weight: 700; font-size: 11px; padding: 4px 10px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.5px;">
                JPMorgan Chase Simulation
            </span>
        </div>
    </div>
    <div class="student-badge-container">
        <div class="student-pill">👤 Student: <strong>Vansh Sharma</strong></div>
        <div class="student-pill">🎓 Enrolment No: <strong>PGD202562849</strong></div>
        <div class="student-pill">📘 Subject: <strong>AI & Digital Transformation</strong></div>
        <div class="student-pill">🏦 Target Institution: <strong>JPMorgan Chase Bank</strong></div>
    </div>
    <div class="disclaimer-box">
        ⚠️ <strong>Academic Simulation Disclaimer:</strong> This application is an educational prototype developed independently by Vansh Sharma (PGD202562849) for academic demonstration. It does not use live banking infrastructure or real customer financial records.
    </div>
</div>
""", unsafe_allow_html=True)

# List of All Distinct Navigation Modules
PAGES = [
    "🏛️ Executive Dashboard",
    "⚡ Authorization Request",
    "➕ Agent Registration",
    "🚫 Agent Revocation",
    "📋 Audit Logs & Traceability",
    "🧪 MBA Test Suite & Verification",
    "📖 Project Info & Rule Governance"
]

# Initialize Session State Navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏛️ Executive Dashboard"

def navigate_to(page_name: str):
    """Reliable callback executed on button click to switch active module."""
    st.session_state.current_page = page_name

# Sidebar Controls & Secondary Navigation
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/J_P_Morgan_Logo_2008_1.svg/320px-J_P_Morgan_Logo_2008_1.svg.png", width=180)
    st.markdown("### **Navigation Menu**")
    
    for idx, page_name in enumerate(PAGES):
        is_active = (st.session_state.current_page == page_name)
        st.button(
            page_name,
            key=f"sidebar_nav_btn_{idx}",
            on_click=navigate_to,
            args=(page_name,),
            type="primary" if is_active else "secondary",
            use_container_width=True
        )

    st.markdown("---")
    st.markdown("#### **Executive Artifacts**")
    try:
        with open("Agent_Gatekeeper_Project_Report.pdf", "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
        st.download_button(
            label="📄 Download 2-Page PDF Report",
            data=pdf_bytes,
            file_name="Agent_Gatekeeper_Project_Report_Vansh_Sharma.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception:
        pass

    st.markdown("#### **Governance Policy Controls**")
    st.info(f"**Autonomous Bill Limit:** ₹{engine.AUTONOMOUS_BILL_PAYMENT_LIMIT:,.0f}\n\n*Transactions above this threshold trigger Step-Up Customer Verification (Rule R5).*")
    
    st.markdown("---")
    st.markdown("#### **System Utilities**")
    if st.button("🔄 Reset Database to Clean State", use_container_width=True):
        db.reset_database()
        st.success("Database restored to default academic simulation state.")
        st.rerun()

    st.markdown("""
    <div style="font-size: 11px; color: #64748B; margin-top: 25px; text-align: center;">
        Developed by <strong>Vansh Sharma</strong><br>
        Enrolment: PGD202562849<br>
        MBA AI & Digital Transformation
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------------------------------------------
# PRIMARY TOP NAVIGATION BAR (Visible across all screens and devices)
# -------------------------------------------------------------------------------------------------
st.markdown("##### 🧭 **System Navigation Bar**")
top_cols = st.columns(len(PAGES))
short_labels = [
    "🏛️ Dashboard",
    "⚡ Auth Request",
    "➕ Register Agent",
    "🚫 Revoke Agent",
    "📋 Audit Logs",
    "🧪 Test Suite",
    "📖 Project Info"
]

for idx, (page_name, short_label) in enumerate(zip(PAGES, short_labels)):
    is_active = (st.session_state.current_page == page_name)
    top_cols[idx].button(
        short_label,
        key=f"top_nav_btn_{idx}",
        on_click=navigate_to,
        args=(page_name,),
        type="primary" if is_active else "secondary",
        use_container_width=True
    )

st.markdown("<hr style='margin-top: 10px; margin-bottom: 20px; border-color: #E2E8F0;'>", unsafe_allow_html=True)


# =================================================================================================
# MODULE 1: EXECUTIVE DASHBOARD
# =================================================================================================
if st.session_state.current_page == "🏛️ Executive Dashboard":
    st.subheader("🏛️ Executive Governance Dashboard")
    st.markdown("High-level oversight of registered autonomous AI agents, risk distribution, and deterministic gatekeeper decisions.")
    
    stats = db.get_dashboard_stats()
    
    # KPI Row
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Registered Agents</div>
            <div class="kpi-value">{stats['total_agents']}</div>
            <div class="kpi-sub">{stats['active_agents']} Active | {stats['revoked_agents']} Revoked</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Invocations</div>
            <div class="kpi-value">{stats['total_requests']}</div>
            <div class="kpi-sub">Lifetime Audit Records</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="kpi-card" style="border-top-color: #10B981;">
            <div class="kpi-label">Allowed (R3, R4)</div>
            <div class="kpi-value" style="color: #10B981;">{stats['allowed_count']}</div>
            <div class="kpi-sub">{stats['allow_rate']:.1f}% Autonomous Approval</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="kpi-card" style="border-top-color: #F59E0B;">
            <div class="kpi-label">Ask Customer (R5, R6)</div>
            <div class="kpi-value" style="color: #F59E0B;">{stats['ask_customer_count']}</div>
            <div class="kpi-sub">{stats['ask_customer_rate']:.1f}% Human-in-the-Loop</div>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
        <div class="kpi-card" style="border-top-color: #EF4444;">
            <div class="kpi-label">Blocked (R1, R2, R7)</div>
            <div class="kpi-value" style="color: #EF4444;">{stats['blocked_count']}</div>
            <div class="kpi-sub">{stats['block_rate']:.1f}% Security Mitigations</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Jump Links (Direct access to Authorization, Registration, Revocation, and Tests)
    st.markdown("##### ⚡ **Quick Operations & Direct Shortcuts**")
    q1, q2, q3, q4 = st.columns(4)
    with q1:
        st.button(
            "⚡ **Submit Authorization Request**\n\n*Test actions against Gatekeeper*",
            key="quick_auth",
            on_click=navigate_to,
            args=("⚡ Authorization Request",),
            use_container_width=True
        )
    with q2:
        st.button(
            "➕ **Register New AI Agent**\n\n*Enroll new bot into registry*",
            key="quick_reg",
            on_click=navigate_to,
            args=("➕ Agent Registration",),
            use_container_width=True
        )
    with q3:
        st.button(
            "🚫 **Revoke AI Agent**\n\n*De-provision agent permissions*",
            key="quick_rev",
            on_click=navigate_to,
            args=("🚫 Agent Revocation",),
            use_container_width=True
        )
    with q4:
        st.button(
            "🧪 **Run MBA Test Suite**\n\n*Validate all 6 core test cases*",
            key="quick_test",
            on_click=navigate_to,
            args=("🧪 MBA Test Suite & Verification",),
            use_container_width=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts Row
    chart_col1, chart_col2 = st.columns([1, 1])

    with chart_col1:
        st.markdown("##### **Gatekeeper Decision Distribution**")
        if stats['total_requests'] > 0:
            decision_df = pd.DataFrame({
                "Decision": ["ALLOW", "ASK CUSTOMER", "BLOCK"],
                "Count": [stats["allowed_count"], stats["ask_customer_count"], stats["blocked_count"]]
            })
            fig_pie = px.pie(
                decision_df,
                values="Count",
                names="Decision",
                color="Decision",
                color_discrete_map={
                    "ALLOW": "#10B981",
                    "ASK CUSTOMER": "#F59E0B",
                    "BLOCK": "#EF4444"
                },
                hole=0.55
            )
            fig_pie.update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                height=280,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No authorization requests logged yet. Submit a request or run the Test Suite to populate analytics.")

    with chart_col2:
        st.markdown("##### **Agent Status & Fleet Health**")
        agent_df = pd.DataFrame({
            "Status": ["Active Agents", "Revoked Agents"],
            "Count": [stats["active_agents"], stats["revoked_agents"]]
        })
        fig_bar = px.bar(
            agent_df,
            x="Status",
            y="Count",
            color="Status",
            color_discrete_map={
                "Active Agents": "#0A2540",
                "Revoked Agents": "#94A3B8"
            },
            text="Count"
        )
        fig_bar.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            height=280,
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Recent Audit Stream Preview
    st.markdown("##### **Recent Gatekeeper Invocations**")
    recent_logs = db.get_audit_logs(limit=5)
    if recent_logs:
        rec_df = pd.DataFrame(recent_logs)[[
            "request_id", "timestamp", "agent_id", "action", "amount", "decision", "rule_id", "risk_level"
        ]]
        rec_df["amount"] = rec_df["amount"].apply(lambda x: f"₹{x:,.2f}" if x and x > 0 else "N/A")
        st.dataframe(rec_df, use_container_width=True, hide_index=True)
    else:
        st.write("No recent invocations found.")


# =================================================================================================
# MODULE 2: AUTHORIZATION REQUEST (GATEKEEPER FORM & EVALUATION)
# =================================================================================================
elif st.session_state.current_page == "⚡ Authorization Request":
    st.subheader("⚡ Gatekeeper Authorization Request")
    st.markdown("Submit a simulated real-time banking action request to observe the Gatekeeper's deterministic risk decision.")

    agents_list = db.list_agents()
    agent_options = {f"{a['agent_id']} - {a['agent_name']} ({a['status']})": a['agent_id'] for a in agents_list}
    agent_options["[TEST SCENARIO] Unknown Rogue Agent (Not in Registry)"] = "AGENT-ROGUE-9999"

    form_col, result_col = st.columns([1.1, 1.2])

    with form_col:
        st.markdown("#### **1. Submit Agent Action Request Form**")
        with st.form("authorization_request_form"):
            selected_agent_key = st.selectbox(
                "Select Initiating AI Agent:",
                options=list(agent_options.keys()),
                help="Select a registered agent or test perimeter defense with an unknown rogue agent."
            )
            agent_id = agent_options[selected_agent_key]

            # Option to manually type any custom agent ID
            custom_id_toggle = st.checkbox("Enter Custom / External Agent ID manually")
            if custom_id_toggle:
                agent_id = st.text_input("Custom Agent ID:", value="AGENT-EXTERNAL-001")

            customer_id = st.text_input("Target Customer ID:", value="CUST-88210")

            action = st.selectbox(
                "Requested Banking Action:",
                options=[
                    engine.ACTION_BALANCE,
                    engine.ACTION_BILL,
                    engine.ACTION_TRANSFER,
                    "Unsupported Action (Test R7 Edge Case)"
                ]
            )

            # Amount input is enabled for transactional operations
            if action in [engine.ACTION_BILL, engine.ACTION_TRANSFER]:
                amount = st.number_input(
                    "Transaction Amount (₹):",
                    min_value=0.0,
                    value=2000.0 if action == engine.ACTION_BILL else 10000.0,
                    step=500.0,
                    help=f"Note: Autonomous limit for bill payments is ₹{engine.AUTONOMOUS_BILL_PAYMENT_LIMIT:,.0f}."
                )
                if action == engine.ACTION_BILL:
                    recipient = st.text_input("Biller / Payee Name:", value="Consolidated Edison Utility")
                else:
                    recipient = st.text_input("Recipient Account / Payee:", value="External Chase Checking (Acc: 9812)")
            else:
                amount = 0.0
                recipient = "JPMorgan Chase Internal"
                st.caption("ℹ️ Read-only inquiries do not require a monetary transaction amount.")

            submitted = st.form_submit_button("⚡ Evaluate Authorization Request", use_container_width=True)

    with result_col:
        st.markdown("#### **2. Gatekeeper Decision & Evaluation Trace**")
        
        if submitted:
            with st.spinner("Processing through Corporate Gatekeeper Rules R1 - R7..."):
                eval_res = engine.evaluate_authorization_request(
                    agent_id=agent_id,
                    action=action,
                    amount=amount,
                    customer_id=customer_id,
                    recipient_or_biller=recipient,
                    log_to_db=True
                )

            dec = eval_res["decision"]
            rule = eval_res["rule_id"]

            if dec == "ALLOW":
                st.markdown(f"""
                <div class="decision-card-allow">
                    <div style="font-size: 22px; font-weight: 700; display: flex; align-items: center; gap: 8px;">
                        <span>✅ DECISION: ALLOW</span>
                        <span style="font-size: 13px; background: #10B981; color: white; padding: 2px 10px; border-radius: 12px;">{rule}</span>
                    </div>
                    <div style="margin-top: 10px; font-size: 15px; font-weight: 600;">{eval_res['rule_description']}</div>
                    <p style="margin-top: 8px; font-size: 13px; line-height: 1.5;">{eval_res['reason']}</p>
                    <hr style="border-color: #A7F3D0; margin: 12px 0;">
                    <div style="font-size: 12px; display: flex; justify-content: space-between;">
                        <span><strong>Request ID:</strong> {eval_res['request_id']}</span>
                        <span><strong>Risk Level:</strong> <span style="color: #047857; font-weight: 700;">{eval_res['risk_level']}</span></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.success("Transaction autonomously executed. Audit log committed to SQLite.")

            elif dec == "ASK CUSTOMER":
                st.markdown(f"""
                <div class="decision-card-ask">
                    <div style="font-size: 22px; font-weight: 700; display: flex; align-items: center; gap: 8px;">
                        <span>⚠️ DECISION: ASK CUSTOMER</span>
                        <span style="font-size: 13px; background: #F59E0B; color: white; padding: 2px 10px; border-radius: 12px;">{rule}</span>
                    </div>
                    <div style="margin-top: 10px; font-size: 15px; font-weight: 600;">{eval_res['rule_description']}</div>
                    <p style="margin-top: 8px; font-size: 13px; line-height: 1.5;">{eval_res['reason']}</p>
                    <hr style="border-color: #FDE68A; margin: 12px 0;">
                    <div style="font-size: 12px; display: flex; justify-content: space-between;">
                        <span><strong>Request ID:</strong> {eval_res['request_id']}</span>
                        <span><strong>Risk Level:</strong> <span style="color: #B45309; font-weight: 700;">{eval_res['risk_level']}</span></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Interactive Customer Step-up simulation
                st.markdown("##### **Simulated Human-in-the-Loop Step-Up Verification**")
                st.write(f"📲 *Push notification dispatched to JPMorgan Chase Mobile App for customer `{customer_id}`:*")
                c_col1, c_col2 = st.columns(2)
                with c_col1:
                    if st.button("👍 Customer Approves (Enter OTP 7821)", key="approve_stepup", use_container_width=True):
                        st.balloons()
                        st.success(f"Customer approved request {eval_res['request_id']}. Transaction finalized under Human Governance.")
                with c_col2:
                    if st.button("🛑 Customer Denies / Flags Suspicious", key="deny_stepup", use_container_width=True):
                        st.error(f"Customer rejected request {eval_res['request_id']}. Security incident flagged.")

            else:  # BLOCK
                st.markdown(f"""
                <div class="decision-card-block">
                    <div style="font-size: 22px; font-weight: 700; display: flex; align-items: center; gap: 8px;">
                        <span>🛑 DECISION: BLOCK</span>
                        <span style="font-size: 13px; background: #EF4444; color: white; padding: 2px 10px; border-radius: 12px;">{rule}</span>
                    </div>
                    <div style="margin-top: 10px; font-size: 15px; font-weight: 600;">{eval_res['rule_description']}</div>
                    <p style="margin-top: 8px; font-size: 13px; line-height: 1.5;">{eval_res['reason']}</p>
                    <hr style="border-color: #FECACA; margin: 12px 0;">
                    <div style="font-size: 12px; display: flex; justify-content: space-between;">
                        <span><strong>Request ID:</strong> {eval_res['request_id']}</span>
                        <span><strong>Risk Level:</strong> <span style="color: #B91C1C; font-weight: 700;">{eval_res['risk_level']}</span></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.error("Operation halted by Gatekeeper Security Perimeter. Incident recorded.")
        else:
            st.info("👈 Select an agent and action on the left, then click 'Evaluate Authorization Request' to test the Gatekeeper.")


# =================================================================================================
# MODULE 3: AGENT REGISTRATION
# =================================================================================================
elif st.session_state.current_page == "➕ Agent Registration":
    st.subheader("➕ AI Agent Registration")
    st.markdown("Register new autonomous AI agents into the JPMorgan Chase cryptographic agent registry with ACTIVE status.")

    reg_col, info_col = st.columns([1.2, 1])

    with reg_col:
        st.markdown("#### **Agent Registration Form**")
        with st.form("agent_registration_form"):
            new_agent_id = st.text_input(
                "Agent Identifier:",
                value=f"AGENT-JPMC-{len(db.list_agents()) + 101}",
                help="Unique alphanumeric ID for the AI agent (e.g., AGENT-JPMC-104)."
            )
            new_agent_name = st.text_input(
                "Agent Name:",
                value="Chase Automated Advisory Bot",
                help="Descriptive name of the agent."
            )
            new_agent_type = st.selectbox(
                "Agent Role / Archetype:",
                [
                    "Customer Support Bot",
                    "Wealth Management Agent",
                    "Recurring Billing Bot",
                    "Autonomous Financial Assistant",
                    "Algorithmic Portfolio Rebalancer"
                ]
            )
            new_customer_id = st.text_input(
                "Assigned Customer ID:",
                value="CUST-88210",
                help="Customer account that this agent is delegated to assist."
            )
            new_description = st.text_area(
                "Scope & Operational Purpose:",
                value="Automated agent authorized for client financial operations within policy limits."
            )

            submitted_reg = st.form_submit_button("💾 Complete Agent Registration", use_container_width=True)
            if submitted_reg:
                success, msg = db.register_agent(
                    agent_id=new_agent_id,
                    agent_name=new_agent_name,
                    agent_type=new_agent_type,
                    assigned_customer_id=new_customer_id,
                    description=new_description
                )
                if success:
                    st.success(f"✅ {msg}")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

    with info_col:
        st.markdown("#### **Registration Guidance**")
        st.info("""
        **Enterprise Best Practices (JPMorgan Chase):**
        - Every agent must have a verified customer binding (`assigned_customer_id`).
        - Newly registered agents start with `ACTIVE` status.
        - Agent permissions are bounded by Gatekeeper rules R3 through R6.
        - If an agent is compromised, use **Agent Revocation** to strip permissions immediately.
        """)

        st.button(
            "🚫 Go to Agent Revocation",
            key="goto_revocation_from_reg",
            on_click=navigate_to,
            args=("🚫 Agent Revocation",),
            use_container_width=True
        )

    st.markdown("---")
    st.markdown("#### **Current Agent Registry (SQLite)**")
    all_agents = db.list_agents()
    if all_agents:
        agents_df = pd.DataFrame(all_agents)[[
            "agent_id", "agent_name", "agent_type", "assigned_customer_id", "status", "registered_at", "revoked_at", "description"
        ]]
        st.dataframe(agents_df, use_container_width=True, hide_index=True)
    else:
        st.write("No agents found in database.")


# =================================================================================================
# MODULE 4: AGENT REVOCATION
# =================================================================================================
elif st.session_state.current_page == "🚫 Agent Revocation":
    st.subheader("🚫 AI Agent Revocation & Credential De-provisioning")
    st.markdown("Revoke an AI agent's operational privileges. Revoked agents immediately trigger Rule R2 (BLOCK) on all subsequent requests.")

    rev_col, react_col = st.columns([1.2, 1])

    with rev_col:
        st.markdown("#### **Revoke an Existing AI Agent**")
        st.warning("⚠️ Revoking an agent immediately strips all authorization permissions. The exact date and timestamp are recorded in the audit trail.")

        active_agents = db.list_agents(status_filter="ACTIVE")
        if active_agents:
            rev_options = {f"{a['agent_id']} - {a['agent_name']} (Customer: {a['assigned_customer_id']})": a['agent_id'] for a in active_agents}
            selected_rev = st.selectbox("Select Active Agent to Revoke:", options=list(rev_options.keys()))
            target_agent_id = rev_options[selected_rev]
            revoke_reason = st.text_input("Reason for Revocation:", value="Routine credential cycling / Suspicious anomaly detection")

            if st.button("🚨 Confirm Agent Revocation", type="primary", use_container_width=True):
                success, msg = db.revoke_agent(target_agent_id, revoke_reason)
                if success:
                    st.success(f"✅ {msg}")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")
        else:
            st.info("No active agents available for revocation.")

    with react_col:
        st.markdown("#### **Reactivate Agent (Testing Utility)**")
        st.caption("Re-activate a revoked agent for testing or academic demonstration.")
        revoked_agents = db.list_agents(status_filter="REVOKED")
        if revoked_agents:
            react_options = {f"{a['agent_id']} - {a['agent_name']} (Revoked on: {a['revoked_at']})": a['agent_id'] for a in revoked_agents}
            selected_react = st.selectbox("Select Revoked Agent to Reactivate:", options=list(react_options.keys()))
            react_agent_id = react_options[selected_react]
            if st.button("🔄 Reactivate Selected Agent", use_container_width=True):
                success, msg = db.reactivate_agent(react_agent_id)
                if success:
                    st.success(f"✅ {msg}")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")
        else:
            st.info("No revoked agents currently in registry.")

        st.markdown("---")
        st.button(
            "➕ Go to Agent Registration",
            key="goto_reg_from_revocation",
            on_click=navigate_to,
            args=("➕ Agent Registration",),
            use_container_width=True
        )

    st.markdown("---")
    st.markdown("#### **Revoked Agents Log**")
    revoked_list = db.list_agents(status_filter="REVOKED")
    if revoked_list:
        rev_df = pd.DataFrame(revoked_list)[[
            "agent_id", "agent_name", "assigned_customer_id", "status", "registered_at", "revoked_at", "description"
        ]]
        st.dataframe(rev_df, use_container_width=True, hide_index=True)
    else:
        st.info("No revoked agents found.")


# =================================================================================================
# MODULE 5: AUDIT LOGS & TRACEABILITY
# =================================================================================================
elif st.session_state.current_page == "📋 Audit Logs & Traceability":
    st.subheader("📋 Immutable Audit Logs & Governance Traceability")
    st.markdown("Every evaluation made by the Agent Gatekeeper is permanently captured with timestamps, rule identifiers, risk levels, and decision context.")

    filter_col1, filter_col2, filter_col3 = st.columns([1, 1, 1])
    with filter_col1:
        dec_filter = st.selectbox("Filter by Decision:", ["ALL", "ALLOW", "ASK CUSTOMER", "BLOCK"])
    with filter_col2:
        log_limit = st.slider("Record Limit:", min_value=10, max_value=200, value=50, step=10)
    with filter_col3:
        search_kw = st.text_input("Search Agent ID / Customer ID / Request ID:", value="")

    logs = db.get_audit_logs(limit=log_limit, decision_filter=dec_filter)

    if logs:
        log_df = pd.DataFrame(logs)
        if search_kw:
            log_df = log_df[
                log_df["agent_id"].str.contains(search_kw, case=False, na=False) |
                log_df["customer_id"].str.contains(search_kw, case=False, na=False) |
                log_df["request_id"].str.contains(search_kw, case=False, na=False)
            ]

        display_cols = [
            "log_id", "request_id", "timestamp", "agent_id", "action", "amount",
            "decision", "rule_id", "risk_level", "execution_notes"
        ]
        st.dataframe(log_df[display_cols], use_container_width=True, hide_index=True)

        # CSV Download
        csv_data = log_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Audit Logs as CSV",
            data=csv_data,
            file_name=f"agent_gatekeeper_audit_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("No audit logs found matching the selected filter criteria.")


# =================================================================================================
# MODULE 6: MBA TEST SUITE & VERIFICATION
# =================================================================================================
elif st.session_state.current_page == "🧪 MBA Test Suite & Verification":
    st.subheader("🧪 MBA Academic Test Suite & Validation")
    st.markdown("Automated validation of the six mandatory core academic test cases specified in the project guidelines.")

    st.markdown("""
    | Test Case | Scenario Description | Expected Decision | Expected Rule |
    | :--- | :--- | :---: | :---: |
    | **TC-01** | Registered active agent requesting account balance | **ALLOW** | **R3** |
    | **TC-02** | Unknown agent requesting account balance | **BLOCK** | **R1** |
    | **TC-03** | Bill payment of ₹10,000 (exceeds ₹5,000 limit) | **ASK CUSTOMER** | **R5** |
    | **TC-04** | Bill payment of ₹2,000 (within ₹5,000 limit) | **ALLOW** | **R4** |
    | **TC-05** | Revoked agent requesting a money transfer | **BLOCK** | **R2** |
    | **TC-06** | Active agent requesting a money transfer | **ASK CUSTOMER** | **R6** |
    | **TC-07 (Edge)** | Invalid / Unsupported action | **BLOCK** | **R7** |
    """)

    if st.button("🚀 Execute Complete Test Suite", type="primary", use_container_width=True):
        with st.spinner("Executing test scenarios against Gatekeeper engine..."):
            test_results = test_suite.run_all_tests(log_to_db=True)

        passed_count = sum(1 for t in test_results if t["passed"])
        total_tests = len(test_results)
        all_passed = (passed_count == total_tests)

        t_col1, t_col2, t_col3 = st.columns(3)
        with t_col1:
            st.metric("Total Scenarios Tested", total_tests)
        with t_col2:
            st.metric("Passed Tests", passed_count, delta=f"{passed_count}/{total_tests}")
        with t_col3:
            st.metric("Failed Tests", total_tests - passed_count)

        if all_passed:
            st.success(f"🎉 **100% Academic Validation Passed ({passed_count}/{total_tests}).** All rules R1 through R7 evaluated in exact priority order.")
        else:
            st.error(f"⚠️ Validation Anomaly: {total_tests - passed_count} test(s) failed.")

        # Results table
        res_df = pd.DataFrame(test_results)[[
            "test_id", "test_name", "agent_id", "action", "amount",
            "expected_decision", "actual_decision", "expected_rule", "actual_rule", "status"
        ]]
        st.dataframe(res_df, use_container_width=True, hide_index=True)


# =================================================================================================
# MODULE 7: PROJECT INFO & RULE GOVERNANCE
# =================================================================================================
elif st.session_state.current_page == "📖 Project Info & Rule Governance":
    st.subheader("📖 Project Overview, Governance Architecture & Business Impact")

    st.markdown("""
    ### 1. Student & Institutional Information
    - **Student Name:** Vansh Sharma
    - **Enrolment Number:** PGD202562849
    - **Subject:** AI & Digital Transformation
    - **Program:** Master of Business Administration (MBA)
    - **Selected Banking Institution:** JPMorgan Chase Bank (Academic Simulation)
    - **Project Title:** Agent Gatekeeper – AI Agent Authorization & Risk Management System

    ---

    ### 2. Corporate Context & Problem Statement (JPMorgan Chase)
    As financial institutions like JPMorgan Chase pilot autonomous generative AI agents (e.g., automated concierge, wealth management copilots, recurring billing bots), an acute operational vulnerability emerges: **unconstrained agent agency**. 

    LLM-based agents are susceptible to:
    1. **Hallucinatory execution:** Ordering unauthorized wire transfers or payments based on ambiguous client chats.
    2. **Prompt injection attacks:** Malicious actors manipulating agents into bypassing internal controls.
    3. **Privilege creep & rogue persistence:** Decommissioned or compromised bots continuing to trigger internal banking APIs.
    
    The **Agent Gatekeeper** provides an independent, non-bypassable, deterministic authorization layer placed directly between AI agents and core banking ledgers.

    ---

    ### 3. Rule Matrix & Evaluation Precedence
    """)

    st.markdown("""
    | Rule ID | Precedence Order | Trigger Condition | Decision | Risk Rating |
    | :---: | :---: | :--- | :---: | :---: |
    | **R7** | 1 (Sanity / Input) | Invalid request, malformed parameters, negative amount, or unsupported action | **BLOCK** | CRITICAL |
    | **R1** | 2 (Identity) | Unknown or unregistered agent attempting any action | **BLOCK** | HIGH |
    | **R2** | 3 (Lifecycle) | Revoked agent attempting any action | **BLOCK** | HIGH |
    | **R3** | 4 (Read Access) | Active agent requesting account balance | **ALLOW** | LOW |
    | **R4** | 5 (Autonomous Cap) | Active agent executing bill payment of **₹5,000 or less** | **ALLOW** | LOW |
    | **R5** | 6 (Step-Up Auth) | Active agent executing bill payment **above ₹5,000** | **ASK CUSTOMER** | MEDIUM |
    | **R6** | 7 (High-Risk Asset) | Active agent requesting a money transfer (any amount) | **ASK CUSTOMER** | HIGH |
    """)

    st.markdown("""
    ---

    ### 4. Strategic MBA Trade-Off Analysis
    #### *The Trade-off of Completely Blocking AI Agents vs. Human-in-the-Loop Governance*

    A frequent conservative reaction in banking risk management is to **completely block autonomous AI agents** from conducting any operational actions. While this achieves near-zero direct agentic fraud risk, an MBA-level strategic analysis reveals severe strategic disadvantages:

    1. **Loss of Operational Scalability & Cost Efficiency:**
       - Processing millions of micro-payments, recurring utilities, and balance inquiries manually or through legacy rigid batch scripts inflates operational overhead. AI agents reduce transaction servicing costs by up to 70%. Completely blocking agents sacrifices this dividend.
    2. **Customer Experience Degradation:**
       - Modern digital banking clients expect instant, 24/7 autonomous friction-free assistance (e.g. paying an electricity bill at midnight). Forcing human manual steps for every mundane task creates customer churn towards fintech competitors.
    3. **The Optimal Strategy – Tiered Human-in-the-Loop (Gatekeeper Paradigm):**
       - Rather than binary extremes (*complete agent freedom* vs. *complete agent blockade*), the **Agent Gatekeeper** establishes a balanced risk frontier:
         - **Autonomous Zone (ALLOW):** Low-risk, low-value, bounded operations (Balance checks, bill payments ≤ ₹5,000).
         - **Governance Zone (ASK CUSTOMER):** Irreversible or high-value operations (Transfers, bill payments > ₹5,000) requiring customer two-factor confirmation.
         - **Security Perimeter (BLOCK):** Rogue, revoked, or malformed interactions intercepted deterministically.
    """)
