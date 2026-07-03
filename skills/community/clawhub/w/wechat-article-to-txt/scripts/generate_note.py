#!/usr/bin/env python3
"""
generate_note.py - 生成 Obsidian 结构化 Markdown 笔记

用法:
    python3 generate_note.py --title "标题" --author "公众号" --source "URL" \\
        --content "正文" --summary_json '{"summary":"..."}' --tags "tag1,tag2" \\
        --output /path/to/note.md
"""

import argparse
import json
import os
import sys
from datetime import datetime


def parse_summary(summary_json_str):
    """解析总结 JSON 字符串"""
    if not summary_json_str:
        return {
            "summary": "",
            "key_points": [],
            "quotes": [],
            "key_data": [],
            "tags": [],
            "related_topics": []
        }
    try:
        data = json.loads(summary_json_str)
        # 确保字段都是数组
        for field in ["key_points", "quotes", "key_data", "tags", "related_topics"]:
            if field in data and isinstance(data[field], str):
                data[field] = [data[field]]
            elif field not in data:
                data[field] = []
        # 确保 summary 是字符串
        if "summary" not in data:
            data["summary"] = ""
        elif not isinstance(data["summary"], str):
            data["summary"] = str(data["summary"])
        return data
    except json.JSONDecodeError:
        return {"summary": summary_json_str, "key_points": [], "quotes": [],
                "key_data": [], "tags": [], "related_topics": []}


def sanitize_filename(name):
    """清理文件名中的非法字符"""
    illegal = r'\/:*?"<>|'
    for c in illegal:
        name = name.replace(c, '')
    if len(name) > 80:
        name = name[:77] + '...'
    return name.strip()


def generate_note(args, summary):
    """生成 Obsidian Markdown 笔记内容"""
    now = datetime.now()
    date_str = args.date or now.strftime('%Y-%m-%d')
    time_str = now.strftime('%Y-%m-%d %H:%M')

    # 处理标签
    tags = list(summary.get('tags', []))
    if args.tags:
        extra_tags = [t.strip() for t in args.tags.split(',') if t.strip()]
        tags.extend(extra_tags)
    # 去重
    seen = set()
    unique_tags = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            unique_tags.append(t)
    if 'wechat' not in unique_tags:
        unique_tags.insert(0, 'wechat')

    lines = []
    # YAML Frontmatter
    lines.append('---')
    lines.append(f'title: "{args.title}"')
    lines.append(f'source: "{args.source}"')
    lines.append(f'author: "{args.author}"')
    lines.append(f'date: {date_str}')
    lines.append('tags:')
    for tag in unique_tags:
        lines.append(f'  - {tag}')
    lines.append('status: inbox')
    lines.append('---')
    lines.append('')

    # 标题
    lines.append(f'# {args.title}')
    lines.append('')

    # 摘要
    summary_text = summary.get('summary', '')
    if summary_text:
        lines.append(f'> **摘要：** {summary_text}')
        lines.append('')

    # 文章信息
    lines.append('## 📄 文章信息')
    lines.append('')
    lines.append(f'- **来源：** [{args.author}]({args.source})')
    lines.append(f'- **日期：** {date_str}')
    lines.append(f'- **链接：** [原文链接]({args.source})')
    lines.append('')

    # 核心观点
    key_points = summary.get('key_points', [])
    if key_points:
        lines.append('## 📌 核心观点')
        lines.append('')
        for i, point in enumerate(key_points, 1):
            lines.append(f'- **{i}.** {point}')
        lines.append('')

    # 金句
    quotes = summary.get('quotes', [])
    if quotes:
        lines.append('## 💬 金句')
        lines.append('')
        for q in quotes:
            lines.append(f'> *“{q}”*')
            lines.append('')
        if lines[-1] == '':
            lines.pop()
        lines.append('')

    # 关键数据
    key_data = summary.get('key_data', [])
    if key_data:
        lines.append('## 📊 关键数据')
        lines.append('')
        for d in key_data:
            lines.append(f'- {d}')
        lines.append('')

    # 分隔线
    lines.append('---')
    lines.append('')

    # 笔记与思考区
    lines.append('## 📝 笔记与思考')
    lines.append('')
    lines.append('*（在此记录你的思考和延伸阅读）*')
    lines.append('')

    # 正文参考
    if args.content:
        lines.append('## 📖 原文参考')
        lines.append('')
        content = args.content
        if len(content) > 3000:
            content = content[:3000] + '\n\n...（原文过长，已截断，完整内容见原文链接）'
        lines.append(content)
        lines.append('')

    # 相关笔记
    related = summary.get('related_topics', [])
    if related:
        lines.append('## 🔗 相关笔记')
        lines.append('')
        for topic in related:
            link_name = topic.strip()
            if link_name:
                lines.append(f'- [[{link_name}]]')
        lines.append('')

    # 脚注
    lines.append('---')
    lines.append('')
    lines.append(f'*自动收录于 {time_str} | 来源：{args.author}*')
    lines.append('')

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='生成 Obsidian 笔记')
    parser.add_argument('--title', required=True, help='文章标题')
    parser.add_argument('--author', default='', help='公众号名称')
    parser.add_argument('--source', default='', help='原文链接')
    parser.add_argument('--date', default='', help='发布日期 (YYYY-MM-DD)')
    parser.add_argument('--content', default='', help='文章正文')
    parser.add_argument('--summary_json', default='', help='总结 JSON 字符串')
    parser.add_argument('--tags', default='', help='额外标签 (逗号分隔)')
    parser.add_argument('--output', '-o', default='', help='输出文件路径')

    args = parser.parse_args()
    summary = parse_summary(args.summary_json)
    note_content = generate_note(args, summary)

    if args.output:
        output_dir = os.path.dirname(args.output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(note_content)
        print(f'✅ 笔记已保存到: {args.output}')
    else:
        print(note_content)


if __name__ == '__main__':
    main()
