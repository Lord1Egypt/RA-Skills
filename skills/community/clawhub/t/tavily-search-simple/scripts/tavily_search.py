#!/usr/bin/env python3
import argparse
import json
import os
import pathlib
import re
import sys
import urllib.request

TAVILY_URL = "https://api.tavily.com/search"

TAVILY_COUNTRY_CHOICES = (
    "afghanistan",
    "albania",
    "algeria",
    "andorra",
    "angola",
    "argentina",
    "armenia",
    "australia",
    "austria",
    "azerbaijan",
    "bahamas",
    "bahrain",
    "bangladesh",
    "barbados",
    "belarus",
    "belgium",
    "belize",
    "benin",
    "bhutan",
    "bolivia",
    "bosnia and herzegovina",
    "botswana",
    "brazil",
    "brunei",
    "bulgaria",
    "burkina faso",
    "burundi",
    "cambodia",
    "cameroon",
    "canada",
    "cape verde",
    "central african republic",
    "chad",
    "chile",
    "china",
    "colombia",
    "comoros",
    "congo",
    "costa rica",
    "croatia",
    "cuba",
    "cyprus",
    "czech republic",
    "denmark",
    "djibouti",
    "dominican republic",
    "ecuador",
    "egypt",
    "el salvador",
    "equatorial guinea",
    "eritrea",
    "estonia",
    "ethiopia",
    "fiji",
    "finland",
    "france",
    "gabon",
    "gambia",
    "georgia",
    "germany",
    "ghana",
    "greece",
    "guatemala",
    "guinea",
    "haiti",
    "honduras",
    "hungary",
    "iceland",
    "india",
    "indonesia",
    "iran",
    "iraq",
    "ireland",
    "israel",
    "italy",
    "jamaica",
    "japan",
    "jordan",
    "kazakhstan",
    "kenya",
    "kuwait",
    "kyrgyzstan",
    "latvia",
    "lebanon",
    "lesotho",
    "liberia",
    "libya",
    "liechtenstein",
    "lithuania",
    "luxembourg",
    "madagascar",
    "malawi",
    "malaysia",
    "maldives",
    "mali",
    "malta",
    "mauritania",
    "mauritius",
    "mexico",
    "moldova",
    "monaco",
    "mongolia",
    "montenegro",
    "morocco",
    "mozambique",
    "myanmar",
    "namibia",
    "nepal",
    "netherlands",
    "new zealand",
    "nicaragua",
    "niger",
    "nigeria",
    "north korea",
    "north macedonia",
    "norway",
    "oman",
    "pakistan",
    "panama",
    "papua new guinea",
    "paraguay",
    "peru",
    "philippines",
    "poland",
    "portugal",
    "qatar",
    "romania",
    "russia",
    "rwanda",
    "saudi arabia",
    "senegal",
    "serbia",
    "singapore",
    "slovakia",
    "slovenia",
    "somalia",
    "south africa",
    "south korea",
    "south sudan",
    "spain",
    "sri lanka",
    "sudan",
    "sweden",
    "switzerland",
    "syria",
    "taiwan",
    "tajikistan",
    "tanzania",
    "thailand",
    "togo",
    "trinidad and tobago",
    "tunisia",
    "turkey",
    "turkmenistan",
    "uganda",
    "ukraine",
    "united arab emirates",
    "united kingdom",
    "united states",
    "uruguay",
    "uzbekistan",
    "venezuela",
    "vietnam",
    "yemen",
    "zambia",
    "zimbabwe",
)


def load_key():
    key = os.environ.get("TAVILY_API_KEY")
    if key:
        return key.strip()

    env_path = pathlib.Path.home() / ".openclaw" / ".env"
    if env_path.exists():
        try:
            txt = env_path.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"^\s*TAVILY_API_KEY\s*=\s*(.+?)\s*$", txt, re.M)
            if m:
                v = m.group(1).strip().strip('"').strip("'")
                if v:
                    return v
        except Exception:
            pass

    return None


def tavily_search(**kwargs):
    key = load_key()
    if not key:
        raise SystemExit(
            "Missing TAVILY_API_KEY. Set env var TAVILY_API_KEY or add it to ~/.openclaw/.env"
        )

    # 构造基础请求载荷
    payload = {
        "api_key": key,
        "query": kwargs.get("query"),
        "max_results": kwargs.get("max_results", 5),
        "search_depth": kwargs.get("search_depth", "basic"),
        "topic": kwargs.get("topic", "general"),
        "include_images": kwargs.get("include_images", False),
        "auto_parameters": kwargs.get("auto_parameters", False),
        "chunks_per_source": kwargs.get("chunks_per_source", 3),
    }

    # 附加可选参数
    for date_field in ["time_range", "start_date", "end_date"]:
        if kwargs.get(date_field):
            payload[date_field] = kwargs.get(date_field)

    if payload["topic"] == "general" and kwargs.get("country"):
        payload["country"] = kwargs.get("country")
            
    # 处理布尔/字符串混合类型参数
    inc_answer = kwargs.get("include_answer")
    payload["include_answer"] = True if str(inc_answer).lower() == "true" else (inc_answer if inc_answer else False)

    inc_raw = kwargs.get("include_raw_content")
    payload["include_raw_content"] = True if str(inc_raw).lower() == "true" else (inc_raw if inc_raw else False)

    # 处理域名过滤列表
    if kwargs.get("include_domains"):
        payload["include_domains"] = [d.strip() for d in kwargs.get("include_domains").split(",") if d.strip()]
        
    if kwargs.get("exclude_domains"):
        payload["exclude_domains"] = [d.strip() for d in kwargs.get("exclude_domains").split(",") if d.strip()]

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        TAVILY_URL,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Tavily API Error {e.code}: {err_body}")

    try:
        obj = json.loads(body)
    except json.JSONDecodeError:
        raise SystemExit(f"Tavily returned non-JSON: {body[:300]}")

    # 规范化输出格式
    out = {
        "query": kwargs.get("query"),
        "results": [],
    }
    
    if obj.get("answer"):
        out["answer"] = obj.get("answer")

    for r in (obj.get("results") or [])[:kwargs.get("max_results", 5)]:
        result_item = {
            "title": r.get("title"),
            "url": r.get("url"),
            "content": r.get("content"),
        }
        if payload.get("include_raw_content") and r.get("raw_content"):
            result_item["raw_content"] = r.get("raw_content")
        out["results"].append(result_item)

    if payload.get("include_images") and obj.get("images"):
        out["images"] = obj.get("images")

    return out


def to_brave_like(obj: dict) -> dict:
    results = []
    for r in obj.get("results", []) or []:
        results.append(
            {
                "title": r.get("title"),
                "url": r.get("url"),
                "snippet": r.get("content"),
            }
        )
    out = {"query": obj.get("query"), "results": results}
    if "answer" in obj:
        out["answer"] = obj.get("answer")
    return out


def to_markdown(obj: dict) -> str:
    lines = []
    if obj.get("answer"):
        lines.append(f"**Answer:** {obj['answer'].strip()}\n")
    for i, r in enumerate(obj.get("results", []) or [], 1):
        title = (r.get("title") or "").strip() or r.get("url") or "(no title)"
        url = r.get("url") or ""
        snippet = (r.get("content") or "").strip()
        lines.append(f"{i}. **{title}**")
        if url:
            lines.append(f"   {url}")
        if snippet:
            lines.append(f"   > {snippet}")
    return "\n".join(lines).strip() + "\n"


def main():
    ap = argparse.ArgumentParser(description="Tavily Search API CLI")
    ap.add_argument("--query", required=True, help="搜索关键词")
    ap.add_argument("--search-depth", default="basic", choices=["basic", "advanced", "fast", "ultra-fast"], help="搜索深度")
    ap.add_argument("--topic", default="general", choices=["general", "news", "finance"], help="搜索主题")
    ap.add_argument("--country", default=None, choices=TAVILY_COUNTRY_CHOICES, help="国家/地区偏好（仅 topic=general 时发往 API）")
    ap.add_argument("--time-range", default=None, choices=["day", "week", "month", "year", "d", "w", "m", "y"], help="时间过滤")
    ap.add_argument("--start-date", default=None, help="起始日期 YYYY-MM-DD")
    ap.add_argument("--end-date", default=None, help="结束日期 YYYY-MM-DD")
    ap.add_argument("--max-results", type=int, default=5, help="最大返回结果数 (0-20)")
    
    # Optional parameters that map to strings or booleans
    ap.add_argument("--include-answer", nargs="?", const="basic", default=False, help="是否包含AI答案 (可选 basic/advanced)")
    ap.add_argument("--include-raw-content", nargs="?", const="markdown", default=False, help="是否包含原始内容 (可选 markdown)")
    ap.add_argument("--include-images", action="store_true", default=False, help="是否包含图片")
    
    ap.add_argument("--include-domains", default=None, help="仅搜索特定域名 (逗号分隔)")
    ap.add_argument("--exclude-domains", default=None, help="排除特定域名 (逗号分隔)")
    ap.add_argument("--chunks-per-source", type=int, default=3, help="每个来源的文本块数 (1-3)")
    ap.add_argument("--auto-parameters", action="store_true", help="允许自动配置参数")
    
    ap.add_argument("--format", default="raw", choices=["raw", "brave", "md"], help="输出格式控制")
    
    args = ap.parse_args()

    # 边界限制
    max_results = max(1, min(args.max_results, 20))
    chunks_per_source = max(1, min(args.chunks_per_source, 3))

    res = tavily_search(
        query=args.query,
        max_results=max_results,
        search_depth=args.search_depth,
        topic=args.topic,
        country=args.country,
        time_range=args.time_range,
        start_date=args.start_date,
        end_date=args.end_date,
        include_answer=args.include_answer,
        include_raw_content=args.include_raw_content,
        include_images=args.include_images,
        include_domains=args.include_domains,
        exclude_domains=args.exclude_domains,
        chunks_per_source=chunks_per_source,
        auto_parameters=args.auto_parameters
    )

    if args.format == "md":
        sys.stdout.write(to_markdown(res))
        return

    if args.format == "brave":
        res = to_brave_like(res)

    json.dump(res, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()