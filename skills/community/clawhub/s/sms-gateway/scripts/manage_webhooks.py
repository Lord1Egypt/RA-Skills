#!/usr/bin/env python3
"""Manage webhooks for SMS events."""
import sys
import urllib.error
from auth import api_request

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else 'list'

    try:
        if action == 'list':
            data = api_request('/webhooks')
            webhooks = data.get('webhooks', [])
            if not webhooks:
                print("No webhooks configured")
                return
            print(f"🔗 Configured Webhooks ({len(webhooks)})")
            for wh in webhooks:
                print(f"   {wh.get('event')}: {wh.get('url')}")

        elif action == 'add' and len(sys.argv) >= 4:
            event = sys.argv[2]
            url = sys.argv[3]
            api_request('/webhooks', method='POST', data={'event': event, 'url': url})
            print(f"✅ Webhook added: {event} -> {url}")

        elif action == 'delete' and len(sys.argv) >= 3:
            event = sys.argv[2]
            api_request(f'/webhooks/{event}', method='DELETE')
            print(f"✅ Webhook deleted: {event}")

        else:
            print("Usage:")
            print("  manage_webhooks.py list")
            print("  manage_webhooks.py add <event> <url>")
            print("  manage_webhooks.py delete <event>")
            print("\nEvents: sms:received, sms:delivered, system:ping")

    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
