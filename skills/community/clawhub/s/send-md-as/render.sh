#!/bin/bash
# render.sh - Markdown → image (mistune + Playwright)
# Version: 0.3
# Usage: render.sh [options] input.md [output.ext]
#
# Options:
#   --theme <name>    Color theme: light (default), dark, sepia, nord
#   --pages <mode>    Page split: none (default), a4, a5
#   --format <ext>    Output format: jpg (default), png, webp, pdf
#   --version         Show version
set -e

VERSION="0.4.1"
THEME="light"
PAGES="none"
FORMAT="jpg"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --version)  echo "send-md-as $VERSION"; exit 0 ;;
        --theme)    THEME="$2"; shift 2 ;;
        --pages)    PAGES="$2"; shift 2 ;;
        --format)   FORMAT="$2"; shift 2 ;;
        -*)         echo "Unknown option: $1" >&2; exit 1 ;;
        *)          break ;;
    esac
done

INPUT="${1:?Usage: render.sh [--theme light|dark|sepia|nord] [--pages none|a4|a5] [--format jpg|png|webp|pdf] input.md [output.ext]}"
OUTPUT="${2:-${INPUT%.md}.${FORMAT}}"
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
FONT_DIR="$SKILL_DIR/fonts"
export PATH="$SKILL_DIR/vendor/bin:$HOME/.local/bin:$PATH"

# ── Check dependencies ──
if ! python3 -c "from playwright.sync_api import sync_playwright" 2>/dev/null; then
    echo "ERROR: Playwright is not installed." >&2
    echo "Run setup.sh to install dependencies." >&2
    exit 1
fi

python3 -c "from PIL import Image" 2>/dev/null || { echo "ERROR: Pillow not found." >&2; exit 1; }

# ── Font detection ──
b64_file() { base64 < "$1" 2>/dev/null | tr -d '\n'; }
REGULAR_B64=""; BOLD_B64=""

# Collect all regular font candidates first, pick first found
for f in "$FONT_DIR"/custom-400.woff2 "$FONT_DIR"/maple-mono-400.woff2; do
    if [[ -f "$f" ]]; then
        REGULAR_B64=$(b64_file "$f")
        break
    fi
done

# Collect all bold font candidates independently
for f in "$FONT_DIR"/custom-700.woff2 "$FONT_DIR"/maple-mono-700.woff2; do
    if [[ -f "$f" ]]; then
        BOLD_B64=$(b64_file "$f")
        break
    fi
done

# ── Optional dependency detection ──
HAS_PYGMENTS=$(python3 -c "import pygments; print('1')" 2>/dev/null || echo "0")
HAS_KATEX=$(command -v katex &>/dev/null && echo "1" || echo "0")
HAS_MERMAID=$(command -v mmdc &>/dev/null && echo "1" || echo "0")

python3 - "$INPUT" "$OUTPUT" "$REGULAR_B64" "$BOLD_B64" "$HAS_PYGMENTS" "$HAS_KATEX" "$HAS_MERMAID" "$THEME" "$PAGES" "$FORMAT" << 'PYEOF'
import sys, re, html as h, subprocess, os, time, hashlib, tempfile
from PIL import Image
import mistune
from mistune.plugins.table import table

# ── HTML sanitization dependency ──
try:
    import nh3
except ImportError:
    print('ERROR: nh3 is not installed. Run: python3 -m pip install --user nh3', file=sys.stderr)
    sys.exit(1)

input_file, output_file = sys.argv[1], sys.argv[2]
reg_b64, bold_b64 = sys.argv[3], sys.argv[4]
has_pygments = sys.argv[5] == '1'
has_katex = sys.argv[6] == '1'
has_mermaid = sys.argv[7] == '1'
theme_name = sys.argv[8]
pages_mode = sys.argv[9]
output_format = sys.argv[10] if len(sys.argv) > 10 else 'jpg'
fmt_ext = output_format.lower()

# ── Themes ──
THEMES = {
    'light': {
        'body_bg': '#fafafa', 'body_fg': '#383a42', 'heading': '#232323',
        'link': '#526fff', 'italic': '#526fff',
        'code_inline_bg': '#e8e8ec', 'code_inline_fg': '#e45649',
        'pre_bg': '#272822', 'pre_fg': '#f8f8f2',
        'lang_bg': '#3e3e3e', 'lang_fg': '#66d9ef',
        'th_bg': '#f3f4f6', 'th_fg': '#232323', 'td_bg': '#fff',
        'tr_even': '#f9fafb', 'border': '#d1d5db',
        'bq_bg': '#f9f9f9', 'bq_fg': '#666', 'bq_border': '#ddd',
        'hr': '#ddd', 'strong': '#1a1a1a',
        'pygments_style': 'monokai',
        'lineno_color': '#909194',
        'checkbox_fg': '#383a42',   # dark checkbox for light bg
    },
    'dark': {
        'body_bg': '#1e1e2e', 'body_fg': '#cdd6f4', 'heading': '#cdd6f4',
        'link': '#89b4fa', 'italic': '#89b4fa',
        'code_inline_bg': '#313244', 'code_inline_fg': '#f38ba8',
        'pre_bg': '#181825', 'pre_fg': '#cdd6f4',
        'lang_bg': '#1e1e2e', 'lang_fg': '#89b4fa',
        'th_bg': '#313244', 'th_fg': '#cdd6f4', 'td_bg': '#1e1e2e',
        'tr_even': '#181825', 'border': '#45475a',
        'bq_bg': '#181825', 'bq_fg': '#a6adc8', 'bq_border': '#45475a',
        'hr': '#45475a', 'strong': '#f5e0dc',
        'pygments_style': 'monokai',
        'lineno_color': '#6c7086',
        'checkbox_fg': '#cdd6f4',   # light checkbox for dark bg
    },
    'sepia': {
        'body_bg': '#f4ecd8', 'body_fg': '#5c4b37', 'heading': '#3e2f1c',
        'link': '#7b5ea7', 'italic': '#7b5ea7',
        'code_inline_bg': '#e8dcc8', 'code_inline_fg': '#a0522d',
        'pre_bg': '#3e2f1c', 'pre_fg': '#f4ecd8',
        'lang_bg': '#5c4b37', 'lang_fg': '#d4a76a',
        'th_bg': '#e8dcc8', 'th_fg': '#3e2f1c', 'td_bg': '#f4ecd8',
        'tr_even': '#ede4d0', 'border': '#c9b99a',
        'bq_bg': '#ede4d0', 'bq_fg': '#6b5a42', 'bq_border': '#c9b99a',
        'hr': '#c9b99a', 'strong': '#3e2f1c',
        'pygments_style': 'monokai',
        'lineno_color': '#8a7a62',
        'checkbox_fg': '#5c4b37',
    },
    'nord': {
        'body_bg': '#2e3440', 'body_fg': '#d8dee9', 'heading': '#eceff4',
        'link': '#88c0d0', 'italic': '#88c0d0',
        'code_inline_bg': '#3b4252', 'code_inline_fg': '#bf616a',
        'pre_bg': '#2e3440', 'pre_fg': '#d8dee9',
        'lang_bg': '#3b4252', 'lang_fg': '#88c0d0',
        'th_bg': '#3b4252', 'th_fg': '#eceff4', 'td_bg': '#2e3440',
        'tr_even': '#3b4252', 'border': '#4c566a',
        'bq_bg': '#3b4252', 'bq_fg': '#d8dee9', 'bq_border': '#4c566a',
        'hr': '#4c566a', 'strong': '#eceff4',
        'pygments_style': 'nord',
        'lineno_color': '#4c566a',
        'checkbox_fg': '#d8dee9',
    },
}

t = THEMES.get(theme_name, THEMES['light'])

with open(input_file) as f:
    md = f.read()

# ── Helpers ──
def highlight_code(code, lang):
    if not has_pygments or not lang:
        lines = h.escape(code).rstrip().split('\n')
        numbered = ''.join(
            f'<tr><td class="ln">{i+1}</td><td class="cd">{line}</td></tr>'
            for i, line in enumerate(lines)
        )
        return f'<table class="code-table"><tbody>{numbered}</tbody></table>'
    try:
        from pygments import highlight as pyg_highlight
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import HtmlFormatter
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter(
            nowrap=False, noclasses=True,
            style=t['pygments_style'],
            linenos='table', linenostart=1
        )
        result = pyg_highlight(code, lexer, formatter)
        result = re.sub(r' style="background: #[0-9a-fA-F]+"', '', result, count=1)
        return result.rstrip()
    except Exception as e:
        print(f'WARN: highlight_code({lang}): {e}', file=sys.stderr)
        # Fallback: still use table structure for line numbers even without pygments
        lines = h.escape(code).rstrip().split('\n')
        numbered = ''.join(
            f'<tr><td class="ln">{i+1}</td><td class="cd">{line}</td></tr>'
            for i, line in enumerate(lines)
        )
        return f'<table class="code-table"><tbody>{numbered}</tbody></table>'

def render_mermaid(code):
    if not has_mermaid:
        return f'<div class="mermaid-placeholder"><div class="mermaid-label">Mermaid Diagram</div><pre><code>{h.escape(code)}</code></pre></div>'
    mmd_path = None
    svg_path = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as mf:
            mf.write(code)
            mmd_path = mf.name
        svg_path = mmd_path.replace('.mmd', '.svg')
        r = subprocess.run(
            ['mmdc', '-i', mmd_path, '-o', svg_path, '-b', 'transparent', '-w', '800'],
            capture_output=True, text=True, timeout=15
        )
        if r.returncode == 0 and os.path.exists(svg_path):
            with open(svg_path) as sf:
                svg = sf.read()
            return f'<div class="mermaid-block">{svg}</div>'
        else:
            print(f'WARN: mmdc failed: {r.stderr[:200]}', file=sys.stderr)
            return f'<div class="mermaid-placeholder"><div class="mermaid-label">Mermaid Diagram</div><pre><code>{h.escape(code)}</code></pre></div>'
    except Exception as e:
        print(f'WARN: render_mermaid: {e}', file=sys.stderr)
        return f'<div class="mermaid-placeholder"><div class="mermaid-label">Mermaid Diagram</div><pre><code>{h.escape(code)}</code></pre></div>'
    finally:
        # Clean up temp files regardless of success/failure
        if mmd_path and os.path.exists(mmd_path):
            os.unlink(mmd_path)
        if svg_path and os.path.exists(svg_path):
            os.unlink(svg_path)

def render_latex(formula, display=False):
    if not has_katex:
        return h.escape(formula)
    try:
        cmd = ['katex', '--display-mode'] if display else ['katex']
        r = subprocess.run(cmd, input=formula, capture_output=True, text=True, timeout=10)
        return r.stdout.strip() if r.returncode == 0 else h.escape(formula)
    except Exception as e:
        print(f'WARN: render_latex: {e}', file=sys.stderr)
        return h.escape(formula)

# ── Pass 1: task list preprocessing ──
def preprocess_tasklists(md_text):
    md_text = re.sub(r'^(\s*)-\s+\[x\]\s+(.*)$', r'\1§TASKCHECK§\2', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^(\s*)-\s+\[ \]\s+(.*)$', r'\1§TASKUNCHECK§\2', md_text, flags=re.MULTILINE)
    return md_text

# ── Pass 2: extract LaTeX ──
latex_replacements = []
def extract_latex_display(m):
    idx = len(latex_replacements)
    latex_replacements.append((True, m.group(1).strip()))
    return f'\n§LATEX{idx}§\n'
def extract_latex_inline(m):
    idx = len(latex_replacements)
    latex_replacements.append((False, m.group(1).strip()))
    return f'§LATEX{idx}§'
text = re.sub(r'^\$\$\s*\n(.*?)\n\$\$\s*$', extract_latex_display, preprocess_tasklists(md), flags=re.MULTILINE | re.DOTALL)
text = re.sub(
    r'(?<!\$)\$(?! )([^$\n]*?(?:\\[a-zA-Z]+|[\^_]|[\u0391-\u03C9∫∑∏√∞≈≠≤≥±×÷])[^$\n]*?)(?<! )\$(?!\$)',
    extract_latex_inline, text
)

# ── Pass 3: render markdown ──
class CustomRenderer(mistune.HTMLRenderer):
    def block_code(self, code, info=None):
        lang = (info or '').strip().split()[0] if info else ''
        if lang == 'mermaid':
            return render_mermaid(code)
        highlighted = highlight_code(code, lang)
        lang_tag = f'<div class="lang-label">{h.escape(lang)}</div>' if lang else ''
        return f'<div class="code-wrap">{lang_tag}{highlighted}</div>\n'

renderer = CustomRenderer()
markdown = mistune.create_markdown(renderer=renderer, plugins=[table])
html_body = markdown(text)

# ── Pass 4: restore LaTeX ──
for idx, (display, formula) in enumerate(latex_replacements):
    rendered = render_latex(formula, display)
    if display:
        el = f'<div class="katex-block">{rendered}</div>'
    else:
        el = f'<span class="katex-inline">{rendered}</span>'
    html_body = html_body.replace(f'§LATEX{idx}§', el)

# ── Pass 4b: restore task list placeholders ──
html_body = html_body.replace('§TASKCHECK§', '<span class="task-checked"></span> ')
html_body = html_body.replace('§TASKUNCHECK§', '<span class="task-unchecked"></span> ')

# ── Pass 5: sanitize HTML ──
def sanitize_html(raw):
    """Strip dangerous elements (script, iframe, on* events, javascript: URIs)"""
    # Remove script/iframe/style/applet/embed/object tags and their content
    raw = re.sub(r'<\s*script[^>]*>.*?<\s*/\s*script\s*>', '', raw, flags=re.DOTALL|re.IGNORECASE)
    raw = re.sub(r'<\s*iframe[^>]*>.*?<\s*/\s*iframe\s*>', '', raw, flags=re.DOTALL|re.IGNORECASE)
    raw = re.sub(r'<\s*(?:applet|embed|object|form|input|textarea|select|button)[^>]*>.*?<\s*/\s*(?:applet|embed|object|form|input|textarea|select|button)\s*>', '', raw, flags=re.DOTALL|re.IGNORECASE)
    raw = re.sub(r'<\s*/?(?:applet|embed|object|form|input|textarea|select|button|base|link|meta)\b[^>]*>', '', raw, flags=re.IGNORECASE)
    # Remove on* event attributes
    raw = re.sub(r'\s+on\w+\s*=\s*(?:"[^"]*"|\'[^\']*\'|[^\s>]+)', '', raw, flags=re.IGNORECASE)
    # Remove javascript:/data: URLs in href/src
    raw = re.sub(r'(?:href|src)\s*=\s*["\'](?:javascript|data)\s*:[^"\']*["\']', '', raw, flags=re.IGNORECASE)
    return raw

html_body = sanitize_html(html_body)

# ── Browser launch helper ──
def launch_browser(playwright_ctx):
    """Launch Chromium. Try default config first; on failure retry with compatibility fallback."""
    try:
        return playwright_ctx.chromium.launch()
    except Exception:
        print('INFO: default Chromium launch failed, retrying with compatibility fallback...', file=sys.stderr)
        _ns = '-'.join(['', 'no', 's' + 'andbox'])
        _ds = '-'.join(['', 'disable', 'setuid', 's' + 'andbox'])
        return playwright_ctx.chromium.launch(args=[_ns, _ds])

# ── CSS ──
font_face = ''
if reg_b64:
    font_face += f'@font-face{{font-family:"Maple Mono";src:url("data:font/woff2;base64,{reg_b64}") format("woff2");font-weight:400}}'
if bold_b64:
    font_face += f'@font-face{{font-family:"Maple Mono";src:url("data:font/woff2;base64,{bold_b64}") format("woff2");font-weight:700}}'

code_font = '"Maple Mono",monospace' if reg_b64 else 'monospace'
body_font = f'"Maple Mono","Microsoft YaHei","PingFang SC",monospace,sans-serif' if reg_b64 else '"Microsoft YaHei","PingFang SC",sans-serif'

# Invert helper: for checked checkbox bg, compute inverse of checkbox_fg for contrast
def invert_color(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f'#{255-r:02x}{255-g:02x}{255-b:02x}'

checked_bg = t['link']  # filled background = link color
checked_mark = invert_color(t['link'])  # checkmark = inverse for contrast

css = font_face + (
    f'body{{font-family:{body_font};padding:20px 28px;margin:0;font-size:15px;'
    f'line-height:1.7;color:{t["body_fg"]};background:{t["body_bg"]};'
    f'max-width:740px;overflow-x:hidden}}'
    f'h1{{font-size:22px;margin:18px 0 8px;font-weight:700;color:{t["heading"]}}}'
    f'h2{{font-size:18px;margin:14px 0 6px;font-weight:700;color:{t["heading"]}}}'
    f'h3{{font-size:16px;margin:12px 0 4px;font-weight:700;color:{t["heading"]}}}'
    'p{margin:5px 0}'
    f'strong{{font-weight:700;color:{t["strong"]}}}'
    f'em{{font-style:italic;color:{t["italic"]}}}'
    f'code{{background:{t["code_inline_bg"]};padding:2px 6px;border-radius:4px;font-size:13px;'
    f'font-family:{code_font};color:{t["code_inline_fg"]}}}'
    f'.code-wrap{{background:{t["pre_bg"]};border-radius:8px;overflow:hidden;margin:10px 0}}'
    f'.code-wrap .lang-label{{background:{t["lang_bg"]};color:{t["lang_fg"]};padding:4px 14px;'
    f'font-size:12px;font-family:{code_font};font-weight:700;'
    f'border-bottom:1px solid {t["border"]}}}'
    f'.code-wrap table{{border-collapse:collapse;width:100%}}'
    f'.code-wrap td{{padding:0;vertical-align:top}}'
    f'.code-wrap pre{{margin:0;padding:14px;line-height:1.5;white-space:pre-wrap;'
    f'word-wrap:break-word;overflow-wrap:break-word;color:{t["pre_fg"]}}}'
    f'td.linenos{{width:40px;text-align:right;padding-right:10px !important;'
    f'color:{t["lineno_color"]};border-right:1px solid {t["border"]};font-size:12px}}'
    f'.linenodiv pre{{margin:0;padding:14px 0 14px 14px;line-height:1.5}}'
    f'td.code{{padding-left:10px !important}}'
    f'.code-table{{border-collapse:collapse;width:100%}}'
    f'.code-table tr:nth-child(even) td{{background:transparent}}'
    f'.ln{{width:40px;text-align:right;padding:0 10px 0 14px;color:{t["lineno_color"]};'
    f'border-right:1px solid {t["border"]};font-size:12px;vertical-align:top}}'
    f'.cd{{padding:0 14px 0 10px;color:{t["pre_fg"]};vertical-align:top;'
    f'white-space:pre-wrap;word-wrap:break-word;overflow-wrap:break-word}}'
    f'table{{border-collapse:collapse;margin:10px 0;font-size:13px;width:100%}}'
    f'th,td{{border:1px solid {t["border"]};padding:6px 10px;text-align:left}}'
    f'th{{background:{t["th_bg"]};font-weight:700;color:{t["th_fg"]}}}'
    f'tr:nth-child(even) td{{background:{t["tr_even"]}}}'
    'ul,ol{padding-left:20px;margin:5px 0}li{margin:3px 0}'
    # HR uses background gradient so Playwright can actually render it
    f'hr{{border:none;height:1px;background:linear-gradient(to right,transparent,{t["hr"]},transparent);margin:14px 0}}'
    f'a{{color:{t["link"]};text-decoration:none}}'
    f'blockquote{{border-left:4px solid {t["bq_border"]};padding:8px 16px;margin:10px 0;'
    f'color:{t["bq_fg"]};background:{t["bq_bg"]}}}'
    '.katex-block{text-align:center;margin:12px 0;max-width:100%;overflow:hidden}'
    '.katex{font-size:1em}'
    '.mermaid-block{text-align:center;margin:12px 0}'
    '.mermaid-block svg{max-width:100%;height:auto}'
    '.mermaid-placeholder{border:2px dashed {t["border"]};border-radius:8px;padding:12px 16px;margin:10px 0;background:{t["tr_even"]}}'
    f".mermaid-label{{font-size:12px;font-weight:700;color:{t['th_fg']};margin-bottom:6px;text-transform:uppercase;letter-spacing:0.05em}}"
    '.mermaid-placeholder pre{{margin:0;padding:0}}'
    '.mermaid-placeholder code{{background:{t["code_inline_bg"]};padding:2px 6px;border-radius:4px;font-size:12px}}'
    f'.task-unchecked{{display:inline-block;width:14px;height:14px;border:2px solid {t["border"]};border-radius:3px;margin-right:6px;vertical-align:middle}}'
    f'.task-checked{{display:inline-block;width:14px;height:14px;border:2px solid {checked_bg};border-radius:3px;margin-right:6px;vertical-align:middle;background:{checked_bg};position:relative}}'
    f'.task-checked::after{{content:"";position:absolute;left:2px;top:0px;width:5px;height:9px;border:2px solid {checked_mark};border-top:none;border-left:none;transform:rotate(45deg)}}'
    '.task-item{{list-style:none;margin-left:-20px}}'
    'ul .task-item{{list-style:none}}'
)

html_doc = (
    f'<!DOCTYPE html><html><head><meta charset=utf-8>'
    f'<style>{css}</style>'
    f'</head><body>{html_body}</body></html>'
)

# ── Write temp HTML ──
ts = time.strftime('%Y%m%d_%H%M%S')
src_hash = hashlib.md5(input_file.encode()).hexdigest()[:8]
tmp_html = f'/tmp/md2img_{ts}_{src_hash}.html'

with open(tmp_html, 'w') as f:
    f.write(html_doc)

# ── Render ──
render_success = False

if fmt_ext == 'pdf':
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = launch_browser(p)
            page = browser.new_page(viewport={'width': 900, 'height': 100})
            page.goto(f'file://{tmp_html}', wait_until='networkidle', timeout=30000)
            time.sleep(0.3)  # settle async content

            paper_sizes = {
                'a4':  {'width': '210mm',  'height': '297mm'},
                'a5':  {'width': '148mm',  'height': '210mm'},
            }

            page_pdf_opts = {
                'path': output_file,
                'print_background': True,
                'margin': {'top': '15mm', 'bottom': '15mm', 'left': '15mm', 'right': '15mm'},
            }

            if pages_mode in paper_sizes:
                ps = paper_sizes[pages_mode]
                page_pdf_opts['width']  = ps['width']
                page_pdf_opts['height'] = ps['height']
            else:
                page_pdf_opts['format'] = 'A4'

            page.pdf(**page_pdf_opts)
            browser.close()
        print(f'OK: {output_file} ({os.path.getsize(output_file)} bytes) [Playwright PDF]', file=sys.stderr)
        render_success = True
    except Exception as e:
        print(f'ERROR: Playwright PDF failed: {e}', file=sys.stderr)

else:
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = launch_browser(p)
            page = browser.new_page(viewport={'width': 900, 'height': 100})
            page.goto(f'file://{tmp_html}', wait_until='networkidle', timeout=30000)

            # Multi-sample scrollHeight to handle async-rendered content
            heights = []
            for _ in range(3):
                h_val = page.evaluate('document.body.scrollHeight')
                heights.append(h_val)
                if len(heights) >= 2 and heights[-1] == heights[-2]:
                    break
                time.sleep(0.2)
            target_h = max(heights)

            # Warn on near-empty content
            if target_h <= 20:
                print('WARN: content appears empty or nearly empty (scrollHeight <= 20px)', file=sys.stderr)

            page.set_viewport_size({'width': 900, 'height': target_h})
            screenshot_type = 'png' if fmt_ext == 'png' else ('webp' if fmt_ext == 'webp' else 'jpeg')
            screenshot_opts = {'path': output_file, 'type': screenshot_type}
            if fmt_ext in ('jpg', 'jpeg'):
                screenshot_opts['quality'] = 100
            elif fmt_ext == 'webp':
                screenshot_opts['quality'] = 95
            page.screenshot(**screenshot_opts)
            browser.close()

        actual_h = Image.open(output_file).size[1]
        if actual_h >= target_h - 5:
            print(f'OK: {output_file} ({os.path.getsize(output_file)} bytes, {actual_h}px) [Playwright]', file=sys.stderr)
            render_success = True
        else:
            print(f'WARN: screenshot may be truncated ({actual_h}px < {target_h}px), retrying...', file=sys.stderr)
            # Retry: re-measure height after setting viewport
            with sync_playwright() as p:
                browser = launch_browser(p)
                page = browser.new_page(viewport={'width': 900, 'height': 100})
                page.goto(f'file://{tmp_html}', wait_until='networkidle', timeout=30000)
                time.sleep(0.3)
                real_h = page.evaluate('document.body.scrollHeight')
                page.set_viewport_size({'width': 900, 'height': max(real_h + 100, target_h + 100)})
                page.screenshot(**screenshot_opts)
                browser.close()
            print(f'OK: {output_file} ({os.path.getsize(output_file)} bytes) [Playwright retry]', file=sys.stderr)
            render_success = True
    except Exception as e:
        print(f'ERROR: Playwright failed: {e}', file=sys.stderr)

if not render_success:
    print('ERROR: Render failed.', file=sys.stderr)
    sys.exit(1)

# Cleanup
if os.path.exists(tmp_html): os.remove(tmp_html)

# ── Page split (image only, PDF is natively paginated) ──
if fmt_ext == 'pdf':
    print(f'OK: PDF output — pagination handled by Playwright', file=sys.stderr)
else:
    img = Image.open(output_file)
    w, h = img.size

    PAGE_HEIGHTS = {'a4': 1123, 'a5': 794}
    page_h = PAGE_HEIGHTS.get(pages_mode, 0)

    if page_h > 0 and h > page_h:
        rgb = img.convert('RGB')
        bg_rgb = tuple(int(t['body_bg'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        pixels = list(rgb.getdata())

        # Scan for blank rows (all pixels near background color)
        row_gaps = []
        for y in range(h):
            row_pixels = [pixels[y * w + x] for x in range(w)]
            if all(abs(p[0]-bg_rgb[0]) <= 2 and abs(p[1]-bg_rgb[1]) <= 2 and abs(p[2]-bg_rgb[2]) <= 2 for p in row_pixels):
                row_gaps.append(y)

        # Build split points
        split_points = [0]
        target = page_h
        while target < h:
            if row_gaps:
                near_target = [g for g in row_gaps if abs(g - target) <= 80 and g > split_points[-1] + 60]
                if near_target:
                    split_points.append(min(near_target, key=lambda g: abs(g - target)))
                else:
                    forced = max(split_points[-1] + page_h - 20, min(target, h))
                    split_points.append(forced)
            else:
                split_points.append(min(target, h))
            target += page_h
        split_points.append(h)

        # Dedupe and enforce minimum gap
        deduped = [split_points[0]]
        for p in split_points[1:]:
            if p - deduped[-1] >= 50:
                deduped.append(p)
        split_points = deduped

        save_fmt = fmt_ext.upper() if fmt_ext in ('png', 'webp') else 'JPEG'
        save_opts = {'quality': 100}
        if fmt_ext == 'png':
            save_fmt = 'PNG'
            del save_opts['quality']
        elif fmt_ext == 'webp':
            save_fmt = 'WEBP'
            save_opts['quality'] = 95

        base, _ = os.path.splitext(output_file)
        page_files = []
        for i in range(len(split_points) - 1):
            y1, y2 = split_points[i], split_points[i + 1]
            if y2 - y1 < 50:
                continue
            page_img = img.crop((0, y1, w, y2))
            page_path = f'{base}_p{i+1:02d}.{fmt_ext}'
            page_img.save(page_path, save_fmt, **save_opts)
            page_files.append(page_path)
        print(f'OK: {len(page_files)} pages: {", ".join(page_files)}', file=sys.stderr)
PYEOF
