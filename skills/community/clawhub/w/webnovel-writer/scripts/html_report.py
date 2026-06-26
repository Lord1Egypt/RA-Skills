#!/usr/bin/env python3
"""检测报告生成器 - 将检测结果渲染为可视化 HTML 报告

用法:
    html_report <正文目录> [--output <路径>] [--title <标题>]
"""

import html
import json
import os
import re
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

SCRIPTS_DIR = Path(__file__).parent


def _read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def run_check(script_name: str, args: list) -> str:
    """运行检测脚本，返回stdout"""
    script = SCRIPTS_DIR / f"{script_name}.py"
    if not script.exists():
        return ""
    import subprocess
    result = subprocess.run(
        [sys.executable, str(script)] + args,
        capture_output=True, text=True, timeout=60
    )
    return result.stdout


def list_chapters(directory: str) -> List[Tuple[int, str, str]]:
    chapters = []
    for f in sorted(Path(directory).glob("*.md")):
        m = re.search(r"第(\d+)", f.name)
        if m:
            chapters.append((int(m.group(1)), str(f), f.name))
    return chapters


def generate_html(
    novel_dir: str,
    title: str = "检测报告",
    output: str = None,
) -> str:
    """生成完整的 HTML 检测报告"""
    chapters = list_chapters(novel_dir)
    if not chapters:
        print("❌ 未找到章节文件")
        return ""

    total_chars = 0
    for _, path, _ in chapters:
        total_chars += len(_read(path))

    # 收集各检测脚本结果
    sections = []

    # 1. 一致性检查
    print("  ⏳ 一致性检查...")
    result = run_check("consistency_check", [novel_dir])
    sections.append(("一致性检查", "shield", result))

    # 2. 重复检测
    print("  ⏳ 重复检测...")
    result = run_check("repetition_check", [novel_dir])
    sections.append(("重复检测", "copy", result))

    # 3. 对话标签
    print("  ⏳ 对话标签...")
    result = run_check("dialogue_tag_check", [novel_dir])
    sections.append(("对话标签质量", "message-square", result))

    # 4. 章末钩子
    print("  ⏳ 章末钩子...")
    result = run_check("chapter_hook_check", [novel_dir])
    sections.append(("章末钩子", "anchor", result))

    # 5. 段落检测
    print("  ⏳ 段落检测...")
    result = run_check("paragraph_check", [novel_dir])
    sections.append(("段落长度", "align-left", result))

    # 6. 节奏检测
    print("  ⏳ 节奏检测...")
    result = run_check("rhythm_check", [novel_dir])
    sections.append(("节奏分析", "activity", result))

    # 构建 HTML
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    section_cards = ""
    for i, (name, icon, content) in enumerate(sections):
        safe_content = html.escape(content) if content else "✅ 无问题"
        # 统计问题数
        issue_count = content.count("❌") + content.count("⚠️") + content.count("⚠")
        status_color = "#ef4444" if issue_count > 10 else "#f59e0b" if issue_count > 0 else "#10b981"
        status_text = f"{issue_count} 个问题" if issue_count > 0 else "通过"
        section_cards += f"""
        <div class="card">
            <div class="card-header">
                <span class="icon">📊</span>
                <h2>{html.escape(name)}</h2>
                <span class="badge" style="background:{status_color}">{status_text}</span>
            </div>
            <details>
                <summary>展开详情</summary>
                <pre class="output">{safe_content}</pre>
            </details>
        </div>"""

    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
           background: #0f172a; color: #e2e8f0; padding: 2rem; }}
    .container {{ max-width: 900px; margin: 0 auto; }}
    h1 {{ font-size: 1.8rem; margin-bottom: 0.5rem; }}
    .meta {{ color: #94a3b8; margin-bottom: 2rem; }}
    .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
             gap: 1rem; margin-bottom: 2rem; }}
    .stat {{ background: #1e293b; border-radius: 12px; padding: 1rem; text-align: center; }}
    .stat-value {{ font-size: 1.5rem; font-weight: bold; color: #38bdf8; }}
    .stat-label {{ font-size: 0.85rem; color: #94a3b8; margin-top: 0.25rem; }}
    .card {{ background: #1e293b; border-radius: 12px; margin-bottom: 1rem;
            overflow: hidden; border: 1px solid #334155; }}
    .card-header {{ display: flex; align-items: center; gap: 0.75rem;
                   padding: 1rem 1.25rem; cursor: pointer; }}
    .card-header h2 {{ font-size: 1.1rem; flex: 1; }}
    .icon {{ font-size: 1.2rem; }}
    .badge {{ padding: 0.2rem 0.6rem; border-radius: 999px; font-size: 0.75rem;
              color: white; font-weight: bold; }}
    summary {{ cursor: pointer; padding: 0.75rem 1.25rem; color: #38bdf8;
              border-top: 1px solid #334155; font-size: 0.9rem; }}
    .output {{ padding: 1rem 1.25rem; font-size: 0.8rem; line-height: 1.6;
               overflow-x: auto; white-space: pre-wrap; color: #cbd5e1; max-height: 500px; }}
    .footer {{ text-align: center; color: #475569; margin-top: 2rem; font-size: 0.8rem; }}
</style>
</head>
<body>
<div class="container">
    <h1>📖 {html.escape(title)}</h1>
    <div class="meta">生成时间: {now} | Novel Writer v3.2</div>

    <div class="stats">
        <div class="stat">
            <div class="stat-value">{len(chapters)}</div>
            <div class="stat-label">总章数</div>
        </div>
        <div class="stat">
            <div class="stat-value">{total_chars:,}</div>
            <div class="stat-label">总字数</div>
        </div>
        <div class="stat">
            <div class="stat-value">{total_chars // len(chapters) if chapters else 0:,}</div>
            <div class="stat-label">平均字数/章</div>
        </div>
        <div class="stat">
            <div class="stat-value">{6}</div>
            <div class="stat-label">检测维度</div>
        </div>
    </div>

    {section_cards}

    <div class="footer">
        Generated by <a href="https://github.com/ZYuanJia/novel-writer" style="color:#38bdf8">Novel Writer</a>
    </div>
</div>
</body>
</html>"""

    if output:
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w", encoding="utf-8") as f:
            f.write(full_html)
        print(f"\n✅ 报告已保存: {output}")
    else:
        default_path = str(Path(novel_dir).parent / f"检测报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
        with open(default_path, "w", encoding="utf-8") as f:
            f.write(full_html)
        print(f"\n✅ 报告已保存: {default_path}")

    return full_html


def main():
    if len(sys.argv) < 2:
        print("📖 HTML 检测报告生成器")
        print("用法: html_report <正文目录> [--output <路径>] [--title <标题>]")
        sys.exit(0)

    novel_dir = sys.argv[1]
    output = None
    title = "小说质量检测报告"

    for i, arg in enumerate(sys.argv):
        if arg == "--output" and i + 1 < len(sys.argv):
            output = sys.argv[i + 1]
        if arg == "--title" and i + 1 < len(sys.argv):
            title = sys.argv[i + 1]

    if not Path(novel_dir).is_dir():
        print(f"❌ 目录不存在: {novel_dir}")
        sys.exit(1)

    print(f"🔍 生成检测报告...\n")
    generate_html(novel_dir, title, output)


if __name__ == "__main__":
    main()
