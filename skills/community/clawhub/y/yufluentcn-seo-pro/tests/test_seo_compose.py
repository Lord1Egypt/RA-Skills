import pytest
from tokenapi_harness.paths import discover_harness_root
from tokenapi_harness.scene_handlers.registry import compose_scene_prompt
from tokenapi_harness.catalog import HarnessCatalog


@pytest.fixture
def harness_root():
    return discover_harness_root()


def test_seo_compose(harness_root):
    cat = HarnessCatalog.load(harness_root)
    comp = compose_scene_prompt(
        cat, "seo_keywords", {"platform": "shopify", "lang": "en", "product": "Lamp", "seed_keywords": "led"}
    )
    assert "shopify" in comp.user_prompt.lower() or "Shopify" in comp.user_prompt
