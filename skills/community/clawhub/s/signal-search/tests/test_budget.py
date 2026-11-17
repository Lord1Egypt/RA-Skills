import budget


def test_monitor_over():
    assert budget.monitor(100, 80)["over"] is True
    assert budget.monitor(50, 80)["over"] is False


def test_estimate_uses_tier_defaults():
    # 默认 L1=8000 的 ~85%
    assert 5000 <= budget.estimate("任意查询", "L1") <= 9000
    assert budget.estimate("任意查询", "L3") > budget.estimate("任意查询", "L0")
