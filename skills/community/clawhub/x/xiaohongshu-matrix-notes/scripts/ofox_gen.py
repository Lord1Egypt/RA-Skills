#!/usr/bin/env python3
"""出图工具 — 经 Ofox 调 openai/gpt-image-2。

- 无参考图 → /v1/images/generations(文生图,用于博主定妆)
- 有参考图 → /v1/images/edits(图生图,image[] 可多张:博主图+产品图)

用法:
    python3 ofox_gen.py "<提示词>" <输出.png> [size] [参考图1 参考图2 ...]
    size 默认 1024x1536(竖版 2:3,贴近小红书 3:4)
"""
import os, sys, json, base64, mimetypes, uuid, time, urllib.request, urllib.error

KEY = os.environ["OFOX_API_KEY"]
BASE = "https://api.ofox.ai/v1"
MODEL = "openai/gpt-image-2"


def _post_multipart(url, fields, files):
    boundary = "----ofox" + uuid.uuid4().hex
    body = b""
    for k, v in fields.items():
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    for k, path in files:
        fn = os.path.basename(path)
        ctype = mimetypes.guess_type(path)[0] or "image/png"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"; filename=\"{fn}\"\r\nContent-Type: {ctype}\r\n\r\n".encode()
        body += open(path, "rb").read() + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": f"Bearer {KEY}",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    })
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def _post_json(url, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def _call(prompt, size, refs):
    if refs:
        fields = {"model": MODEL, "prompt": prompt, "size": size, "response_format": "b64_json"}
        files = [("image[]", p) for p in refs]
        return _post_multipart(f"{BASE}/images/edits", fields, files)
    return _post_json(f"{BASE}/images/generations", {
        "model": MODEL, "prompt": prompt, "size": size, "response_format": "b64_json"})


def generate(prompt, out_path, size="1024x1536", refs=None, retries=4):
    refs = refs or []
    d = None
    for attempt in range(retries):
        try:
            d = _call(prompt, size, refs)
            break
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
            wait = 2 ** attempt
            print(f"  重试 {attempt+1}/{retries}({e})… {wait}s 后重试")
            time.sleep(wait)
    if d is None:
        print("⚠️ 多次重试仍失败:", out_path); return False
    if "error" in d:
        print("⚠️ ERROR:", json.dumps(d["error"], ensure_ascii=False)[:300]); return False
    data = d.get("data", [])
    if not (data and data[0].get("b64_json")):
        print("⚠️ 无图:", json.dumps(d, ensure_ascii=False)[:300]); return False
    raw = base64.b64decode(data[0]["b64_json"])
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    open(out_path, "wb").write(raw)
    print(f"✅ {out_path} ({len(raw)//1024} KB)")
    return True


if __name__ == "__main__":
    prompt, out = sys.argv[1], sys.argv[2]
    size = sys.argv[3] if len(sys.argv) > 3 else "1024x1536"
    refs = sys.argv[4:]
    generate(prompt, out, size, refs)
