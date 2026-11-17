"""上线前质量收尾 Wave2 回归测试：全局态有界化 / 冷却分级 / robots 失败缓存。

对应缺陷：
- D4 域名封禁只增不减 → 永久禁抓 + 内存慢泄漏
- D5 robots.txt 抓取失败不写缓存 → 抖动期间每抓一页重拉一次
- P2 academic/finance/github 丢弃返回值的冗余 config 磁盘读
"""

import os
import sys
import time

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
)

import common  # noqa: E402
import scrape  # noqa: E402


# ---------- BoundedTTLMap 基础语义 ----------
def test_bounded_ttl_map_expires_and_evicts():
    m = common.BoundedTTLMap(maxsize=3, ttl=10.0)
    m.set("a", 1)
    assert m.get("a") == 1 and "a" in m

    # 过期即失效
    m.set("b", 2, ttl=0.01)
    time.sleep(0.05)
    assert m.get("b") is None and "b" not in m

    # 超上限 FIFO 淘汰最早条目
    for i in range(10):
        m.set(f"k{i}", i)
    assert len(m) <= 3
    assert m.get("k0") is None
    assert m.get("k9") == 9

    m.clear()
    assert len(m) == 0


def test_bounded_ttl_map_is_thread_safe():
    import threading

    m = common.BoundedTTLMap(maxsize=64, ttl=30.0)

    def worker(n):
        for i in range(200):
            m.set(f"d{n}-{i % 32}", i)
            m.get(f"d{n}-{i % 32}")

    threads = [threading.Thread(target=worker, args=(n,)) for n in range(6)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    assert len(m) <= 64  # 并发写入下仍不越界


# ---------- D4 封禁冷却而非永久拉黑 ----------
def test_blocked_domain_cooldown_expires():
    scrape._blocked_domains.clear()
    try:
        scrape._blocked_domains.set("x.example.com", "status 429", ttl=0.05)
        assert scrape._blocked_domains.get("x.example.com") is not None
        time.sleep(0.1)
        assert scrape._blocked_domains.get("x.example.com") is None, "冷却到期后必须自动放行"
    finally:
        scrape._blocked_domains.clear()


def test_cooldown_length_differs_by_failure_type():
    assert scrape._cooldown_for("status 429") == scrape._BLOCK_TTL_SEC
    assert scrape._cooldown_for("challenge page detected") == scrape._BLOCK_TTL_SEC
    # 网络抖动（curl rc=56 / 超时）只短冷却，不能等同于被封
    assert (
        scrape._cooldown_for("Recv failure: Connection was reset (rc=56)")
        == scrape._BLOCK_TRANSIENT_TTL_SEC
    )
    assert scrape._cooldown_for(None) == scrape._BLOCK_TRANSIENT_TTL_SEC


def test_blocked_domains_is_bounded():
    scrape._blocked_domains.clear()
    try:
        for i in range(scrape._BLOCK_MAX + 50):
            scrape._blocked_domains.set(f"d{i}.example.com", "failed")
        assert len(scrape._blocked_domains) <= scrape._BLOCK_MAX
    finally:
        scrape._blocked_domains.clear()


def test_scrape_short_circuits_while_in_cooldown():
    scrape._blocked_domains.clear()
    try:
        scrape._blocked_domains.set("cool.example.com", "status 429")
        html, info = scrape.scrape(
            "https://cool.example.com/page",
            {"cfg": {"compliance": {"enabled": False, "respect_robots": False}}},
        )
        assert html is None and info["blocked"] is True
        assert "cooldown" in info["error"]
    finally:
        scrape._blocked_domains.clear()


def test_last_call_throttle_state_is_bounded():
    scrape._last_call.clear()
    cfg = {"compliance": {"enabled": True, "rate_limit_per_sec": 1000}}  # 间隔≈1ms，不拖慢测试
    try:
        for i in range(scrape._LAST_CALL_MAX + 30):
            scrape._throttle(f"t{i}.example.com", cfg)
        assert len(scrape._last_call) <= scrape._LAST_CALL_MAX
    finally:
        scrape._last_call.clear()


# ---------- D5 robots 抓取失败也进缓存（短 TTL） ----------
def test_robots_failure_is_cached_to_avoid_refetch(monkeypatch):
    calls = {"n": 0}

    def _fake_get(*a, **k):
        calls["n"] += 1
        return ""  # 模拟抓取失败/空 robots

    monkeypatch.setattr(scrape, "_simple_get", _fake_get)
    scrape._robots_cache.clear()
    cfg = {"compliance": {"respect_robots": True, "robots_scope": "all"}}
    try:
        for _ in range(5):
            assert scrape._robots_ok("https://r.example.com/page", cfg) is True
        assert calls["n"] == 1, "失败结果必须进缓存，不能每抓一页重拉一次 robots.txt"
    finally:
        scrape._robots_cache.clear()


def test_robots_failure_cache_uses_short_ttl(monkeypatch):
    monkeypatch.setattr(scrape, "_simple_get", lambda *a, **k: "")
    monkeypatch.setattr(scrape, "_ROBOTS_FAIL_TTL_SEC", 0.05)
    scrape._robots_cache.clear()
    cfg = {"compliance": {"respect_robots": True, "robots_scope": "all"}}
    try:
        scrape._robots_ok("https://r2.example.com/page", cfg)
        assert scrape._robots_cache.get("r2.example.com") is True
        time.sleep(0.1)
        # 短 TTL 到期后重新探测，避免一次抖动等价于永久关闭 robots 检查
        assert scrape._robots_cache.get("r2.example.com") is None
    finally:
        scrape._robots_cache.clear()


def test_robots_success_still_parsed_and_cached(monkeypatch):
    monkeypatch.setattr(scrape, "_simple_get", lambda *a, **k: "User-agent: *\nDisallow: /private")
    scrape._robots_cache.clear()
    cfg = {"compliance": {"respect_robots": True, "robots_scope": "all"}}
    try:
        assert scrape._robots_ok("https://ok.example.com/private/x", cfg) is False
        assert scrape._robots_cache.get("ok.example.com") is False
    finally:
        scrape._robots_cache.clear()


# ---------- P2 冗余 config 磁盘读 ----------
def test_source_modules_have_no_discarded_config_read():
    """academic/finance/github 不得保留"丢弃返回值"的 _load_cfg 调用（纯冗余磁盘读）。"""
    import academic
    import finance
    import github

    for mod in (academic, finance, github):
        with open(mod.__file__, "r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                stripped = line.split("#")[0].strip()
                assert not stripped.startswith(
                    "_load_cfg("
                ), f"{mod.__name__}:{lineno} 残留丢弃返回值的配置读取"


# ---------- P4 置信度单一口径 ----------
def test_confidence_single_source_of_truth():
    import report

    scores = [{"weighted": 0.8}, {"weighted": 0.4}]
    assert report.confidence_of(scores) == 0.6
    assert report.confidence_of([]) == 0.0
    body = report.synthesize([{"url": "https://a.com", "snippet": "答案"}], scores, "q")
    assert "置信度：0.6" in body


def test_uncertainties_appended_without_resynthesis():
    """未确认项是纯末尾追加：追加结果必须与"带 uncertainties 重跑一遍"完全一致。"""
    import report

    srcs = [
        {"url": "https://a.com", "snippet": "答案A", "text": "指标 答案A"},
        {"url": "https://b.com", "snippet": "答案B", "text": "风险 答案B"},
    ]
    scores = [{"weighted": 0.9}, {"weighted": 0.5}]
    unc = [{"fact": "某结论", "reason": "无二源交叉"}]
    schema = [{"name": "指标", "detail_level": "简要"}, {"name": "风险", "detail_level": "详细"}]

    for sch in (None, schema):
        once = report.append_uncertainties(report.synthesize(srcs, scores, "q", schema=sch), unc)
        twice = report.synthesize(srcs, scores, "q", schema=sch, uncertainties=unc)
        assert once == twice
