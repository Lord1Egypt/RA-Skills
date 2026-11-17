#!/usr/bin/env python3
"""Build a clickable traceability dialog HTML for an analysis."""

import argparse
import html
import json
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--title", default="可查技能原文")
    parser.add_argument("--sources", default="[]")
    parser.add_argument("--sources-file")
    return parser.parse_args()


def render(sources, title):
    rows = []
    for item in sources:
        book = html.escape(str(item.get("book", "未命名书籍")))
        skill = html.escape(str(item.get("skill", "")))
        source = html.escape(str(item.get("source", "")))
        note = html.escape(str(item.get("note", "")))
        lines = [f"<li><strong>{book}</strong>"]
        if skill:
            lines.append(f'<p>技能：<a href="{skill}" target="_blank" rel="noopener">{skill}</a></p>')
        if source:
            lines.append(f'<p>原文：<a href="{source}" target="_blank" rel="noopener">{source}</a></p>')
        if note:
            lines.append(f"<p class=\"note\">{note}</p>")
        lines.append("</li>")
        rows.append("".join(lines))

    if rows:
        list_html = "<ul>" + "".join(rows) + "</ul>"
    else:
        list_html = "<p>本次未使用书籍技能，未提供原文链路。</p>"

    return f"""<!doctype html>
<html lang="zh">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    body {{
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      background: #f5f6f8;
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
    }}
    button.trigger {{
      padding: 12px 22px;
      border: 0;
      border-radius: 8px;
      background: #2f4f6f;
      color: #fff;
      font-size: 16px;
      cursor: pointer;
    }}
    button.trigger:hover {{ background: #1f3e5c; }}
    dialog {{
      border: 0;
      border-radius: 10px;
      padding: 0;
      width: min(760px, 92vw);
      max-height: 82vh;
      box-shadow: 0 16px 50px rgba(0,0,0,.25);
    }}
    dialog::backdrop {{ background: rgba(15,23,32,.45); }}
    .panel {{ padding: 22px 26px; overflow: auto; }}
    h1 {{ font-size: 20px; margin: 0 0 14px; }}
    ul {{ list-style: none; padding: 0; margin: 0 0 18px; }}
    li {{ border-top: 1px solid #e4e7eb; padding: 14px 0; }}
    li:first-child {{ border-top: 0; }}
    a {{ color: #1f6feb; word-break: break-all; }}
    .note {{ color: #6b7280; font-size: 13px; }}
    .close {{
      padding: 8px 18px;
      border: 0;
      border-radius: 8px;
      background: #eef1f4;
      color: #1f2937;
      cursor: pointer;
    }}
  </style>
</head>
<body>
  <button class="trigger" id="open">查看可查技能原文</button>
  <dialog id="dialog">
    <div class="panel">
      <h1>{html.escape(title)}</h1>
      {list_html}
      <button class="close" id="close">关闭</button>
    </div>
  </dialog>
  <script>
    const openBtn = document.getElementById("open");
    const closeBtn = document.getElementById("close");
    const dialog = document.getElementById("dialog");
    openBtn.addEventListener("click", () => dialog.showModal());
    closeBtn.addEventListener("click", () => dialog.close());
    dialog.addEventListener("click", (event) => {{
      if (event.target === dialog) dialog.close();
    }});
  </script>
</body>
</html>
"""


def main():
    args = parse_args()
    if args.sources_file:
        sources = json.loads(Path(args.sources_file).read_text(encoding="utf-8"))
    else:
        sources = json.loads(args.sources)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(sources, args.title), encoding="utf-8")
    print("output", out)


if __name__ == "__main__":
    main()
