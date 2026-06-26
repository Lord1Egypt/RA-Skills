import sys
import json
import os
import requests
from typing import Any, Dict, List


# 服务根地址（与 apis 约定一致；换环境请直接改此处）
API_BASE_URL = "http://intra-znjs-yqt-agent-wx-beta.midu.cc".rstrip("/")


def _resolve_api_key(base_url: str) -> str:
    """Prefer MIDU_API_KEY; otherwise GET {base}/apiKey."""
    key = os.environ.get("MIDU_API_KEY")
    if key and key.strip():
        return key.strip()
    url = f"{base_url}/apiKey"
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    text = response.text.strip()
    if not text:
        return ""
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            for k in ("key", "api_key", "token", "data"):
                v = data.get(k)
                if isinstance(v, str) and v.strip():
                    return v.strip()
    except json.JSONDecodeError:
        pass
    return text


def _validate_message(message: str) -> str:
    if not isinstance(message, str) or not message.strip():
        raise ValueError("'message' must be a non-empty string")
    return message


def generate_report(message: str) -> dict:
    """Generate a public opinion analysis report.
    Args:
        query: The query to generate a public opinion analysis report.
    Returns:
        A dictionary containing the public opinion analysis report. The result is in Markdown format.
    """
    root = API_BASE_URL
    api_key = _resolve_api_key(root)
    chat_url = f"{root}/api/chat"
    headers = {"Content-Type": "application/json", "podName": "public-opinion-report-skill-user", "podNameSpace": "beta-nlp"}
    if api_key:
        headers["Authorization"] = "Bearer %s" % api_key

    body = {"messages": [{"role": "user", "content": message}]}
    response = requests.post(chat_url, json=body, headers=headers, timeout=1200)
    response.raise_for_status()
    data = response.json()
    if "result" not in data:
        raise ValueError("Unexpected response: missing 'result' field")
    return data


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 report.py '<JSON>'")
        sys.exit(1)

    raw = sys.argv[1]
    try:
        parse_data = json.loads(raw)
    except json.JSONDecodeError as e:
        print("JSON parse error: %s" % e)
        sys.exit(1)

    if not isinstance(parse_data, dict):
        print("Error: root JSON must be an object.")
        sys.exit(1)

    extra = set(parse_data.keys()) - {"message"}
    if extra:
        print("Error: unknown keys: %s (only 'messages' is allowed)" % ", ".join(sorted(extra)))
        sys.exit(1)

    try:
        message = parse_data.get("message")
    except ValueError as e:
        print("Error: %s" % e)
        sys.exit(1)

    try:
        out = generate_report(message)
        print(json.dumps(out, indent=2, ensure_ascii=False))
    except requests.HTTPError as e:
        print("HTTP error: %s" % e)
        if e.response is not None and e.response.text:
            print(e.response.text[:2000])
        sys.exit(1)
    except Exception as e:
        print("Error: %s" % e)
        sys.exit(1)


    # _resolve_api_key(API_BASE_URL)
    # print("API key resolved successfully")