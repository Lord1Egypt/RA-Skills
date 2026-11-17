"""tests/test_hardening.py - 上线前收尾加固回归（缺陷排查/边界/并发/去重）。

锁定本轮修复，防复发：
- 停止判定传参（首轮不得被自身结果遮蔽 → "连续两轮无新信息"变死代码）
- 系统 curl 兜底的真实 HTTP 状态码（原恒返 0，429/503 退避信号丢失）
- cfg 裁剪后的引擎选择容错（原直接索引 cfg["engines"] 抛 KeyError）
- 外部 docs 缺 url 的兜底（不可被引文校验消费，不静默进 sources）
- 跨轮证据按 url 去重（多轮研究回传上一轮 sources，不去重会逐轮叠加）
- robots 缓存容量上限（长跑进程防无界增长）
- 落地页失败计数可观测
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import connector
import deepfetch
import orchestrate
import research as research_mod
import scrape
import stop
import verify

CONFIG_PATH = os.path.join(ROOT, "config.json")


def _fast_cfg():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        cfg = json.load(f)
    cfg["compliance"]["rate_limit_per_sec"] = 100.0
    return cfg


def _ext_doc(url, text):
    return {
        "url": url,
        "engine": "external",
        "source_type": "media",
        "text": text,
        "snippet": text[:40],
        "landing_resolved": True,
    }


# ---------- F10 停止判定传参 ----------
def test_stop_first_round_has_fresh_info():
    """首轮无历史轮次：新结果必须算作新信息，不能判"连续两轮无新信息"。"""
    d = stop.should_stop("L1", [], [{"url": "https://a.com"}], budget_hit=False)
    assert d["reason"] != "连续两轮无新信息"
    assert d["stop"] is False


def test_stop_second_round_detects_no_new_info():
    """第二轮全是旧 url：判定才应触发（证明该分支不是死代码）。"""
    d = stop.should_stop("L1", [[{"url": "https://a.com"}]], [{"url": "https://a.com"}])
    assert d["stop"] is True
    assert d["reason"] == "连续两轮无新信息"


def test_orchestrate_first_round_history_is_empty(monkeypatch):
    captured = {}

    def _spy(tier, history, new_results, **kw):
        captured["history"] = history
        captured["new"] = new_results
        return {"stop": True, "reason": "覆盖饱和度达成(子问题全答/缺口闭合)", "exhausted": False}

    monkeypatch.setattr(stop, "should_stop", _spy)
    orchestrate.retrieve(
        "个税起征点", {}, cfg=_fast_cfg(), docs=[_ext_doc("https://gov.cn/a", "政策 5000 元")]
    )
    assert captured["history"] == []  # 首轮无历史轮次
    assert len(captured["new"]) == 1  # 本轮新增可被识别为新信息


# ---------- F11 系统 curl 真实状态码 ----------
def test_system_curl_extracts_http_code(monkeypatch):
    class _R:
        returncode = 0
        stdout = "<html>body</html>" + scrape._CURL_CODE_MARK + "503"

    monkeypatch.setattr(scrape.subprocess, "run", lambda *a, **k: _R())
    status, body, _ = scrape._fetch_system_curl("https://x.com", {"User-Agent": "ua"}, None)
    assert status == 503  # 原实现恒返 0，封禁信号丢失
    assert body == "<html>body</html>"  # 状态码尾标已剥离，不污染正文


def test_system_curl_falls_back_to_zero_without_marker(monkeypatch):
    class _R:
        returncode = 0
        stdout = "<html>body</html>"

    monkeypatch.setattr(scrape.subprocess, "run", lambda *a, **k: _R())
    status, body, _ = scrape._fetch_system_curl("https://x.com", {"User-Agent": "ua"}, None)
    assert status == 0
    assert body == "<html>body</html>"


# ---------- F12 引擎选择容错 ----------
def test_select_tolerates_missing_engines_key():
    assert connector._select("任意查询", {}, {}) == ["Baidu", "Sogou"]
    assert connector._select("任意查询", {"domain": "finance"}, {}) == ["Baidu", "Sogou"]


# ---------- F13 外部 docs 缺 url ----------
def test_external_doc_without_url_dropped():
    docs = [
        _ext_doc("https://gov.cn/a", "政策 5000 元"),
        {"engine": "external", "text": "无 url 的碎片", "snippet": "无 url 的碎片"},
    ]
    res = orchestrate.retrieve("个税起征点", {}, cfg=_fast_cfg(), docs=docs)
    assert all(s.get("url") for s in res["sources"])
    assert len(res["sources"]) == 1


# ---------- F16 跨轮证据去重 ----------
def test_prior_evidence_same_url_not_duplicated():
    doc = _ext_doc("https://e.com/same", "TCP 面向连接")
    res = orchestrate.retrieve(
        "TCP 是什么", {}, cfg=_fast_cfg(), docs=[dict(doc)], prior_evidence=[dict(doc)]
    )
    urls = [s["url"] for s in res["sources"]]
    assert urls.count("https://e.com/same") == 1


def test_research_evidence_merge_dedups_by_url():
    ev = [{"url": "https://a.com", "text": "x"}]
    research_mod._merge_evidence(
        ev, [{"url": "https://a.com", "text": "x"}, {"url": "https://b.com", "text": "y"}]
    )
    assert [e["url"] for e in ev] == ["https://a.com", "https://b.com"]


def test_research_l3_accumulates_evidence_across_rounds():
    """L3 各轮必须拿到逐轮增长的证据基底，否则等于重复跑同一次检索。"""
    seen = []

    def _retriever(query, cfg=None, schema=None, prior_evidence=None, **kw):
        seen.append(len(prior_evidence or []))
        return {
            "findings": f"round{len(seen)}" * len(seen),
            "uncertainties": [],
            "sources": [{"url": f"https://e.com/{len(seen)}", "text": "t", "snippet": "t"}],
        }

    research_mod.research(
        "研究 TCP 拥塞控制的演进", cfg={"research": {}}, tier="L3", max_iter=3, retriever=_retriever
    )
    assert seen == [0, 1, 2]  # 原实现三轮恒为 0（证据从不回灌）


# ---------- F5/F6 核验热路径边界 ----------
def test_fact_verify_tolerates_sources_without_text():
    verdicts = verify.fact_level_verify("TCP 是传输层协议。", [{"url": "https://a.com"}])
    assert verdicts and all(v["verdict"] in ("TRUE", "UNCERTAIN") for v in verdicts)


def test_fact_verify_anchors_to_overlapping_source():
    src = [
        {"url": "https://a.com", "text": "无关内容"},
        {"url": "https://b.com", "text": "TCP 是传输层协议，提供可靠传输"},
    ]
    verdicts = verify.fact_level_verify("TCP 是传输层协议。", src)
    assert verdicts[0]["verdict"] == "TRUE"
    assert verdicts[0]["source"] == "https://b.com"


# ---------- F21 robots 缓存有界 ----------
def test_robots_cache_is_bounded(monkeypatch):
    monkeypatch.setattr(scrape, "_simple_get", lambda *a, **k: "")
    scrape._robots_cache.clear()
    cfg = {"compliance": {"respect_robots": True, "robots_scope": "all"}}
    try:
        for i in range(scrape._ROBOTS_CACHE_MAX + 20):
            scrape._robots_ok(f"https://d{i}.example.com/page", cfg)
        assert len(scrape._robots_cache) <= scrape._ROBOTS_CACHE_MAX
    finally:
        scrape._robots_cache.clear()


# ---------- F18 落地页失败可观测 ----------
def test_deepfetch_counts_landing_failures():
    cfg = {"deep_fetch": {"enabled": True, "fallback_to_serp": True}, "cache": {"enabled": False}}
    out = deepfetch.resolve(
        [{"url": "https://x.com/s?wd=a", "raw_html": "", "engine": "Baidu", "snippet": "s"}], cfg
    )
    assert deepfetch.LAST_STATS["no_links"] == 1
    assert out[0]["landing_failed"] is True
    assert out[0]["landing_fail_reason"] == "no_serp_links"
