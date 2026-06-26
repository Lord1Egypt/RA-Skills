#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号草稿上传脚本
功能：将 Markdown 文件转换为微信公众号格式，上传封面图并创建草稿
用法：python upload_draft.py --appid <APPID> --secret <SECRET> --md <文章路径> [--cover <封面图路径>] [--author <作者名>] [--digest <摘要>]
"""

import argparse
import json
import os
import re
import sys
import tempfile
import urllib.request
import urllib.parse
import urllib.error


# ─────────────────────────────────────────────
# 1. 工具函数
# ─────────────────────────────────────────────

def http_get(url):
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_post_json(url, payload):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_post_multipart(url, fields, file_field, file_path, mime_type):
    """multipart/form-data 上传文件（纯标准库实现）"""
    boundary = "----WorkBuddyBoundary7MA4YWxkTrZu0gW"
    body_parts = []

    for name, value in fields.items():
        body_parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}'.encode())

    with open(file_path, "rb") as f:
        file_data = f.read()
    filename = os.path.basename(file_path)
    body_parts.append(
        f'--{boundary}\r\nContent-Disposition: form-data; name="{file_field}"; filename="{filename}"\r\nContent-Type: {mime_type}\r\n\r\n'.encode()
        + file_data
    )
    body_parts.append(f"--{boundary}--".encode())

    body = b"\r\n".join(body_parts)
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ─────────────────────────────────────────────
# 2. 获取 Access Token
# ─────────────────────────────────────────────

def get_access_token(appid, secret):
    url = (
        f"https://api.weixin.qq.com/cgi-bin/token"
        f"?grant_type=client_credential&appid={appid}&secret={secret}"
    )
    result = http_get(url)
    if "access_token" not in result:
        raise RuntimeError(f"获取 access_token 失败：{result}")
    print(f"[OK] 获取 access_token 成功（有效期 {result.get('expires_in', '?')} 秒）")
    return result["access_token"]


# ─────────────────────────────────────────────
# 3. Markdown → 微信公众号 HTML
# ─────────────────────────────────────────────

def md_to_wechat_html(md_text):
    """简易 Markdown 转 HTML，适配微信公众号内联样式"""

    lines = md_text.split("\n")
    html_lines = []
    in_blockquote = False

    # 行内样式转换（bold / italic / inline-code / link）
    def inline(text):
        # 粗体
        text = re.sub(r"\*\*(.+?)\*\*", r'<strong style="font-weight:bold;">\1</strong>', text)
        text = re.sub(r"__(.+?)__", r'<strong style="font-weight:bold;">\1</strong>', text)
        # 斜体
        text = re.sub(r"\*(.+?)\*", r'<em>\1</em>', text)
        # 行内代码
        text = re.sub(r"`(.+?)`", r'<code style="background:#f4f4f4;padding:2px 4px;border-radius:3px;font-size:0.9em;">\1</code>', text)
        # 链接
        text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)
        # 水平线
        text = re.sub(r"^-{3,}$", r'<hr style="border:none;border-top:1px solid #eee;margin:24px 0;"/>', text)
        return text

    i = 0
    while i < len(lines):
        line = lines[i]

        # 标题
        h_match = re.match(r"^(#{1,6})\s+(.*)", line)
        if h_match:
            level = len(h_match.group(1))
            content = inline(h_match.group(2))
            sizes = {1: "1.8em", 2: "1.5em", 3: "1.3em", 4: "1.1em", 5: "1em", 6: "0.9em"}
            weights = {1: "bold", 2: "bold", 3: "bold", 4: "bold", 5: "normal", 6: "normal"}
            style = f'font-size:{sizes[level]};font-weight:{weights[level]};margin:24px 0 12px;color:#333;'
            if level == 2:
                style += "border-left:4px solid #07C160;padding-left:10px;"
            html_lines.append(f'<h{level} style="{style}">{content}</h{level}>')
            i += 1
            continue

        # 无序列表
        if re.match(r"^[-*+]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^[-*+]\s+", lines[i]):
                items.append(f'<li style="margin:6px 0;">{inline(lines[i][2:].strip())}</li>')
                i += 1
            html_lines.append('<ul style="padding-left:1.5em;margin:12px 0;">' + "".join(items) + "</ul>")
            continue

        # 有序列表
        if re.match(r"^\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i]):
                items.append(f'<li style="margin:6px 0;">{inline(re.sub(r"^\d+\.\s+", "", lines[i]))}</li>')
                i += 1
            html_lines.append('<ol style="padding-left:1.5em;margin:12px 0;">' + "".join(items) + "</ol>")
            continue

        # 引用块
        if line.startswith("> "):
            content = inline(line[2:])
            html_lines.append(
                f'<blockquote style="border-left:4px solid #07C160;margin:12px 0;padding:10px 16px;'
                f'background:#f9f9f9;color:#555;">{content}</blockquote>'
            )
            i += 1
            continue

        # 分割线
        if re.match(r"^-{3,}$", line.strip()) or re.match(r"^\*{3,}$", line.strip()):
            html_lines.append('<hr style="border:none;border-top:1px solid #eee;margin:24px 0;"/>')
            i += 1
            continue

        # 空行
        if line.strip() == "":
            html_lines.append("")
            i += 1
            continue

        # 普通段落
        html_lines.append(f'<p style="line-height:1.8;margin:12px 0;color:#333;">{inline(line)}</p>')
        i += 1

    body = "\n".join(html_lines)
    return f"""<section style="font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;font-size:16px;max-width:677px;margin:0 auto;padding:0 16px;color:#333;">
{body}
</section>"""


# ─────────────────────────────────────────────
# 4. 生成默认封面图（纯色 + 文字，无第三方依赖）
# ─────────────────────────────────────────────

def generate_default_cover(title, output_path):
    """尝试用 Pillow 生成封面；若不可用则下载一张免费占位图"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new("RGB", (900, 500), color=(7, 193, 96))
        draw = ImageDraw.Draw(img)
        # 尝试加载中文字体，失败则用默认字体
        font = None
        for fp in [
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simhei.ttf",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        ]:
            if os.path.exists(fp):
                try:
                    font = ImageFont.truetype(fp, 48)
                    break
                except Exception:
                    pass
        if font is None:
            font = ImageFont.load_default()

        # 文字换行
        max_chars = 16
        words = list(title)
        wrapped = []
        current = ""
        for w in words:
            current += w
            if len(current) >= max_chars:
                wrapped.append(current)
                current = ""
        if current:
            wrapped.append(current)

        total_h = len(wrapped) * 60
        y = (500 - total_h) // 2
        for line in wrapped:
            bbox = draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
            draw.text(((900 - w) // 2, y), line, fill="white", font=font)
            y += 60

        img.save(output_path, "JPEG")
        print(f"[OK] 使用 Pillow 生成封面：{output_path}")
        return output_path

    except ImportError:
        pass

    # Pillow 不可用，下载占位图
    placeholder_url = "https://placehold.co/900x500/07C160/FFFFFF/png?text=AI+Smart+Care"
    try:
        print("[..] Pillow 未安装，正在下载占位封面图...")
        urllib.request.urlretrieve(placeholder_url, output_path)
        print(f"[OK] 占位封面已下载：{output_path}")
        return output_path
    except Exception as e:
        print(f"[!!] 封面图下载失败（{e}），将不使用封面")
        return None


# ─────────────────────────────────────────────
# 5. 上传封面图到素材库
# ─────────────────────────────────────────────

def upload_cover_image(access_token, image_path):
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image"
    ext = os.path.splitext(image_path)[1].lower()
    mime_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".gif": "image/gif"}
    mime = mime_map.get(ext, "image/jpeg")

    result = http_post_multipart(url, {}, "media", image_path, mime)
    if "media_id" not in result:
        raise RuntimeError(f"上传封面图失败：{result}")
    print(f"[OK] 封面图上传成功，media_id = {result['media_id']}")
    return result["media_id"]


# ─────────────────────────────────────────────
# 6. 创建草稿
# ─────────────────────────────────────────────

def create_draft(access_token, title, content_html, thumb_media_id, author="", digest=""):
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    article = {
        "title": title,
        "author": author,
        "digest": digest,
        "content": content_html,
        "thumb_media_id": thumb_media_id,
        "need_open_comment": 0,
        "only_fans_can_comment": 0,
    }
    payload = {"articles": [article]}
    result = http_post_json(url, payload)
    if "media_id" not in result:
        raise RuntimeError(f"创建草稿失败：{result}")
    print(f"[OK] 草稿创建成功！草稿 media_id = {result['media_id']}")
    return result["media_id"]


# ─────────────────────────────────────────────
# 7. 主流程
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="将 Markdown 文章上传到微信公众号草稿箱")
    parser.add_argument("--appid",  required=True, help="公众号 AppID")
    parser.add_argument("--secret", required=True, help="公众号 AppSecret")
    parser.add_argument("--md",     required=True, help="Markdown 文件路径")
    parser.add_argument("--cover",  default=None,  help="封面图路径（可选，不提供则自动生成）")
    parser.add_argument("--author", default="",    help="文章作者（可选）")
    parser.add_argument("--digest", default="",    help="文章摘要（可选，最多120字）")
    args = parser.parse_args()

    # 读取 Markdown
    if not os.path.isfile(args.md):
        print(f"[ERR] 文件不存在：{args.md}")
        sys.exit(1)

    with open(args.md, "r", encoding="utf-8") as f:
        md_text = f.read()

    # 提取标题（第一个 # 行）
    title_match = re.search(r"^#\s+(.+)", md_text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else os.path.splitext(os.path.basename(args.md))[0]
    print(f"[>>] 文章标题：{title}")

    # 自动生成摘要（取正文前 100 字）
    if not args.digest:
        plain = re.sub(r"[#*`>\[\]!]", "", md_text)
        plain = re.sub(r"\s+", " ", plain).strip()
        args.digest = plain[:100]

    # 获取 access_token
    print("\n[..] 正在获取 access_token...")
    token = get_access_token(args.appid, args.secret)

    # 处理封面图
    cover_path = args.cover
    tmp_cover = None
    if not cover_path:
        tmp_cover = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        tmp_cover.close()
        cover_path = generate_default_cover(title, tmp_cover.name)

    thumb_media_id = None
    if cover_path and os.path.isfile(cover_path):
        print("\n[..] 正在上传封面图...")
        thumb_media_id = upload_cover_image(token, cover_path)
    else:
        print("[!!] 无法获取封面图，草稿将使用默认封面（可能导致接口报错）")

    # 清理临时文件
    if tmp_cover and os.path.exists(tmp_cover.name):
        try:
            os.unlink(tmp_cover.name)
        except Exception:
            pass

    if not thumb_media_id:
        print("[ERR] 缺少封面图 media_id，无法继续创建草稿")
        sys.exit(1)

    # 转换内容
    print("\n[..] 正在转换 Markdown --> 微信公众号 HTML...")
    content_html = md_to_wechat_html(md_text)

    # 创建草稿
    print("\n[..] 正在创建草稿...")
    draft_media_id = create_draft(token, title, content_html, thumb_media_id, args.author, args.digest)

    print(f"\n[DONE] 完成！文章《{title}》已成功上传至草稿箱。")
    print(f"       草稿 media_id：{draft_media_id}")
    print("       请登录微信公众平台 -> 草稿箱查看。")


if __name__ == "__main__":
    main()
