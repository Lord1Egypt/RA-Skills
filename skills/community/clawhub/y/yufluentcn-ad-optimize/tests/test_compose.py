import pytest
from tokenapi_harness.catalog import HarnessCatalog
from tokenapi_harness.paths import discover_harness_root
from tokenapi_harness.scene_handlers.registry import compose_scene_prompt


@pytest.fixture
def harness_root():
    return discover_harness_root()


def test_ad_compose_meta_targeting(harness_root):
    cat = HarnessCatalog.load(harness_root)
    comp = compose_scene_prompt(
        cat,
        "ad_optimize",
        {
            "platform": "meta",
            "lang": "zh",
            "message": "加购未下单多，请给再营销分层",
            "dimension": "targeting",
            "market": "Vietnam",
        },
    )
    assert comp.template_id == "ad-optimize-v1"
    assert "再营销" in comp.user_prompt
    assert "Pixel" in comp.user_prompt or "Conversions API" in comp.user_prompt


def test_ad_compose_google_analytics(harness_root):
    cat = HarnessCatalog.load(harness_root)
    comp = compose_scene_prompt(
        cat,
        "ad_optimize",
        {
            "platform": "google",
            "lang": "en",
            "message": "How to set up conversion tracking and weekly review?",
            "dimension": "analytics",
        },
    )
    assert "Google" in comp.user_prompt or "google" in comp.user_prompt.lower()


def test_ad_dimension_alias_budget(harness_root):
    cat = HarnessCatalog.load(harness_root)
    comp = compose_scene_prompt(
        cat,
        "ad_optimize",
        {
            "platform": "multi",
            "lang": "zh",
            "message": "预算如何分配",
            "dimension": "budget",
        },
    )
    assert "出价" in comp.user_prompt or "预算" in comp.user_prompt


def test_ad_compose_structured_metrics(harness_root):
    cat = HarnessCatalog.load(harness_root)
    comp = compose_scene_prompt(
        cat,
        "ad_optimize",
        {
            "platform": "meta",
            "lang": "zh",
            "message": "请根据当前数据给预算建议",
            "dimension": "bidding",
            "metrics_data": {
                "summary": {"roas": "1.4", "spend": "800"},
                "campaigns": [{"name": "Retargeting", "status": "Active"}],
            },
        },
    )
    assert "roas: 1.4" in comp.user_prompt
    assert "Retargeting" in comp.user_prompt


def test_ad_dimension_inferred_from_message_when_not_specified():
    """隐患 B：无显式 dimension 时从 message 关键词推断，避免一刀切默认 targeting。"""
    cat = HarnessCatalog.load(discover_harness_root())

    cases = [
        ("ROAS 从 2.1 降到 1.4，请给预算重组建议", "bidding"),
        ("CTR 下滑，请给 4 周素材轮换测试表", "creatives"),
        ("加购未下单用户很多，请给再营销分层方案", "targeting"),
        ("落地页加载慢、加购后不结账，怎么优化", "landing"),
        ("FB 和 Google 都在投，如何看归因和分配预算？", "analytics"),
    ]
    for message, expected_dim in cases:
        comp = compose_scene_prompt(
            cat,
            "ad_optimize",
            {"platform": "meta", "lang": "zh", "message": message},
        )
        assert expected_dim in comp.user_prompt.lower() or expected_dim in comp.user_prompt, (
            f"message={message!r} 期望推断到 {expected_dim}，实际 prompt：{comp.user_prompt[:300]}"
        )


def test_ad_dimension_explicit_overrides_message_inference():
    """隐患 B 边界：显式 dimension 优先于 message 推断，不被关键词覆盖。"""
    cat = HarnessCatalog.load(discover_harness_root())
    comp = compose_scene_prompt(
        cat,
        "ad_optimize",
        {
            "platform": "meta",
            "lang": "zh",
            "message": "ROAS 低怎么调预算",  # message 强信号 bidding
            "dimension": "targeting",  # 但显式指定 targeting
        },
    )
    assert "定向" in comp.user_prompt or "targeting" in comp.user_prompt.lower()


def test_ad_channel_inferred_hint_when_platform_not_specified():
    """隐患 D：未显式提供 platform 时 prompt 标注「未显式指定渠道」提示用户确认。"""
    cat = HarnessCatalog.load(discover_harness_root())
    comp = compose_scene_prompt(
        cat,
        "ad_optimize",
        {"lang": "zh", "message": "请给优化建议"},  # 无 platform/channel/ad_channel
    )
    assert "未显式指定渠道" in comp.user_prompt
    assert "默认按" in comp.user_prompt


def test_ad_channel_inferred_hint_absent_when_platform_specified():
    """隐患 D 边界：显式提供 platform 时不出现「未显式指定渠道」提示。"""
    cat = HarnessCatalog.load(discover_harness_root())
    comp = compose_scene_prompt(
        cat,
        "ad_optimize",
        {"platform": "google", "lang": "zh", "message": "请给优化建议"},
    )
    assert "未显式指定渠道" not in comp.user_prompt
    assert "Google Ads" in comp.user_prompt
