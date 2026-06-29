"""离线冒烟：Harness 模板与平台规范可加载，无需 TokenApi。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from listing_generator import ListingGenerator, TEMPLATE_FILES  # noqa: E402
from tokenapi_harness.catalog import HarnessCatalog
from tokenapi_harness.composer import compose_listing_user_prompt
from tokenapi_harness.paths import discover_harness_root


def test_all_platform_templates_exist():
    harness_root = discover_harness_root()
    for platform, filename in TEMPLATE_FILES.items():
        path = harness_root / "scenes" / "listing" / "templates" / filename
        assert path.is_file(), f"missing harness template: {path}"
        text = ListingGenerator.load_prompt_template(platform)
        assert "{product}" in text
        assert "{keywords}" in text


def test_all_platform_references_in_harness():
    harness_root = discover_harness_root()
    cat = HarnessCatalog.load(harness_root)
    for platform in TEMPLATE_FILES:
        pcfg = cat.get_platform(platform)
        assert pcfg.rules
        assert (harness_root / pcfg.rules).is_file()


def test_compose_listing_includes_reference():
    harness_root = discover_harness_root()
    cat = HarnessCatalog.load(harness_root)
    prompt, _ = compose_listing_user_prompt(
        cat,
        platform="amazon",
        lang="zh",
        variables={
            "product": "测试产品",
            "keywords": "关键词A, 关键词B",
            "features": "- 卖点1",
            "target_audience": "测试人群",
            "brand_tone": "专业",
            "competitor_info": "",
            "language_prompt": "",
        },
    )
    assert "测试产品" in prompt
    assert "平台规范参考" in prompt
    assert "A9" in prompt or "标题" in prompt


if __name__ == "__main__":
    test_all_platform_templates_exist()
    test_all_platform_references_in_harness()
    test_compose_listing_includes_reference()
    print("OK: all template tests passed")
