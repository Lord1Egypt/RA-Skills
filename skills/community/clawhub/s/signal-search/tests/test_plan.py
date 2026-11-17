import plan


def test_intent_fact():
    r = plan.classify_intent("Python 怎么读文件")
    assert r["intent"] in ("fact", "howto")


def test_intent_compare():
    r = plan.classify_intent("对比 A 和 B 的隐私差异")
    assert r["intent"] == "compare"


def test_plan_compare_decompose():
    leaves = plan.plan_queries(
        "对比 百度学术 与 Google Scholar 的文献覆盖",
        plan.classify_intent("对比 百度学术 与 Google Scholar 的文献覆盖"),
        width_cap=8,
    )
    # 应拆出多个子查询（成分型 fan-out）
    assert len(leaves) >= 2
    assert all("文献覆盖" in leaf["q"] for leaf in leaves if not leaf.get("truncated"))


def test_plan_width_cap():
    intent = plan.classify_intent("某研究主题")
    # 直接验证截断逻辑：plan_queries 对超宽做截断
    leaves = plan.plan_queries("调研 X", intent, width_cap=20)
    assert len(leaves) <= 21  # 20 + 可能 1 个 note
