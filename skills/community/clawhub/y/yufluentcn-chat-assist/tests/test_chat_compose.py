from tokenapi_harness.scene_handlers.registry import compose_scene_prompt
from tokenapi_harness.catalog import HarnessCatalog
from tokenapi_harness.composer import compose_template_scene
from tokenapi_harness.paths import discover_harness_root


def test_compose_scene_prompt_listing(harness_root):
    cat = HarnessCatalog.load(harness_root)
    comp = compose_scene_prompt(
        cat,
        "listing",
        {
            "platform": "amazon",
            "lang": "zh",
            "product": "测试",
            "keywords": "a",
        },
    )
    assert comp.template_id == "amazon-prompt-v1"
    assert comp.platform == "amazon"


def test_compose_chat_reply_includes_guard(harness_root):
    cat = HarnessCatalog.load(harness_root)
    comp = compose_scene_prompt(
        cat,
        "chat_reply",
        {
            "platform": "amazon",
            "lang": "en",
            "message": "I want a refund now!",
        },
    )
    assert "buyer_message" not in comp.user_prompt  # formatted in
    assert "refund" in comp.user_prompt.lower() or "Refund" in comp.user_prompt
    assert "禁止" in comp.user_prompt or "不得" in comp.user_prompt or "Do not" in comp.user_prompt.lower()
    assert comp.template_id == "amazon-reply-v1"


def test_shopify_category_rules_loaded(harness_root):
    cat = HarnessCatalog.load(harness_root)
    comp = compose_template_scene(
        cat,
        scene_id="listing",
        platform="shopify",
        lang="en",
        variables={
            "product": "Lamp",
            "keywords": "led",
            "features": "- dimmable",
            "target_audience": "home",
            "brand_tone": "warm",
            "competitor_info": "",
        },
        category="home",
    )
    assert "家居" in comp.user_prompt or "尺寸" in comp.user_prompt


def test_all_platforms_have_categories_dir(harness_root):
    cat = HarnessCatalog.load(harness_root)
    for pid in ("amazon", "shopify", "tiktok"):
        p = cat.get_platform(pid)
        assert p.categories_dir
        for cid in ("electronics", "apparel", "home", "beauty"):
            assert (harness_root / p.categories_dir / f"{cid}.md").is_file()
