#!/usr/bin/env python3
"""
公众号文章生成与排版脚本 — 输出标准格式，支持配图建议

用法:
  python3 article_builder.py --input draft.md         # 从草稿生成成品
  python3 article_builder.py --preview                 # 生成预览HTML
  python3 article_builder.py --stats draft.md          # 统计文章数据
"""

import argparse
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path


def count_chinese_chars(text: str) -> int:
    """统计中文字数"""
    return len(re.findall(r'[\u4e00-\u9fa5]', text))


def count_english_words(text: str) -> int:
    """统计英文单词数"""
    words = re.findall(r'[a-zA-Z]+', text)
    return len(words)


def estimate_reading_time(text: str) -> int:
    """估算阅读时长（分钟）"""
    zh_chars = count_chinese_chars(text)
    en_words = count_english_words(text)
    # 中文阅读速度约300字/分钟，英文约150词/分钟
    zh_minutes = zh_chars / 300
    en_minutes = en_words / 150
    total = zh_minutes + en_minutes
    return max(1, round(total))


def article_stats(markdown_text: str) -> dict:
    """分析文章统计信息"""
    stats = {
        "total_chars": len(markdown_text),
        "chinese_chars": count_chinese_chars(markdown_text),
        "english_words": count_english_words(markdown_text),
        "paragraphs": len([p for p in markdown_text.split("\n\n") if p.strip()]),
        "estimated_read_time": estimate_reading_time(markdown_text),
    }

    # 标题统计
    h2_titles = re.findall(r'^##\s+(.*)', markdown_text, re.MULTILINE)
    h3_titles = re.findall(r'^###\s+(.*)', markdown_text, re.MULTILINE)
    stats["h2_count"] = len(h2_titles)
    stats["h3_count"] = len(h3_titles)

    # 句子数量（粗略）
    sentences = re.split(r'[。！？.!?]', markdown_text)
    stats["sentences"] = len([s for s in sentences if len(s.strip()) > 5])

    # 平均段落长度
    paras = [p for p in markdown_text.split("\n\n") if p.strip()]
    if paras:
        stats["avg_para_length"] = round(len(markdown_text) / len(paras), 1)

    return stats


def generate_html_preview(markdown_text: str, title: str = "", author: str = "") -> str:
    """生成手机端预览HTML"""
    stats = article_stats(markdown_text)

    # 简单Markdown转HTML
    html_content = ""
    lines = markdown_text.split("\n")
    in_list = False

    for line in lines:
        stripped = line.strip()

        # 标题
        if stripped.startswith("## "):
            if in_list:
                html_content += "</ul>\n"
                in_list = False
            html_content += f'<h3>{stripped[3:]}</h3>\n'
        elif stripped.startswith("### "):
            if in_list:
                html_content += "</ul>\n"
                in_list = False
            html_content += f'<h4>{stripped[4:]}</h4>\n'
        # 列表
        elif stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                html_content += "<ul>\n"
                in_list = True
            html_content += f'<li>{stripped[2:]}</li>\n'
        # 数字列表
        elif re.match(r'^\d+\.\s', stripped):
            if not in_list:
                html_content += "<ol>\n"
                in_list = True
            html_content += f'<li>{re.sub(r"^\d+\.\s", "", stripped)}</li>\n'
        # 引用
        elif stripped.startswith(">"):
            if in_list:
                html_content += "</ul>\n"
                in_list = False
            html_content += f'<blockquote>{stripped[1:].strip()}</blockquote>\n'
        # 图片
        elif stripped.startswith("!["):
            alt_match = re.search(r'!\[(.*?)\]', stripped)
            src_match = re.search(r'\((.*?)\)', stripped)
            alt = alt_match.group(1) if alt_match else ""
            src = src_match.group(1) if src_match else ""
            html_content += f'<figure><img src="{src}" alt="{alt}" style="max-width:100%;border-radius:8px;"><figcaption style="text-align:center;font-size:13px;color:#999;margin-top:6px;">{alt}</figcaption></figure>\n'
        # 分割线
        elif stripped == "---":
            if in_list:
                html_content += "</ul>\n"
                in_list = False
            html_content += "<hr>\n"
        # 空行
        elif not stripped:
            if in_list:
                html_content += "</ul>\n"
                in_list = False
        # 正文
        else:
            if in_list:
                html_content += "</ul>\n"
                in_list = False
            # 内联格式化
            formatted = line
            formatted = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted)
            formatted = re.sub(r'\*(.*?)\*', r'<em>\1</em>', formatted)
            # 空行或单句加空行
            if formatted.strip():
                html_content += f'<p>{formatted}</p>\n'

    if in_list:
        html_content += "</ul>\n"

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<title>文章预览 - {title}</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    font-family: -apple-system, "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif;
    color: #333;
    background: #FAFBFC;
    padding: 20px 16px 60px;
    -webkit-font-smoothing: antialiased;
  }}
  .article-header {{ margin-bottom: 28px; }}
  .article-title {{
    font-size: 22px; font-weight: 700; line-height: 1.4;
    color: #1a1a1a; margin-bottom: 12px;
  }}
  .article-meta {{
    font-size: 13px; color: #999;
    display: flex; gap: 16px; flex-wrap: wrap;
  }}
  .article-meta span {{ display: flex; align-items: center; gap: 4px; }}
  .cover-image {{
    width: 100%; border-radius: 12px; margin-bottom: 28px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    height: 200px; display: flex; align-items: center; justify-content: center;
    color: white; font-size: 18px; font-weight: 600;
  }}
  .article-body {{ line-height: 1.8; font-size: 16px; }}
  .article-body h3 {{
    font-size: 18px; font-weight: 700; color: #1a1a1a;
    margin: 32px 0 12px; padding-left: 14px;
    border-left: 4px solid #4E79A7;
  }}
  .article-body h4 {{
    font-size: 16px; font-weight: 600; color: #555;
    margin: 24px 0 10px;
  }}
  .article-body p {{ margin-bottom: 16px; text-align: justify; letter-spacing: 0.5px; }}
  .article-body strong {{ color: #333; }}
  .article-body blockquote {{
    margin: 16px 0; padding: 14px 18px; background: #f0f4f8;
    border-left: 4px solid #4E79A7; border-radius: 0 8px 8px 0;
    color: #555; font-size: 15px;
  }}
  .article-body ul, .article-body ol {{ margin: 12px 0 16px 20px; }}
  .article-body li {{ margin-bottom: 8px; }}
  .article-body figure {{ margin: 20px 0; }}
  .article-body hr {{ border: none; height: 1px; background: #eee; margin: 24px 0; }}
  .stats-card {{
    background: white; border-radius: 12px; padding: 16px 20px;
    margin: 32px 0; border: 1px solid #e8ecf0;
    display: grid; grid-template-columns: repeat(4,1fr); gap: 12px;
  }}
  .stats-item {{ text-align: center; }}
  .stats-value {{ font-size: 20px; font-weight: 700; color: #4E79A7; }}
  .stats-label {{ font-size: 12px; color: #999; margin-top: 4px; }}
  @media (max-width:480px) {{
    .stats-card {{ grid-template-columns: repeat(2,1fr); }}
  }}
</style>
</head>
<body>
<div class="article-header">
  <div class="article-title">{title or "文章标题"}</div>
  <div class="article-meta">
    <span>📝 {author or "公众号"}</span>
    <span>📅 {datetime.now().strftime("%Y-%m-%d")}</span>
    <span>⏱ 阅读约 {stats["estimated_read_time"]} 分钟</span>
    <span>📖 {stats["chinese_chars"]} 字</span>
  </div>
</div>
<div class="stats-card">
  <div class="stats-item"><div class="stats-value">{stats["chinese_chars"]}</div><div class="stats-label">中文字数</div></div>
  <div class="stats-item"><div class="stats-value">{stats["estimated_read_time"]} min</div><div class="stats-label">阅读时长</div></div>
  <div class="stats-item"><div class="stats-value">{stats["paragraphs"]}</div><div class="stats-label">段落</div></div>
  <div class="stats-item"><div class="stats-value">{stats["average_sentence_length"] if stats.get("average_sentence_length") else "-"}</div><div class="stats-label">句长</div></div>
</div>
<div class="cover-image">📷 封面图占位<br><span style="font-size:13px;opacity:0.8;">{title or "封面标题"}</span></div>
<div class="article-body">
{html_content}
</div>
</body>
</html>'''
    return html


def process_draft(input_file: str, output_dir: str = "workspace/wechat_output"):
    """处理草稿文件，生成统计和预览"""
    in_path = Path(input_file)
    if not in_path.exists():
        print(f"❌ 文件不存在: {input_file}")
        return

    text = in_path.read_text(encoding="utf-8")
    stats = article_stats(text)

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 提取标题
    title_match = re.search(r'^#\s+(.*)', text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else in_path.stem

    # 生成预览
    basename = in_path.stem
    html = generate_html_preview(text, title)
    html_path = out_dir / f"{basename}_preview.html"
    html_path.write_text(html, encoding="utf-8")

    # 保存统计
    stats_path = out_dir / f"{basename}_stats.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(f"""
📊 文章分析报告
{'=' * 40}
  标题: {title}
  字数: {stats['chinese_chars']} 字（含英文共计 {stats['total_chars']} 字符）
  段落: {stats['paragraphs']} 段
  章节: {stats['h2_count']} 个大标题 + {stats['h3_count']} 个小标题
  阅读时长: 约 {stats['estimated_read_time']} 分钟

  📄 预览文件: {html_path}
  📊 统计数据: {stats_path}
""")

    # 给出优化建议
    suggestions = []
    if stats['chinese_chars'] < 800:
        suggestions.append("⚠️ 文章偏短（< 800字），建议增加内容深度或案例")
    elif stats['chinese_chars'] > 5000:
        suggestions.append("💡 文章较长（> 5000字），建议拆分为系列文章或增加小标题分段")

    avg_para = stats.get('avg_para_length', 0)
    if avg_para > 200:
        suggestions.append("💡 段落偏长（均值 > 200字符），建议缩短段落，单段不超过手机一屏")

    if stats['h2_count'] == 0 and stats['h3_count'] == 0:
        suggestions.append("💡 没有使用任何标题，建议增加H2/H3分级标题提升可读性")

    if suggestions:
        print(f"\n📝 优化建议:")
        for s in suggestions:
            print(f"  {s}")

    return stats


def main():
    parser = argparse.ArgumentParser(description="公众号文章生成与排版工具")
    parser.add_argument("--input", help="输入Markdown草稿文件")
    parser.add_argument("--preview", action="store_true", help="从输入文件生成预览HTML")
    parser.add_argument("--stats", help="分析指定文章文件")
    parser.add_argument("--output", default="workspace/wechat_output", help="输出目录")

    args = parser.parse_args()

    if args.input or args.preview:
        input_file = args.input or "draft.md"
        process_draft(input_file, args.output)
    elif args.stats:
        stats = article_stats(Path(args.stats).read_text(encoding="utf-8"))
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        print("公众号文章排版工具")
        print("=" * 40)
        print("用法:")
        print("  python3 article_builder.py --input article.md")
        print("  python3 article_builder.py --preview article.md")


if __name__ == "__main__":
    main()
