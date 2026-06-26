"""
create_draft.py - 将 Markdown 文章转换为微信草稿 JSON

用法:
  python create_draft.py <文章.md路径> <封面media_id> <输出.json路径> [摘要]

依赖: 标准库（re, json）
无需第三方库
"""
import json
import re
import sys


def md_to_wechat_html(md_text):
    html_parts = []
    lines = md_text.strip().split("\n")
    in_code_block = False

    for line in lines:
        line = line.strip()

        if line.startswith("```"):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            html_parts.append(
                f'<p style="background:#f6f8fa;padding:10px;font-family:monospace;">{escaped}</p>'
            )
            continue

        # 分割线
        if line == "---":
            html_parts.append('<hr style="border:none;border-top:1px solid #eee;margin:20px 0;"/>')
            continue

        # h2 标题
        if line.startswith("## "):
            title = escape_html(line[3:])
            html_parts.append(
                f'<h2 style="font-size:20px;font-weight:bold;margin:24px 0 10px 0;border-left:4px solid #5766d9;padding-left:10px;">{title}</h2>'
            )
            continue

        # 主标题（# 开头的第一行，跳过）
        if line.startswith("# "):
            continue

        # 修改记录等辅助段落（以 ## 修改记录 开头则截断）
        if line.startswith("## 修改记录"):
            break

        # 空行
        if not line:
            continue

        # 列表项
        if line.startswith("- "):
            item = process_inline(line[2:])
            html_parts.append(
                f'<p style="margin:6px 0;padding-left:16px;color:#555;">&#8226; {item}</p>'
            )
            continue

        line = process_inline(line)
        html_parts.append(
            f'<p style="margin:12px 0;line-height:1.9;font-size:15px;">{line}</p>'
        )

    return "\n".join(html_parts)


def process_inline(text):
    # 粗体 **text**
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return text


def escape_html(text):
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


def create_draft(md_path, thumb_media_id, output_path, digest=None):
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 提取主标题（第一个 # 后面那行）
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "无标题"

    # 提取第一段作为摘要（如果未提供）
    if digest is None:
        paragraphs = [l.strip() for l in content.split("\n")
                      if l.strip() and not l.strip().startswith("#")
                      and not l.strip().startswith("##") and l.strip() != "---"]
        digest = paragraphs[0][:54] + "..." if paragraphs else ""

    html_content = md_to_wechat_html(content)

    draft = {
        "articles": [
            {
                "title": title,
                "author": "",
                "digest": digest,
                "content": html_content,
                "content_source_url": "",
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 1,
                "only_fans_can_comment": 0
            }
        ]
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(draft, f, ensure_ascii=False, indent=2)

    print(f"标题: {title}")
    print(f"内容长度: {len(html_content)} 字符")
    print(f"草稿已保存到: {output_path}")
    return draft


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法: python create_draft.py <文章.md> <thumb_media_id> <输出.json> [摘要]")
        sys.exit(1)

    md_path = sys.argv[1]
    thumb_media_id = sys.argv[2]
    output_path = sys.argv[3]
    digest = sys.argv[4] if len(sys.argv) > 4 else None

    create_draft(md_path, thumb_media_id, output_path, digest)
