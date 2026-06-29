# Python Integration Reference

## Dependencies

```bash
pip install requests
```

For the CLI script (`scripts/chat.py`), only Python stdlib is needed (uses `urllib`).

---

## 1. TC3-HMAC-SHA256 Signing

```python
import hashlib
import hmac
import time

def tc3_sign(secret_id: str, secret_key: str, host: str,
             payload_body: str, region: str = "ap-guangzhou"):
    """
    Generate TencentCloud TC3-HMAC-SHA256 authorization header.

    Critical constraints:
    1. timestamp = int(time.time()), NOT datetime.utcnow() (macOS timezone drift)
    2. x-tc-timestamp MUST be in SignedHeaders
    3. credential_scope = date/tdai/tc3_request (service name mandatory)
    4. host in canonical_headers must match the actual request host

    Returns: (authorization_header_value, timestamp_int)
    """
    timestamp = int(time.time())
    date = time.strftime("%Y-%m-%d", time.gmtime(timestamp))
    service = "tdai"
    ct = "application/json"

    canonical_headers = (
        f"content-type:{ct}\n"
        f"host:{host}\n"
        f"x-tc-timestamp:{timestamp}\n"
    )
    signed_headers = "content-type;host;x-tc-timestamp"
    hashed_payload = hashlib.sha256(payload_body.encode("utf-8")).hexdigest()

    canonical_request = (
        f"POST\n/\n\n"
        f"{canonical_headers}\n"
        f"{signed_headers}\n"
        f"{hashed_payload}"
    )

    credential_scope = f"{date}/{service}/tc3_request"
    hashed_canonical = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    string_to_sign = (
        f"TC3-HMAC-SHA256\n{timestamp}\n{credential_scope}\n{hashed_canonical}"
    )

    def _sign(key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    k_date = _sign(("TC3" + secret_key).encode("utf-8"), date)
    k_service = _sign(k_date, service)
    k_signing = _sign(k_service, "tc3_request")
    signature = hmac.new(k_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

    auth = (
        f"TC3-HMAC-SHA256 Credential={secret_id}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, "
        f"Signature={signature}"
    )
    return auth, timestamp
```

---

## 2. HTTP Headers

```python
auth, timestamp = tc3_sign(secret_id, secret_key, host, body_str)

headers = {
    "Content-Type": "application/json",
    "Accept": "text/event-stream",
    "Host": "tdai.ai.tencentcloudapi.com",
    "X-TC-Timestamp": str(timestamp),
    "X-TC-Action": "CreateChatCompletion",
    "X-TC-Version": "2025-07-17",
    "X-TC-Region": "ap-guangzhou",
    "Authorization": auth,
}
```

---

## 3. Request Body

```python
import json

body = json.dumps({
    "InstanceId": "clawins-xxxxxx",   # Your instance ID
    "InputContent": "Your question here",
    # Optional: "ChatId": "chat-xxx" (for multi-turn)
})
```

> **Do NOT include** `AppId`, `Uin`, `OwnerUin`, `IdempotencyKey` in body.
> Identity is derived from the AK/SK used for signing.

---

## 4. SSE Stream Parsing

```python
import requests

resp = requests.post(
    "https://tdai.ai.tencentcloudapi.com/",
    headers=headers,
    data=body.encode("utf-8"),
    stream=True,
    timeout=120,
)
resp.raise_for_status()

full_content = ""
for line in resp.iter_lines(decode_unicode=True):
    if not line:
        continue
    if not line.startswith("data: "):
        continue
    data_str = line[6:]
    if data_str == "[DONE]":
        break

    event = json.loads(data_str)
    # Unwrap Response wrapper if present
    if "Response" in event and isinstance(event["Response"], dict):
        event = event["Response"]
    # Check for error
    if "Error" in event:
        raise RuntimeError(f"{event['Error']['Code']}: {event['Error']['Message']}")

    choices = event.get("Choices", [])
    if not choices:
        continue
    choice = choices[0]
    delta = choice.get("Delta", {})
    content = delta.get("Content", "")
    if content:
        full_content += content
        print(content, end="", flush=True)
    if choice.get("FinishReason") == "stop":
        break

print(f"\n\n[Done] Total: {len(full_content)} chars")
```

---

## 5. Error Diagnosis

| Error Code | Meaning | Fix |
|-----------|---------|-----|
| `InternalError` | Wrong host (`tdai.tencentcloudapi.com` instead of `tdai.ai.tencentcloudapi.com`) | Use SSE host |
| `UnknownParameter` | Body has fields API doesn't accept | Remove AppId/Uin/OwnerUin from body |
| `MissingParameter` | Required field missing | Ensure `InputContent` is in body |
| `AuthFailure.SignatureExpire` | Timestamp >5min from server | Use `int(time.time())` |
| `InvalidAuthorization` | credential_scope wrong | Format: `date/tdai/tc3_request` |
| `InvalidAction` | Service or action name wrong | service=`tdai`, action=`CreateChatCompletion` |
| `MissingParameter` (X-TC-Action) | Missing header | Add `X-TC-Action` header |

---

## 6. Key Constraints

| Constraint | Value |
|-----------|-------|
| SSE Host | `tdai.ai.tencentcloudapi.com` |
| Non-SSE Host | `tdai.tencentcloudapi.com` |
| Service | `tdai` |
| API Version | `2025-07-17` |
| Rate limit | 20 req/s |
| Instance status | Must be `running` |
| Heartbeat | Every 20s (ignore) |
| Stream end | `data: [DONE]` |
