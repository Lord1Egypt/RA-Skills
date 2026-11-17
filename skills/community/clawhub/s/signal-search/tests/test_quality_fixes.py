"""P0–P2 质量层修复的回归单测（零依赖、纯函数、无 IO）。

覆盖：自主不检索 / 置信度合成 / M51 已由 test_verify 覆盖 / 时效性衰减 /
多语种分词 / 内联引用 M31 / 缓存默认开 / vault 默认关 / 失败可见性。
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import cache
import common
import report
import research
import route
import score


def test_should_skip_search():
    # 不可检索
    assert route.should_skip_search("") == (True, "不可检索")
    assert route.should_skip_search("你好") == (True, "不可检索")
    # 无需检索：关于本能力自身
    assert route.should_skip_search("你能做什么") == (True, "无需检索")
    # 需澄清：疑问但无实体且很短
    assert route.should_skip_search("为什么？") == (True, "需澄清")
    # 正常可检索查询一律放行
    assert route.should_skip_search("TCP 和 UDP 的核心区别") == (False, "无")
    assert route.should_skip_search("比亚迪2025年销量") == (False, "无")
    assert route.should_skip_search("谁发明了万维网") == (False, "无")
    # 兼容别名
    assert route.decide_not("你好") == (True, "不可检索")


def test_recency_decay():
    assert score._recency(None) == 0.5
    assert score._recency("无年份文本") == 0.6
    assert score._recency("2026 年报道", "近1年") == 1.0  # age 0
    assert score._recency("2025 年报道", "近1年") == 0.2  # age 1
    assert score._recency("2020 年报道", "近1年") == 0.1  # 下限
    # 越新越高（无明确窗口的温和衰减）
    assert score._recency("2024 年", "中") > score._recency("2010 年", "中")


def test_tokenize_multilingual():
    t = common.tokenize("苹果 iPhone 芯片性能")
    assert "苹果" in t and "iphone" in t and "芯片" in t
    # 日语（汉字 2-gram + 假名词）
    assert any("日本" in x for x in common.tokenize("日本語のテスト"))
    # 阿拉伯语（按词切分，空白降级）
    assert any("مرحبا" in x for x in common.tokenize("مرحبا بالعالم"))


def test_inline_citation_m31():
    srcs = [
        {"url": "http://a.com", "snippet": "结论一"},
        {"url": "http://b.com", "snippet": "结论二"},
    ]
    scs = [{"weighted": 0.9, "url": "http://a.com"}, {"weighted": 0.5, "url": "http://b.com"}]
    out = report.synthesize(srcs, scs, "q")
    assert "[1]" in out and "[2]" in out
    assert "来源：" in out and "[1] http://a.com" in out


def test_confidence_synthesis():
    # 全锚定 → 高于旧均值
    scores = [{"weighted": 0.8}, {"weighted": 0.6}]
    verdicts = [
        {"verdict": "TRUE", "reason": "source_anchor"},
        {"verdict": "TRUE", "reason": "source_anchor"},
    ]
    conf = report.confidence_of(scores, verdicts=verdicts, citation_real_rate=1.0, n_uncertain=0)
    assert conf >= 0.9
    # 含数字矛盾 → 显著降权
    verdicts2 = [
        {"verdict": "TRUE", "reason": "source_anchor"},
        {"verdict": "UNCERTAIN", "reason": "numeric_mismatch"},
    ]
    conf2 = report.confidence_of(scores, verdicts=verdicts2, citation_real_rate=1.0, n_uncertain=0)
    assert conf2 < conf
    # 引文不真实 → 直接压低
    conf3 = report.confidence_of(scores, verdicts=verdicts, citation_real_rate=0.0, n_uncertain=0)
    assert conf3 == 0.0


def test_cache_default_on():
    cd = tempfile.mkdtemp()
    c = cache.Cache({"cache": {"enabled": True, "ttl_minutes": 10, "dir": cd}})
    assert c.enabled is True
    c.put("k", {"v": 1})
    assert c.get("k") == {"v": 1}
    c2 = cache.Cache({"cache": {"enabled": False, "dir": cd}})
    assert c2.enabled is False and c2.get("k") is None


def test_vault_default_off():
    def fake(q, **kw):
        return {"findings": "f", "uncertainties": [], "sources": []}

    r = research.research("比亚迪销量", cfg={"research": {"agent_dispatch": False}}, retriever=fake)
    assert r["meta"]["vault"]["enabled"] is False
    # 显式开启
    vd = tempfile.mkdtemp()
    r2 = research.research(
        "比亚迪销量",
        cfg={"research": {"agent_dispatch": False, "vault_enabled": True, "vault_dir": vd}},
        retriever=fake,
        vault_dir=vd,
    )
    assert r2["meta"]["vault"]["enabled"] is True


def test_warnings_surfaced():
    def fake_warn(q, **kw):
        return {
            "findings": "f",
            "uncertainties": [],
            "sources": [],
            "warnings": ["connector: 源 A 失败"],
        }

    r = research.research(
        "比亚迪销量", cfg={"research": {"agent_dispatch": False}}, retriever=fake_warn
    )
    assert r["meta"]["warnings"] == ["connector: 源 A 失败"]
