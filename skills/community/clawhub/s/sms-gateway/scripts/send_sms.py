#!/usr/bin/env python3
"""Send SMS via sms-gate.app local gateway."""
import sys
import urllib.error
from auth import api_request

def main():
    if len(sys.argv) < 3:
        print("Usage: send_sms.py '<phone_number>' '<message>' [delivery_report=true/false]", file=sys.stderr)
        sys.exit(1)

    phone = sys.argv[1].replace('+', '')
    message = sys.argv[2]
    delivery_report = sys.argv[3].lower() == 'true' if len(sys.argv) > 3 else True

    try:
        data = api_request('/message', method='POST', data={
            'phoneNumbers': [phone],
            'textMessage': {'text': message},
            'withDeliveryReport': delivery_report
        })
        msg_id = data.get('id', 'unknown')
        state = data.get('state', 'unknown')
        print(f"✅ SMS sent | ID: {msg_id} | State: {state}")
        print(f"   To: +{phone}")
        print(f"   Message: {message[:50]}...")
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
