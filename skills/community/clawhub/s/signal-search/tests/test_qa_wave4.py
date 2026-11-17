"""收尾 Wave4 回归：D6 缓存清理 / D7 嵌入加锁 / P3 线程池复用 / P5 闭环记忆 / D8 去重分桶。"""

import os


def test_cache_expired_file_removed(tmp_path):
    """D6：TTL 过期后 get() 返回 None 且删除残留文件（不再无界增长）。"""
    from cache import Cache

    cfg = {"cache": {"enabled": True, "ttl_minutes": 0, "dir": str(tmp_path)}}
    c = Cache(cfg)
    c.put("k", {"v": 1})
    p = c._path("k")
    assert os.path.exists(p)
    assert c.get("k") is None
    assert not os.path.exists(p)  # 过期即删


def test_cache_cleanup_removes_expired(tmp_path):
    """D6：cleanup() 主动清过期，返回清理条数。"""
    from cache import Cache

    cfg = {"cache": {"enabled": True, "ttl_minutes": 0, "dir": str(tmp_path)}}
    c = Cache(cfg)
    c.put("a", 1)
    c.put("b", 2)
    n = c.cleanup()
    assert n == 2
    assert list(tmp_path.iterdir()) == []


def test_embed_concurrent_no_crash():
    """D7：并发调用 embed 不崩溃（验证模型懒加载加锁路径）。"""
    import concurrent.futures as cf

    from embed import embed

    texts = ["人工智能 搜索 质量", "信号处理 傅里叶 变换"]
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        futs = [ex.submit(embed, texts) for _ in range(8)]
        for f in futs:
            assert f.result() is not None


def test_deepfetch_resolves_landing(monkeypatch):
    """P3：resolve() 复用单线程池仍能正确完成两跳落地页解析（行为不变）。"""
    import deepfetch
    import extract
    import scrape
    import search

    def fake_scrape(url, meta):
        return f"<html>landing body for {url}</html>", {"final_url": url}

    monkeypatch.setattr(scrape, "scrape", fake_scrape)
    monkeypatch.setattr(
        extract,
        "parse_serp_links",
        lambda html, engine, cfg, max_links=None, serp_url=None: ["http://t1.com"],
    )
    monkeypatch.setattr(
        extract,
        "extract",
        lambda d, cfg: d.update(text="落地正文 " + "足够长用于保留和校验抽取结果" * 4),
    )
    monkeypatch.setattr(extract, "is_serp_host", lambda u: False)
    monkeypatch.setattr(search, "classify_source_type", lambda u: "web")

    serp = [
        {"url": "http://x/serp", "engine": "Google", "raw_html": "<a href='http://t1.com'>a</a>"}
    ]
    out = deepfetch.resolve(serp, cfg={"deep_fetch": {"enabled": True, "max_pages_per_query": 1}})
    assert len(out) == 1
    assert out[0].get("landing_resolved") is True
    assert "落地正文" in (out[0].get("text") or "")


def test_closure_satisfied_stable_and_grows():
    """P5：闭环判定稳定（命中记忆）且证据增长后结果正确。"""
    from research import _closure_satisfied

    ev = [{"url": "http://a", "text": "机器学习 模型 训练", "snippet": ""}]
    schema = [{"name": "机器学习 训练"}]
    assert _closure_satisfied(schema, ev, "结论") is True
    assert _closure_satisfied(schema, ev, "结论") is True  # 同对象再调不报错
    ev.append({"url": "http://b", "text": "深度学习 推理", "snippet": ""})
    assert _closure_satisfied([{"name": "深度学习 推理"}], ev, "结论") is True


def test_near_dup_block_bucket():
    """D8：分块 LSH 去重——URL 精确 + simhash 近似（不漏检）。"""
    from dedup import near_dup

    docs = [
        {"url": "u1", "title": "机器学习 模型 训练 方法", "snippet": "关于机器学习的内容"},
        {
            "url": "u1",
            "title": "机器学习 模型 训练 方法",
            "snippet": "关于机器学习的内容",
        },  # URL 重复
        {
            "url": "u2",
            "title": "机器学习 模型 训练 方法",
            "snippet": "关于机器学习的内容",
        },  # simhash 重复
        {"url": "u3", "title": "完全不同 的 主题 内容", "snippet": "另一回事"},
    ]
    out = near_dup(docs)
    urls = [d["url"] for d in out]
    assert urls == ["u1", "u3"]
