#!/usr/bin/env python3
import json
import sys
import urllib.request
import urllib.error


def call(url, method="GET", headers=None, body=None, timeout=8):
    req = urllib.request.Request(url, method=method, headers=headers or {}, data=body)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read().decode("utf-8", "ignore")
            try:
                parsed = json.loads(raw)
            except Exception:
                parsed = raw
            return {"status": r.status, "body": parsed}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "ignore")
        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = raw
        return {"status": e.code, "body": parsed}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


def main():
    if len(sys.argv) < 2:
        print("usage: validate_relay.py <base-url> [api-key]", file=sys.stderr)
        sys.exit(2)

    base = sys.argv[1].rstrip("/")
    api_key = sys.argv[2] if len(sys.argv) > 2 else None

    out = {}
    out["health"] = call(f"{base}/health")

    headers = {"Accept": "application/json"}
    if api_key:
        headers["X-API-Key"] = api_key

    out["poll"] = call(f"{base}/poll?since=0&limit=1", headers=headers)
    out["attachment_probe"] = call(f"{base}/attachment/test-message/test-attachment", headers=headers)

    send_headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if api_key:
        send_headers["X-API-Key"] = api_key
    out["send_shape_check"] = call(
        f"{base}/send",
        method="POST",
        headers=send_headers,
        body=json.dumps({"to": "TEST", "text": "probe"}).encode(),
    )

    summary = {
        "reachable": isinstance(out["health"], dict) and out["health"].get("status") == 200,
        "poll_supported": isinstance(out["poll"], dict) and out["poll"].get("status") != 404,
        "attachment_endpoint_present": isinstance(out["attachment_probe"], dict) and out["attachment_probe"].get("status") != 404,
        "modern_health": False,
    }
    body = out.get("health", {}).get("body") if isinstance(out.get("health"), dict) else None
    if isinstance(body, dict):
        summary["modern_health"] = all(k in body for k in ["ok", "sessionId", "inboundEnabled", "queued", "lastSeq"])

    print(json.dumps({"summary": summary, "checks": out}, indent=2))


if __name__ == "__main__":
    main()
