"""scripts/parallel.py - L3 并行研究（§5.x / M19–M24）。planner → 并行 crawler → publisher。"""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List

CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json"
)
MAX_WORKERS = 8


from common import load_config as _load_cfg


def _crawl_one(
    sub: Dict[str, Any], cfg: Dict[str, Any], web_fetch=None, doi_resolver=None, github_token=None
) -> List[Dict[str, Any]]:
    try:
        import connector
        import extract

        docs = connector.load(
            sub["q"],
            sub.get("freshness", "中"),
            None,
            cfg,
            web_fetch=web_fetch,
            doi_resolver=doi_resolver,
            github_token=github_token,
        )
        for d in docs:
            extract.extract(d, cfg)
        return docs
    except Exception:
        return []


def run_l3(
    query: str,
    constraints: dict = None,
    cfg: Dict[str, Any] = None,
    web_fetch: Any = None,
    doi_resolver: Any = None,
    github_token: Any = None,
) -> List[Dict[str, Any]]:
    """L3 编排：意图→叶子拆解→并行抓取+抽取→返回 doc 列表（去重/打分在 orchestrate 做）。

    透传"调用方注入"回调（web_fetch/doi_resolver/github_token）到每个 leaf 的 connector.load，
    避免 L3 并行路径静默丢弃调用方注入的 GitHub token / DOI resolver / web_fetch 兜底（D1）。
    """
    cfg = _load_cfg(cfg)
    import plan

    intent = plan.classify_intent(query)
    cap = cfg.get("tier_defaults", {}).get("L3", {}).get("max_sources", 20)
    leaves = plan.plan_queries(query, intent, width_cap=cap)
    docs: List[Dict[str, Any]] = []
    tasks = [lv for lv in leaves if not lv.get("truncated")]
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futs = [
            ex.submit(_crawl_one, lv, cfg, web_fetch, doi_resolver, github_token) for lv in tasks
        ]
        for f in as_completed(futs):
            docs += f.result()
    return docs
