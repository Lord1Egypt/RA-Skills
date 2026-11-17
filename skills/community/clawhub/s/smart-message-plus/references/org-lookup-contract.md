# Org Lookup Contract（自定义组织架构接口契约）

When `org_lookup.mode = "custom"`, department broadcast resolves members through
**your own HTTP service** instead of the vendor contact APIs. Implement one
endpoint per this contract.

## Why custom mode?

- Your company's org chart lives in an internal HR system, not in DingTalk/Feishu
- Vendor contact permissions are locked down but you have an internal directory service
- You want cross-platform identity mapping under your own control

## Request

```
POST {custom_url}
Content-Type: application/json
Authorization: <value of env ${custom_auth_header_env}>   # optional

{
  "dept_name": "技术部",        // department name as typed by the user
  "provider": "dingtalk"        // target platform: dingtalk | feishu
}
```

## Response（200）

```json
{
  "dept_id": "1059799007",
  "dept_name": "技术部",
  "dept_path": "公司/研发中心/技术部",
  "member_ids": ["userId1", "userId2"],
  "member_count": 2
}
```

Field rules:

| Field | Required | Notes |
|-------|----------|-------|
| `member_ids` | ✅ | **Must be provider-native ids** (DingTalk userId / Feishu open_id) — the caller sends to these directly |
| `dept_id` | recommended | any string |
| `dept_path` | recommended | shown to the user for confirmation |
| `dept_name` | optional | fallback display |
| `member_count` | optional | informational |

Errors: non-200 status or empty `member_ids` → CLI aborts with your response body
in the error message (keep it human-readable).

## Config

```json
{
  "org_lookup": {
    "mode": "custom",
    "custom_url": "https://your-directory.example.com/api/dept-members",
    "custom_auth_header_env": "SMP_ORG_AUTH",
    "timeout": 10
  }
}
```

Auth: set env `SMP_ORG_AUTH="Bearer xxx"` — the value is sent as the
`Authorization` header. Never store tokens in config files.

## Mock server (for local testing)

```python
#!/usr/bin/env python3
"""Minimal mock: python3 mock_org_server.py 8080"""
import json, sys
from http.server import BaseHTTPRequestHandler, HTTPServer

FAKE = {"技术部": {"dingtalk": ["userA", "userB"], "feishu": ["ou_a", "ou_b"]}}

class H(BaseHTTPRequestHandler):
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        dept, prov = body.get("dept_name"), body.get("provider")
        members = FAKE.get(dept, {}).get(prov)
        if members is None:
            self.send_response(404); self.end_headers()
            self.wfile.write(json.dumps({"error": f"dept not found: {dept}"}).encode())
            return
        resp = {"dept_id": "d1", "dept_name": dept, "dept_path": f"公司/{dept}",
                "member_ids": members, "member_count": len(members)}
        self.send_response(200)
        self.send_header("Content-Type", "application/json"); self.end_headers()
        self.wfile.write(json.dumps(resp, ensure_ascii=False).encode())

HTTPServer(("127.0.0.1", int(sys.argv[1]) if len(sys.argv) > 1 else 8080), H).serve_forever()
```

Test:

```bash
python3 mock_org_server.py 8080 &
# config.json: org_lookup.mode=custom, custom_url=http://127.0.0.1:8080
python3 send.py --broadcast --department 技术部 --msg test --dry-run
```
