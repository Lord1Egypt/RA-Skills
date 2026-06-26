import sys
import json
import os

import requests


def _load_env_from_config() -> dict:
    """Read skill env from ~/.openclaw/openclaw.json under skills.entries.turing-skills.env."""
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    try:
        with open(config_path) as f:
            config = json.load(f)
        return (
            config.get("skills", {})
            .get("entries", {})
            .get("turing-skills", {})
            .get("env", {})
        )
    except Exception:
        return {}


def _getcfg(key: str, cfg: dict) -> str:
    return cfg.get(key, "")


def turing_search(api_key: str, client: str, environment: str, api_base: str, request_body: dict) -> list:
    url = f"{api_base}/api/v1/proxy/tavily/search"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "client": client,
        "environment": environment,
        "Content-Type": "application/json",
        "User-Agent": "openclaw-tavily-web-search",
    }

    response = requests.post(url, json=request_body, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()

    if "code" in data and data["code"] != 200:
        raise Exception(data.get("message", "Unknown error"))

    results = data.get("results", [])
    keys_to_remove = {"score"}
    for item in results:
        for key in keys_to_remove:
            item.pop(key, None)

    output = {"results": results}
    if data.get("answer"):
        output["answer"] = data["answer"]

    return output


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts.py '<JSON>'")
        sys.exit(1)

    try:
        parse_data = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        sys.exit(1)

    if "query" not in parse_data:
        print("Error: 'query' must be present in request body.")
        sys.exit(1)

    _cfg        = _load_env_from_config()
    api_key     = _getcfg("TURING_API_KEY", _cfg)
    client      = _getcfg("TURING_CLIENT", _cfg)
    environment = _getcfg("TURING_ENVIRONMENT", _cfg)
    api_base    = (_getcfg("TURING_API_BASE", _cfg) or "https://live-turing.cn.llm.tcljd.com").rstrip("/")

    for name, val in [("TURING_API_KEY", api_key), ("TURING_CLIENT", client), ("TURING_ENVIRONMENT", environment)]:
        if not val:
            print(f"Error: {name} must be set in environment.")
            sys.exit(1)

    request_body = {
        "query":              parse_data["query"],
        "max_results":        parse_data.get("max_results", 10),
        "max_tokens_per_page": parse_data.get("max_tokens_per_page", 1024),
    }
    if "search_domain_filter" in parse_data:
        request_body["search_domain_filter"] = parse_data["search_domain_filter"]

    try:
        result = turing_search(api_key, client, environment, api_base, request_body)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
