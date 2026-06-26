"""Smoke tests for core capabilities — run before every push.

Usage: python scripts/smoke_test.py
Exit code 0 = all passed, 1 = failures detected.

These tests are pure-Python and require no network, no bb-browser,
and no Chrome instance.
"""

from __future__ import annotations

import subprocess
import sys
import traceback

PASSED = 0
FAILED = 0


def check(name: str, fn):
    global PASSED, FAILED
    try:
        fn()
        PASSED += 1
        print(f"  PASS  {name}")
    except Exception as e:
        FAILED += 1
        print(f"  FAIL  {name}")
        traceback.print_exc(limit=3)
        print()


# ---------------------------------------------------------------------------
# 1. Platform routing
# ---------------------------------------------------------------------------

def test_chinese_london_alias_routes_to_uk():
    from used_price_compare.platforms import (
        get_country_for_city,
        normalize_city,
        resolve_platforms,
    )
    assert normalize_city("伦敦") == "london"
    assert normalize_city("英国伦敦") == "london"
    assert get_country_for_city("伦敦") == "uk"
    plats = resolve_platforms(city="英国伦敦")
    names = {p.name for p in plats}
    assert "ebay-uk" in names and "gumtree" in names


def test_uk_city_routes_to_uk():
    from used_price_compare.platforms import resolve_platforms, get_country_for_city
    for city in ("london", "leeds", "glasgow", "edinburgh"):
        assert get_country_for_city(city) == "uk", f"{city} should be uk"
        plats = resolve_platforms(city=city)
        names = {p.name for p in plats}
        assert "gumtree" in names, f"gumtree missing for {city}"
        assert "ebay-uk" in names, f"ebay-uk missing for {city}"
        assert "amazon-uk" in names, f"amazon-uk missing for {city}"
        assert "ebay-us" not in names, f"ebay-us should not be in {city}"


def test_us_city_routes_to_us():
    from used_price_compare.platforms import resolve_platforms, get_country_for_city
    for city in ("los-angeles", "boston", "miami", "new-york"):
        assert get_country_for_city(city) == "us", f"{city} should be us"
        plats = resolve_platforms(city=city)
        names = {p.name for p in plats}
        assert "ebay-us" in names, f"ebay-us missing for {city}"
        assert "amazon-us" in names, f"amazon-us missing for {city}"
        assert "gumtree" not in names, f"gumtree should not be in {city}"


def test_no_craigslist_in_platforms():
    from used_price_compare.platforms import PLATFORMS
    assert "craigslist" not in PLATFORMS, "craigslist should be removed"


def test_platform_filter_family():
    from used_price_compare.platforms import resolve_platforms
    plats = resolve_platforms(city="london", platform_filter=["ebay"])
    names = [p.name for p in plats]
    assert "ebay-uk" in names, f"family filter 'ebay' should resolve to ebay-uk for london"


def test_bb_browser_json_error_on_stdout():
    """bb-browser --json puts failures on stdout; stderr is often empty."""
    from used_price_compare.bb_browser_cli import parse_site_json_output

    r = subprocess.CompletedProcess(
        args=["bb-browser", "site", "ok/search", "x"],
        returncode=1,
        stdout='{"success":false,"error":"Chrome not connected (CDP)","hint":"Try tab list"}',
        stderr="",
    )
    out = parse_site_json_output(r)
    assert out.get("error") == "daemon_disconnected", out
    assert "Chrome" in (out.get("detail") or ""), out

    r2 = subprocess.CompletedProcess(
        args=[],
        returncode=1,
        stdout='{"success":false,"error":"HTTP 403","hint":"Check login"}',
        stderr="",
    )
    out2 = parse_site_json_output(r2)
    assert out2.get("error") and "403" in out2["error"], out2


# ---------------------------------------------------------------------------
# 2. CLI output structure
# ---------------------------------------------------------------------------

def test_format_comparison_table_shape():
    from used_price_compare.compare import CompareItem, CompareResult, format_comparison_table

    items = [
        CompareItem(
            title="iPhone 15 Pro 128GB", price=750.0,
            price_display="$750.00", currency="USD",
            url="https://example.com/1", source="ok", source_display="OK.com",
            condition="like new",
        ),
    ]
    result = CompareResult(
        keyword="iPhone 15 Pro", city="los-angeles",
        platforms_queried=["ok"], platforms_success=["ok"],
        items=items, lowest_price=items[0], ok_best=items[0],
    )
    output = format_comparison_table(result)

    assert output["success"] is True
    assert output["keyword"] == "iPhone 15 Pro"
    assert len(output["price_ranking"]) == 1
    assert output["price_ranking"][0]["title"] == "iPhone 15 Pro 128GB"
    assert output["lowest_price"]["price"] == "$750.00"
    assert output["ok_best"]["price"] == "$750.00"
    assert "ok_search_url" in output
    assert "ok.com" in output["ok_search_url"]
    assert "analysis" not in output, "analysis should no longer be in CLI output"
    assert "recommendation" not in output, "recommendation should no longer be in CLI output"


def test_format_empty_result():
    from used_price_compare.compare import CompareResult, format_comparison_table

    result = CompareResult(keyword="test", city="london", items=[])
    output = format_comparison_table(result)
    assert output["success"] is True
    assert output["price_ranking"] == []
    assert output["lowest_price"] is None
    assert output["ok_best"] is None
    assert "ok_search_url" in output


def test_forced_platform_output_includes_failed():
    from used_price_compare.compare import CompareItem, CompareResult, format_comparison_table

    item = CompareItem(
        title="iPhone 15 Pro 128GB",
        price=750.0,
        price_display="£750.00",
        currency="GBP",
        url="https://example.com/iphone",
        source="ebay-uk",
        source_display="eBay UK",
    )
    result = CompareResult(
        keyword="iPhone 15 Pro",
        city="london",
        platforms_queried=["ebay-uk", "amazon-uk"],
        platforms_success=["ebay-uk"],
        platforms_failed={"amazon-uk": "HTTP 503"},
        platform_display_names={"ebay-uk": "eBay UK", "amazon-uk": "Amazon UK"},
        items=[item],
        lowest_price=item,
    )
    output = format_comparison_table(result)

    assert "eBay UK" in output["by_platform"]
    assert "Amazon UK" in output["by_platform"]
    assert output["by_platform"]["Amazon UK"] == []
    sections = {s["name"]: s for s in output["platform_sections"]}
    assert sections["amazon-uk"]["status"] == "failed"
    assert "503" in sections["amazon-uk"]["error"]


def test_ok_search_url_uses_city_slug():
    from used_price_compare.compare import CompareResult, _ok_search_url

    r = CompareResult(keyword="PS5 console", city="london")
    url = _ok_search_url(r)
    assert "city-greater-london" in url, "London OK.com path should use greater-london slug"
    assert "PS5%20console" in url, "keyword should be URL-encoded"
    assert url.startswith("https://uk.ok.com/"), f"London should use uk subdomain, got {url}"


def test_ok_domain_routing():
    from used_price_compare.compare import _ok_domain_for_city
    assert _ok_domain_for_city("london") == "uk"
    assert _ok_domain_for_city("boston") == "us"
    assert _ok_domain_for_city("sydney") == "au"


def test_currency_detection():
    from used_price_compare.compare import _detect_currency
    assert _detect_currency("$750.00") == "USD"
    assert _detect_currency("£650") == "GBP"
    assert _detect_currency("€499") == "EUR"
    assert _detect_currency("A$1,200") == "AUD"


# ---------------------------------------------------------------------------
# 3. URL-to-adapter routing (evaluate sub-skill)
# ---------------------------------------------------------------------------

def test_url_routing_ok():
    from used_price_compare.fetcher import resolve_adapter
    result = resolve_adapter("https://us.ok.com/en/item/12345")
    assert result is not None
    assert result[0] == "ok/detail"
    assert result[1] == "ok.com"


def test_url_routing_ebay():
    from used_price_compare.fetcher import resolve_adapter
    for url, expected_label in [
        ("https://www.ebay.com/itm/123", "ebay"),
        ("https://www.ebay.co.uk/itm/456", "ebay"),
        ("https://www.ebay.com.au/itm/789", "ebay"),
    ]:
        result = resolve_adapter(url)
        assert result is not None, f"Should resolve {url}"
        assert result[0] == "ebay/detail"
        assert result[1] == expected_label


def test_url_routing_gumtree():
    from used_price_compare.fetcher import resolve_adapter
    result = resolve_adapter("https://www.gumtree.com/p/phones/iphone/12345")
    assert result is not None
    assert result[0] == "gumtree/detail"


def test_url_routing_amazon():
    from used_price_compare.fetcher import resolve_adapter
    for url in [
        "https://www.amazon.com/dp/B0CHX3QBCH",
        "https://www.amazon.co.uk/dp/B0CHX3QBCH",
    ]:
        result = resolve_adapter(url)
        assert result is not None, f"Should resolve {url}"
        assert result[0] == "amazon/detail"


def test_url_routing_unsupported():
    from used_price_compare.fetcher import resolve_adapter
    assert resolve_adapter("https://www.google.com/search?q=test") is None
    assert resolve_adapter("not-a-url") is None


# ---------------------------------------------------------------------------
# 4. Evaluator scoring
# ---------------------------------------------------------------------------

def test_evaluator_basic():
    from used_price_compare.evaluator import evaluate_item
    from used_price_compare.models import ItemDetail, SellerInfo

    item = ItemDetail(
        title="iPhone 15 Pro 128GB Unlocked",
        price="$750.00",
        price_numeric=750.0,
        currency="USD",
        description="Great condition iPhone, barely used. Comes with original box and charger. " * 5,
        condition="Like new",
        images=["img1.jpg", "img2.jpg", "img3.jpg", "img4.jpg", "img5.jpg"],
        seller=SellerInfo(name="john", rating="99.5%", reviews_count=200, member_since="2020-03"),
        platform="ebay",
        source_url="https://www.ebay.com/itm/123",
    )
    result = evaluate_item(item, median_price=800.0)
    assert result.scores.overall > 0
    assert result.verdict in ("highly_recommended", "recommended", "caution", "avoid")
    assert result.verdict_label in ("强烈推荐", "推荐购买", "建议谨慎", "不建议")
    assert len(result.rationale) > 0


def test_evaluator_flags_suspicious():
    from used_price_compare.evaluator import evaluate_item
    from used_price_compare.models import ItemDetail, SellerInfo

    item = ItemDetail(
        title="iPhone case cover",
        price="$5.00",
        price_numeric=5.0,
        description="",
        condition="",
        images=[],
        seller=SellerInfo(),
        platform="ebay",
        source_url="https://www.ebay.com/itm/456",
    )
    result = evaluate_item(item, median_price=800.0)
    assert "likely_accessory" in result.flags
    assert result.verdict in ("caution", "avoid")


def test_evaluate_items_ranking():
    from used_price_compare.evaluator import evaluate_items
    from used_price_compare.models import ItemDetail, SellerInfo

    good = ItemDetail(
        title="iPhone 15 Pro 256GB", price="$780", price_numeric=780.0,
        description="Excellent condition " * 20, condition="excellent",
        images=["a.jpg"] * 5,
        seller=SellerInfo(name="top_seller", rating="99.9%", reviews_count=5000),
        platform="ebay", source_url="https://www.ebay.com/itm/1",
    )
    bad = ItemDetail(
        title="Phone case", price="$2", price_numeric=2.0,
        description="", condition="", images=[],
        seller=SellerInfo(), platform="ebay",
        source_url="https://www.ebay.com/itm/2",
    )
    results = evaluate_items([bad, good])
    assert results[0].item.title == "iPhone 15 Pro 256GB", "Higher-scoring item should rank first"
    assert results[0].scores.overall > results[1].scores.overall


def test_format_eval_results_shape():
    from used_price_compare.evaluator import evaluate_items, format_eval_results
    from used_price_compare.models import ItemDetail, SellerInfo

    item = ItemDetail(
        title="Test Item", price="$100", price_numeric=100.0,
        description="A decent product " * 10, condition="good",
        images=["img.jpg"], seller=SellerInfo(name="seller1"),
        platform="ok.com", source_url="https://us.ok.com/en/item/1",
    )
    results = evaluate_items([item])
    output = format_eval_results(results)

    assert output["success"] is True
    assert output["total"] == 1
    assert len(output["items"]) == 1
    entry = output["items"][0]
    assert "scores" in entry
    assert "image_quality" in entry["scores"], "scores should include image_quality"
    assert "images_count" in entry, "entry should include images_count"
    assert "verdict" in entry
    assert "rationale" in entry
    assert "seller" in entry
    assert "best_value" in output


def test_gumtree_lower_seller_weight():
    """Gumtree items should use lower seller_trust weight than eBay."""
    from used_price_compare.evaluator import _get_weights

    gumtree_w = _get_weights("gumtree", has_vision=False)
    ebay_w = _get_weights("ebay", has_vision=False)
    assert gumtree_w["seller_trust"] < ebay_w["seller_trust"], \
        "Gumtree seller_trust weight should be lower than eBay"
    assert gumtree_w["seller_trust"] <= 0.05


def test_vision_weights_differ():
    """With vision model, image_quality should get its own weight."""
    from used_price_compare.evaluator import _get_weights

    no_vision = _get_weights("ebay", has_vision=False)
    with_vision = _get_weights("ebay", has_vision=True)
    assert no_vision["image_quality"] == 0.0, "Without vision, image_quality weight should be 0"
    assert with_vision["image_quality"] > 0.0, "With vision, image_quality weight should be > 0"
    total_nv = sum(no_vision.values())
    total_wv = sum(with_vision.values())
    assert abs(total_nv - 1.0) < 0.01, f"No-vision weights should sum to ~1.0, got {total_nv}"
    assert abs(total_wv - 1.0) < 0.01, f"Vision weights should sum to ~1.0, got {total_wv}"


def test_image_quality_heuristic():
    """Without vision model, image_quality should be scored by photo count."""
    from used_price_compare.evaluator import _score_image_quality
    from used_price_compare.models import ItemDetail

    many = ItemDetail(images=["a.jpg"] * 5)
    few = ItemDetail(images=[])

    score_many, flags_many, _ = _score_image_quality(many)
    score_few, flags_few, _ = _score_image_quality(few)

    assert score_many > score_few
    assert "no_photos" in flags_few
    assert "no_photos" not in flags_many


# ---------------------------------------------------------------------------
# 5. CLI parser (new subcommands registered)
# ---------------------------------------------------------------------------

def test_cli_parser_has_new_subcommands():
    sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
    from cli import build_parser
    parser = build_parser()
    for subcmd in ("fetch-detail", "evaluate", "summarize"):
        try:
            parser.parse_args([subcmd, "--url" if subcmd == "fetch-detail" else "--urls", "http://example.com"])
        except SystemExit:
            raise AssertionError(f"CLI parser should accept '{subcmd}' subcommand")


def test_cli_parser_vision_config_subcommand():
    from cli import build_parser
    parser = build_parser()
    args = parser.parse_args(["vision-config"])
    assert args.action == "show"
    args = parser.parse_args(["vision-config", "init", "--force"])
    assert args.action == "init"
    assert args.force is True


def test_load_vision_config_defaults():
    """load_vision_config returns a VisionConfig; without file/env it's disabled."""
    import os
    from unittest.mock import patch

    from used_price_compare import evaluator as evaluator_mod
    from used_price_compare.evaluator import load_vision_config

    saved = {k: os.environ.pop(k, None) for k in ("VISION_API_BASE", "VISION_API_KEY", "VISION_MODEL")}
    try:
        # Isolate from developer ~/.config/.../vision.json so CI and local match.
        with patch.object(evaluator_mod, "_CONFIG_SEARCH_PATHS", []):
            cfg = load_vision_config()
        assert cfg.enabled is False, "Without any config, vision should be disabled"
        assert cfg.max_images == 5
        assert cfg.timeout == 60
    finally:
        for k, v in saved.items():
            if v is not None:
                os.environ[k] = v


def test_load_vision_config_env_override():
    """Environment variables should override config file values."""
    import os
    from used_price_compare.evaluator import load_vision_config

    saved = {k: os.environ.get(k) for k in ("VISION_API_BASE", "VISION_API_KEY", "VISION_MODEL")}
    os.environ["VISION_API_BASE"] = "https://test.example.com/v1"
    os.environ["VISION_API_KEY"] = "sk-test-key"
    os.environ["VISION_MODEL"] = "test-model"
    try:
        cfg = load_vision_config()
        assert cfg.api_base == "https://test.example.com/v1"
        assert cfg.api_key == "sk-test-key"
        assert cfg.model == "test-model"
        assert cfg.enabled is True
    finally:
        for k, v in saved.items():
            if v is not None:
                os.environ[k] = v
            else:
                os.environ.pop(k, None)


def test_load_vision_config_cli_override():
    """CLI model_override should take highest priority."""
    import os
    from used_price_compare.evaluator import load_vision_config

    saved = {k: os.environ.get(k) for k in ("VISION_API_BASE", "VISION_API_KEY", "VISION_MODEL")}
    os.environ["VISION_API_BASE"] = "https://test.example.com/v1"
    os.environ["VISION_API_KEY"] = "sk-test-key"
    os.environ["VISION_MODEL"] = "env-model"
    try:
        cfg = load_vision_config(model_override="cli-model")
        assert cfg.model == "cli-model", "CLI override should win over env var"
    finally:
        for k, v in saved.items():
            if v is not None:
                os.environ[k] = v
            else:
                os.environ.pop(k, None)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def main():
    print("=== Used Price Compare — Smoke Tests ===\n")

    sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

    tests = [
        # Platform routing
        ("Chinese London alias -> UK platforms", test_chinese_london_alias_routes_to_uk),
        ("UK city -> UK platforms", test_uk_city_routes_to_uk),
        ("US city -> US platforms", test_us_city_routes_to_us),
        ("No craigslist in PLATFORMS", test_no_craigslist_in_platforms),
        ("Platform filter by family", test_platform_filter_family),
        ("bb-browser JSON errors on stdout (exit 1)", test_bb_browser_json_error_on_stdout),
        # Compare output
        ("format_comparison_table shape", test_format_comparison_table_shape),
        ("format empty result", test_format_empty_result),
        ("forced per-platform output includes failed", test_forced_platform_output_includes_failed),
        ("OK.com search URL uses city slug", test_ok_search_url_uses_city_slug),
        ("OK.com domain routing", test_ok_domain_routing),
        ("Currency detection", test_currency_detection),
        # URL routing (evaluate)
        ("URL routing: OK.com", test_url_routing_ok),
        ("URL routing: eBay (multi-domain)", test_url_routing_ebay),
        ("URL routing: Gumtree", test_url_routing_gumtree),
        ("URL routing: Amazon (multi-domain)", test_url_routing_amazon),
        ("URL routing: unsupported", test_url_routing_unsupported),
        # Evaluator
        ("Evaluator: basic scoring", test_evaluator_basic),
        ("Evaluator: flags suspicious items", test_evaluator_flags_suspicious),
        ("Evaluator: ranking order", test_evaluate_items_ranking),
        ("Evaluator: output format shape", test_format_eval_results_shape),
        ("Evaluator: Gumtree lower seller weight", test_gumtree_lower_seller_weight),
        ("Evaluator: vision weights differ", test_vision_weights_differ),
        ("Evaluator: image quality heuristic", test_image_quality_heuristic),
        # Vision config
        ("Vision config: defaults (disabled)", test_load_vision_config_defaults),
        ("Vision config: env var override", test_load_vision_config_env_override),
        ("Vision config: CLI override priority", test_load_vision_config_cli_override),
        # CLI
        ("CLI parser has new subcommands", test_cli_parser_has_new_subcommands),
        ("CLI parser: vision-config subcommand", test_cli_parser_vision_config_subcommand),
    ]

    for name, fn in tests:
        check(name, fn)

    print(f"\n{'='*40}")
    print(f"  {PASSED} passed, {FAILED} failed")
    print(f"{'='*40}")

    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
