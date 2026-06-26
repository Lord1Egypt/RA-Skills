#!/usr/bin/env python3
"""
wen-cai CLI — 同花顺问财全功能统一入口
合并了12个子技能：行情、指数、财务、基本资料、事件、经营、机构评级、研报、公告、新闻、选A股、选板块

依赖：仅 Python 标准库（urllib / json / os / argparse）
环境变量：
  IWENCAI_API_KEY   — 必填
  IWENCAI_BASE_URL  — 可选，默认 https://openapi.iwencai.com
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

# ─────────────────────────────────────────────
# 配置
# ─────────────────────────────────────────────
BASE_URL = os.environ.get("IWENCAI_BASE_URL", "https://openapi.iwencai.com").rstrip("/")
API_KEY  = os.environ.get("IWENCAI_API_KEY", "")

# type → (接口路径, channel)
# channel 为 None 表示使用 query2data
TYPE_MAP = {
    "market":       ("/v1/query2data",          None),
    "index":        ("/v1/query2data",          None),
    "finance":      ("/v1/query2data",          None),
    "basic":        ("/v1/query2data",          None),
    "event":        ("/v1/query2data",          None),
    "business":     ("/v1/query2data",          None),
    "rating":       ("/v1/query2data",          None),
    "stock-select": ("/v1/query2data",          None),
    "sector-select":("/v1/query2data",          None),
    "report":       ("/v1/comprehensive/search","report"),
    "announcement": ("/v1/comprehensive/search","announcement"),
    "news":         ("/v1/comprehensive/search","news"),
}

TYPE_ALIASES = {
    # 中文别名 → 英文 key
    "行情":     "market",
    "指数":     "index",
    "财务":     "finance",
    "基本资料": "basic",
    "事件":     "event",
    "经营":     "business",
    "评级":     "rating",
    "选股":     "stock-select",
    "选板块":   "sector-select",
    "研报":     "report",
    "公告":     "announcement",
    "新闻":     "news",
}

# ─────────────────────────────────────────────
# HTTP 工具
# ─────────────────────────────────────────────
def _post(url: str, payload: dict, timeout: int = 30) -> dict:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type":  "application/json",
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req  = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {err_body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"网络错误: {e.reason}") from e


# ─────────────────────────────────────────────
# 两种接口封装
# ─────────────────────────────────────────────
def call_query2data(query: str, page: str = "1", limit: str = "10",
                    is_cache: str = "1", expand_index: str = "true") -> dict:
    """行情/指数/财务/基本资料/事件/经营/评级/选股/选板块 通用接口"""
    url = f"{BASE_URL}/v1/query2data"
    payload = {
        "query":        query,
        "page":         page,
        "limit":        limit,
        "is_cache":     is_cache,
        "expand_index": expand_index,
    }
    return _post(url, payload)


def call_comprehensive(query: str, channel: str) -> dict:
    """研报(report) / 公告(announcement) / 新闻(news) 接口"""
    url = f"{BASE_URL}/v1/comprehensive/search"
    payload = {
        "channels": [channel],
        "app_id":   "AIME_SKILL",
        "query":    query,
    }
    return _post(url, payload)


# ─────────────────────────────────────────────
# 结果格式化
# ─────────────────────────────────────────────
def fmt_query2data(result: dict, limit_display: int = 30) -> str:
    status_code = result.get("status_code", 0)
    status_msg  = result.get("status_msg", "")
    if status_code != 0:
        return f"[错误] status_code={status_code}, msg={status_msg}"

    datas      = result.get("datas", [])
    code_count = result.get("code_count", 0)
    chunks     = result.get("chunks_info", {})

    if not datas:
        return "（无数据，建议访问 https://www.iwencai.com/unifiedwap/chat 查询）"

    lines = []
    lines.append(f"共找到 {code_count} 条记录，当前返回 {len(datas)} 条")
    if chunks:
        lines.append(f"查询解析: {json.dumps(chunks, ensure_ascii=False)}")
    lines.append("")

    # 收集所有字段名
    all_keys = []
    seen = set()
    for row in datas:
        for k in row:
            if k not in seen:
                seen.add(k)
                all_keys.append(k)

    # 打印为 Markdown 表格
    header = " | ".join(all_keys)
    sep    = " | ".join(["---"] * len(all_keys))
    lines.append(f"| {header} |")
    lines.append(f"| {sep} |")
    for row in datas[:limit_display]:
        vals = [str(row.get(k, "")) for k in all_keys]
        lines.append("| " + " | ".join(vals) + " |")

    if code_count > len(datas):
        lines.append(f"\n> 还有更多数据，请使用 --page 2 --limit 20 翻页查看（共 {code_count} 条）")

    lines.append("\n数据来源：同花顺问财")
    return "\n".join(lines)


def fmt_comprehensive(result: dict, limit_display: int = 20) -> str:
    items = result.get("data", [])
    if not items:
        return "（无数据，建议访问 https://www.iwencai.com/unifiedwap/chat 查询）"

    lines = [f"共返回 {len(items)} 条结果\n"]
    for i, item in enumerate(items[:limit_display], 1):
        title   = item.get("title", "（无标题）")
        date    = str(item.get("publish_date", ""))[:10]
        summary = (item.get("summary") or "")[:150]
        url     = item.get("url", "")
        lines.append(f"**[{i}] {title}** ({date})")
        if summary:
            lines.append(f"  {summary}...")
        if url:
            lines.append(f"  {url}")
        lines.append("")

    lines.append("数据来源：同花顺问财")
    return "\n".join(lines)


# ─────────────────────────────────────────────
# 主程序
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="wen-cai — 同花顺问财全功能统一 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
可用 --type 值：
  market        行情数据（股价、涨跌幅、资金流向、技术指标）
  index         指数数据（上证指数、沪深300、创业板指等）
  finance       财务数据（营收、净利润、ROE、负债率、现金流）
  basic         基本资料（公司简介、上市日期、行业、股本）
  event         事件数据（业绩预告、增发、质押、解禁、调研、监管函）
  business      经营数据（主营业务、客户、供应商、重大合同）
  rating        机构评级（研报评级、目标价、业绩预测、ESG、券商金股）
  stock-select  A股选股（按行情/财务/技术形态/行业概念筛选）
  sector-select 板块筛选（行业/概念/地域板块，按资金/涨跌幅等筛选）
  report        研报搜索（主流投研机构研究报告）
  announcement  公告搜索（年报/季报/分红/回购/重组等公告）
  news          新闻搜索（财经新闻、行业动态、政策资讯）

示例：
  python3 scripts/cli.py --type market --query "比亚迪最新价格涨跌幅"
  python3 scripts/cli.py --type finance --query "比亚迪2025年净利润ROE"
  python3 scripts/cli.py --type report --query "新能源车行业研报"
  python3 scripts/cli.py --type announcement --query "比亚迪最新公告"
  python3 scripts/cli.py --type stock-select --query "今日涨幅超5%的A股" --limit 20
  python3 scripts/cli.py --type news --query "人工智能政策动态"
        """
    )
    parser.add_argument("--type",    required=True, help="查询类型，见上方说明")
    parser.add_argument("--query",   required=True, help="自然语言查询内容")
    parser.add_argument("--page",    default="1",   help="分页，从1开始（query2data接口）")
    parser.add_argument("--limit",   default="10",  help="每页条数（query2data接口）")
    parser.add_argument("--is-cache",default="1",   help="是否使用缓存（1=是，0=否）")
    parser.add_argument("--api-key", default="",    help="API Key（默认从 IWENCAI_API_KEY 环境变量读取）")
    parser.add_argument("--json",    action="store_true", help="输出原始 JSON")
    args = parser.parse_args()

    # 覆盖全局 API_KEY（若命令行传入）
    global API_KEY
    if args.api_key:
        API_KEY = args.api_key

    if not API_KEY:
        print("[错误] 未设置 IWENCAI_API_KEY 环境变量，请先执行：\n"
              "  export IWENCAI_API_KEY='your-key'", file=sys.stderr)
        sys.exit(1)

    # 解析 type，支持中文别名
    qtype = args.type.strip()
    qtype = TYPE_ALIASES.get(qtype, qtype)

    if qtype not in TYPE_MAP:
        print(f"[错误] 不支持的 --type '{qtype}'。\n"
              f"支持的类型：{', '.join(TYPE_MAP)}", file=sys.stderr)
        sys.exit(1)

    _, channel = TYPE_MAP[qtype]

    try:
        if channel is None:
            # query2data
            result = call_query2data(
                query        = args.query,
                page         = args.page,
                limit        = args.limit,
                is_cache     = args.is_cache,
            )
            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(fmt_query2data(result))
        else:
            # comprehensive/search
            result = call_comprehensive(args.query, channel)
            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(fmt_comprehensive(result))

    except RuntimeError as e:
        print(f"[错误] {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
