import urllib.request
import json
import base64

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

# Call get_login_qrcode
payload = {
    'jsonrpc': '2.0',
    'method': 'tools/call',
    'params': {
        'name': 'get_login_qrcode',
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

with open(r'C:\Users\15822\.agents\skills\xhsmander\scripts\qrcode_result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# Extract and save QR code image
if 'result' in result and 'content' in result['result']:
    for item in result['result']['content']:
        if item.get('type') == 'image':
            image_data = item.get('data', '')
            if image_data:
                image_bytes = base64.b64decode(image_data)
                with open(r'C:\Users\15822\.agents\skills\xhsmander\scripts\qrcode.png', 'wb') as f:
                    f.write(image_bytes)
                print('QR code saved to qrcode.png')
                break

print('Done')
