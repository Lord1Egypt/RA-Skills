"""Convert HTML to PDF using Playwright's native PDF engine (text is searchable, not screenshots).

Usage: python convert_pdf_model.py <deck_html_path>
"""
import re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if len(sys.argv) < 2:
    print("Usage: python convert_pdf_model.py <deck_html_path>")
    sys.exit(1)

HTML_FILE = Path(sys.argv[1]).resolve()
if not HTML_FILE.exists():
    print(f"File not found: {HTML_FILE}")
    sys.exit(1)

DIR = HTML_FILE.parent
OUTPUT_PDF = DIR / f"{HTML_FILE.stem}.pdf"

# Read HTML and inline all CSS
html = HTML_FILE.read_text(encoding="utf-8")

def inline_css(content):
    def replace_link(match):
        href = match.group(1)
        css_path = DIR / href
        if css_path.exists():
            return f"<style>{css_path.read_text(encoding='utf-8')}</style>"
        return match.group(0)
    return re.sub(r'<link[^>]+href="([^"]+)"[^>]*>', replace_link, content)

html = inline_css(html)

# Fix pdf-model layout for print: inject override CSS with !important.
# Uses descendant selectors to match regardless of how the HTML author wrote the original CSS.
print_css = """
@page { size: 810px 1080px; margin: 0; }
.tpl-pdf-model .deck {
  height: auto !important;
  overflow: visible !important;
  position: static !important;
}
.tpl-pdf-model .slide {
  position: relative !important;
  inset: auto !important;
  opacity: 1 !important;
  pointer-events: auto !important;
  transform: none !important;
  page-break-after: always;
  break-after: page;
}
.tpl-pdf-model .slide:last-child { page-break-after: avoid; }
"""
html = html.replace("</head>", f"<style>{print_css}</style></head>")
print("CSS inlined, generating PDF via Playwright native engine...")

with sync_playwright() as p:
    try:
        browser = p.chromium.launch(channel="msedge")
    except Exception:
        print("msedge 不可用，回退到默认 Chromium")
        browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 810, "height": 1080})

    page.route("**/*", lambda route: route.abort()
               if "fonts.googleapis.com" in route.request.url or "fonts.gstatic.com" in route.request.url
               else route.continue_())

    page.set_content(html, wait_until="networkidle")
    page.wait_for_timeout(2000)

    page.pdf(
        path=str(OUTPUT_PDF),
        width="8.44in",
        height="11.25in",
        print_background=True,
        prefer_css_page_size=True,
    )

    browser.close()

print(f"PDF saved: {OUTPUT_PDF}")
print("Done — text is searchable and vector-sharp")
