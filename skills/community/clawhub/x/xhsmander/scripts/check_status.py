import urllib.request
import json
import sys

url = 'http://localhost:18060/mcp'
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/event-stream'
}

# Initialize
payload = {
    'jsonrpc': '2.0',
    'method': 'initialize',
    'params': {},
    'id': 1
}
req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode(),
    headers=headers,
    method='POST'
)
with urllib.request.urlopen(req, timeout=10) as resp:
    session_id = resp.headers.get('Mcp-Session-Id')

headers['Mcp-Session-Id'] = session_id

# Call check_login_status
payload = {
    'jsonrpc': '2.0',
    'method': 'tools/call',
    'params': {
        'name': 'check_login_status',
        'arguments': {}
    },
    'id': 2
}
req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode(),
    headers=headers,
    method='POST'
)
with urllib.request.urlopen(req, timeout=60) as resp:
    result = json.loads(resp.read().decode())

with open(r'C:\Users\15822\.agents\skills\xhsmander\scripts\login_status.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print('Done')
