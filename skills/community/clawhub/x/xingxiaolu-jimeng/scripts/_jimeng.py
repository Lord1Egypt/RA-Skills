#!/usr/bin/env python3
"""即梦AI 共享库 - Volcengine 签名 & API调用"""
import json, hashlib, hmac, time, urllib.request, sys, os

BASE_URL = "https://visual.volcengineapi.com"
REGION = "cn-beijing"
SERVICE = "cv"

def get_credentials():
    """从 secrets.json 获取凭证"""
    secrets_file = os.path.expanduser("~/.openclaw/workspace/secrets.json")
    try:
        with open(secrets_file, encoding="utf-8") as f:
            data = json.load(f)
        entry = data.get("entries", {}).get("jimeng", {})
        fields = entry.get("fields", {})
        return fields.get("AccessKeyId"), fields.get("SecretAccessKey")
    except Exception as e:
        print(f"Error loading credentials: {e}", file=sys.stderr)
        return None, None

def hmac_sha256(key, data):
    return hmac.new(key, data.encode('utf-8'), hashlib.sha256).digest()

def sign(method, path, query, body, date_short, date_full, access_key, secret_key):
    body_hash = hashlib.sha256(body.encode('utf-8')).hexdigest()
    signed_headers = "content-type;host;x-date;x-content-sha256"
    canonical = f"{method}\n{path}\n{query}\ncontent-type:application/json\nhost:{BASE_URL.replace('https://', '')}\nx-date:{date_full}\nx-content-sha256:{body_hash}\n\n{signed_headers}\n{body_hash}"
    hashed_canonical = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
    credential_scope = f"{date_short}/{REGION}/{SERVICE}/request"
    string_to_sign = f"HMAC-SHA256\n{date_full}\n{credential_scope}\n{hashed_canonical}"
    k_date = hmac_sha256(secret_key.encode('utf-8'), date_short)
    k_region = hmac_sha256(k_date, REGION)
    k_service = hmac_sha256(k_region, SERVICE)
    k_signing = hmac_sha256(k_service, "request")
    signature = hmac.new(k_signing, string_to_sign.encode('utf-8'), hashlib.sha256).digest()
    authorization = f"HMAC-SHA256 Credential={access_key}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature.hex()}"
    return authorization, body_hash

def call_api(action, body_dict, access_key, secret_key):
    path = "/api/v1"
    body = json.dumps(body_dict)
    query = f"Action={action}&Version=2024-06-06"
    date_full = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    date_short = time.strftime("%Y%m%d", time.gmtime())
    authorization, body_hash = sign("POST", path, query, body, date_short, date_full, access_key, secret_key)
    headers = {
        "Content-Type": "application/json",
        "Host": BASE_URL.replace("https://", ""),
        "X-Date": date_full,
        "X-Content-Sha256": body_hash,
        "Authorization": authorization
    }
    url = f"{BASE_URL}{path}?{query}"
    req = urllib.request.Request(url, data=body.encode(), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())
    except Exception as e:
        return {"error": str(e)}
