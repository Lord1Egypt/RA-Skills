#!/usr/bin/env python3
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


DEFAULT_TIMEOUT = float(os.getenv("PUGOING_TIMEOUT", "30"))


def die(message, code=1):
    print(json.dumps({"ok": False, "error": message}, ensure_ascii=False, indent=2))
    raise SystemExit(code)


def load_spec(argv):
    if len(argv) < 2 or argv[1] == "-":
        raw = sys.stdin.read().strip()
        if not raw:
            die("missing JSON input; pass a file path or pipe JSON to stdin")
        return json.loads(raw)

    source = argv[1]

    if os.path.isfile(source):
        with open(source, "r", encoding="utf-8") as f:
            return json.load(f)

    die("input must be a JSON file path or '-' to read JSON from stdin")


def resolve_url(spec):
    url = spec.get("url")
    if url:
        return url

    path = spec.get("path")
    if not path:
        die("request spec requires either 'path' or 'url'")

    base_url = os.getenv("PUGOING_BASE_URL", "http://127.0.0.1:8080").rstrip("/")
    if not path.startswith("/"):
        path = "/" + path
    return base_url + path


def build_headers(spec):
    headers = {"Accept": "application/json"}
    headers.update(spec.get("headers") or {})

    api_key = os.getenv("PUGOING_API_KEY", "").strip()
    if api_key and "X-API-Key" not in headers:
        headers["X-API-Key"] = api_key

    return headers


def build_request(spec):
    method = (spec.get("method") or "GET").upper()
    url = resolve_url(spec)
    params = spec.get("params") or {}
    data = spec.get("data")

    if method == "GET" and not params and isinstance(data, dict):
        params = data
        data = None

    if params:
        query = urllib.parse.urlencode(params, doseq=True)
        separator = "&" if "?" in url else "?"
        url = f"{url}{separator}{query}"

    body = None
    headers = build_headers(spec)
    if data is not None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url=url, data=body, method=method, headers=headers)
    return req, url


def parse_json_or_text(body_bytes):
    text = body_bytes.decode("utf-8", errors="replace")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def collect_sse_response(resp):
    result = {
        "ok": True,
        "status": getattr(resp, "status", 200),
        "text": "",
        "reasoning": "",
        "logs": [],
    }

    for raw_line in resp:
        line = raw_line.decode("utf-8", errors="replace").strip()
        if not line.startswith("data: "):
            continue

        payload = line[6:]
        if payload == "[DONE]":
            break

        if payload.startswith("ERROR: "):
            result["ok"] = False
            result["error"] = payload[7:]
            continue

        try:
            item = json.loads(payload)
        except json.JSONDecodeError:
            result["text"] += payload
            continue

        item_type = item.get("type")
        content = item.get("content", "")

        if item_type == "text":
            result["text"] += content
        elif item_type == "reasoning":
            result["reasoning"] += content
        elif item_type == "log":
            try:
                result["logs"].append(json.loads(content))
            except Exception:
                result["logs"].append(content)
        else:
            result.setdefault("raw", []).append(item)

    return result


def execute(spec):
    req, final_url = build_request(spec)
    timeout = float(spec.get("timeout", DEFAULT_TIMEOUT))

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content_type = resp.headers.get("Content-Type", "")
            if "text/event-stream" in content_type or final_url.endswith("/api/ai/chat"):
                payload = collect_sse_response(resp)
            else:
                payload = parse_json_or_text(resp.read())

            return {
                "ok": True,
                "status": getattr(resp, "status", 200),
                "url": final_url,
                "result": payload,
            }
    except urllib.error.HTTPError as exc:
        body = exc.read()
        return {
            "ok": False,
            "status": exc.code,
            "url": final_url,
            "error": parse_json_or_text(body),
        }
    except urllib.error.URLError as exc:
        return {
            "ok": False,
            "url": final_url,
            "error": str(exc.reason),
        }


def main():
    try:
        spec = load_spec(sys.argv)
    except json.JSONDecodeError as exc:
        die(f"invalid JSON input: {exc}")

    result = execute(spec)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
