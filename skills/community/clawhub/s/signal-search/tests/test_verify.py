import verify


def test_citation_not_fetched():
    sources = [{"url": "https://a.com/1"}]
    findings = "见 https://a.com/1 与 https://b.com/2"
    issues = verify.verify(sources, findings)
    assert any(i["type"] == "citation_not_fetched" and "b.com" in i["url"] for i in issues)


def test_fact_verify_true():
    sources = [{"url": "a", "snippet": "珠峰海拔 8848.86 米"}]
    findings = "珠峰海拔 8848.86 米"
    res = verify.fact_level_verify(findings, sources)
    # M51 真锚定：命中事实必须绑定具体来源 URL（不再是 source=None 空壳）
    assert res and res[0]["verdict"] == "TRUE"
    assert res[0]["source"] == "a"


def test_fact_verify_uncertain():
    sources = [{"url": "a", "snippet": "苹果产业链相关公司"}]
    findings = "立讯精密是苹果核心供应商之一"
    res = verify.fact_level_verify(findings, sources)
    assert res and res[0]["verdict"] == "UNCERTAIN"
    assert res[0]["source"] is None


def test_fact_anchors_to_correct_source():
    # 两条事实应分别锚到真正包含它的来源，而非笼统命中任意源
    sources = [
        {"url": "u_alpha", "text": "Alpha 公司 2024 年营收 12 亿元"},
        {"url": "u_beta", "text": "Beta 实验室发布了新模型"},
    ]
    findings = "Alpha 公司 2024 年营收 12 亿元。Beta 实验室发布了新模型。"
    res = verify.fact_level_verify(findings, sources)
    by_fact = {r["fact"]: r for r in res}
    assert by_fact["Alpha 公司 2024 年营收 12 亿元"]["source"] == "u_alpha"
    assert by_fact["Beta 实验室发布了新模型"]["source"] == "u_beta"


def test_semantic_fact_verify_anchors(monkeypatch):
    """语义核验：关键词预筛命中后，语义相似度 ≥ 阈值 → TRUE 并锚定来源。"""

    def fake_embed(texts):
        # 含相同关键词的文本向量一致 → 高相似
        return [
            [1.0, 0.0] if any(k in t for k in ("TCP", "面向连接")) else [0.0, 1.0] for t in texts
        ]

    def fake_sim(a, b):
        return 1.0 if a == b else 0.0

    monkeypatch.setattr("embed.embed", fake_embed)
    monkeypatch.setattr("embed.similarity", fake_sim)
    monkeypatch.setattr("embed._TRY_ST", True)

    findings = "TCP 是面向连接的传输层协议。"
    sources = [{"url": "https://x.com/a", "text": "TCP 是面向连接的传输层协议，提供可靠传输。"}]
    res = verify.semantic_fact_verify(findings, sources, {"verify": {"semantic_threshold": 0.55}})
    assert res and res[0]["verdict"] == "TRUE"
    assert res[0]["source"] == "https://x.com/a"
    assert res[0].get("score", 0) >= 0.55


def test_semantic_fact_verify_falls_back_without_st(monkeypatch):
    """无 sentence-transformers 时语义路径自动回退关键词基线，不报假语义。"""
    monkeypatch.setattr("embed._TRY_ST", False)
    findings = "TCP 是面向连接的传输层协议。"
    sources = [{"url": "https://x.com/a", "text": "TCP 是面向连接的传输层协议，提供可靠传输。"}]
    res = verify.semantic_fact_verify(findings, sources, {"verify": {"semantic_threshold": 0.55}})
    # 回退 fact_level_verify → 关键词重叠 ≥1 → TRUE
    assert res and res[0]["verdict"] == "TRUE"
    assert res[0]["source"] == "https://x.com/a"


def test_semantic_fact_verify_uncertain_below_threshold(monkeypatch):
    """语义相似度低于阈值 → UNCERTAIN（不轻判 FALSE）。"""

    def fake_embed(texts):
        return [[1.0, 0.0], [0.0, 1.0]]  # 事实与来源语义正交

    def fake_sim(a, b):
        return 0.1

    monkeypatch.setattr("embed.embed", fake_embed)
    monkeypatch.setattr("embed.similarity", fake_sim)
    monkeypatch.setattr("embed._TRY_ST", True)

    findings = "月球是地球的卫星。"
    sources = [{"url": "https://x.com/a", "text": "TCP 是面向连接的传输层协议。"}]
    res = verify.semantic_fact_verify(findings, sources, {"verify": {"semantic_threshold": 0.55}})
    assert res and res[0]["verdict"] == "UNCERTAIN"
    assert res[0]["source"] is None
