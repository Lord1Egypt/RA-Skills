#!/usr/bin/env python3
"""List recent messages via sms-gate.app."""
import sys
import urllib.error
from auth import api_request

def main():
    limit = sys.argv[1] if len(sys.argv) > 1 else '10'

    try:
        data = api_request(f'/messages?limit={limit}')
        messages = data if isinstance(data, list) else data.get('messages', [])
        if not messages:
            print("No messages found")
            return

        print(f"📨 Recent Messages ({len(messages)} shown)")
        print("-" * 60)
        for m in messages:
            msg_type = "📤 OUT" if m.get('isSent') else "📥 IN"
            state = m.get('state', 'unknown')
            recipients = m.get('recipients', [])
            if recipients:
                phone = recipients[0].get('phoneNumber', 'N/A')
                recipient_state = recipients[0].get('state', state)
            else:
                phone = m.get('phoneNumber', 'N/A')
                recipient_state = state
            msg_id = m.get('id', 'N/A')[:12]
            print(f"{msg_type} [{recipient_state:10}] {phone:18} | {msg_id}")
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
