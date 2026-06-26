"""Compose a self-contained HTML report.

Architecture:
- One shared HTML shell (head + page wrapper + doc-head + report section).
- One CSS theme picked by name (``default`` / ``print``); skills may layer
  additional CSS via ``extra_css``.
- One built-in UI-decoration IIFE: hides standalone ``---`` paragraphs,
  rotates h2 accent hue, colorizes numeric / labelled table cells.
- Pluggable per-skill ChartHooks: each contributes a JSON payload (merged
  under its ``name`` into a single ``<script id="chart-data">``) plus a JS
  body that runs inside an IIFE; the JS reads its slice via
  ``window.__chartData[name]``.
- Optional skill-supplied UI decoration JS (for hero cards that vary per
  report kind).
- The final HTML is run through ``validate_text_preserved``; failure raises
  ``RuntimeError`` (callers convert to warning if they want a non-strict
  CLI).
"""

from __future__ import annotations

import html
from datetime import datetime
from importlib import resources
from typing import List, Optional

from .chart_hook import ChartHook
from .markdown_engine import render_markdown
from .safe_json import safe_json_for_script
from .text_validator import validate_text_preserved


_FONT_LINKS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700'
    '&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">'
)


_BASE_UI_JS = """\
(function () {
  const root = document.getElementById("report-body");
  if (!root) return;

  /* hide standalone "---" separator paragraphs */
  root.querySelectorAll("p").forEach(p => {
    const txt = p.textContent.trim();
    if (/^-{3,}$/.test(txt)) { p.style.display = "none"; p.setAttribute("aria-hidden", "true"); }
  });

  /* rotate h2 accent hue across the six theme colors */
  let h2Idx = 0;
  root.querySelectorAll("h2").forEach(h => { h.setAttribute("data-idx", String(h2Idx % 6)); h2Idx += 1; });

  /* colorize numeric and star-rating table cells (domain-specific pill rules
     live in each skill's add_ui_decoration block) */
  root.querySelectorAll("td").forEach(td => {
    const trimmed = td.textContent.trim();
    if (!trimmed || td.children.length > 0) return;
    if (/^[★☆]+$/.test(trimmed)) {
      const filled = (trimmed.match(/★/g) || []).length;
      const total = Math.max(filled, 3);
      let h = "";
      for (let i = 0; i < total; i++) {
        h += i < filled ? '<span class="stars">★</span>' : '<span class="stars dim">★</span>';
      }
      td.innerHTML = h;
      return;
    }
    const signed = trimmed.match(/^([+\\-])(\\d[\\d,]*\\.?\\d*)\\s*(%|pct|x|倍|亿|万亿|分位)?$/);
    if (signed) {
      td.innerHTML = `<span class="${signed[1] === "+" ? "num-pos" : "num-neg"}">${trimmed}</span>`;
      return;
    }
    if (/[+\\-]\\d/.test(trimmed)) {
      td.innerHTML = td.innerHTML.replace(/([+\\-])(\\d+(?:[\\.,]\\d+)?)(%|pct|倍|x)?/g,
        (_, sign, num, unit) => `<span class="${sign === "+" ? "num-pos" : "num-neg"}">${sign}${num}${unit || ""}</span>`);
    }
  });

  /* expose the chart-data envelope under window.__chartData for ChartHook JS */
  const dataEl = document.getElementById("chart-data");
  try { window.__chartData = JSON.parse(dataEl ? (dataEl.textContent || "{}") : "{}"); }
  catch (e) { window.__chartData = {}; }
})();
"""


def _load_theme_css(theme: str) -> str:
    safe = theme.replace("/", "_").replace("\\", "_")
    pkg = resources.files(__package__) / "themes" / f"{safe}.css"
    if not pkg.is_file():
        available = ", ".join(list_themes())
        raise ValueError(f"unknown theme {theme!r}; available: {available}")
    return pkg.read_text(encoding="utf-8")


def list_themes() -> List[str]:
    themes_dir = resources.files(__package__) / "themes"
    return sorted(
        p.name[:-4]
        for p in themes_dir.iterdir()
        if p.is_file() and p.name.endswith(".css") and not p.name.startswith("_")
    )


class HtmlReportBuilder:
    def __init__(
        self,
        title: str,
        theme: str = "default",
        meta_text: str = "",
        extra_css: str = "",
        extra_head: str = "",
        lang: str = "zh-CN",
    ) -> None:
        self.title = title
        self.theme = theme
        self.meta_text = meta_text
        self.extra_css = extra_css
        self.extra_head = extra_head
        self.lang = lang
        self._theme_css = _load_theme_css(theme)
        self._hooks: List[ChartHook] = []
        self._ui_decorations: List[str] = []

    def add_chart_hook(self, hook: ChartHook) -> None:
        self._hooks.append(hook)

    def add_ui_decoration(self, js: str) -> None:
        """Append a skill-specific UI decoration IIFE that runs after the
        built-in one (e.g. promote a particular heading into a hero card).
        The supplied snippet should be a complete ``(function () { ... })();``
        block or equivalent; it is inserted verbatim inside ``<script>`` tags.
        """
        self._ui_decorations.append(js)

    def render(self, markdown_text: str, *, validate: bool = True) -> str:
        body_html = render_markdown(markdown_text)
        chart_envelope = {hook.name: hook.payload for hook in self._hooks}
        chart_json = safe_json_for_script(chart_envelope)
        hook_scripts = "\n".join(
            f"<script>\n(function () {{\n  const __payload = (window.__chartData || {{}})[{hook.name!r}] || {{}};\n{hook.js}\n}})();\n</script>"
            for hook in self._hooks
        )
        ui_extras = "\n".join(f"<script>\n{js}\n</script>" for js in self._ui_decorations)

        escaped_title = html.escape(self.title)
        doc_head_html = ""
        if self.meta_text:
            meta_html = html.escape(self.meta_text)
            doc_head_html = (
                '<div class="doc-head">\n'
                f'      <span class="dh-title">{escaped_title}</span>\n'
                f'      <span class="dh-meta">{meta_html}</span>\n'
                '    </div>\n    '
            )

        out = f"""<!doctype html>
<html lang="{self.lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escaped_title}</title>
  {_FONT_LINKS}
  <style>
{self._theme_css}
{self.extra_css}
  </style>
  {self.extra_head}
</head>
<body>
  <main class="page">
    {doc_head_html}<section class="section report" id="report-body">
      {body_html}
    </section>
  </main>
  <script id="chart-data" type="application/json">{chart_json}</script>
  <script>
{_BASE_UI_JS}  </script>
{ui_extras}
{hook_scripts}
</body>
</html>
"""
        if validate:
            validate_text_preserved(markdown_text, out)
        return out

    @property
    def generated_at(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
