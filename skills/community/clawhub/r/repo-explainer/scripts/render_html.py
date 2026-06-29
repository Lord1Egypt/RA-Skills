#!/usr/bin/env python3
"""Stage 5 (v3): render summary.json into HTML with pluggable theme system.

Theme resolution priority (highest first):
  1. --theme-override <path>  : user JSON file, deep-merged onto base theme
  2. --theme <name>           : one of themes.json keys (midnight/light/terminal)
  3. default                  : midnight

CSS-var-driven design — every visual aspect is wired through CSS variables,
so a theme override only needs to redefine the vars it cares about.
"""
import argparse
import html
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
THEMES_FILE = SCRIPT_DIR.parent / "templates" / "themes.json"

HTML_TPL = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<!-- Default link target is a NEW tab. We deliberately do NOT use
     target="_top" here, otherwise the JS click handler below would
     double-fire: the browser navigates the current frame to the new URL
     AND window.open() opens a second tab, leaving two copies of the
     report's new URL visible. With _blank the JS handler stays in
     control; if JS is disabled the link still opens externally. -->
<base target="_blank">
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {{
{css_vars}
  --font-primary: {font_primary};
  --font-mono: {font_mono};
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ scroll-behavior: smooth; }}
body {{
  font-family: var(--font-primary);
  background: var(--bg);
  color: var(--fg);
  line-height: 1.7;
  font-size: 15px;
  -webkit-font-smoothing: antialiased;
}}
.container {{ max-width: 1200px; margin: 0 auto; padding: 40px 28px 80px; }}

/* HERO */
.hero {{
  position: relative; padding: 56px 48px;
  background: var(--hero-grad);
  border-radius: 20px; margin-bottom: 32px;
  overflow: hidden; box-shadow: var(--shadow-lg);
}}
.hero::before {{
  content: ''; position: absolute; top: -50%; right: -20%;
  width: 600px; height: 600px;
  background: radial-gradient(circle, rgba(124,58,237,0.3) 0%, transparent 70%);
  pointer-events: none;
}}
.hero::after {{
  content: ''; position: absolute; bottom: -40%; left: -10%;
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(6,182,212,0.2) 0%, transparent 70%);
  pointer-events: none;
}}
.hero-content {{ position: relative; z-index: 1; }}
.hero h1 {{
  font-size: 42px; font-weight: 800; letter-spacing: -0.02em;
  color: #fff; margin-bottom: 12px;
}}
.hero .one-liner {{
  font-size: 19px; color: rgba(255,255,255,0.92);
  margin-bottom: 24px; line-height: 1.5; max-width: 820px;
}}
.hero .repo-link {{
  display: inline-flex; align-items: center; gap: 8px;
  color: #fff; text-decoration: none;
  font-family: var(--font-mono); font-size: 14px;
  padding: 8px 14px; background: rgba(255,255,255,0.15);
  border-radius: 8px; backdrop-filter: blur(10px);
  transition: all 0.2s; border: 1px solid rgba(255,255,255,0.1);
}}
.hero .repo-link:hover {{ background: rgba(255,255,255,0.25); transform: translateY(-1px); }}
.hero .badges {{ display: flex; gap: 10px; flex-wrap: wrap; margin-top: 20px; }}
.hero .badge {{
  background: rgba(255,255,255,0.15); backdrop-filter: blur(10px);
  padding: 6px 12px; border-radius: 20px;
  font-size: 13px; font-weight: 500; color: #fff;
  border: 1px solid rgba(255,255,255,0.1);
}}

/* SECTIONS */
.section {{
  background: var(--card); border: 1px solid var(--border);
  border-radius: 16px; padding: 32px; margin-bottom: 24px;
  transition: border-color 0.2s;
}}
.section:hover {{ border-color: var(--border-strong); }}
.section-header {{ display: flex; align-items: center; gap: 12px; margin-bottom: 24px; }}
.section-header h2 {{ font-size: 22px; font-weight: 700; letter-spacing: -0.01em; }}
.section-header .icon {{
  width: 36px; height: 36px; border-radius: 10px;
  background: var(--accent-grad);
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; color: #fff;
}}

/* TLDR */
.tldr {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }}
.tldr-card {{
  background: var(--bg-soft);
  border: 1px solid var(--border);
  padding: 20px; border-radius: 12px;
  transition: transform 0.2s, border-color 0.2s;
}}
.tldr-card:hover {{ transform: translateY(-2px); border-color: var(--accent); }}
.tldr-card .label {{
  font-size: 11px; color: var(--accent-2); text-transform: uppercase;
  letter-spacing: 1.2px; font-weight: 600; margin-bottom: 10px;
}}
.tldr-card .value {{ font-size: 16px; font-weight: 500; color: var(--fg); }}

/* TABLES */
.table-wrap {{ overflow-x: auto; border-radius: 12px; border: 1px solid var(--border); }}
table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
thead {{ background: var(--bg-soft); }}
th {{
  text-align: left; padding: 14px 18px;
  font-weight: 600; color: var(--accent-2);
  text-transform: uppercase; letter-spacing: 0.5px; font-size: 12px;
  border-bottom: 1px solid var(--border);
}}
td {{
  padding: 14px 18px; border-bottom: 1px solid var(--border);
  vertical-align: top; color: var(--fg-dim);
}}
tbody tr:last-child td {{ border-bottom: none; }}
tbody tr:hover td {{ background: var(--card-hover); color: var(--fg); }}
td strong {{ color: var(--fg); font-weight: 600; }}
code {{
  background: var(--code-bg);
  padding: 3px 8px; border-radius: 5px;
  font-family: var(--font-mono); font-size: 12.5px;
  color: var(--accent); border: 1px solid var(--border);
}}
.evidence {{
  font-family: var(--font-mono); font-size: 12px;
  color: var(--accent-2); text-decoration: none;
  padding: 2px 8px; border-radius: 4px;
  background: var(--bg-soft);
  border: 1px solid var(--border);
  transition: all 0.15s; display: inline-block;
  cursor: pointer;
}}
.evidence:hover {{ border-color: var(--accent-2); color: var(--fg); text-decoration: underline; }}
.evidence:visited {{ color: var(--accent-2); }}
.ev-link::after {{ content: " ↗"; opacity: 0.55; font-size: 0.85em; }}
.ev-link {{ cursor: pointer; }}
.ev-link:hover {{ background: var(--accent); color: var(--bg); border-color: var(--accent); }}
.ev-link:hover::after {{ opacity: 1; }}

/* MERMAID */
.mermaid-wrap {{
  position: relative;
  background: var(--diagram-bg);
  border: 1px solid var(--diagram-border);
  border-radius: 16px; padding: 40px 32px;
  overflow-x: auto; text-align: center;
  box-shadow: var(--diagram-shadow);
}}
.mermaid-wrap::before {{
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: var(--accent-grad);
  border-radius: 16px 16px 0 0; opacity: 0.7;
}}
.mermaid {{
  font-family: var(--font-primary) !important; min-height: 240px;
  display: flex; justify-content: center; align-items: center;
}}
.mermaid svg {{ max-width: 100%; height: auto !important; filter: drop-shadow(0 4px 12px rgba(0,0,0,0.18)); }}
.mermaid .cluster rect {{ rx: 12 !important; ry: 12 !important; stroke-width: 1.5px !important; stroke-dasharray: 4 3 !important; }}
.mermaid .cluster text {{ font-weight: 700 !important; font-size: 14px !important; letter-spacing: 0.3px; }}
.mermaid .node rect, .mermaid .node polygon, .mermaid .node circle, .mermaid .node ellipse, .mermaid .node path {{
  rx: 10 !important; ry: 10 !important; stroke-width: 2px !important;
}}
.mermaid .node .label {{ font-weight: 600 !important; }}
.mermaid .edgePath .path {{ stroke-width: 1.8px !important; }}
.mermaid .edgeLabel {{ padding: 4px 8px !important; border-radius: 6px !important; font-size: 12.5px !important; }}
.mermaid .actor {{ stroke-width: 2px !important; }}
.mermaid .actor-line {{ stroke-width: 1.5px !important; stroke-dasharray: 4 3 !important; opacity: 0.6; }}
.mermaid .messageText {{ font-weight: 600 !important; font-size: 13.5px !important; }}
.mermaid .noteText {{ font-weight: 500 !important; }}
.diagram-legend {{
  display: flex; gap: 14px; flex-wrap: wrap; justify-content: center;
  margin-top: 18px; padding-top: 16px; border-top: 1px dashed var(--border);
  font-size: 12px; color: var(--fg-muted);
}}
.diagram-legend .swatch {{
  display: inline-flex; align-items: center; gap: 6px;
}}
.diagram-legend .dot {{
  width: 12px; height: 12px; border-radius: 3px; border: 1.5px solid;
}}

/* MODULE CARDS */
.modules-grid {{ display: grid; grid-template-columns: 1fr; gap: 20px; }}
.module-card {{
  background: var(--bg-soft);
  border: 1px solid var(--border);
  border-left: 3px solid var(--accent);
  border-radius: 12px; padding: 24px;
  transition: all 0.2s;
}}
.module-card:hover {{ border-left-color: var(--accent-2); transform: translateX(4px); }}
.module-card-header {{
  display: flex; align-items: baseline; justify-content: space-between;
  flex-wrap: wrap; gap: 12px; margin-bottom: 14px;
}}
.module-card-header .name {{
  font-size: 18px; font-weight: 700; color: var(--fg);
  font-family: var(--font-mono);
}}
.module-card-header .path {{ font-family: var(--font-mono); font-size: 13px; color: var(--fg-muted); }}
.module-card .responsibility {{ color: var(--fg-dim); margin-bottom: 16px; line-height: 1.7; }}
.module-card .principle {{
  background: var(--card);
  border-left: 2px solid var(--accent);
  padding: 12px 16px; border-radius: 0 8px 8px 0;
  margin: 12px 0; font-size: 14px; color: var(--fg);
}}
.module-card .principle strong {{ color: var(--accent-2); }}
.module-card .subflow {{ margin-top: 16px; padding-top: 16px; border-top: 1px dashed var(--border); }}
.module-card .subflow-title {{
  font-size: 12px; text-transform: uppercase; letter-spacing: 0.8px;
  color: var(--accent-3); font-weight: 600; margin-bottom: 12px;
}}
.module-card .subflow-steps {{ display: flex; flex-direction: column; gap: 8px; }}
.module-card .subflow-step {{
  display: flex; align-items: flex-start; gap: 10px;
  font-size: 13.5px; color: var(--fg-dim);
}}
.module-card .subflow-step .num {{
  flex-shrink: 0; width: 22px; height: 22px;
  background: var(--accent-grad); color: white;
  border-radius: 6px; display: flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 700;
}}
.module-card .evidence-row {{ margin-top: 14px; display: flex; flex-wrap: wrap; gap: 6px; }}

/* HIGHLIGHTS */
.highlights-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; }}
.highlight-card {{
  background: var(--bg-soft);
  border: 1px solid var(--border);
  border-left: 3px solid var(--accent-3);
  padding: 16px 18px; border-radius: 10px;
  font-size: 14.5px; color: var(--fg);
  display: flex; align-items: flex-start; gap: 12px;
}}
.highlight-card .star {{ color: var(--accent-3); font-size: 18px; flex-shrink: 0; }}

/* LIMITATIONS */
.limitations-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 16px; }}
.limit-card {{
  background: var(--bg-soft);
  border: 1px solid var(--border);
  border-left: 3px solid #ef4444;
  border-radius: 10px; padding: 18px 20px;
  display: flex; flex-direction: column; gap: 10px;
}}
.limit-card .limit-head {{ display: flex; align-items: center; justify-content: space-between; gap: 10px; flex-wrap: wrap; }}
.limit-card .limit-title {{ font-weight: 700; color: var(--fg); font-size: 15px; flex: 1; line-height: 1.4; }}
.limit-card .limit-tags {{ display: flex; gap: 6px; flex-shrink: 0; flex-wrap: wrap; }}
.limit-card .tag {{
  font-size: 11px; font-weight: 600; text-transform: uppercase;
  padding: 3px 8px; border-radius: 4px; letter-spacing: 0.4px;
  font-family: var(--font-mono);
}}
.limit-card .tag.sev-high {{ background: rgba(239,68,68,0.18); color: #ef4444; border: 1px solid rgba(239,68,68,0.4); }}
.limit-card .tag.sev-medium {{ background: rgba(245,158,11,0.18); color: #f59e0b; border: 1px solid rgba(245,158,11,0.4); }}
.limit-card .tag.sev-low {{ background: rgba(34,197,94,0.15); color: #22c55e; border: 1px solid rgba(34,197,94,0.4); }}
.limit-card .tag.cat {{ background: var(--card); color: var(--fg-dim); border: 1px solid var(--border); }}
.limit-card .limit-detail {{ font-size: 14px; color: var(--fg-dim); line-height: 1.65; }}
.limit-card .limit-evidence {{ margin-top: 4px; }}

/* GLOSSARY */
.glossary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 14px; }}
.glossary-item {{
  background: var(--bg-soft); padding: 16px 18px; border-radius: 10px;
  border: 1px solid var(--border);
}}
.glossary-item .term {{
  font-weight: 700; color: var(--accent-2);
  font-family: var(--font-mono); font-size: 14px; margin-bottom: 6px;
}}
.glossary-item .plain {{ font-size: 13.5px; color: var(--fg-dim); line-height: 1.6; }}

/* FOOTER */
.footer {{
  text-align: center; color: var(--fg-muted); font-size: 12px;
  margin-top: 48px; padding-top: 24px; border-top: 1px solid var(--border);
}}
.empty {{ color: var(--fg-muted); font-style: italic; }}

/* THEME PICKER */
.theme-picker {{
  position: fixed; top: 20px; right: 20px; z-index: 100;
  background: var(--card); border: 1px solid var(--border);
  border-radius: 10px; padding: 6px;
  display: flex; gap: 4px; box-shadow: var(--shadow-lg);
  backdrop-filter: blur(10px);
}}
.theme-picker button {{
  background: transparent; border: 1px solid transparent;
  color: var(--fg-dim); padding: 6px 12px; border-radius: 6px;
  font-size: 12px; cursor: pointer; font-family: var(--font-primary);
  transition: all 0.15s;
}}
.theme-picker button:hover {{ color: var(--fg); border-color: var(--border); }}
.theme-picker button.active {{
  background: var(--accent); color: #fff; border-color: var(--accent);
}}

@media (max-width: 768px) {{
  .container {{ padding: 20px 16px 60px; }}
  .hero {{ padding: 32px 24px; }}
  .hero h1 {{ font-size: 30px; }}
  .hero .one-liner {{ font-size: 16px; }}
  .section {{ padding: 24px 20px; }}
  .module-card-header {{ flex-direction: column; gap: 6px; }}
  .theme-picker {{ top: auto; bottom: 20px; right: 20px; }}
}}

@media print {{
  body {{ background: white; color: black; }}
  .hero, .section {{ break-inside: avoid; box-shadow: none; }}
  .theme-picker {{ display: none; }}
}}
</style>
</head>
<body>

<div class="theme-picker">
  <button data-theme="midnight">Midnight</button>
  <button data-theme="light">Light</button>
  <button data-theme="terminal">Terminal</button>
</div>

<div class="container">

  <div class="hero">
    <div class="hero-content">
      <h1>{project_name}</h1>
      <p class="one-liner">{one_liner}</p>
      {repo_link}
      <div class="badges">{badges}</div>
    </div>
  </div>

  <div class="section">
    <div class="section-header"><div class="icon">🎯</div><h2>一句话看懂</h2></div>
    <div class="tldr">
      <div class="tldr-card"><div class="label">面向谁</div><div class="value">{who_for}</div></div>
      <div class="tldr-card"><div class="label">解决什么</div><div class="value">{problem_solved}</div></div>
      <div class="tldr-card"><div class="label">核心价值</div><div class="value">{core_value}</div></div>
    </div>
  </div>

  <div class="section">
    <div class="section-header"><div class="icon">⚙️</div><h2>技术栈</h2></div>
    <div class="table-wrap">{tech_stack_table}</div>
  </div>

  <div class="section">
    <div class="section-header"><div class="icon">🏗️</div><h2>系统架构</h2></div>
    <div class="mermaid-wrap">
      <pre class="mermaid">{architecture_mermaid}</pre>
      {architecture_legend}
    </div>
  </div>

  <div class="section">
    <div class="section-header"><div class="icon">🗂️</div><h2>核心模型</h2></div>
    <div class="table-wrap">{key_models_table}</div>
  </div>

  <div class="section">
    <div class="section-header"><div class="icon">🧩</div><h2>关键模块详解</h2></div>
    <div class="modules-grid">{key_modules_cards}</div>
  </div>

  <div class="section">
    <div class="section-header"><div class="icon">🔄</div><h2>主流程时序</h2></div>
    <div class="mermaid-wrap"><pre class="mermaid">{sequence_mermaid}</pre></div>
  </div>

  {api_surface_section}

  <div class="section">
    <div class="section-header"><div class="icon">📦</div><h2>关键依赖</h2></div>
    <div class="table-wrap">{dependencies_table}</div>
  </div>

  <div class="section">
    <div class="section-header"><div class="icon">✨</div><h2>项目特色</h2></div>
    <div class="highlights-grid">{highlights_grid}</div>
  </div>

  <div class="section">
    <div class="section-header"><div class="icon">⚠️</div><h2>限制 / 待优化点</h2></div>
    <div class="limitations-grid">{limitations_grid}</div>
  </div>

  <div class="section">
    <div class="section-header"><div class="icon">📖</div><h2>术语对照</h2></div>
    <div class="glossary">{glossary_items}</div>
  </div>

  <div class="footer">
    由 repo-explainer 基于源码生成 · 每条结论可点 path:line 跳转 GitHub 校对<br>
    {footer_meta} · 共扫描 {file_count} 个代码文件 · 主题:<span id="cur-theme">{theme_name}</span>
  </div>
</div>

<script id="theme-data" type="application/json">{theme_data_json}</script>
<script>
const THEMES = JSON.parse(document.getElementById('theme-data').textContent);
const ACTIVE_KEY = 'repo-explainer-theme';

function applyTheme(name) {{
  const t = THEMES[name];
  if (!t) return;
  const root = document.documentElement;
  Object.entries(t.css_vars).forEach(([k,v]) => root.style.setProperty(k, v));
  root.style.setProperty('--font-primary', t.fonts.primary);
  root.style.setProperty('--font-mono', t.fonts.mono);
  document.getElementById('cur-theme').textContent = t.name;
  document.querySelectorAll('.theme-picker button').forEach(b => {{
    b.classList.toggle('active', b.dataset.theme === name);
  }});
  localStorage.setItem(ACTIVE_KEY, name);
  // re-render mermaid with new theme
  mermaid.initialize({{
    startOnLoad: false,
    theme: t.mermaid.theme,
    themeVariables: t.mermaid.themeVariables,
    securityLevel: 'loose',
    flowchart: {{ curve: 'basis', padding: 24, nodeSpacing: 60, rankSpacing: 80, htmlLabels: true, useMaxWidth: true, diagramPadding: 16 }},
    sequence: {{ actorMargin: 70, boxMargin: 14, messageMargin: 50, boxTextMargin: 8, noteMargin: 12, mirrorActors: false, bottomMarginAdj: 12, useMaxWidth: true, rightAngles: false, showSequenceNumbers: true, wrap: true }}
  }});
  // reset rendered mermaid blocks
  document.querySelectorAll('.mermaid').forEach((el, i) => {{
    if (!el.dataset.source) el.dataset.source = el.textContent;
    el.removeAttribute('data-processed');
    el.innerHTML = el.dataset.source;
  }});
  mermaid.run();
}}

document.querySelectorAll('.theme-picker button').forEach(b => {{
  b.addEventListener('click', () => applyTheme(b.dataset.theme));
}});

const saved = localStorage.getItem(ACTIVE_KEY) || '{initial_theme}';
applyTheme(saved);

// ---------------------------------------------------------------------
// Click-escape-hatch for code-path / evidence links.
// When this report is opened inside a strict sandboxed iframe (Mira /
// Lark / Notion preview pane), plain <a> navigation can be silently
// blocked. We override the default click and try, in order:
//   1. window.open(href, '_blank', 'noopener') — opens a NEW tab without
//      touching the current page (preferred behaviour)
//   2. top.location.href = href                — only used when window.open
//      is blocked (popup blocker / strict sandbox)
//   3. location.href = href                    — final same-frame fallback
// All three are wrapped in try/catch so a thrown SecurityError falls
// through to the next. ev.preventDefault() + stopPropagation() ensures
// the browser does NOT also navigate the current frame via <base>, so
// a successful window.open never produces two tabs.
// ---------------------------------------------------------------------
function openExternal(href, ev) {{
  if (!href) return;
  if (ev) {{ ev.preventDefault(); ev.stopPropagation(); }}
  let win = null;
  try {{ win = window.open(href, '_blank', 'noopener,noreferrer'); }} catch (e) {{}}
  if (win) return;
  try {{ top.location.href = href; return; }} catch (e) {{}}
  try {{ window.location.href = href; }} catch (e) {{}}
}}

document.addEventListener('click', function (ev) {{
  const a = ev.target.closest('a.ev-link, a.repo-link');
  if (!a) return;
  const href = a.getAttribute('href');
  if (!href) return;
  openExternal(href, ev);
}}, true);

// Middle-click / ctrl+click should also work — browser handles those
// natively as long as href is present, which it is.
</script>
</body>
</html>
"""


def deep_merge(base, override):
    if not isinstance(base, dict) or not isinstance(override, dict):
        return override
    out = dict(base)
    for k, v in override.items():
        out[k] = deep_merge(out.get(k), v) if k in out else v
    return out


def load_themes(override_path: str | None):
    with open(THEMES_FILE) as f:
        bundle = json.load(f)
    themes = bundle["themes"]
    if override_path:
        with open(override_path) as f:
            user = json.load(f)
        # user file may be {"themes": {...}} or just a single theme {"css_vars": ...}
        if "themes" in user:
            for name, t in user["themes"].items():
                themes[name] = deep_merge(themes.get(name, {}), t)
        else:
            themes["custom"] = deep_merge(themes.get("midnight", {}), user)
    return themes


def esc(s):
    if s is None: return ""
    return html.escape(str(s))


# heuristics to colour-classify nodes inside subgraphs of the architecture diagram
SUBGRAPH_CLASS_HINTS = [
    ("user", ["user", "用户", "客户端", "client", "ui", "前端", "console", "cli", "agent", "上层"]),
    ("kernel", ["kernel", "内核", "ebpf", "bpf", "btrfs", "syscall", "lsm"]),
    ("store", ["store", "storage", "存储", "db", "数据库", "rocks", "sqlite", "fts", "queue", "cache"]),
    ("module", ["module", "模块", "能力", "service", "engine", "worker", "actor", "plugin"]),
    ("core", ["core", "守护", "daemon", "scheduler", "调度", "controller", "manager", "orchestrat"]),
]


def _classify_subgraph(title: str) -> str:
    t = (title or "").lower()
    for cls, kws in SUBGRAPH_CLASS_HINTS:
        if any(kw in t for kw in kws):
            return cls
    return "module"


def enrich_architecture_mermaid(src: str, palette: dict) -> tuple[str, list[tuple[str, dict]]]:
    """Auto-inject classDef + class statements based on subgraph membership.
    Returns (enriched_mermaid_source, legend_used)
    """
    if not src or "graph" not in src.split("\n", 1)[0].lower():
        return src, []
    # if user already provided classDef, leave it untouched
    if "classDef" in src:
        return src, []

    import re
    lines = src.split("\n")
    # parse subgraphs: subgraph ID["Title"]   ...   end
    # extract node ids that appear inside each subgraph
    node_id_re = re.compile(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*[\[\(\{]')
    sub_open_re = re.compile(r'^\s*subgraph\s+(\S+?)(?:\s*\[\s*"?([^"\]]+)"?\s*\])?\s*$')
    class_assignments = {}  # node_id -> class
    used_classes = set()
    stack = []  # list of current class names

    for ln in lines:
        m = sub_open_re.match(ln)
        if m:
            sg_id, sg_title = m.group(1), m.group(2) or m.group(1)
            cls = _classify_subgraph(sg_title or sg_id)
            stack.append(cls)
            continue
        if ln.strip().lower() == "end":
            if stack:
                stack.pop()
            continue
        if stack:
            nm = node_id_re.match(ln)
            if nm:
                nid = nm.group(1)
                if nid not in {"subgraph", "end", "graph", "flowchart"}:
                    class_assignments[nid] = stack[-1]
                    used_classes.add(stack[-1])

    if not class_assignments:
        return src, []

    classdef_lines = []
    for cls in sorted(used_classes):
        p = palette.get(cls)
        if not p:
            continue
        classdef_lines.append(
            f"classDef {cls} fill:{p['fill']},stroke:{p['stroke']},color:{p['color']},stroke-width:2px,rx:10,ry:10"
        )
    # group node ids per class
    grouped = {}
    for nid, cls in class_assignments.items():
        grouped.setdefault(cls, []).append(nid)
    class_lines = [f"class {','.join(sorted(set(ids)))} {cls}" for cls, ids in grouped.items()]

    enriched = src.rstrip() + "\n" + "\n".join(classdef_lines + class_lines) + "\n"
    legend = [(cls, palette[cls]) for cls in sorted(used_classes) if cls in palette]
    return enriched, legend


def render_legend(legend: list) -> str:
    if not legend:
        return ""
    label_map = {
        "user": "用户 / 客户端",
        "core": "核心 / 调度",
        "module": "业务模块",
        "kernel": "内核 / 底层",
        "store": "存储 / 数据",
    }
    items = "".join(
        f'<span class="swatch"><span class="dot" style="background:{p["fill"]};border-color:{p["stroke"]}"></span>{label_map.get(cls, cls)}</span>'
        for cls, p in legend
    )
    return f'<div class="diagram-legend">{items}</div>'


def evidence_link(ev: str, repo_url: str, sha: str) -> str:
    if not ev or ":" not in ev:
        return '<span class="empty">—</span>'
    path, line = ev.rsplit(":", 1)
    if not line.isdigit():
        path = ev; line = "1"
    # Local-directory mode: no GitHub URL is available, so render the
    # evidence as monospace text rather than a broken-link anchor.
    if not repo_url:
        return f'<code class="evidence">{esc(ev)}</code>'
    url = f"{repo_url}/blob/{sha}/{path}#L{line}"
    # No target attr — <base target="_top"> in <head> forces top-level
    # navigation, which works inside Mira / Lark / Notion preview iframes
    # where target="_blank" would otherwise be silently blocked by the
    # sandbox policy.
    return f'<a class="evidence ev-link" href="{esc(url)}" rel="noopener noreferrer">{esc(ev)}</a>'


def path_link(path: str, repo_url: str, sha: str) -> str:
    """Render a bare repo path (file or dir) as a clickable GitHub link.

    Files → /blob/<sha>/<path>; directories → /tree/<sha>/<path>.
    Falls back to a plain `<code>` if repo_url is missing.

    NOTE: we deliberately do NOT wrap the visible text in <code> — nested
    <code> inside <a> visually masks the link affordance in some browsers
    / embedded preview iframes and trips users into thinking it's a label.
    The .ev-link CSS class supplies the monospace + chip styling instead.
    """
    if not path:
        return '<span class="empty">—</span>'
    clean = path.strip().rstrip("/")
    if not clean or not repo_url:
        return f"<code>{esc(path)}</code>"
    is_dir = path.rstrip().endswith("/") or "." not in clean.rsplit("/", 1)[-1]
    kind = "tree" if is_dir else "blob"
    url = f"{repo_url}/{kind}/{sha}/{clean}"
    return f'<a class="evidence ev-link" href="{esc(url)}" rel="noopener noreferrer">{esc(path)}</a>'


def render_tech_stack(items):
    if not items: return '<p class="empty">未识别</p>'
    rows = "".join(
        f"<tr><td><strong>{esc(it.get('layer'))}</strong></td><td>{esc(', '.join(it.get('items', [])))}</td></tr>"
        for it in items
    )
    return f"<table><thead><tr><th style='width:25%'>层</th><th>组件</th></tr></thead><tbody>{rows}</tbody></table>"


def render_modules_cards(items, repo_url, sha):
    if not items: return '<p class="empty">未识别</p>'
    cards = []
    for it in items:
        principle = it.get("principle", "")
        principle_html = f'<div class="principle"><strong>核心原理:</strong> {esc(principle)}</div>' if principle else ""
        subflow = it.get("subflow", [])
        subflow_html = ""
        if subflow:
            steps = "".join(
                f'<div class="subflow-step"><span class="num">{i+1}</span><span>{esc(s)}</span></div>'
                for i, s in enumerate(subflow)
            )
            subflow_html = f'<div class="subflow"><div class="subflow-title">关键流程</div><div class="subflow-steps">{steps}</div></div>'
        evidence_list = it.get("evidence_list", [])
        if not evidence_list and it.get("evidence"):
            evidence_list = [it["evidence"]]
        ev_html = "".join(evidence_link(e, repo_url, sha) for e in evidence_list)
        ev_row = f'<div class="evidence-row">{ev_html}</div>' if ev_html else ""
        cards.append(f"""
        <div class="module-card">
          <div class="module-card-header">
            <span class="name">{esc(it.get('name'))}</span>
            <span class="path">{path_link(it.get('path', ''), repo_url, sha)}</span>
          </div>
          <div class="responsibility">{esc(it.get('responsibility'))}</div>
          {principle_html}
          {subflow_html}
          {ev_row}
        </div>""")
    return "".join(cards)


def render_api(items, repo_url, sha):
    """Return the full <section> for 对外接口, or '' to hide it entirely.

    Hides when items is empty, or when no row carries all three required
    fields (type / signature / purpose). Rows missing any required field
    are silently dropped rather than rendered as half-empty noise.
    """
    if not items:
        return ""
    valid = [
        it for it in items
        if (it.get("type") or "").strip()
        and (it.get("signature") or "").strip()
        and (it.get("purpose") or "").strip()
    ]
    if not valid:
        return ""
    rows = "".join(
        f"<tr>"
        f"<td><strong>{esc(it.get('type'))}</strong></td>"
        f"<td><code>{esc(it.get('signature'))}</code></td>"
        f"<td>{esc(it.get('purpose'))}</td>"
        f"<td>{evidence_link(it.get('evidence', ''), repo_url, sha) if it.get('evidence') else '<span class=\"empty\">—</span>'}</td>"
        f"</tr>"
        for it in valid
    )
    table = (
        "<table><thead><tr><th>类型</th><th>签名</th><th>用途</th><th>证据</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
    )
    return (
        '<div class="section">'
        '<div class="section-header"><div class="icon">🔌</div><h2>对外接口</h2></div>'
        f'<div class="table-wrap">{table}</div>'
        '</div>'
    )


def render_deps(items):
    if not items: return '<p class="empty">未识别</p>'
    rows = "".join(
        f"<tr><td><code>{esc(it.get('name'))}</code></td><td>{esc(it.get('purpose'))}</td>"
        f"<td><strong>{esc(it.get('criticality'))}</strong></td></tr>"
        for it in items
    )
    return f"<table><thead><tr><th>依赖</th><th>用途</th><th>重要度</th></tr></thead><tbody>{rows}</tbody></table>"


def render_highlights_grid(items):
    if not items: return '<div class="empty">未识别</div>'
    return "".join(f'<div class="highlight-card"><span class="star">★</span><span>{esc(it)}</span></div>' for it in items)


def render_key_models(items, repo_url, sha):
    if not items: return '<p class="empty">未识别</p>'
    rows = []
    for it in items:
        ev = it.get("evidence", "")
        ev_html = evidence_link(ev, repo_url, sha) if ev else '<span class="empty">—</span>'
        fields = it.get("key_fields", "")
        fields_html = f"<div style='margin-top:4px;font-family:var(--font-mono);font-size:12px;color:var(--fg-muted)'>{esc(fields)}</div>" if fields else ""
        rows.append(
            f"<tr>"
            f"<td><strong>{esc(it.get('name'))}</strong>{fields_html}</td>"
            f"<td>{path_link(it.get('path', ''), repo_url, sha)}</td>"
            f"<td>{esc(it.get('purpose'))}</td>"
            f"<td>{ev_html}</td>"
            f"</tr>"
        )
    return ("<table><thead><tr>"
            "<th style='width:20%'>模型</th>"
            "<th style='width:22%'>定义位置</th>"
            "<th>作用</th>"
            "<th style='width:18%'>证据</th>"
            "</tr></thead><tbody>"
            + "".join(rows) + "</tbody></table>")


def render_limitations(items, repo_url, sha):
    if not items: return '<div class="empty">未识别</div>'
    cards = []
    for it in items:
        sev = (it.get("severity") or "medium").lower()
        cat = it.get("category") or "other"
        ev = it.get("evidence", "")
        # evidence may be path:line or a free-form URL/note
        if ev and ":" in ev and not ev.startswith("http"):
            ev_html = f'<div class="limit-evidence">{evidence_link(ev, repo_url, sha)}</div>'
        elif ev:
            ev_html = f'<div class="limit-evidence"><a class="evidence ev-link" href="{esc(ev)}" rel="noopener noreferrer">{esc(ev)}</a></div>' if ev.startswith("http") else f'<div class="limit-evidence"><span class="evidence">{esc(ev)}</span></div>'
        else:
            ev_html = ""
        cards.append(
            f'<div class="limit-card">'
            f'  <div class="limit-head">'
            f'    <div class="limit-title">{esc(it.get("title"))}</div>'
            f'    <div class="limit-tags">'
            f'      <span class="tag sev-{esc(sev)}">{esc(sev)}</span>'
            f'      <span class="tag cat">{esc(cat)}</span>'
            f'    </div>'
            f'  </div>'
            f'  <div class="limit-detail">{esc(it.get("detail"))}</div>'
            f'  {ev_html}'
            f'</div>'
        )
    return "".join(cards)


def render_glossary(items):
    if not items: return '<div class="empty">无</div>'
    return "".join(
        f'<div class="glossary-item"><div class="term">{esc(it.get("term"))}</div><div class="plain">{esc(it.get("plain"))}</div></div>'
        for it in items
    )


def render_css_vars(theme):
    lines = []
    for k, v in theme["css_vars"].items():
        lines.append(f"  {k}: {v};")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("summary_json")
    ap.add_argument("--meta_json", required=True)
    ap.add_argument("--file_count", default="?")
    ap.add_argument("--theme", default="midnight", help="midnight | light | terminal | (custom name from override)")
    ap.add_argument("--theme-override", default=None, help="path to a user JSON file to deep-merge into the theme bundle")
    args = ap.parse_args()

    themes = load_themes(args.theme_override)
    if args.theme not in themes:
        sys.exit(f"ERROR: unknown theme '{args.theme}'. Available: {list(themes.keys())}")
    active = themes[args.theme]

    summary = json.loads(Path(args.summary_json).read_text())
    meta = json.loads(Path(args.meta_json).read_text())
    # Local-mode safety: owner/repo/commit_sha may all be missing if the
    # source was a non-git local directory. Renderers downstream already
    # degrade clickable links to plain code when repo_url is "" — here we
    # only need to compute the values defensively (no KeyError).
    owner = meta.get("owner") or ""
    repo = meta.get("repo") or ""
    repo_url = f"https://github.com/{owner}/{repo}" if owner and repo else ""
    sha = meta.get("commit_sha") or ""
    gh_meta = meta.get("github_meta") or {}

    arch_src = summary.get("architecture_mermaid", "graph TD\n  A[未生成]")
    palette = active.get("diagram_class_palette", {})
    arch_src_enriched, legend = enrich_architecture_mermaid(arch_src, palette)

    # ---- hero: repo-link + badges (skip pieces we have no data for) -----
    if repo_url:
        gh_svg = (
            '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">'
            '<path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 '
            '11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416'
            '-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083'
            '-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 '
            '2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305'
            '-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124'
            '-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 '
            '1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 '
            '3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 '
            '1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 '
            '5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 '
            '4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12'
            '-12z"/></svg>'
        )
        repo_link_html = (
            f'<a class="repo-link" href="{esc(repo_url)}">{gh_svg}{esc(repo_url)}</a>'
        )
    else:
        # Local-directory mode: show the local path read-only instead.
        local_path = meta.get("local_path") or ""
        repo_link_html = (
            f'<div class="repo-link" title="本地目录,无远程仓库链接">'
            f'📁 {esc(local_path)}</div>' if local_path else ""
        )

    badge_bits: list[str] = []
    if gh_meta.get("stars") is not None:
        badge_bits.append(f'<span class="badge">★ {esc(gh_meta.get("stars"))}</span>')
    lang = gh_meta.get("language") or gh_meta.get("primary_language")
    if lang:
        badge_bits.append(f'<span class="badge">主语言 {esc(lang)}</span>')
    if sha:
        badge_bits.append(f'<span class="badge">commit {esc(sha[:7])}</span>')
    if meta.get("branch"):
        badge_bits.append(f'<span class="badge">branch {esc(meta["branch"])}</span>')
    if meta.get("mode") == "local":
        badge_bits.append('<span class="badge">本地目录</span>')
    badges_html = "".join(badge_bits)

    footer_bits: list[str] = []
    if sha:
        footer_bits.append(f"commit {esc(sha[:7])}")
    if meta.get("mode") == "local":
        footer_bits.append("本地目录分析")
    footer_meta = " · ".join(footer_bits) if footer_bits else "基于源码生成"

    out = HTML_TPL.format(
        title=esc(summary.get("project_name", repo or "Local Project")),
        project_name=esc(summary.get("project_name", repo or "Local Project")),
        one_liner=esc(summary.get("one_liner", gh_meta.get("description", ""))),
        repo_link=repo_link_html,
        badges=badges_html,
        footer_meta=footer_meta,
        who_for=esc(summary.get("who_for", "")),
        problem_solved=esc(summary.get("problem_solved", "")),
        core_value=esc(summary.get("core_value", "")),
        tech_stack_table=render_tech_stack(summary.get("tech_stack", [])),
        architecture_mermaid=arch_src_enriched,
        architecture_legend=render_legend(legend),
        key_models_table=render_key_models(summary.get("key_models", []), repo_url, sha),
        key_modules_cards=render_modules_cards(summary.get("key_modules", []), repo_url, sha),
        sequence_mermaid=summary.get("sequence_mermaid", "sequenceDiagram\n  Note over A: 未生成"),
        api_surface_section=render_api(summary.get("api_surface", []), repo_url, sha),
        dependencies_table=render_deps(summary.get("dependencies", [])),
        highlights_grid=render_highlights_grid(summary.get("highlights", [])),
        limitations_grid=render_limitations(summary.get("limitations", []), repo_url, sha),
        glossary_items=render_glossary(summary.get("glossary", [])),
        file_count=esc(args.file_count),
        css_vars=render_css_vars(active),
        font_primary=active["fonts"]["primary"],
        font_mono=active["fonts"]["mono"],
        theme_name=esc(active["name"]),
        initial_theme=args.theme,
        theme_data_json=json.dumps(themes, ensure_ascii=False),
    )
    print(out)


if __name__ == "__main__":
    main()
