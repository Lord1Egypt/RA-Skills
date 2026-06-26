#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
即梦AI 文生图 - 集成 OpenClaw 图片工具链
用法:
    python generate.py --prompt "描述" [--aspect 16:9] [--output path]
    
输出格式:
    - 有 output 时: 保存图片到本地
    - 无 output 时: 输出 MEDIA_URL: <url>
"""
import argparse, os, sys, json, base64, time, hashlib, hmac, urllib.request

# === 凭证 ===
SECRETS_FILE = os.path.expanduser("~/.openclaw/workspace/secrets.json")

def get_credentials():
    try:
        with open(SECRETS_FILE, encoding="utf-8") as f:
            data = json.load(f)
        entry = data.get("entries", {}).get("jimeng", {})
        fields = entry.get("fields", {})
        return fields.get("AccessKeyId"), fields.get("SecretAccessKey")
    except Exception:
        return None, None

# === Volcengine 签名 ===
BASE_URL = "https://visual.volcengineapi.com"
REGION = "cn-beijing"; SERVICE = "cv"

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
    headers = {"Content-Type": "application/json", "Host": BASE_URL.replace("https://", ""), "X-Date": date_full, "X-Content-Sha256": body_hash, "Authorization": authorization}
    url = f"{BASE_URL}{path}?{query}"
    req = urllib.request.Request(url, data=body.encode(), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())

def wait_and_get_image(task_id, access_key, secret_key, max_wait=60, interval=3):
    for _ in range(max_wait // interval):
        time.sleep(interval)
        result = call_api("JimengT2IV40GetResult", {"req_key": "jimeng_t2i_v40", "task_id": task_id}, access_key, secret_key)
        data = result.get("Result", {}).get("data", {})
        status = data.get("status", "unknown")
        if status == "done":
            # 优先用 image_urls
            urls = data.get("image_urls") or []
            if urls:
                return urls[0], None
            # 其次用 base64
            b64_list = data.get("binary_data_base64") or []
            if b64_list:
                img_data = base64.b64decode(b64_list[0])
                return None, img_data
            return None, None
        elif status == "failed":
            raise Exception(f"Task failed: {result}")
    raise TimeoutError(f"Timeout waiting for task {task_id}")

def main():
    parser = argparse.ArgumentParser(description="即梦AI 文生图")
    parser.add_argument("--prompt", "-p", required=True, help="图像描述")
    parser.add_argument("--aspect", default="1:1", help="宽高比: 1:1, 3:4, 4:3, 16:9, 9:16")
    parser.add_argument("--output", "-o", help="输出文件路径 (不指定则输出 MEDIA_URL)")
    parser.add_argument("--seed", type=int, default=-1, help="随机种子")
    args = parser.parse_args()

    access_key, secret_key = get_credentials()
    if not access_key:
        print("ERROR: No jimeng credentials found in secrets.json", file=sys.stderr)
        sys.exit(1)

    # 提交任务
    result = call_api("JimengT2IV40SubmitTask", {
        "req_key": "jimeng_t2i_v40",
        "prompt": args.prompt,
        "aspect_ratio": args.aspect,
        "seed": args.seed
    }, access_key, secret_key)

    if result.get("Result", {}).get("code") != 10000:
        print(f"ERROR: {result}", file=sys.stderr)
        sys.exit(1)

    task_id = result["Result"]["data"]["task_id"]
    print(f"Task submitted: {task_id}", file=sys.stderr)

    # 等待完成
    url, img_data = wait_and_get_image(task_id, access_key, secret_key)

    if args.output:
        if img_data:
            with open(args.output, "wb") as f:
                f.write(img_data)
            print(f"IMAGE_SAVED: {args.output}")
        else:
            # 下载 URL 图片
            with urllib.request.urlopen(url, timeout=30) as resp:
                data = resp.read()
            with open(args.output, "wb") as f:
                f.write(data)
            print(f"IMAGE_SAVED: {args.output}")
    else:
        if url:
            print(f"MEDIA_URL: {url}")
        else:
            # 保存临时文件输出
            tmp = os.path.join(os.path.dirname(__file__), "..", "temp_output.png")
            if img_data:
                with open(tmp, "wb") as f:
                    f.write(img_data)
                print(f"MEDIA_URL: file://{os.path.abspath(tmp)}")
            else:
                print("ERROR: No image data returned", file=sys.stderr)
                sys.exit(1)

if __name__ == "__main__":
    main()
