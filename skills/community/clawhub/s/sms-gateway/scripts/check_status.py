#!/usr/bin/env python3
"""Check SMS delivery status via sms-gate.app."""
import sys
import urllib.error
from auth import api_request

def main():
    if len(sys.argv) < 2:
        print("Usage: check_status.py '<message_id>'", file=sys.stderr)
        sys.exit(1)

    msg_id = sys.argv[1]

    try:
        data = api_request(f'/message/{msg_id}')
        print(f"📱 Message Status")
        print(f"   ID: {data.get('id', 'N/A')}")
        print(f"   State: {data.get('state', 'N/A')}")
        print(f"   To: {data.get('phoneNumber', 'N/A')}")
        print(f"   Message: {data.get('text', 'N/A')[:50]}...")
        print(f"   Created: {data.get('createdAt', 'N/A')}")
        print(f"   Delivered: {data.get('deliveredAt', 'Not yet')}")
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
