import os
import requests
import time
import sys
from dotenv import load_dotenv

# Load .env from current or parent directory
load_dotenv()

VETO_API_KEY = os.getenv("VETO_API_KEY")
BASE_URL = "https://vetoapi.com/api/v1"


def ask_human_permission(action_title: str, user_email: str, context: str = "Requested via VetoAPI") -> bool:
    """
    Pause the agent and wait for human approval via VetoAPI.

    Args:
        action_title: Short description of the action requiring approval.
        user_email:   Email address of the human approver.
        context:      Optional additional details shown in the approval email.

    Returns:
        True if approved, False if rejected or on error.
    """
    if not VETO_API_KEY:
        print("Error: VETO_API_KEY not found in environment variables.")
        print("Add 'VETO_API_KEY=veto_live_...' to your .env file.")
        return False

    payload = {
        "api_key": VETO_API_KEY,
        "user_email": user_email,
        "action_title": action_title,
        "context": context,
    }

    try:
        print(f"Requesting approval for: '{action_title}'...")
        response = requests.post(f"{BASE_URL}/request", json=payload)

        if response.status_code == 401:
            print("Error: Invalid VetoAPI key.")
            return False

        response.raise_for_status()
        request_id = response.json().get("request_id")

        print(f"Approval email sent to {user_email}.")
        print(f"Waiting for decision (Request ID: {request_id})...")

        while True:
            poll = requests.get(f"{BASE_URL}/request/{request_id}")
            poll.raise_for_status()
            status = poll.json().get("status")

            if status == "approved":
                print("\n[APPROVED] Human gave the green light. Proceeding...")
                return True
            elif status == "rejected":
                print("\n[REJECTED] Human denied the request. Aborting.")
                return False

            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(5)

    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        action = sys.argv[1]
        email = sys.argv[2]
        ctx = sys.argv[3] if len(sys.argv) > 3 else ""
        ask_human_permission(action, email, ctx)
    else:
        print("Usage: python veto_skill.py <action_title> <user_email> [context]")
