"""
Tests for Shopify Store Optimizer handler.py
Run: python3 tests/test_handler.py
"""

import sys
import os

# Ensure handler is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from handler import DiagnosticEngine, handle, APP_CATALOG, CONVERSION_TIPS, SEO_TIPS, UX_TIPS


def test_area_detection_conversion():
    """Test that conversion-related input is correctly detected."""
    engine = DiagnosticEngine("我的Shopify店转化率只有0.5%，怎么处理")
    assert engine.area == "conversion", f"Expected 'conversion', got '{engine.area}'"
    print("✓ test_area_detection_conversion passed")


def test_area_detection_seo():
    """Test that SEO-related input is correctly detected."""
    engine = DiagnosticEngine("我的店SEO做得怎么样？")
    assert engine.area == "seo", f"Expected 'seo', got '{engine.area}'"
    print("✓ test_area_detection_seo passed")


def test_area_detection_all():
    """Test that general health query triggers 'all' area."""
    engine = DiagnosticEngine("帮我看看我的Shopify店有哪些问题")
    assert engine.area == "all", f"Expected 'all', got '{engine.area}'"
    print("✓ test_area_detection_all passed")


def test_area_detection_ux():
    """Test that UX-related input is correctly detected."""
    engine = DiagnosticEngine("我的店移动端体验很差，怎么优化")
    assert engine.area == "ux", f"Expected 'ux', got '{engine.area}'"
    print("✓ test_area_detection_ux passed")


def test_conversion_rate_extraction():
    """Test numeric conversion rate extraction from Chinese text."""
    engine = DiagnosticEngine("我的店转化率是1.8%，转化很低")
    assert engine.conversion_rate == 1.8, f"Expected 1.8, got {engine.conversion_rate}"
    print("✓ test_conversion_rate_extraction passed")


def test_products_count_extraction():
    """Test product count extraction."""
    engine = DiagnosticEngine("我有200个产品，销量不好")
    assert engine.products_count == 200, f"Expected 200, got {engine.products_count}"
    print("✓ test_products_count_extraction passed")


def test_traffic_extraction():
    """Test monthly traffic extraction."""
    engine = DiagnosticEngine("月访问量是5000，转化很差")
    assert engine.traffic == 5000, f"Expected 5000, got {engine.traffic}"
    print("✓ test_traffic_extraction passed")


def test_handle_returns_string():
    """Test that handle() returns a non-empty string."""
    result = handle("帮我诊断Shopify店铺")
    assert isinstance(result, str), "Result must be a string"
    assert len(result) > 100, "Result too short to be a valid report"
    assert "Shopify" in result, "Result must contain 'Shopify'"
    print("✓ test_handle_returns_string passed")


def test_report_contains_sections():
    """Test that the generated report contains expected sections."""
    result = handle("我的Shopify店月访问量3000，转化率0.8%")
    assert "##" in result, "Report must have markdown headers"
    assert "转化率" in result, "Report must mention conversion rate"
    assert "SEO" in result or "seo" in result.lower(), "Report must mention SEO"
    print("✓ test_report_contains_sections passed")


def test_conversion_low_score():
    """Test that conversion rate < 1% is scored as low."""
    engine = DiagnosticEngine("转化率0.5%")
    score, label = engine._score_conversion()
    assert score == "low", f"Expected 'low', got '{score}'"
    print("✓ test_conversion_low_score passed")


def test_conversion_healthy_score():
    """Test that conversion rate >= 1.5% is scored as good."""
    engine = DiagnosticEngine("转化率2.5%")
    score, label = engine._score_conversion()
    assert score == "high", f"Expected 'high', got '{score}'"
    print("✓ test_conversion_healthy_score passed")


def test_app_catalog_has_entries():
    """Test that APP_CATALOG has entries for all three categories."""
    assert "conversion" in APP_CATALOG, "APP_CATALOG must have 'conversion'"
    assert "seo" in APP_CATALOG, "APP_CATALOG must have 'seo'"
    assert "ux" in APP_CATALOG, "APP_CATALOG must have 'ux'"
    assert len(APP_CATALOG["conversion"]) > 0, "conversion apps list must not be empty"
    print("✓ test_app_catalog_has_entries passed")


def test_tips_are_nonempty():
    """Test that all tip libraries are non-empty."""
    assert len(CONVERSION_TIPS) > 0, "CONVERSION_TIPS must not be empty"
    assert len(SEO_TIPS) > 0, "SEO_TIPS must not be empty"
    assert len(UX_TIPS) > 0, "UX_TIPS must not be empty"
    print("✓ test_tips_are_nonempty passed")


def test_report_no_api_claim():
    """Test that the report explicitly states no real API is called."""
    result = handle("帮我诊断店铺")
    assert "API" in result or "api" in result.lower(), "Report must mention no-API nature"
    print("✓ test_report_no_api_claim passed")


def test_english_input_handled():
    """Test that English input is handled gracefully."""
    engine = DiagnosticEngine("My Shopify store conversion rate is 0.9%")
    assert engine.area == "conversion", f"Expected 'conversion' for English input, got '{engine.area}'"
    result = handle("How can I improve my Shopify store conversion rate?")
    assert len(result) > 50, "English input should produce a valid report"
    print("✓ test_english_input_handled passed")


if __name__ == "__main__":
    print("=" * 60)
    print("Shopify Store Optimizer - Test Suite")
    print("=" * 60)
    print()

    tests = [
        test_area_detection_conversion,
        test_area_detection_seo,
        test_area_detection_all,
        test_area_detection_ux,
        test_conversion_rate_extraction,
        test_products_count_extraction,
        test_traffic_extraction,
        test_handle_returns_string,
        test_report_contains_sections,
        test_conversion_low_score,
        test_conversion_healthy_score,
        test_app_catalog_has_entries,
        test_tips_are_nonempty,
        test_report_no_api_claim,
        test_english_input_handled,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1

    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed > 0:
        sys.exit(1)
    else:
        print("All tests passed!")
        sys.exit(0)
