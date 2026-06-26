"""
Playwright tests for browser-side export behaviour.

Tests run against tests/fixtures/minimal_report.html, which contains
the exact capture() JS from SKILL.md and a mock html2canvas that records
element state at the moment of capture.

Covers:
  - TOC toggle visibility regression (appeared in screenshots when sidebar closed)
  - Export resolution regression (1× → 2-3×)
  - Export button hidden during capture
  - Animations forced visible before capture
"""
import pytest


# ── helpers ───────────────────────────────────────────────────────────────────

def trigger_export(page, button_id: str):
    """Open the export menu, click a specific export button, wait for async capture."""
    page.evaluate("document.getElementById('export-btn').click()")
    page.evaluate(f"document.getElementById('{button_id}').click()")
    page.wait_for_timeout(300)  # html2canvas mock is async


def last_capture(page) -> dict:
    """Return the most recent capture log entry."""
    log = page.evaluate("window._captureLog")
    assert log, "No capture was triggered — check the button IDs in the fixture"
    return log[-1]


def reset_log(page):
    page.evaluate("window._captureLog = []")


# ── TOC toggle visibility ─────────────────────────────────────────────────────

class TestTocToggleVisibility:
    """
    Regression: TOC toggle button appeared in screenshots even when the
    sidebar was closed.  capture() must hide it unless the sidebar is open.
    """

    def test_toc_hidden_during_capture_when_sidebar_closed(self, report_page):
        """TOC toggle must be hidden at the moment html2canvas is called if sidebar is closed."""
        assert not report_page.evaluate(
            "document.getElementById('toc-sidebar').classList.contains('open')"
        ), "Precondition: sidebar must start closed"

        trigger_export(report_page, "export-png-mobile")
        entry = last_capture(report_page)

        assert entry["tocToggleVisibility"] == "hidden", (
            "TOC toggle was visible during screenshot with sidebar closed. "
            "This pollutes the screenshot with a floating button."
        )

    def test_toc_restored_after_capture_when_sidebar_closed(self, report_page):
        """After capture completes, TOC toggle must become visible again."""
        reset_log(report_page)
        trigger_export(report_page, "export-png-mobile")
        report_page.wait_for_timeout(100)

        visibility = report_page.evaluate(
            "document.getElementById('toc-toggle-btn').style.visibility"
        )
        assert visibility == "", (
            "TOC toggle was not restored after capture — "
            "the button stays invisible and the user can't open the TOC"
        )

    def test_toc_visible_during_capture_when_sidebar_open(self, report_page):
        """When sidebar IS open the toggle should stay visible in the screenshot."""
        report_page.evaluate(
            "document.getElementById('toc-sidebar').classList.add('open')"
        )
        reset_log(report_page)
        trigger_export(report_page, "export-png-mobile")
        entry = last_capture(report_page)

        assert entry["tocToggleVisibility"] == "", (
            "TOC toggle was hidden even though sidebar was open — "
            "the sidebar contents should be visible in the screenshot"
        )
        # cleanup
        report_page.evaluate(
            "document.getElementById('toc-sidebar').classList.remove('open')"
        )


# ── Export button hidden during capture ──────────────────────────────────────

class TestExportButtonHidden:
    """The export button must disappear while capture is in progress."""

    def test_export_btn_hidden_at_capture_time(self, report_page):
        """Export button must be hidden when html2canvas fires."""
        reset_log(report_page)
        trigger_export(report_page, "export-png-mobile")
        entry = last_capture(report_page)

        assert entry["exportBtnVisibility"] == "hidden", (
            "Export button was visible during html2canvas capture — "
            "it will appear in the exported image"
        )

    def test_export_btn_restored_after_capture(self, report_page):
        """After capture, the export button must be visible again."""
        reset_log(report_page)
        trigger_export(report_page, "export-png-mobile")
        report_page.wait_for_timeout(100)

        visibility = report_page.evaluate(
            "document.getElementById('export-btn').style.visibility"
        )
        assert visibility == "", "Export button must be restored after capture"


# ── Fade-in animations forced visible ────────────────────────────────────────

class TestAnimationsVisible:
    """Elements with .fade-in-up must be made visible before screenshot."""

    def test_fade_in_elements_visible_after_capture(self, report_page):
        """All .fade-in-up elements must have .visible added before html2canvas fires."""
        reset_log(report_page)
        trigger_export(report_page, "export-png-mobile")
        report_page.wait_for_timeout(100)

        hidden_count = report_page.evaluate(
            "document.querySelectorAll('.fade-in-up:not(.visible)').length"
        )
        assert hidden_count == 0, (
            f"{hidden_count} .fade-in-up elements are still invisible after capture — "
            "they will appear as blank in the exported image"
        )


# ── Background color passed to html2canvas ────────────────────────────────────

class TestBackgroundColor:
    """
    Regression: mobile/IM exports capture .report-wrapper, not body.
    html2canvas defaults to white when no backgroundColor is given, producing
    a white background on dark-theme reports.
    Passing body.backgroundColor is still insufficient when the page uses
    gradients or image backgrounds and body.backgroundColor resolves to transparent.
    """

    def test_mobile_capture_passes_background_color(self, report_page):
        """html2canvas must receive a non-null backgroundColor for mobile export."""
        reset_log(report_page)
        trigger_export(report_page, "export-png-mobile")
        entry = last_capture(report_page)

        assert entry["backgroundColor"] is not None, (
            "backgroundColor was not passed to html2canvas for mobile export — "
            "dark-theme reports will render with a white background."
        )

    def test_im_capture_passes_background_color(self, report_page):
        """html2canvas must receive a non-null backgroundColor for IM export."""
        reset_log(report_page)
        trigger_export(report_page, "export-im-share")
        entry = last_capture(report_page)

        assert entry["backgroundColor"] is not None, (
            "backgroundColor was not passed to html2canvas for IM export — "
            "dark-theme reports will render with a white background."
        )

    def test_mobile_capture_uses_non_transparent_export_background(self, report_page):
        """Mobile export must resolve to a concrete report background, not transparent."""
        reset_log(report_page)
        trigger_export(report_page, "export-png-mobile")
        entry = last_capture(report_page)

        assert entry["backgroundColor"] not in ("transparent", "rgba(0, 0, 0, 0)", "rgba(0,0,0,0)"), (
            "mobile export passed a transparent backgroundColor to html2canvas — "
            "gradient/background-image reports lose their page background in the exported image."
        )


# ── Resolution regression ─────────────────────────────────────────────────────

class TestExportResolution:
    """
    Regression: before fix, mobile/IM used 1× scale (blurry on retina screens).
    All modes must use >= 2× scale so exported images look sharp on modern displays.
    """

    def test_mobile_canvas_is_retina_width(self, report_page):
        """Mobile export canvas must be ~1500px wide (750px target × 2× retina).

        The JS formula is (750 / el.offsetWidth) * 2, so scale varies by element width,
        but the final canvas pixel width is always ≈ 750 × 2 = 1500px.
        Before the fix: canvas was ≈ 750px (1×, blurry on retina).
        """
        reset_log(report_page)
        trigger_export(report_page, "export-png-mobile")
        entry = last_capture(report_page)

        canvas_w = round(entry["width"] * entry["scale"])
        assert canvas_w >= 1350, (  # 750 * 2 * 0.9 = 1350 (10% tolerance)
            f"Mobile canvas width {canvas_w}px is too low — expected ~1500px (750px × 2×). "
            "Before the fix it was ~750px (1×), blurry on retina screens."
        )

    def test_im_canvas_is_retina_width(self, report_page):
        """IM export canvas must be ~1600px wide (800px target × 2× retina).

        Before the fix: canvas was ≈ 800px (1×, blurry in WeChat/DingTalk).
        """
        reset_log(report_page)
        trigger_export(report_page, "export-im-share")
        entry = last_capture(report_page)

        canvas_w = round(entry["width"] * entry["scale"])
        assert canvas_w >= 1440, (  # 800 * 2 * 0.9 = 1440
            f"IM canvas width {canvas_w}px is too low — expected ~1600px (800px × 2×). "
            "Before the fix it was ~800px (1×), blurry in IM apps."
        )

    def test_desktop_export_scale_is_high_resolution(self, report_page):
        """Desktop export must pass scale >= 2.5 to html2canvas."""
        reset_log(report_page)
        trigger_export(report_page, "export-png-desktop")
        entry = last_capture(report_page)

        assert entry["scale"] >= 2.5, (
            f"Desktop html2canvas scale is {entry['scale']} — "
            "was 1.5× before the fix"
        )

    def test_mobile_canvas_wider_than_css_element(self, report_page):
        """Canvas pixel width must exceed the element's CSS width (proves > 1× rendering)."""
        reset_log(report_page)
        trigger_export(report_page, "export-png-mobile")
        entry = last_capture(report_page)

        css_w = report_page.evaluate(
            "document.querySelector('.report-wrapper').scrollWidth"
        )
        canvas_w = round(entry["width"] * entry["scale"])
        assert canvas_w > css_w, (
            f"Canvas width {canvas_w}px must exceed element CSS width {css_w}px — "
            "otherwise the export is 1× (blurry) or smaller than the source"
        )
