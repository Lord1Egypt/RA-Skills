"""scripts/deepfetch.py - 两跳取源：SERP → 落地页（方案 B / §5.5）。

第一跳 SERP 已由 connector 取回（robots 按 Plan A 分层豁免）。本模块做第二跳：
  1) 解析 SERP 结果链接（extract.parse_serp_links）
  2) 抓落地页：跨域直链严格守 robots（落地页守 robots）；经搜索引擎重定向器(/link?)进入的
     继承 SERP 豁免（等同于用户点击结果跳转，meta.serp_exempt=True）
  3) trafilatura 抽干净正文
  4) 用落地页替换原 SERP doc 的 url/text/snippet/source_type（保留 engine 归因 + serp_url 溯源）

落地页取不到（被封/空正文）时：按 fallback_to_serp 回退保留 SERP 片段（标 landing_failed）；
若 fallback=False 则丢弃该噪声源。deep_fetch.enabled=false 时原样返回 SERP doc（单跳）。
"""

import os
import sys
from functools import partial
from typing import Any, Dict, List

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from common import load_config as _load_cfg

# 最近一次 resolve() 的落地页统计（观测用；两跳失败率是"取源质量"的先行指标）
LAST_STATS: Dict[str, int] = {
    "serp_docs": 0,
    "resolved": 0,
    "no_links": 0,
    "unreachable": 0,
    "dropped": 0,
}


def _is_redirector(url: str, engine: str) -> bool:
    """搜索引擎结果重定向器（同域、继续 302 到真实站点）→ 继承 SERP 豁免。"""
    u = (url or "").lower()
    if engine == "Baidu" and "/link" in u:
        return True
    if "baidu.com/link" in u or "sogou.com/link" in u:
        return True
    return False


def _fetch_landing(u: str, engine: str, cfg, cache, timeout: int):
    """抓取单个落地页（P3 抽出的模块级函数，便于经 partial 复用线程池）。"""
    try:
        if cache:
            c = cache.get(u)
            if c and c.get("text"):
                return (
                    u,
                    c.get("text"),
                    c.get("title", ""),
                    c.get("snippet", ""),
                    c.get("url") or u,
                    True,
                )
        from scrape import scrape

        serp_exempt = _is_redirector(u, engine)
        lhtml, meta = scrape(
            u, {"engine": engine, "cfg": cfg, "serp_exempt": serp_exempt, "timeout": timeout}
        )
        return (u, lhtml, None, None, (meta or {}).get("final_url") or u, False)
    except Exception:
        return (u, None, None, None, u, False)


def resolve(
    serp_docs: List[Dict[str, Any]], cfg=None, max_pages: int = None
) -> List[Dict[str, Any]]:
    """把 SERP doc 列表解析为落地页 doc 列表（两跳第二跳）。

    返回结构与上游一致（dict 含 url/text/snippet/source_type/engine 等），
    便于 score/dedup/report/verify 无缝消费。

    性能（② 落地页慢）：每个 SERP doc 的多个落地页链接用 ThreadPoolExecutor 并发抓取
    （max_workers=max_pages），把"页数×超时"的串行延迟压成约"单页超时"。抓取前先查
    cache.Cache（受 config.cache.enabled 门控），命中则跳过网络抓取直接复用正文。
    """
    cfg = _load_cfg(cfg)
    df = cfg.get("deep_fetch", {})
    if not df.get("enabled", True):
        return list(serp_docs)  # 关闭则单跳原样返回
    max_pages = max_pages or df.get("max_pages_per_query", 3)
    fallback = df.get("fallback_to_serp", True)
    timeout = df.get("timeout_per_page", 15)

    cache = None
    try:
        from cache import Cache

        cache = Cache(cfg)
    except Exception:
        cache = None

    # P3：整次 resolve() 复用同一线程池（不再每 SERP doc 新建/销毁），并发上限仍由 max_pages 约束
    from concurrent.futures import ThreadPoolExecutor

    ex = ThreadPoolExecutor(max_workers=max(1, max_pages))

    stats = {
        "serp_docs": len(serp_docs or []),
        "resolved": 0,
        "no_links": 0,
        "unreachable": 0,
        "dropped": 0,
    }
    out: List[Dict[str, Any]] = []
    for d in serp_docs:
        html = d.get("raw_html") or ""
        engine = d.get("engine", "")
        links: List[str] = []
        try:
            from extract import parse_serp_links

            links = parse_serp_links(html, engine, cfg, max_links=max_pages, serp_url=d.get("url"))
        except Exception:
            links = []

        if not links:
            stats["no_links"] += 1
            if fallback:
                d = dict(d)
                d["landing_failed"] = True
                d["landing_fail_reason"] = "no_serp_links"
                d.setdefault("text", "")
                out.append(d)
            else:
                stats["dropped"] += 1
            continue

        # —— 并发抓取落地页（缓存命中则跳过抓取；复用整次调用的共享线程池）——
        resolved = None
        results = list(
            ex.map(
                partial(_fetch_landing, engine=engine, cfg=cfg, cache=cache, timeout=timeout),
                links[:max_pages],
            )
        )
        # 顺序取第一个有效落地页（保序、保留 SERP 归因）
        for u, lhtml, _t, _s, final_url, cached in results:
            try:
                if not lhtml:
                    continue
                from extract import extract as _ext
                from extract import is_serp_host

                ld = {"url": final_url, "raw_html": lhtml, "engine": engine}
                # 重定向器若落回搜索引擎自身门户/新闻页（非真实答案源），跳过换下一个
                if is_serp_host(ld["url"]):
                    continue
                _ext(ld, cfg)
                text = ld.get("text", "")
                if not text or len(text) < 40:
                    continue
                from search import classify_source_type

                if cache and not cached:
                    cache.put(
                        u,
                        {
                            "url": ld["url"],
                            "text": text,
                            "title": ld.get("title", ""),
                            "snippet": ld.get("snippet", ""),
                        },
                    )
                resolved = {
                    "url": ld["url"],
                    "raw_html": None,
                    "title": ld.get("title", ""),
                    "text": text,
                    "snippet": ld.get("snippet", ""),
                    "engine": engine,
                    "source_type": classify_source_type(ld["url"]),
                    "serp_url": d.get("url"),
                    "landing_resolved": True,
                }
                break
            except Exception:
                continue

        if resolved:
            stats["resolved"] += 1
            out.append(resolved)
        else:
            stats["unreachable"] += 1
            if fallback:
                d = dict(d)
                d["landing_failed"] = True
                d["landing_fail_reason"] = "landing_unreachable"
                d.setdefault("text", "")
                out.append(d)
            else:
                stats["dropped"] += 1  # fallback=False 且无落地：丢弃该 SERP 噪声源
    ex.shutdown()  # P3：释放共享线程池
    LAST_STATS.update(stats)
    return out
