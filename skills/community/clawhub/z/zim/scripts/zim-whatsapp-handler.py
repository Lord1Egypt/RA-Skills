#!/usr/bin/env python3
"""Bridge script: OpenClaw agent → Zim WhatsApp Agent.

Usage:
    python3 zim-whatsapp-handler.py --message "Find flights DXB to CPH May 1" --user-id "whatsapp:+971544042230"

Outputs the Zim agent response text to stdout.
State is persisted in SQLite so conversation context survives across calls.
"""

import argparse
import json
import os
import sys
from datetime import date, datetime

# Ensure the zim package is importable (handles running from anywhere)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, PROJECT_ROOT)

from zim.whatsapp_agent import ZimWhatsAppAgent
from zim.state_store import SQLiteStateStore

# Persistent state in the zim project directory
STATE_DB = os.path.join(PROJECT_ROOT, "data", "whatsapp_state.db")


def main():
    parser = argparse.ArgumentParser(description="Zim WhatsApp message handler")
    parser.add_argument("--message", "-m", required=True, help="User message text")
    parser.add_argument("--user-id", "-u", required=True, help="WhatsApp user ID (e.g. whatsapp:+971544042230)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    # Ensure data directory exists
    os.makedirs(os.path.dirname(STATE_DB), exist_ok=True)

    store = SQLiteStateStore(db_path=STATE_DB)
    agent = ZimWhatsAppAgent(state_store=store)

    try:
        response = agent.handle_message(args.message, user_id=args.user_id)
    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e), "success": False}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps({"response": response, "success": True}))
    else:
        print(response)


if __name__ == "__main__":
    main()
