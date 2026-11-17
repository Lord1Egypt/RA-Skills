# -*- coding: utf-8 -*-
"""slug 语义校验（verb-noun-platform）。"""
from __future__ import annotations

import unittest

from util.slug_naming import (
    LEGACY_EXEMPT_SLUGS,
    classify_slug_form,
    parse_slug_segments,
    validate_slug_semantics,
)


class TestSlugNaming(unittest.TestCase):
    def test_parse_slug_segments(self) -> None:
        self.assertEqual(parse_slug_segments("download-settlement-report-amazon"), [
            "download",
            "settlement",
            "report",
            "amazon",
        ])

    def test_classify_standard(self) -> None:
        segments = parse_slug_segments("download-settlement-report-amazon")
        self.assertEqual(classify_slug_form(segments, slug="download-settlement-report-amazon"), "standard")

    def test_classify_scope(self) -> None:
        segments = parse_slug_segments("generate-article-all")
        self.assertEqual(classify_slug_form(segments, slug="generate-article-all"), "scope")

    def test_classify_legacy_exempt(self) -> None:
        segments = parse_slug_segments("your-skill-slug")
        self.assertEqual(classify_slug_form(segments, slug="your-skill-slug"), "legacy_exempt")

    def test_valid_hyphenated_platform_slug(self) -> None:
        slug = "fill-export-declaration-single-window"
        segments = parse_slug_segments(slug)
        self.assertEqual(classify_slug_form(segments, slug=slug), "standard")
        errors, warnings = validate_slug_semantics(slug)
        self.assertEqual(errors, [], msg=f"errors={errors!r} warnings={warnings!r}")

    def test_valid_standard_slugs(self) -> None:
        for slug in (
            "download-settlement-report-amazon",
            "add-product-shopee",
            "generate-article-all",
            "your-skill-slug",
            "account-manager",
        ):
            with self.subTest(slug=slug):
                errors, warnings = validate_slug_semantics(slug)
                self.assertEqual(errors, [], msg=f"errors={errors!r} warnings={warnings!r}")

    def test_invalid_slugs(self) -> None:
        cases = (
            "amazon-download-settlement-report",
            "enter-cross-border-sales-receipt-voucher-kingdee",
            "reconcile-finance",
            "download-settlement-report-unknownplat",
            "foobar-settlement-report-amazon",
        )
        for slug in cases:
            with self.subTest(slug=slug):
                errors, _warnings = validate_slug_semantics(slug)
                self.assertTrue(errors, msg=f"expected errors for {slug!r}")

    def test_length_boundary_48_passes(self) -> None:
        slug = "query-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-amazon"
        self.assertEqual(len(slug), 48)
        errors, _warnings = validate_slug_semantics(slug)
        self.assertEqual(errors, [])

    def test_length_boundary_49_fails(self) -> None:
        slug = "query-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-amazon"
        self.assertEqual(len(slug), 49)
        errors, _warnings = validate_slug_semantics(slug)
        self.assertTrue(errors)
        self.assertTrue(any("48" in err for err in errors))

    def test_legacy_exempt_set(self) -> None:
        self.assertIn("your-skill-slug", LEGACY_EXEMPT_SLUGS)
        self.assertIn("account-manager", LEGACY_EXEMPT_SLUGS)


if __name__ == "__main__":
    unittest.main()
