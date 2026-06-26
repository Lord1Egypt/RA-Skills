#!/usr/bin/env python3
"""Check for new incoming SMS via polling."""
import os
import sys
import json
import urllib.error
from datetime import datetime, timezone
from auth import api_request

def main():
    state_file = os.path.expanduser('~/.sms_gateway_last_check')
    last_check = None
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r') as f:
                last_check = datetime.fromisoformat(f.read().strip())
        except Exception:
            pass

    if not last_check:
        last_check = datetime.now(timezone.utc)

    try:
        messages = api_request('/messages?limit=20')
        if not isinstance(messages, list):
            messages = messages.get('messages', [])

        new_incoming = []
        for m in messages:
            if m.get('isSent'):
                continue
            states = m.get('states', {})
            delivered_at = states.get('Delivered') or states.get('Pending')
            if delivered_at:
                msg_time = datetime.fromisoformat(delivered_at.replace('Z', '+00:00'))
                if msg_time > last_check:
                    new_incoming.append(m)

        with open(state_file, 'w') as f:
            f.write(datetime.now(timezone.utc).isoformat())

        if new_incoming:
            print(f"📥 {len(new_incoming)} new incoming SMS:")
            print("-" * 60)
            for m in new_incoming:
                recipients = m.get('recipients', [])
                sender = recipients[0].get('phoneNumber', 'Unknown') if recipients else 'Unknown'
                text = m.get('text', 'N/A')[:100]
                msg_id = m.get('id', 'N/A')[:12]
                print(f"From: {sender}")
                print(f"Text: {text}")
                print(f"ID: {msg_id}")
                print("-" * 60)
        else:
            print("📭 No new incoming SMS")

    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
