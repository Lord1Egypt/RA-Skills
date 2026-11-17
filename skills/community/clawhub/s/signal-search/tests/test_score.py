import score


def test_weighted_formula():
    s = {"url": "u", "snippet": "某政府发布政策", "source_type": "gov"}
    out = score.score_source(
        s,
        "政策",
        {
            "gov": 0.95,
            "media": 0.85,
            "academic": 0.9,
            "vendor": 0.7,
            "forum": 0.4,
            "selfmedia": 0.35,
            "unknown": 0.5,
        },
    )
    # 加权 = 0.35*cred + 0.30*rel + 0.15*rec + 0.15*auth + 0.05*(1-bias)
    assert out["credibility"] == 0.95
    assert 0 < out["weighted"] <= 1.0
    # gov 应高于 selfmedia
    s2 = {"url": "u2", "snippet": "某自媒体说", "source_type": "selfmedia"}
    out2 = score.score_source(
        s2,
        "政策",
        {
            "gov": 0.95,
            "media": 0.85,
            "academic": 0.9,
            "vendor": 0.7,
            "forum": 0.4,
            "selfmedia": 0.35,
            "unknown": 0.5,
        },
    )
    assert out["weighted"] > out2["weighted"]
