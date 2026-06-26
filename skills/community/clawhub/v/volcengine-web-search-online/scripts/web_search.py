#!/usr/bin/env python3
"""
火山联网搜索 API 调用脚本
接口：POST https://coze-js-api.devtool.uk/volcengine/web-search
购买/查看文档：https://devtool.uk/plugin
"""

import argparse
import json
import os
import sys

try:
    import requests
except ImportError:
    print("缺少依赖库，请先安装：pip install requests", file=sys.stderr)
    sys.exit(1)

API_URL = "https://coze-js-api.devtool.uk/volcengine/web-search"


def parse_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError("布尔参数仅支持 true/false")


def get_api_key(arg_key: str | None) -> str:
    key = arg_key or os.environ.get("AZT_API_KEY", "").strip()
    if not key:
        print(
            "❌ 未检测到 API Key。\n"
            "   请前往 https://devtool.uk/plugin 购买或查看使用说明，\n"
            "   然后通过以下任一方式提供 Key：\n"
            "   1. 设置环境变量：export AZT_API_KEY=\"your_key\"\n"
            "   2. 传入参数：python3 web_search.py --azt_api_key your_key --query 关键词 --search_type web",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def web_search(
    api_key: str,
    query: str,
    search_type: str,
    count: int | None,
    need_summary: bool | None,
    time_range: str | None,
    content_formats: str | None,
    industry: str | None,
    query_rewrite: bool | None,
) -> dict:
    payload: dict = {
        "api_key": api_key,
        "query": query,
        "search_type": search_type,
    }

    if count is not None:
        payload["count"] = count
    if need_summary is not None:
        payload["need_summary"] = need_summary
    if time_range:
        payload["time_range"] = time_range
    if content_formats:
        payload["content_formats"] = content_formats
    if industry:
        payload["industry"] = industry
    if query_rewrite is not None:
        payload["query_control"] = {"QueryRewrite": query_rewrite}

    try:
        response = requests.post(
            API_URL,
            json=payload,
            timeout=60,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print("❌ 请求超时，请检查网络后重试。", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as exc:
        print(f"❌ 请求失败：{exc}", file=sys.stderr)
        sys.exit(1)


def print_results(resp: dict) -> None:
    code = resp.get("code")
    msg = resp.get("msg", "")

    if code != 200:
        print(f"❌ 接口返回错误（code={code}）：{msg}")
        data = resp.get("data")
        if data is not None:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        sys.exit(1)

    data = resp.get("data", {})
    search_context = data.get("search_context") if isinstance(data, dict) else None
    search_type = ""
    if isinstance(search_context, dict):
        search_type = str(search_context.get("SearchType") or search_context.get("search_type") or "")

    print(f"✅ 请求成功  {msg}")
    print("-" * 70)
    print(f"request_id: {data.get('request_id')}")
    print(f"result_count: {data.get('result_count')}")
    if search_context:
        print(f"search_context: {json.dumps(search_context, ensure_ascii=False)}")

    summary_text = data.get("summary_text") if isinstance(data, dict) else None
    if summary_text:
        print("\n【summary_text】")
        print(summary_text)

    usage = data.get("usage") if isinstance(data, dict) else None
    if usage:
        print("\n【usage】")
        print(json.dumps(usage, ensure_ascii=False, indent=2))

    if search_type in {"web", "web_summary"}:
        web_results = data.get("web_results") if isinstance(data, dict) else None
        if isinstance(web_results, list) and web_results:
            print("\n【web_results】")
            for idx, item in enumerate(web_results, start=1):
                title = item.get("Title") or item.get("title") or "—"
                url = item.get("Url") or item.get("url") or "—"
                snippet = item.get("Snippet") or item.get("snippet") or ""
                print(f"{idx:>2}. {title}")
                print(f"    {url}")
                if snippet:
                    print(f"    {snippet}")
                print()

    if search_type == "image":
        image_results = data.get("image_results") if isinstance(data, dict) else None
        if isinstance(image_results, list) and image_results:
            print("\n【image_results】")
            for idx, item in enumerate(image_results, start=1):
                title = item.get("Title") or item.get("title") or "—"
                url = item.get("Url") or item.get("url") or "—"
                img = item.get("Image") or item.get("image") or {}
                img_url = img.get("Url") if isinstance(img, dict) else None
                print(f"{idx:>2}. {title}")
                print(f"    page: {url}")
                if img_url:
                    print(f"    image: {img_url}")
                print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="调用火山联网搜索接口",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例：\n"
            "  python3 web_search.py --query \"今日最新的AI资讯\" --search_type web_summary --need_summary true\n"
            "  python3 web_search.py --query \"北京天气\" --search_type image --count 5"
        ),
    )

    parser.add_argument("--query", required=True, help="搜索词（必填）")
    parser.add_argument("--search_type", required=True, choices=["web", "web_summary", "image"], help="搜索类型（必填）")
    parser.add_argument("--azt_api_key", default=None, help="API Key（也可通过环境变量 AZT_API_KEY 设置）")

    parser.add_argument("--count", type=int, default=None, help="返回条数（默认走接口 20）")
    parser.add_argument("--need_summary", type=parse_bool, default=None, help="是否需要总结：true/false")
    parser.add_argument("--time_range", default=None, help="时间范围，如 OneDay/OneWeek/OneMonth/OneYear")
    parser.add_argument("--content_formats", default=None, help="正文格式：text/markdown")
    parser.add_argument("--industry", default=None, help="行业类型，如 finance/game")
    parser.add_argument("--query_rewrite", type=parse_bool, default=None, help="是否开启 QueryRewrite：true/false")

    parser.add_argument("--json", action="store_true", dest="output_json", help="输出原始 JSON")
    args = parser.parse_args()

    api_key = get_api_key(args.azt_api_key)

    result = web_search(
        api_key=api_key,
        query=args.query,
        search_type=args.search_type,
        count=args.count,
        need_summary=args.need_summary,
        time_range=args.time_range,
        content_formats=args.content_formats,
        industry=args.industry,
        query_rewrite=args.query_rewrite,
    )

    if args.output_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_results(result)


if __name__ == "__main__":
    main()
