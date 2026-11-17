"""Coverage-gap tests: search / report / embed / batch / trace / common / research.confirm_outline.

不依赖真实外网：网络层(scrape.scrape / orchestrate.retrieve)一律 monkeypatch；
数据源(github._api_get)在既有 test_upgrade_sources.py 已覆盖。本文件补齐此前零测试的核心模块。
"""

import json
import os
import sys

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import trace

import batch
import common
import embed
import orchestrate
import report
import research
import scrape
import search


# ============================================================
# search.py — 多引擎抓取层
# ============================================================
def test_classify_source_type_gov():
    for u in ["https://www.gov.cn/x", "https://people.com.cn/x", "https://news.cn/x"]:
        assert search.classify_source_type(u) == "gov"


def test_classify_source_type_academic():
    for u in [
        "https://arxiv.org/abs/123",
        "https://scholar.google.com",
        "https://cnki.net",
        "https://wanfang.com",
    ]:
        assert search.classify_source_type(u) == "academic"


def test_classify_source_type_pubmed():
    # PubMed 挂在 .gov 下（NCBI/NLM/NIH），但内容是学术文献，应判 academic 而非 gov。
    # 方案 B：ACADEMIC_HOSTS 精确白名单在裸 "gov" 之前判定，避免被误吞。
    assert search.classify_source_type("https://pubmed.ncbi.nlm.nih.gov/123") == "academic"
    # 其它挂在 .gov 下的学术库同理
    assert search.classify_source_type("https://www.ncbi.nlm.nih.gov/123") == "academic"
    assert search.classify_source_type("https://www.nlm.nih.gov/123") == "academic"


def test_classify_source_type_selfmedia():
    for u in [
        "https://weibo.com/x",
        "https://www.zhihu.com/x",
        "https://toutiao.com",
        "https://mp.weixin.qq.com/x",
    ]:
        assert search.classify_source_type(u) == "selfmedia"


def test_classify_source_type_forum():
    for u in ["https://stackoverflow.com/q", "https://tieba.baidu.com", "https://x.com/forum"]:
        assert search.classify_source_type(u) == "forum"


def test_classify_source_type_unknown():
    assert search.classify_source_type("https://example.com/page") == "unknown"


_CFG = {
    "engines": {
        "cn": [{"id": "baidu", "search_url": "https://baidu.com/s?q={q}"}],
        "global": [],
        "academic": [],
        "vertical": {},
    }
}


def _fake_scrape(url, meta=None):
    return ("<html><body>结果</body></html>", {"status": 200, "method": "system_curl"})


def test_search_fetch_unknown_engine():
    assert search.fetch("nope", "query", cfg=_CFG) == []


def test_search_fetch_ok(monkeypatch):
    monkeypatch.setattr(scrape, "scrape", _fake_scrape)
    docs = search.fetch("baidu", "机器学习", cfg=_CFG)
    assert len(docs) == 1
    d = docs[0]
    assert "baidu.com/s?q=" in d["url"]
    assert d["raw_html"] == "<html><body>结果</body></html>"
    assert d["engine"] == "baidu"
    assert d["source_type"] == "unknown"  # baidu.com 不命中 _map_type 任一类别


def test_search_fetch_html_none_returns_empty(monkeypatch):
    monkeypatch.setattr(scrape, "scrape", lambda url, meta=None: (None, {"blocked": True}))
    assert search.fetch("baidu", "q", cfg=_CFG) == []


# ============================================================
# report.py — 答案合成层
# ============================================================
def _src(url, snippet, weighted=0.9, text=None):
    return {
        "url": url,
        "snippet": snippet,
        "text": text if text is not None else snippet,
        "weighted": weighted,
    }


def test_synthesize_empty():
    out = report.synthesize([], [], "q")
    assert "未检索到可用来源" in out


def test_synthesize_empty_with_schema():
    schema = [{"name": "市场", "detail_level": "简要"}, {"name": "技术", "detail_level": "简要"}]
    out = report.synthesize([], [], "q", schema=schema)
    assert "## 市场（简要）" in out and "（无来源）" in out
    assert "## 技术（简要）" in out


def test_synthesize_empty_with_uncertainties():
    unc = [{"fact": "X 是否属实", "reason": "无直接来源"}]
    out = report.synthesize([], [], "q", uncertainties=unc)
    assert "未确认项" in out and "X 是否属实" in out


def test_synthesize_refs_and_confidence():
    srcs = [_src("https://a.com/1", "结论A", 0.9), _src("https://b.com/2", "结论B", 0.7)]
    out = report.synthesize(srcs, [{"weighted": 0.9}, {"weighted": 0.7}], "q")
    assert "https://a.com/1" in out and "https://b.com/2" in out
    assert "置信度：" in out


def test_synthesize_conflict_flag():
    # 最低分 < 最高分 * 0.6 → 标"相反观点"
    srcs = [
        _src("https://a.com/1", "主流观点认为X", 1.0),
        _src("https://b.com/2", "反对观点认为Y", 0.4),
    ]
    out = report.synthesize(srcs, [{"weighted": 1.0}, {"weighted": 0.4}], "q")
    assert "相反观点" in out and "反对观点认为Y" in out


def test_synthesize_schema_layout_match():
    schema = [{"name": "大模型", "detail_level": "简要"}]
    srcs = [_src("https://a.com/1", "大模型进展很快", 0.9)]
    out = report.synthesize(srcs, [{"weighted": 0.9}], "q", schema=schema)
    assert "## 大模型（简要）" in out
    assert "大模型进展很快" in out


def test_uncertain_section():
    out = report._uncertain_section([{"fact": "F1", "reason": "R1"}])
    assert "未确认项" in out and "F1" in out and "R1" in out


# ============================================================
# embed.py — 向量化（默认关；降级关键词向量）
# ============================================================
def test_similarity_identical():
    v = [1.0, 2.0, 3.0]
    assert embed.similarity(v, v) == 1.0


def test_similarity_orthogonal():
    assert embed.similarity([1.0, 0.0], [0.0, 1.0]) == 0.0


def test_similarity_zero_vector():
    assert embed.similarity([0.0, 0.0], [1.0, 2.0]) == 0.0


def test_embed_empty_none():
    assert embed.embed([]) is None


def test_embed_degraded_shape(monkeypatch):
    monkeypatch.setattr(embed, "_get_model", lambda: None)
    out = embed.embed(["机器学习", "深度学习"])
    assert isinstance(out, list) and len(out) == 2
    assert all(len(v) == 64 for v in out)
    assert all(isinstance(x, float) for v in out for x in v)


def test_embed_degraded_similarity(monkeypatch):
    monkeypatch.setattr(embed, "_get_model", lambda: None)
    a = embed.embed(["机器学习"])[0]
    same = embed.embed(["机器学习"])[0]
    diff = embed.embed(["足球比赛"])[0]
    assert embed.similarity(a, same) == 1.0
    # 不同文本集合 → 不可能与自身完全相同 → 相似度严格低于同文本
    assert embed.similarity(a, diff) < embed.similarity(a, same)


# ============================================================
# batch.py — 批量检索
# ============================================================
def test_run_batch_calls_retrieve_each(monkeypatch):
    captured = []

    def fake_retrieve(q, constraints=None, cfg=None, **kwargs):
        captured.append(q)
        return {
            "query": q,
            "sources": [],
            "scores": [],
            "findings": "",
            "confidence": 0.0,
            "token_used": 0,
            "tier_used": "L1",
            "warnings": [],
            "verify_issues": [],
        }

    monkeypatch.setattr(orchestrate, "retrieve", fake_retrieve)
    out = batch.run_batch(["q1", "q2", "q3"], cfg={})
    assert captured == ["q1", "q2", "q3"]
    assert len(out) == 3
    assert all(isinstance(o, dict) for o in out)


# ============================================================
# trace.py — 可观测追踪
# ============================================================
def test_trace_disabled_default():
    t = trace.Trace({})
    assert t.enabled is False
    t.event("start", {"k": 1})
    assert len(t.events) == 1
    assert t.events[0]["name"] == "start"
    snap = t.snapshot()
    assert snap["run_id"] == t.run_id and len(snap["events"]) == 1


def test_trace_enabled_writes_jsonl(tmp_path):
    cfg = {"observability": {"trace": True, "log_dir": str(tmp_path / "trace")}}
    t = trace.Trace(cfg)
    assert t.enabled is True
    t.event("step1", {"v": 2})
    files = list((tmp_path / "trace").glob("*.jsonl"))
    assert len(files) == 1
    lines = files[0].read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    rec = json.loads(lines[0])
    assert rec["name"] == "step1" and rec["data"]["v"] == 2


# ============================================================
# common.py — 共享配置加载
# ============================================================
def test_load_config_passthrough():
    assert common.load_config({"a": 1}) == {"a": 1}


def test_load_config_missing_file(monkeypatch):
    monkeypatch.setattr(common, "CONFIG_PATH", "/nonexistent_path_xyz/config.json")
    assert common.load_config(None, force_reload=True) == {}


def test_load_config_reads_real():
    cfg = common.load_config(None)
    assert isinstance(cfg, dict) and bool(cfg)  # 真实 config.json 存在且非空


# ============================================================
# research.py — confirm_outline 早返回（HITL 入口）
# ============================================================
def test_confirm_outline_early_returns(tmp_path):
    called = {"n": 0}

    def fake_retriever(*a, **k):
        called["n"] += 1
        return {
            "findings": "",
            "sources": [],
            "scores": [],
            "confidence": 0.0,
            "token_used": 0,
            "tier_used": "L1",
            "warnings": [],
            "verify_issues": [],
        }

    out = research.research(
        "测试问题",
        tier="L1",
        retriever=fake_retriever,
        vault_dir=str(tmp_path),
        confirm_outline=True,
    )
    assert out["needs_confirm"] is True
    assert out["findings"] == ""
    assert out["iterations"] == 0
    assert called["n"] == 0  # 早返回，未触发检索
    assert "outline.md" in out["outline"]
    assert os.path.exists(out["outline"])
