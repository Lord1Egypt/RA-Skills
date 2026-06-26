import sys
import json
import requests
import os


DEFAULT_WEB_SEARCH_URL = "https://qianfan.baidubce.com/v2/ai_search/web_search"
DEFAULT_CHAT_URL = "https://qianfan.baidubce.com/v2/ai_search/chat/completions"
DEFAULT_SUMMARY_URL = "https://qianfan.baidubce.com/v2/ai_search/web_summary"


def _post_json(url, api_key, request_body):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "X-Appbuilder-From": "openclaw",
        "Content-Type": "application/json",
    }
    resp = requests.post(url, json=request_body, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code"):
        raise Exception(data.get("message", f"API error code={data.get('code')}"))
    return data


def _normalize_results(results, source=None, endpoint=None):
    refs = results.get("references", [])
    if refs:
        out = []
        for item in refs:
            item = dict(item)
            item.pop("snippet", None)
            item["source"] = source
            item["source_endpoint"] = endpoint
            item["request_id"] = results.get("request_id") or results.get("id", "")
            out.append(item)
        return out

    answer = (
        results.get("result")
        or results.get("choices", [{}])[0].get("message", {}).get("content", "")
    )
    return [{
        "answer": answer,
        "request_id": results.get("request_id") or results.get("id", ""),
        "source": source,
        "source_endpoint": endpoint,
    }]


def _build_request_body(parse_data):
    return {
        "messages": [
            {
                "content": parse_data["query"],
                "role": "user",
            }
        ],
        "stream": parse_data.get("stream", False),
        "edition": parse_data.get("edition", "standard"),
        "search_source": "baidu_search_v2",
        "resource_type_filter": parse_data.get(
            "resource_type_filter", [{"type": "web", "top_k": 20}]
        ),
        "search_filter": parse_data.get("search_filter", {}),
        "block_websites": parse_data.get("block_websites"),
        "search_recency_filter": parse_data.get("search_recency_filter", "year"),
        "safe_search": parse_data.get("safe_search", False),
    }


def _run_endpoint(url, api_key, request_body, source):
    return _normalize_results(_post_json(url, api_key, request_body), source=source, endpoint=url)


def _search_chain_urls():
    # 百度更新后，chat 与 web_search 在搜索场景下经常返回同构 references；
    # 默认优先走更直观稳定的 web_search，把 chat 降级为兼容回退。
    web_url = os.getenv("BAIDU_WEB_SEARCH_ENDPOINT", DEFAULT_WEB_SEARCH_URL)
    chat_url = os.getenv("BAIDU_CHAT_SEARCH_ENDPOINT", DEFAULT_CHAT_URL)

    urls = [("web_search", web_url)]
    if chat_url and chat_url != web_url:
        urls.append(("chat", chat_url))
    return urls


def _run_search_chain(api_key, request_body):
    errors = []
    for source, url in _search_chain_urls():
        try:
            return _run_endpoint(url, api_key, request_body, source)
        except Exception as e:
            errors.append(f"{source}_failed({url}): {e}")

    raise Exception("; ".join(errors) if errors else "Unknown search API error")


def _run_summary_last_chain(api_key, request_body):
    summary_url = os.getenv("BAIDU_SUMMARY_ENDPOINT", DEFAULT_SUMMARY_URL)

    errors = []
    try:
        return _run_search_chain(api_key, request_body)
    except Exception as e:
        errors.append(str(e))

    try:
        return _run_endpoint(summary_url, api_key, request_body, "web_summary")
    except Exception as e:
        errors.append(f"summary_failed({summary_url}): {e}")

    raise Exception("; ".join(errors) if errors else "Unknown search/summary API error")


def _route_mode(parse_data):
    mode = parse_data.get("mode", "auto").lower()
    if mode in {"summary", "search", "auto"}:
        return mode
    return "auto"


def baidu_route(api_key, parse_data):
    request_body = _build_request_body(parse_data)
    mode = _route_mode(parse_data)

    if mode == "summary":
        summary_url = os.getenv("BAIDU_SUMMARY_ENDPOINT", DEFAULT_SUMMARY_URL)
        return _run_endpoint(summary_url, api_key, request_body, "web_summary")

    if mode == "search":
        return _run_search_chain(api_key, request_body)

    # auto: search-first, summary-last fallback
    return _run_summary_last_chain(api_key, request_body)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search.py '<JSON>'")
        sys.exit(1)

    raw = sys.argv[1]
    parse_data = {}
    try:
        parse_data = json.loads(raw)
        print(f"success parse request body: {parse_data}")
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")

    if "query" not in parse_data:
        print("Error: query must be present in request body.")
        sys.exit(1)

    api_key = os.getenv("BAIDU_API_KEY")
    if not api_key:
        print("Error: BAIDU_API_KEY must be set in environment.")
        sys.exit(1)

    try:
        results = baidu_route(api_key, parse_data)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
