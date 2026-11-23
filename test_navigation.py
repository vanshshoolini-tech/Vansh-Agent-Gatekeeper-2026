"""
Automated Streamlit Navigation Test
Verifies all 7 navigation buttons in app.py using Streamlit AppTest.
Student: Vansh Sharma | Enrolment: PGD202562849
"""

import sys
from streamlit.testing.v1 import AppTest

PAGES = [
    ("top_nav_btn_0", "🏛️ Executive Dashboard", "Executive Governance Dashboard"),
    ("top_nav_btn_1", "⚡ Authorization Request", "Gatekeeper Authorization Request"),
    ("top_nav_btn_2", "➕ Agent Registration", "AI Agent Registration"),
    ("top_nav_btn_3", "🚫 Agent Revocation", "AI Agent Revocation"),
    ("top_nav_btn_4", "📋 Audit Logs & Traceability", "Immutable Audit Logs"),
    ("top_nav_btn_5", "🧪 MBA Test Suite & Verification", "MBA Academic Test Suite"),
    ("top_nav_btn_6", "📖 Project Info & Rule Governance", "Project Overview, Governance Architecture"),
]


def test_all_seven_navigation_buttons():
    print("=" * 80)
    print("STARTING STREAMLIT NAVIGATION INTEGRATION TEST")
    print("=" * 80)

    at = AppTest.from_file("app.py", default_timeout=30)
    at.run()

    if at.exception:
        print("FAIL: Initial AppTest run failed with exception:")
        print(at.exception)
        sys.exit(1)

    print("PASS: Initial load successful. Current page:", at.session_state.current_page)
    assert at.session_state.current_page == "🏛️ Executive Dashboard"

    # Test each of the seven top navigation buttons sequentially
    for btn_key, expected_page, expected_text in PAGES:
        print(f"\n--> Testing button: '{btn_key}' for page '{expected_page}'")
        
        # Locate button
        button = at.button(key=btn_key)
        assert button is not None, f"Button with key {btn_key} not found!"
        
        # Click button
        button.click()
        at.run()

        if at.exception:
            print(f"FAIL: Exception occurred after clicking {btn_key}:", at.exception)
            sys.exit(1)

        # Check session state
        actual_page = at.session_state.current_page
        print(f"    Session State Page: {actual_page}")
        assert actual_page == expected_page, f"Expected {expected_page}, got {actual_page}"

        # Verify page content rendered
        markdown_texts = " ".join([m.value for m in at.markdown])
        subheader_texts = " ".join([s.value for s in at.subheader])
        all_text = markdown_texts + " " + subheader_texts
        assert expected_text in all_text, f"Expected phrase '{expected_text}' not found in rendered page text!"
        print(f"    PASS: Page content verified (found '{expected_text}')")

    # Test Sidebar Navigation
    print("\n--> Testing Sidebar Navigation Buttons...")
    side_button_2 = at.button(key="sidebar_nav_btn_2")  # Register Agent
    side_button_2.click()
    at.run()
    assert at.session_state.current_page == "➕ Agent Registration"
    print("    PASS: Sidebar button navigated to '➕ Agent Registration'")

    side_button_0 = at.button(key="sidebar_nav_btn_0")  # Dashboard
    side_button_0.click()
    at.run()
    assert at.session_state.current_page == "🏛️ Executive Dashboard"
    print("    PASS: Sidebar button navigated back to '🏛️ Executive Dashboard'")

    # Test Dashboard Quick Action Shortcuts
    print("\n--> Testing Dashboard Quick Operation Buttons...")
    quick_auth = at.button(key="quick_auth")
    quick_auth.click()
    at.run()
    assert at.session_state.current_page == "⚡ Authorization Request"
    print("    PASS: Quick Action button 'quick_auth' navigated to '⚡ Authorization Request'")

    print("\n" + "=" * 80)
    print("ALL 7 NAVIGATION BUTTONS & SIDEBAR BUTTONS VERIFIED AND WORKING 100%!")
    print("=" * 80)


if __name__ == "__main__":
    test_all_seven_navigation_buttons()
