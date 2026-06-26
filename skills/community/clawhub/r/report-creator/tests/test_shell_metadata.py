from scripts.shell_metadata import (
    footer_watermark_html,
    footer_watermark_text,
    normalize_version,
)


def test_normalize_version_adds_v_prefix_once():
    assert normalize_version("1.21.0") == "v1.21.0"
    assert normalize_version("v1.21.0") == "v1.21.0"


def test_footer_watermark_text_uses_version_then_theme():
    assert (
        footer_watermark_text("1.21.0", "corporate-blue")
        == "kai-report-creator v1.21.0 corporate-blue"
    )


def test_footer_watermark_html_contains_visible_and_hidden_forms():
    html = footer_watermark_html("1.21.0", "corporate-blue")
    expected = "kai-report-creator v1.21.0 corporate-blue"
    assert f'<div class="report-footer">{expected}</div>' in html
    assert f'data-watermark="{expected}"' in html
    assert "IR hash" not in html
    assert "Source condensed" not in html
