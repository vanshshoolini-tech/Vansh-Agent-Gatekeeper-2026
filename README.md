# Agent Gatekeeper – AI Agent Authorization & Risk Management System

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B.svg)](https://streamlit.io/)
[![Database](https://img.shields.io/badge/Database-SQLite3-003B57.svg)](https://www.sqlite.org/)
[![Academic](https://img.shields.io/badge/Academic-MBA%20Project-0A2540.svg)](#student-details)
[![Tests](https://img.shields.io/badge/Test%20Suite-7%2F7%20Passed-10B981.svg)](#test-cases--validation)

> **MBA Academic Project in AI & Digital Transformation**  
> Developed for **JPMorgan Chase Bank** (Academic Simulation)

---

## Student Details
- **Student Name:** Vansh Sharma
- **Enrolment Number:** PGD202562849
- **Course / Programme:** Master of Business Administration (MBA)
- **Subject:** AI & Digital Transformation
- **Selected Institution:** JPMorgan Chase Bank
- **Project Title:** Agent Gatekeeper – AI Agent Authorization & Risk Management System

---

## 1. Executive Summary & Project Objective

As premier financial institutions like **JPMorgan Chase** deploy autonomous AI agents (such as concierge bots, wealth copilot assistants, and automated recurring billing bots), they face an existential governance challenge: **how to grant AI agents operational agency without exposing the bank to catastrophic financial, cybersecurity, and regulatory risks.**

Large Language Models (LLMs) are probabilistic and prone to hallucination, prompt injection, and intent drift. Letting an AI agent directly invoke banking APIs without deterministic safeguards creates unacceptable exposure.

The **Agent Gatekeeper** is an independent, non-bypassable authorization and risk-governance gateway that sits directly between client-facing AI agents and core banking ledgers. It evaluates every requested action in real time and enforces deterministic banking rules to return one of three binding decisions:
- **`ALLOW`**: Immediate autonomous execution for safe, low-value, bounded operations.
- **`ASK CUSTOMER`**: Mandatory step-up human-in-the-loop verification (via mobile push notification / OTP) for sensitive, high-value, or irreversible actions.
- **`BLOCK`**: Instant perimeter rejection of unauthorized, revoked, unknown, or malformed transactions.

---

## 2. Technology Stack

- **Core Programming Language:** Python 3.11
- **User Interface:** Streamlit (Custom corporate styling tailored to JPMorgan Chase palette)
- **Database Management:** SQLite3 (Serverless, local, zero-configuration relational persistence)
- **Data Analytics & Visualization:** Pandas, Plotly Express
- **Executive Reporting:** ReportLab (Automated 2-page academic PDF generator)
- **Version Control:** Git & GitHub
- **Production Deployment:** Streamlit Community Cloud

---

## 3. System Architecture & File Structure

```
vansh ai assignment/
├── app.py                             # Main Streamlit web application & executive dashboard
├── authorization_engine.py            # Deterministic rule engine evaluating R1 - R7 in priority order
├── database.py                        # SQLite layer for agent registry, revocation tracking & audit logs
├── test_suite.py                      # Automated validation suite executing the 6 core + 1 edge test cases
├── generate_report.py                 # Python ReportLab script generating the 2-page academic PDF report
├── Agent_Gatekeeper_Project_Report.pdf# Generated 2-page executive PDF report
├── requirements.txt                   # Python dependencies for local setup & Streamlit Cloud
├── .gitignore                         # Git exclusion rules
├── PROMPTS.md                         # AI prompts, personas & prompt injection defense docs
├── TEST_RESULTS.md                    # Detailed verification matrix and test case analysis
└── README.md                          # Comprehensive project documentation
```

---

## 4. Authorization Rules & Precedence Hierarchy

The engine evaluates actions strictly following a four-tier precedence hierarchy. Input sanity and identity checks take precedence over transactional policies:

```
[Incoming Action Request]
          │
          ▼
   1. Input Sanity (R7)? ───────> (Malformed / Invalid Amount / Unsupported Action) ──> [BLOCK]
          │ (Valid)
          ▼
   2. Identity Check (R1)? ─────> (Agent Not in Registry) ────────────────────────────> [BLOCK]
          │ (Registered)
          ▼
   3. Lifecycle Status (R2)? ───> (Agent Revoked) ──────────────────────────────────> [BLOCK]
          │ (Active)
          ▼
   4. Action & Threshold Policies (R3, R4, R5, R6)
          ├── View Account Balance ────────────────────────────────────────────────> [ALLOW] (R3)
          ├── Pay a Bill (Amount ≤ ₹5,000) ────────────────────────────────────────> [ALLOW] (R4)
          ├── Pay a Bill (Amount > ₹5,000) ────────────────────────────────────────> [ASK CUSTOMER] (R5)
          └── Transfer Money (Any Amount) ─────────────────────────────────────────> [ASK CUSTOMER] (R6)
```

### Rule Evaluation Matrix

| Rule ID | Precedence | Condition / Trigger | Decision | Risk Rating | Business Rationale |
| :---: | :---: | :--- | :---: | :---: | :--- |
| **R7** | Priority 1 | Invalid request, unsupported action, or non-positive amount | **BLOCK** | CRITICAL | Sanitizes inputs and halts malformed/injected API payloads at perimeter. |
| **R1** | Priority 2 | Unknown or unregistered agent identifier | **BLOCK** | HIGH | Zero-trust authentication; prevents rogue bots from querying bank APIs. |
| **R2** | Priority 3 | Revoked agent attempting any banking operation | **BLOCK** | HIGH | Enforces instant lifecycle de-provisioning; decommissioned bots cannot act. |
| **R3** | Priority 4 | Active agent requesting read-only Account Balance | **ALLOW** | LOW | Read-only inquiry carries zero financial debit risk. |
| **R4** | Priority 5 | Active agent making a bill payment of **₹5,000 or less** | **ALLOW** | LOW | Bounded autonomous micro-payment within pre-approved limit. |
| **R5** | Priority 6 | Active agent making a bill payment **above ₹5,000** | **ASK CUSTOMER** | MEDIUM | Exceeds autonomous threshold; requires client mobile step-up confirmation. |
| **R6** | Priority 7 | Active agent requesting a money transfer (any amount) | **ASK CUSTOMER** | HIGH | Irreversible capital movement; mandatory human two-factor verification. |

> **Autonomous Limit:** The autonomous bill payment limit is strictly configured at **₹5,000.00**.

---

## 5. Core Banking Actions Supported

1. **View Account Balance:** Read-only inquiry into the client's current checking or savings balance.
2. **Pay a Bill:** Operational settlement of recurring utility, water, electricity, or telecom invoices.
3. **Transfer Money:** High-risk peer-to-peer or external wire transfer of client capital.

---

## 6. Test Cases & Academic Validation

The system includes an automated test harness covering all six mandatory academic test cases plus an edge validation scenario:

| Test ID | Test Scenario | Agent ID | Action | Amount (₹) | Expected | Actual | Rule | Status |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **TC-01** | Registered active agent requesting balance | `AGENT-JPMC-101` | View Account Balance | N/A | **ALLOW** | **ALLOW** | **R3** | **PASS** |
| **TC-02** | Unknown agent requesting balance | `AGENT-ROGUE-9999` | View Account Balance | N/A | **BLOCK** | **BLOCK** | **R1** | **PASS** |
| **TC-03** | Bill payment of ₹10,000 (> ₹5,000 limit) | `AGENT-JPMC-101` | Pay a Bill | ₹10,000.00 | **ASK CUSTOMER** | **ASK CUSTOMER** | **R5** | **PASS** |
| **TC-04** | Bill payment of ₹2,000 (≤ ₹5,000 limit) | `AGENT-JPMC-101` | Pay a Bill | ₹2,000.00 | **ALLOW** | **ALLOW** | **R4** | **PASS** |
| **TC-05** | Revoked agent requesting money transfer | `AGENT-JPMC-999` | Transfer Money | ₹15,000.00 | **BLOCK** | **BLOCK** | **R2** | **PASS** |
| **TC-06** | Active agent requesting money transfer | `AGENT-JPMC-101` | Transfer Money | ₹3,500.00 | **ASK CUSTOMER** | **ASK CUSTOMER** | **R6** | **PASS** |
| **TC-07** | Unsupported / Malformed request (Edge Case) | `AGENT-JPMC-101` | Crypto Currency Purchase | ₹50,000.00 | **BLOCK** | **BLOCK** | **R7** | **PASS** |

**Global Test Outcome:** 7 out of 7 Tests Passed (100% Academic Compliance).

---

## 7. Strategic MBA Trade-Off Analysis

### The Strategic Trade-off of Completely Blocking AI Agents vs. Human-in-the-Loop Governance

A standard conservative reaction among institutional risk officers is to **completely block AI agents** from conducting any operational actions, restricting them strictly to passive FAQ search bots.

While a complete blockade eliminates direct automated transaction fraud, an MBA-level strategic analysis reveals that this approach causes severe competitive and operational damage:

1. **Loss of Operational Cost Efficiency:**
   - Routine banking operations (balance checks and micro utility bills) constitute over 70% of customer support contact volume. Servicing these through call center agents costs approximately $4.00 to $6.00 per inquiry. An autonomous AI agent reduces this cost to under $0.15. Completely blocking agents forfeits millions in operational savings.
2. **Customer Friction & Fintech Disintermediation:**
   - Digital-native banking customers expect instant, 24/7 autonomous task resolution (e.g., paying an electricity bill at midnight without manually filling out IBAN forms). If JPMorgan Chase blocks autonomous agents, customers will migrate to agile fintech competitors (e.g., Revolut, Chime, Apple Pay) that offer seamless agentic assistance.
3. **The Optimal Frontier: Tiered Human-in-the-Loop Governance:**
   - Rather than choosing between binary extremes (unfettered autonomous risk vs. complete agent paralysis), the **Agent Gatekeeper** establishes a balanced, tiered risk frontier:
     - **Autonomous Zone (`ALLOW`):** Safe, low-value, routine actions (balances, bills ≤ ₹5,000) are automated for maximum efficiency.
     - **Governance Zone (`ASK CUSTOMER`):** Sensitive, high-value, irreversible actions (wire transfers, bills > ₹5,000) mandate client step-up approval, ensuring human oversight where it matters most.
     - **Perimeter Defense (`BLOCK`):** Rogue, revoked, or malformed commands are intercepted deterministically.

---

## 8. How to Run and Test Locally

### Prerequisites
- Python 3.9, 3.10, or 3.11 installed
- Git installed

### Step 1: Open Terminal / PowerShell
Navigate to the project directory:
```powershell
cd "c:\Users\asus\OneDrive\Ai tools\Desktop\vansh ai assignment"
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Run the Automated Test Suite (CLI)
Verify the authorization rules and database persistence:
```powershell
python test_suite.py
```
*Expected Output:* `Summary: 7/7 Tests Passed. Global Status: ALL TESTS PASSED`

### Step 4: Launch the Streamlit Banking Application
```powershell
streamlit run app.py
```
The browser will automatically open at `http://localhost:8501`.

### Step 5: Generate the 2-Page Executive PDF Report (Optional)
```powershell
python generate_report.py
```
This generates `Agent_Gatekeeper_Project_Report.pdf` formatted exactly to two pages.

---

## 9. GitHub Version Control & Streamlit Cloud Deployment Guide

Follow these exact steps to push this project to your GitHub account and deploy it to Streamlit Community Cloud:

### Part A: Push to Your GitHub Account
1. Open PowerShell in the project directory:
   ```powershell
   git init
   git add .
   git commit -m "feat: complete Agent Gatekeeper prototype for Vansh Sharma (PGD202562849)"
   ```
2. Create a new public repository on [GitHub](https://github.com/new) named:
   `agent-gatekeeper-jpmc`
3. Link your local repository and push:
   ```powershell
   git branch -M main
   git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/agent-gatekeeper-jpmc.git
   git push -u origin main
   ```

### Part B: Deploy to Streamlit Community Cloud
1. Visit [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
2. Click **"New app"**.
3. Select your repository: `<YOUR_GITHUB_USERNAME>/agent-gatekeeper-jpmc`.
4. Set the **Branch** to `main`.
5. Set the **Main file path** to `app.py`.
6. Click **"Deploy!"**.
7. Within 1-2 minutes, your live web dashboard will be accessible via a public URL (e.g. `https://agent-gatekeeper-jpmc.streamlit.app/`).

---

## 10. Academic Presentation Guide (For Vansh Sharma)

When presenting this project to your professor or viva panel, use this structured 3-minute talking track:

1. **Slide 1 / Introduction (30 seconds):**
   - Introduce yourself: *"Good morning/afternoon, my name is Vansh Sharma (PGD202562849). Today I am presenting my AI & Digital Transformation project: Agent Gatekeeper, an AI Agent Authorization & Risk Management System modeled for JPMorgan Chase Bank."*
2. **Slide 2 / Business Problem (45 seconds):**
   - Highlight the dilemma: *"Banks are adopting autonomous AI agents to automate transactions. However, generative AI is non-deterministic and can hallucinate or be tricked by prompt injections into initiating unauthorized wires. A bank cannot trust an AI agent to govern itself."*
3. **Slide 3 / The Gatekeeper Architecture (45 seconds):**
   - Explain the 3 verdicts: *"I designed an external, deterministic Gatekeeper. It applies a 4-step precedence hierarchy: checking input sanity (R7), agent existence (R1), agent revocation (R2), and transaction limits (R3-R6). It yields three verdicts: ALLOW for safe routine tasks, ASK CUSTOMER for transfers or bills above ₹5,000, and BLOCK for rogue or revoked bots."*
4. **Slide 4 / Live Demo & 100% Test Results (45 seconds):**
   - Show the Streamlit dashboard: Demonstrate the Executive KPIs, run the 6 test cases with 1 click, show the simulated mobile push notification, and present the downloadable 2-page PDF report.
5. **Slide 5 / Strategic Trade-off (15 seconds):**
   - Conclude with the MBA insight: *"Completely banning AI agents leads to customer churn and high costs; complete autonomy is reckless. The Gatekeeper provides the optimal tiered governance frontier."*

---

## 11. Academic Simulation Disclaimer

> **Important Academic Notice:**  
> This project is an academic prototype created independently by **Vansh Sharma (Enrolment: PGD202562849)** for educational evaluation in the **AI & Digital Transformation** MBA course. It is a simulation inspired by JPMorgan Chase Bank's public AI transformation initiatives and does not use proprietary banking infrastructure, real customer data, or live monetary settlement systems.
