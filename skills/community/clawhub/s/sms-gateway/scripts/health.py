#!/usr/bin/env python3
"""Health check for sms-gate.app device."""
import sys
import urllib.request
import urllib.error
import json
from auth import _load_env, _get_config

def main():
    base_url = _get_config()[0]

    try:
        req = urllib.request.Request(f"{base_url}/health")
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())

        status = data.get('status', 'unknown')
        version = data.get('version', 'N/A')
        icon = '✅' if status == 'pass' else '⚠️' if status == 'warn' else '❌'

        print(f"{icon} Gateway: {status} (v{version})")
        print("-" * 40)

        checks = data.get('checks', {})
        for name, check in checks.items():
            s = check.get('status', '?')
            val = check.get('observedValue', '?')
            unit = check.get('observedUnit', '')
            ci = '✓' if s == 'pass' else '⚠' if s == 'warn' else '✗'

            if name == 'battery:level':
                print(f"  {ci} Battery: {val}%")
            elif name == 'battery:charging':
                charging = 'yes' if val == 2 else 'no'
                print(f"  {ci} Charging: {charging}")
            elif name == 'connection:status':
                connected = 'yes' if val == 1 else 'no'
                print(f"  {ci} Connected: {connected}")
            elif name == 'messages:failed':
                print(f"  {ci} Failed msgs (1h): {val}")
            else:
                print(f"  {ci} {name}: {val} {unit}")

        if status != 'pass':
            sys.exit(1)

    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError:
        print(f"❌ Gateway unreachable at {base_url}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
