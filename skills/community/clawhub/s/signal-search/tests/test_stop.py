import stop


def test_l0_budget_stop():
    r = stop.should_stop("L0", [[]], [], budget_hit=True)
    assert r["stop"] and not r["exhausted"]
    assert "缩范围" in r["reason"]


def test_l2_coverage_stop():
    r = stop.should_stop("L2", [[]], [], coverage_closed=True)
    assert r["stop"] and "覆盖" in r["reason"]


def test_l2_budget_exhausted():
    # L2/L3 预算截断必须显式标未穷尽（不静默）；构造 fresh>0 以命中预算分支
    r = stop.should_stop("L2", [[{"url": "x"}]], [{"url": "y"}], budget_hit=True)
    assert r["stop"] and r["exhausted"]
    assert "未穷尽" in r["reason"] or "不完整" in r["reason"]


def test_no_new_info_stops():
    hist = [[{"url": "x"}]]
    new = [{"url": "x"}]  # 无新 url
    r = stop.should_stop("L1", hist, new)
    assert r["stop"] and "无新信息" in r["reason"]
