#!/usr/bin/env python3
"""
Chart builder v3: project-based chart generation.

Each chart project lives in output/chart-html/<project-name>/
  index.html   — the chart page
  generate.py  — the generation script (optional, for reproducibility)
  README.md    — title, description, data sources
  data.json    — raw data snapshot
  screenshot.png — exported PNG (via Playwright or button)

Usage:
  from skills.chart.scripts.build_chart import (
      create_project, build_chart, build_chart_custom, save_chart, screenshot_chart
  )

  # Create project directory
  project_dir = create_project('btc-gold-90d')

  # Build HTML
  html = build_chart_custom(title='BTC vs Gold', ...)
  save_chart(html, project_dir=project_dir)

  # Optional: screenshot for direct image delivery
  screenshot_chart(project_dir)
"""

import os
import json
from datetime import datetime
from pathlib import Path

SKILL_DIR = os.path.join(os.path.dirname(__file__), '..')
SCRIPTS_DIR = os.path.join(SKILL_DIR, 'scripts')
TEMPLATES_DIR = os.path.join(SKILL_DIR, 'templates')
CHART_HTML_DIR = os.path.join('/data/workspace', 'output', 'chart-html')


def _read(path):
    with open(path, 'r') as f:
        return f.read()


def get_base_css():
    return _read(os.path.join(SCRIPTS_DIR, 'base-styles.css'))


def get_base_js():
    return _read(os.path.join(SCRIPTS_DIR, 'base-export.js'))


def create_project(name, description='', data_sources=None):
    """Create a new chart project directory.

    Args:
        name: Project folder name (e.g. 'btc-gold-90d-20250701')
        description: What this chart shows
        data_sources: list of data source strings

    Returns:
        Absolute path to the project directory
    """
    project_dir = os.path.join(CHART_HTML_DIR, name)
    os.makedirs(project_dir, exist_ok=True)

    # Write README.md
    readme = f"# {name}\n\n"
    readme += f"**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    if description:
        readme += f"{description}\n\n"
    if data_sources:
        readme += "**Data Sources:**\n"
        for src in data_sources:
            readme += f"- {src}\n"

    readme_path = os.path.join(project_dir, 'README.md')
    if not os.path.exists(readme_path):
        with open(readme_path, 'w') as f:
            f.write(readme)

    return project_dir


def build_chart(template_name, title='Chart', subtitle='', replacements=None):
    """Build chart from a template file.

    Args:
        template_name: template filename without .html extension (e.g. 'line', 'bar')
        title: chart page title
        subtitle: subtitle text
        replacements: dict of additional {{KEY}} → value replacements

    Returns:
        Complete HTML string
    """
    tpl_path = os.path.join(TEMPLATES_DIR, f'{template_name}.html')
    html = _read(tpl_path)

    css = get_base_css()
    js = get_base_js()

    html = html.replace('{{BASE_STYLES}}', css)
    html = html.replace('{{BASE_EXPORT_JS}}', js)
    html = html.replace('{{TITLE}}', title)
    html = html.replace('{{SUBTITLE}}', subtitle)

    if replacements:
        for k, v in replacements.items():
            html = html.replace(f'{{{{{k}}}}}', v)

    return html


def build_chart_custom(title='Chart', subtitle='', body_html='', chart_js='',
                       extra_css='', kpi_html='', layout='vertical'):
    """Build a fully custom chart page without using a template.

    IMPORTANT: chart_js MUST:
    1. Set window.CHART_INSTANCES = []; at the start
    2. Push each echarts instance: CHART_INSTANCES.push(chartVar);
    3. Optionally set window.CHART_LAYOUT = 'grid'; for 2-column export layout

    Args:
        title: page title
        subtitle: subtitle text below title
        body_html: HTML for chart containers (inside #chart-area)
        chart_js: JavaScript for chart initialization (must register CHART_INSTANCES)
        extra_css: additional CSS
        kpi_html: optional KPI cards HTML (placed above chart-area, not exported)
        layout: 'vertical' (default) or 'grid' — how charts are merged in export PNG

    Returns:
        Complete HTML string
    """
    css = get_base_css()
    js = get_base_js()
    layout_js = f"window.CHART_LAYOUT = '{layout}';" if layout != 'vertical' else ''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
  <style>
    {css}
    {extra_css}
  </style>
</head>
<body>
  <div class="toolbar">
    <div>
      <h1>{title}</h1>
      <div class="subtitle">{subtitle}</div>
    </div>
    <div class="actions">
      <button onclick="downloadPNG(this)">📥 Download PNG</button>
      <button onclick="copyToClipboard(this)">📋 Copy Image</button>
      <button onclick="saveToProject(this)">💾 Save Image</button>
    </div>
  </div>
  {kpi_html}
  <div id="chart-area">
    {body_html}
  </div>
  <script>
    {js}
    {layout_js}
  </script>
  <script>
    {chart_js}
  </script>
</body>
</html>'''


def save_chart(html, filename='index.html', project_dir=None, output_dir=None):
    """Save HTML to project directory or a legacy output directory.

    Args:
        html: HTML string
        filename: filename (default 'index.html')
        project_dir: project directory path (preferred)
        output_dir: legacy fallback directory

    Returns:
        The file path written
    """
    if project_dir:
        target_dir = project_dir
    elif output_dir:
        target_dir = output_dir
    else:
        target_dir = CHART_HTML_DIR

    os.makedirs(target_dir, exist_ok=True)
    path = os.path.join(target_dir, filename)
    with open(path, 'w') as f:
        f.write(html)
    return path


def save_data(data, project_dir, filename='data.json'):
    """Save data snapshot to project directory.

    Args:
        data: dict or list to serialize as JSON
        project_dir: project directory path
        filename: filename (default 'data.json')

    Returns:
        The file path written
    """
    os.makedirs(project_dir, exist_ok=True)
    path = os.path.join(project_dir, filename)
    with open(path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


def save_generate_script(script_content, project_dir):
    """Save the generation script for reproducibility.

    Args:
        script_content: Python script as string
        project_dir: project directory path

    Returns:
        The file path written
    """
    os.makedirs(project_dir, exist_ok=True)
    path = os.path.join(project_dir, 'generate.py')
    with open(path, 'w') as f:
        f.write(script_content)
    return path


def screenshot_chart(project_dir, filename='screenshot.png', width=1280, height=720):
    """Generate PNG via the same merge pipeline as the "Save Image" button.

    This ensures one-click screenshot output is visually equivalent to saveToProject()
    in the browser (title included, merged multi-chart layout consistent).

    Args:
        project_dir: project directory containing index.html
        filename: output PNG filename
        width: viewport width
        height: viewport height

    Returns:
        The screenshot file path, or None if failed
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[chart] Playwright not available, skipping screenshot")
        return None

    html_path = os.path.join(project_dir, 'index.html')
    if not os.path.exists(html_path):
        print(f"[chart] No index.html found in {project_dir}")
        return None

    out_path = os.path.join(project_dir, filename)
    file_url = f"file://{os.path.abspath(html_path)}"

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={'width': width, 'height': height})
            page.goto(file_url)
            page.wait_for_timeout(2200)  # let ECharts render

            # Reuse front-end merge/export logic for fidelity with save button.
            data_url = page.evaluate(
                """
                async () => {
                  if (typeof mergeChartsToDataURL === 'function') {
                    return await mergeChartsToDataURL();
                  }
                  throw new Error('mergeChartsToDataURL is not available on page');
                }
                """
            )

            if not data_url or ',' not in data_url:
                raise RuntimeError('Invalid data URL returned from page export pipeline')

            b64 = data_url.split(',', 1)[1]
            import base64
            png_bytes = base64.b64decode(b64)
            with open(out_path, 'wb') as f:
                f.write(png_bytes)

            browser.close()

        print(f"[chart] Screenshot saved: {out_path}")
        return out_path
    except Exception as e:
        print(f"[chart] Screenshot failed: {e}")
        return None


if __name__ == '__main__':
    # Quick test
    proj = create_project('test-chart')
    html = build_chart('line', title='Test Chart', subtitle='Testing build v3')
    path = save_chart(html, project_dir=proj)
    print(f'Built: {path}')
