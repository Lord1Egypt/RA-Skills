"""scripts/connector.py - 连接器 + 失败隔离(B5) + 可选 SearXNG(B9)（§5.8）。"""

import threading
from typing import Any, Dict, List

from common import load_config as _load_config

# 跨源 warning 累积（供 orchestrate 透出到返回 meta.warnings）。
# 用锁 +「原子整体替换」而非 clear/extend 交错，避免 L3 多线程并行调用 load 时
# 对全局 list 的并发 clear/extend 互相覆盖导致 warnings 丢失/错乱（D2）。
_warn_lock = threading.Lock()
LAST_WARNINGS: List[str] = []


def _cfg_section(cfg: dict, *path: str) -> dict:
    """安全嵌套取值：逐层 dict.get，任意层缺失/非 dict 返回 {}（不抛 KeyError）。"""
    node: Any = cfg or {}
    for k in path:
        if not isinstance(node, dict):
            return {}
        node = node.get(k) or {}
    return node if isinstance(node, dict) else {}


def _select(query: str, constraints: dict, cfg: Dict[str, Any], freshness: str = "中") -> List[str]:
    """按 domain 命中垂直源；否则通用 cn+global 精选；SearXNG 启用时折叠为单一入口。

    cfg 缺 engines/searxng 键时按默认引擎收敛，不抛 KeyError（调用方可传裁剪过的 cfg）。
    P1-4 时效性：当 freshness 为近窗口（近1月/3月/6月/1年）时，把名称含 "news" 的引擎
    优先排到前面（若配置了新闻类引擎）；默认 Baidu/Sogou 不含 news，顺序不变（真实时效杠杆在打分/排序）。
    """
    domain = (constraints or {}).get("domain")
    vertical = _cfg_section(cfg, "engines", "vertical")
    if domain and domain in vertical:
        engines = [e["id"] for e in vertical[domain]]
    else:
        searxng = _cfg_section(cfg, "searxng")
        if searxng.get("enabled") and searxng.get("url"):
            engines = ["__searxng__"]
        else:
            # 路径B：默认仅百度/搜狗内部抓取（沙箱可达）；其余引擎由 agent 层用 web_fetch 扩展
            engines = ["Baidu", "Sogou"]
    if freshness in ("近1月", "近3月", "近6月", "近1年"):
        engines = sorted(engines, key=lambda e: (0 if "news" in str(e).lower() else 1, str(e)))
    return engines


_FINANCE_KW = [
    "股价",
    "股市",
    "股票",
    "财报",
    "营收",
    "市值",
    "波动",
    "k线",
    "K线",
    "市盈率",
    "净利润",
    "季报",
    "年报",
    "上市",
    "退市",
    "券商",
    "研报",
    "主力资金",
    "净流入",
    "涨跌",
    "行情",
]
_GITHUB_KW = [
    "github",
    "开源",
    "代码仓库",
    "repo",
    "sdk",
    "框架",
    "npm",
    "pip install",
    "源码",
    "star数",
    "star 数",
    "issue",
    "pull request",
    "代码库",
    "开源项目",
]

_ACADEMIC_KW = [
    "arxiv",
    "论文",
    "文献",
    "doi",
    "参考文献",
    "预印本",
    "综述文献",
    "学术搜索",
    "citation",
    "引用文献",
    "期刊",
]


def _source_intent(query: str) -> str:
    """零 LLM 意图路由：finance / github / general。

    命中金融/GitHub 关键词则路由到原生检索域（B1/B2）；否则走通用检索。
    """
    q = (query or "").lower()
    if any(k in q for k in _GITHUB_KW):
        return "github"
    if any(k in q for k in _FINANCE_KW):
        return "finance"
    if any(k in q for k in _ACADEMIC_KW):
        return "academic"
    return "general"


def _general_search(
    query: str, freshness: str, constraints: dict, cfg: Dict[str, Any], web_fetch: Any
) -> List[Dict[str, Any]]:
    """通用检索路径（B5 失败隔离 + 降级换源）。金融/GitHub 路由空返回时复用。"""
    engine_ids = _select(query, constraints, cfg, freshness)
    docs: List[Dict[str, Any]] = []
    for eid in engine_ids:
        try:
            if eid == "__searxng__":
                from searxng_client import fetch as fetch_searxng

                docs += fetch_searxng(query, cfg, web_fetch=web_fetch)
                continue
            import search

            docs += search.fetch(eid, query, freshness, cfg)
        except Exception:
            continue  # B5：单源失败跳过，不中断
    if not docs:
        try:
            import search

            docs = search.fetch("Baidu", query, freshness, cfg)  # 降级
        except Exception:
            docs = []
    return docs


def load(
    query: str,
    freshness: str = "中",
    constraints: dict = None,
    cfg: Dict[str, Any] = None,
    web_fetch: Any = None,
    doi_resolver: Any = None,
    github_token: Any = None,
) -> List[Dict[str, Any]]:
    """统一接口 load()；原生检索域路由（B1/B2）+ 通用路径（B5 失败隔离 + 降级换源）。

    web_fetch：可选回调（agent/CodeBuddy 注入），供金融/GitHub 主传输失败时兜底抓网页。
    跨源 warning 累积到 LAST_WARNINGS（线程安全），由 orchestrate 透出到返回 meta.warnings。
    """
    cfg = cfg or _load_config()
    warns: List[str] = []

    # 原生检索域路由（B1 金融 / B2 GitHub）
    intent = _source_intent(query)
    if intent == "finance":
        import finance

        docs, warns = finance.fetch(query, cfg, web_fetch)
        if not docs:
            # 金融源空返回（名称未识别/接口被封且无 web_fetch）→ 降级通用检索，避免静默空壳
            warns.append("金融源未返回数据，已降级为通用检索（如需财报请改用股票代码）")
            docs = _general_search(query, freshness, constraints, cfg, web_fetch)
    elif intent == "github":
        import github

        docs, warns = github.search(query, cfg, web_fetch, github_token=github_token)
    elif intent == "academic":
        import academic

        docs, warns = academic.search(query, cfg, web_fetch, doi_resolver=doi_resolver)
    else:
        docs = _general_search(query, freshness, constraints, cfg, web_fetch)

    with _warn_lock:
        LAST_WARNINGS[:] = warns  # 原子整体替换，避免并发 clear/extend 交错
    return docs
