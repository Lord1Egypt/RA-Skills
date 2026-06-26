import argparse
import json
import os

THEME_TOKEN_KEYS = [
    "text",
    "heading",
    "accent",
    "muted",
    "surface",
    "border",
    "quoteSurface",
    "codeSurface",
    "codeText",
    "tableHeader",
    "tableBorder",
]

DEFAULT_STYLES = {
    "article": "max-width: 677px; margin: 0 auto; padding: 28px 18px 34px; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; font-size: 16px; line-height: 1.8; letter-spacing: 0; word-break: break-word; overflow-wrap: anywhere;",
    "hero": "margin: 0 0 24px; padding: 28px 18px 18px; border-bottom: 1px solid;",
    "eyebrow": "margin: 0 0 10px; font-size: 12px; line-height: 1.5; letter-spacing: 0; font-family: Menlo, Consolas, monospace;",
    "moduleLabel": "margin: 0 0 10px; font-size: 12px; line-height: 1.5; letter-spacing: 0; font-family: Menlo, Consolas, monospace;",
    "h1": "margin: 0 0 14px; font-size: 24px; line-height: 1.25; font-weight: 760; letter-spacing: 0;",
    "dek": "margin: 12px 0 0; font-size: 17px; line-height: 1.8; letter-spacing: 0;",
    "p": "margin: 0 0 14px; font-size: 16px; line-height: 1.8; letter-spacing: 0; word-break: break-word; overflow-wrap: anywhere;",
    "section": "margin: 30px 0 0;",
    "h2": "margin: 0 0 14px; font-size: 20px; line-height: 1.35; font-weight: 720; letter-spacing: 0;",
    "h3": "margin: 24px 0 10px; font-size: 16px; line-height: 1.45; font-weight: 700; letter-spacing: 0;",
    "quote": "margin: 20px 0; padding: 16px; border: 1px solid; border-radius: 8px;",
    "quoteText": "margin: 0; font-size: 18px; line-height: 1.75; font-family: 'Songti SC', STSong, SimSun, serif;",
    "figure": "margin: 22px 0;",
    "image": "display: block; width: 100%; height: auto; border: 1px solid; border-radius: 8px;",
    "figcaption": "margin: 8px 0 0; font-size: 13px; line-height: 1.6; text-align: center;",
    "callout": "margin: 20px 0; padding: 16px; border: 1px solid; border-radius: 8px;",
    "calloutTitle": "margin: 0 0 10px; font-size: 12px; line-height: 1.5; letter-spacing: 0; font-family: Menlo, Consolas, monospace; font-weight: 700;",
    "ul": "margin: 12px 0 16px; padding-left: 1.2em;",
    "ol": "margin: 12px 0 16px; padding-left: 1.2em;",
    "li": "margin: 0 0 8px; font-size: 16px; line-height: 1.8;",
    "summary": "margin: 24px 0 0; padding: 16px; border: 1px solid; border-radius: 8px;",
    "summaryTitle": "margin: 0 0 10px; font-size: 12px; line-height: 1.5; letter-spacing: 0; font-family: Menlo, Consolas, monospace; font-weight: 700;",
    "summaryText": "margin: 0 0 10px;",
    "table": "width: 100%; border-collapse: collapse; margin: 18px 0; table-layout: fixed; word-break: break-word; overflow-wrap: anywhere; font-size: 14px; line-height: 1.65;",
    "th": "padding: 12px 8px; text-align: left; border: 1px solid; font-weight: 700; word-break: break-word; overflow-wrap: anywhere;",
    "td": "padding: 12px 8px; border: 1px solid; vertical-align: top; word-break: break-word; overflow-wrap: anywhere;",
    "code": "padding: 2px 6px; border-radius: 5px; font-family: Menlo, Consolas, monospace; font-size: 14px; line-height: 1.6; word-break: break-word; overflow-wrap: anywhere;",
    "pre": "margin: 18px 0; padding: 14px; border-radius: 8px; overflow-x: auto; white-space: pre-wrap; word-break: break-word; font-family: Menlo, Consolas, monospace; font-size: 13px; line-height: 1.65;",
    "strong": "font-weight: 700;",
    "a": "text-decoration: none; border-bottom: 1px solid;",
    "hr": "margin: 30px 0; border: 0; border-top: 1px solid;",
}


def strip_code(value):
    value = value.strip()
    if value.startswith("`") and value.endswith("`"):
        return value[1:-1]
    return value


def load_default_themes(base_dir):
    presets_path = os.path.join(base_dir, "references", "theme-presets.md")
    with open(presets_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    themes = {}
    in_table = False
    for line in lines:
        if line.startswith("## Fixed Color Tokens"):
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if not in_table or not line.startswith("| `"):
            continue

        columns = [strip_code(part) for part in line.strip().strip("|").split("|")]
        if len(columns) < 13:
            continue

        preset_id = columns[0].strip()
        token_values = [value.strip() for value in columns[2:13]]
        themes[preset_id] = dict(zip(THEME_TOKEN_KEYS, token_values))

    if not themes:
        raise ValueError(f"No theme presets found in {presets_path}")
    return themes


def read_json_or_default(path, default_factory):
    if path:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return json.dumps(default_factory(), ensure_ascii=False, separators=(",", ":"))


def generate_preview(title, content_path, themes_path=None, styles_path=None, output_path=None, ask_open=False):
    if output_path is None:
        raise ValueError("output_path is required")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_parts_dir = os.path.join(base_dir, 'references', 'template-parts')
    
    layout_path = os.path.join(template_parts_dir, 'layout.html')
    css_path = os.path.join(template_parts_dir, 'style.css')
    js_path = os.path.join(template_parts_dir, 'script.js')
    
    with open(layout_path, 'r', encoding='utf-8') as f:
        layout = f.read()
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()
    with open(js_path, 'r', encoding='utf-8') as f:
        js = f.read()
        
    with open(content_path, 'r', encoding='utf-8') as f:
        content = f.read()
    themes = read_json_or_default(themes_path, lambda: load_default_themes(base_dir))
    styles = read_json_or_default(styles_path, lambda: DEFAULT_STYLES)
        
    html = layout.replace('{{ARTICLE_TITLE}}', title)
    html = html.replace('{{CSS_CONTENT}}', css)
    html = html.replace('{{JS_CONTENT}}', js)
    html = html.replace('{{LLM_CONTENT_PLACEHOLDER}}', content)
    html = html.replace('{{THEME_PRESETS_JSON}}', themes)
    html = html.replace('{{THEME_STYLES_JSON}}', styles)
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"Successfully generated preview at {output_path}")
    
    if ask_open:
        try:
            choice = input("是否通过浏览器打开该 HTML 预览？[y/N]: ").strip().lower()
            if choice in ('y', 'yes'):
                import webbrowser
                webbrowser.open(os.path.abspath(output_path))
                print("已在浏览器中打开预览。")
            else:
                print("已取消打开浏览器。")
        except KeyboardInterrupt:
            print("\n操作已取消。")
        except Exception as e:
            print(f"打开浏览器失败: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate WeChat HTML Preview')
    parser.add_argument('--title', default='文章预览', help='Title of the article')
    parser.add_argument('--content', required=True, help='Path to content HTML file')
    parser.add_argument('--themes', help='Optional path to themes JSON file. Defaults to built-in presets.')
    parser.add_argument('--styles', help='Optional path to styles JSON file. Defaults to built-in component styles.')
    parser.add_argument('--output', required=True, help='Path to output HTML file')
    parser.add_argument('--open', action='store_true', help='Prompt the user to open the output HTML in a browser')
    
    args = parser.parse_args()
    
    generate_preview(
        title=args.title,
        content_path=args.content,
        themes_path=args.themes,
        styles_path=args.styles,
        output_path=args.output,
        ask_open=args.open
    )
