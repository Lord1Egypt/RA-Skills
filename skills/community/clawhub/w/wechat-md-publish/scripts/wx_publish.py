# -*- coding: utf-8 -*-
"""
微信公众号文章发布脚本

通过微信公众平台 API 将 Markdown 文章发布到微信公众号。
默认创建草稿，加 --publish 参数可自动发布。
封面图片由 agent 调用 ImageGen 生成后通过 --thumb-image 传入，或手动指定。
支持 HTML 卡片渲染：将 HTML 模板渲染为图片插入文章。

用法:
  python wx_publish.py --title "标题" --content article.md --thumb-image cover.png
  python wx_publish.py --title "标题" --content article.md --thumb-image cover.png --publish
  python wx_publish.py --upload-thumb cover.jpg
  python wx_publish.py --title "标题" --content article.md --thumb-media-id xxx
  python wx_publish.py --title "标题" --content article.md --author "作者" --digest "摘要"
  python wx_publish.py --html-card card.html --card-width 750 --card-height 1200
  python wx_publish.py --title "标题" --content article.md --html-card card.html --thumb-image cover.png
"""

import argparse
import json
import os
import re
import sys
import time

import markdown
import requests

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".wechat_publish")
TOKEN_CACHE_FILE = os.path.join(CONFIG_DIR, "token_cache.json")

API_BASE = "https://api.weixin.qq.com"

# ---------------------------------------------------------------------------
# Token 管理
# ---------------------------------------------------------------------------


def load_config():
    """从 ~/.wechat_publish/config.json 加载 app_id 和 app_secret"""
    cfg_path = os.path.join(CONFIG_DIR, "config.json")
    if not os.path.exists(cfg_path):
        print(f"配置文件不存在: {cfg_path}")
        print("请先创建配置文件，内容如下:")
        print(json.dumps({"app_id": "你的AppID", "app_secret": "你的AppSecret"}, indent=2, ensure_ascii=False))
        sys.exit(1)
    with open(cfg_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_access_token(force_refresh=False):
    """获取 access_token，带缓存（2 小时有效期）"""
    config = load_config()
    app_id = config["app_id"]
    app_secret = config["app_secret"]

    # 尝试从缓存读取
    if not force_refresh and os.path.exists(TOKEN_CACHE_FILE):
        with open(TOKEN_CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)
        if time.time() - cache.get("time", 0) < 7000:  # 留 200s 余量
            return cache["token"]

    # 请求新 token
    url = f"{API_BASE}/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    resp = requests.get(url, timeout=10)
    data = resp.json()

    if "access_token" not in data:
        print(f"获取 access_token 失败: {data}")
        sys.exit(1)

    token = data["access_token"]

    # 写入缓存
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(TOKEN_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({"time": time.time(), "token": token}, f)

    return token


# ---------------------------------------------------------------------------
# 素材上传
# ---------------------------------------------------------------------------


def upload_thumb(image_path):
    """上传封面图片为永久素材，返回 thumb_media_id"""
    token = get_access_token()
    url = f"{API_BASE}/cgi-bin/material/add_material?access_token={token}&type=image"
    with open(image_path, "rb") as f:
        resp = requests.post(url, files={"media": f}, timeout=30)
    data = resp.json()
    if "media_id" not in data:
        print(f"上传封面失败: {data}")
        sys.exit(1)
    return data["media_id"]


def upload_content_image(image_path):
    """上传图文消息内的图片，返回微信 URL"""
    token = get_access_token()
    url = f"{API_BASE}/cgi-bin/media/uploadimg?access_token={token}"
    with open(image_path, "rb") as f:
        resp = requests.post(url, files={"media": f}, timeout=30)
    data = resp.json()
    if "url" not in data:
        print(f"上传图片失败 ({image_path}): {data}")
        return None
    return data["url"]


# ---------------------------------------------------------------------------
# Markdown 处理
# ---------------------------------------------------------------------------


def md_to_html(md_text):
    """将 Markdown 转为微信公众号兼容的 HTML"""
    html = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "codehilite"],
        extension_configs={"codehilite": {"guess_lang": False}},
    )
    html = apply_wechat_styles(html)
    return html


def apply_wechat_styles(html):
    """为 HTML 标签添加内联样式，适配微信公众号渲染"""

    # 样式定义
    styles = {
        "h1": "margin-top:24px; margin-bottom:16px; font-size:22px; font-weight:bold; color:#1a1a1a; border-bottom:2px solid #3b82f6; padding-bottom:8px;",
        "h2": "margin-top:24px; margin-bottom:16px; font-size:19px; font-weight:bold; color:#1a1a1a; border-bottom:1px solid #e5e7eb; padding-bottom:6px;",
        "h3": "margin-top:20px; margin-bottom:12px; font-size:16px; font-weight:bold; color:#374151;",
        "h4": "margin-top:16px; margin-bottom:8px; font-size:15px; font-weight:bold; color:#4b5563;",
        "p": "margin-top:0; margin-bottom:16px; font-size:15px; line-height:1.8; color:#333;",
        "blockquote": "margin:16px 0; padding:12px 16px; border-left:4px solid #3b82f6; background-color:#f0f5ff; color:#555; font-size:14px; line-height:1.7;",
        "ul": "margin:12px 0; padding-left:24px; font-size:15px; line-height:1.8; color:#333;",
        "ol": "margin:12px 0; padding-left:24px; font-size:15px; line-height:1.8; color:#333;",
        "li": "margin-bottom:6px; font-size:15px; line-height:1.8; color:#333;",
        "table": "margin:16px 0; border-collapse:collapse; width:100%; font-size:14px;",
        "th": "border:1px solid #d1d5db; padding:10px 14px; background-color:#f3f4f6; font-weight:bold; color:#1f2937; text-align:left;",
        "td": "border:1px solid #d1d5db; padding:10px 14px; color:#374151;",
        "code": "background-color:#f1f5f9; color:#e11d48; padding:2px 6px; border-radius:3px; font-size:14px; font-family:'Menlo','Consolas',monospace;",
        "pre": "margin:16px 0; padding:16px; background-color:#1e293b; border-radius:6px; overflow-x:auto; line-height:1.6; white-space:pre-wrap; word-wrap:break-word;",
        "pre_code": "background-color:transparent; color:#e2e8f0; padding:0; font-size:13px; font-family:'Menlo','Consolas',monospace;",
        "hr": "margin:24px 0; border:none; border-top:1px solid #e5e7eb;",
        "img": "max-width:100%; height:auto; margin:12px 0; border-radius:4px;",
        "strong": "color:#1a1a1a; font-weight:bold;",
        "a": "color:#3b82f6; text-decoration:none;",
    }

    def add_style(match):
        """为标签插入 style 属性，保留原有属性"""
        tag_name = match.group(1)
        existing_attrs = match.group(2) or ""
        style = styles.get(tag_name, "")
        if not style:
            return match.group(0)
        # 如果已有 style 属性则跳过
        if "style=" in existing_attrs:
            return match.group(0)
        return f'<{tag_name} style="{style}"{existing_attrs}>'

    # 先处理 pre>code 嵌套
    pre_style = styles["pre"]
    pre_code_style = styles["pre_code"]
    html = re.sub(
        r'(<pre)([^>]*>)((?:(?!<pre).)*?)(<code)([^>]*>)((?:(?!</code>).)*?)(</code>)(</pre>)',
        lambda m: (
            f'<pre style="{pre_style}"{m.group(2)}'
            f'<code style="{pre_code_style}"{m.group(5)}'
            f'{m.group(6)}'
            f'{m.group(7)}{m.group(8)}'
        ),
        html,
        flags=re.DOTALL,
    )

    # 再处理其余标签（跳过已处理的 pre 和 code）
    for tag in ["h1", "h2", "h3", "h4", "p", "blockquote", "ul", "ol", "li",
                "table", "th", "td", "pre", "code", "hr", "img", "strong", "a"]:
        if tag in ("pre", "code"):
            # 只处理不在 pre>code 嵌套中的独立 pre/code
            html = re.sub(
                rf"<{tag}(?![^>]*style=)([^>]*)>",
                lambda m, t=tag: f'<{t} style="{styles[t]}"{m.group(1)}>',
                html,
            )
        else:
            html = re.sub(
                rf"<{tag}(?![^>]*style=)(\s[^>]*)?>",
                lambda m, t=tag: f'<{t} style="{styles[t]}"{m.group(1) or ""}>',
                html,
            )

    return html


def process_local_images(html, base_dir):
    """将 HTML 中引用的本地图片上传到微信，替换为微信 URL"""
    pattern = re.compile(r'<img\s+[^>]*src="([^"]+)"[^>]*>', re.IGNORECASE)

    def replace_match(m):
        img_tag = m.group(0)
        src = m.group(1)

        if src.startswith(("http://", "https://", "data:")):
            return img_tag

        if os.path.isabs(src):
            local_path = src
        else:
            local_path = os.path.join(base_dir, src)

        if not os.path.exists(local_path):
            print(f"  [WARN] 图片不存在，跳过: {local_path}")
            return img_tag

        print(f"  上传图片: {local_path}")
        wx_url = upload_content_image(local_path)
        if wx_url:
            return img_tag.replace(src, wx_url)
        return img_tag

    return pattern.sub(replace_match, html)


# ---------------------------------------------------------------------------
# HTML 卡片渲染
# ---------------------------------------------------------------------------


def html_to_image(html_content, output_path, width=750):
    """将 HTML 渲染为图片，使用 Playwright + 系统 Edge/Chrome 浏览器"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  [WARN] Playwright 未安装，无法渲染 HTML 卡片。请运行:")
        print("    pip install playwright")
        return None

    # 优先使用系统 Edge（Windows 自带），其次 Chrome，最后 Chromium
    channel = None
    for ch in ["msedge", "chrome"]:
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                p.chromium.launch(channel=ch).close()
            channel = ch
            break
        except Exception:
            continue

    launch_kwargs = {}
    if channel:
        launch_kwargs["channel"] = channel

    with sync_playwright() as p:
        browser = p.chromium.launch(**launch_kwargs)
        page = browser.new_page(viewport={"width": width, "height": 800})
        page.set_content(html_content, wait_until="networkidle")
        page.wait_for_timeout(500)
        page.screenshot(path=output_path, full_page=True)
        browser.close()

    print(f"  HTML 卡片已渲染: {output_path}")
    return output_path


def render_html_cards(html_card_paths, base_dir, width=750):
    """渲染多个 HTML 卡片文件为图片，上传到微信，返回可插入文章的 HTML 片段"""
    if not html_card_paths:
        return ""

    card_html_parts = []
    for card_path in html_card_paths:
        if not os.path.isabs(card_path):
            card_path = os.path.join(base_dir, card_path)
        if not os.path.exists(card_path):
            print(f"  [WARN] HTML 卡片文件不存在: {card_path}")
            continue

        with open(card_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # 渲染为图片
        safe_name = re.sub(r'[\\/:*?"<>|]', "", os.path.splitext(os.path.basename(card_path))[0])[:50]
        img_path = os.path.join(CONFIG_DIR, "cards", f"{safe_name}.png")
        os.makedirs(os.path.dirname(img_path), exist_ok=True)

        result = html_to_image(html_content, img_path, width=width)
        if not result:
            continue

        # 上传图片到微信
        print(f"  上传卡片图片: {img_path}")
        wx_url = upload_content_image(img_path)
        if wx_url:
            card_html_parts.append(
                f'<p style="text-align:center;"><img src="{wx_url}" style="max-width:100%; border-radius:6px;" /></p>'
            )

    return "\n".join(card_html_parts)


# ---------------------------------------------------------------------------
# 草稿 & 发布
# ---------------------------------------------------------------------------


def add_draft(token, title, content_html, thumb_media_id, author="", digest=""):
    """新建草稿，返回 media_id"""
    url = f"{API_BASE}/cgi-bin/draft/add?access_token={token}"
    payload = {
        "articles": [
            {
                "title": title,
                "author": author,
                "digest": digest,
                "content": content_html,
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 0,
                "only_fans_can_comment": 0,
            }
        ]
    }
    resp = requests.post(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        timeout=30,
    )
    data = resp.json()
    if "media_id" not in data:
        print(f"创建草稿失败: {data}")
        sys.exit(1)
    return data["media_id"]


def publish_draft(token, media_id):
    """发布草稿，返回 publish_id"""
    url = f"{API_BASE}/cgi-bin/freepublish/submit?access_token={token}"
    payload = {"media_id": media_id}
    resp = requests.post(url, json=payload, timeout=30)
    data = resp.json()
    if data.get("errcode", 0) != 0:
        print(f"发布失败: {data}")
        sys.exit(1)
    return data


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="微信公众号文章发布工具")
    parser.add_argument("--title", help="文章标题")
    parser.add_argument("--content", help="Markdown 文件路径")
    parser.add_argument("--author", default="", help="作者名（可选）")
    parser.add_argument("--digest", required=True, help="文章摘要（由 AI 总结，不超过 120 字节/约 40 字）")
    parser.add_argument("--thumb-media-id", help="封面图片素材 ID（需先通过 --upload-thumb 获取）")
    parser.add_argument("--thumb-image", help="封面图片本地路径，自动上传获取 thumb_media_id")
    parser.add_argument("--upload-thumb", metavar="IMAGE", help="仅上传封面图片，输出 thumb_media_id")
    parser.add_argument("--html-card", nargs="+", metavar="HTML", help="HTML 卡片文件路径（可多个），渲染为图片插入文章")
    parser.add_argument("--card-width", type=int, default=750, help="HTML 卡片渲染宽度（默认 750px）")
    parser.add_argument("--publish", action="store_true", help="创建草稿后自动发布")
    args = parser.parse_args()

    # 仅上传封面模式
    if args.upload_thumb:
        media_id = upload_thumb(args.upload_thumb)
        print(f"thumb_media_id: {media_id}")
        return

    # 发布模式需要 title 和 content
    if not args.title or not args.content:
        parser.error("发布文章需要 --title 和 --content 参数")

    content_path = args.content
    if not os.path.exists(content_path):
        print(f"文件不存在: {content_path}")
        sys.exit(1)

    # 1. 读取 Markdown 并转 HTML
    with open(content_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    print("[1/3] 转换 Markdown -> HTML ...")
    html = md_to_html(md_text)

    # 2. 上传本地图片
    base_dir = os.path.dirname(os.path.abspath(content_path))
    print("[2/4] 处理本地图片 ...")
    html = process_local_images(html, base_dir)

    # 3. 渲染 HTML 卡片（可选）
    card_html = ""
    if args.html_card:
        print("[3/4] 渲染 HTML 卡片 ...")
        card_html = render_html_cards(args.html_card, base_dir, width=args.card_width)
    else:
        print("[3/4] 跳过 HTML 卡片 ...")

    # 将卡片图片插入到文章开头（如果有的话）
    if card_html:
        html = card_html + "\n" + html

    # 4. 获取封面素材 ID
    thumb_media_id = args.thumb_media_id
    if not thumb_media_id and args.thumb_image:
        print("[4/4] 上传封面图片 ...")
        thumb_media_id = upload_thumb(args.thumb_image)
    elif thumb_media_id:
        print("[4/4] 使用指定封面素材 ID ...")

    if not thumb_media_id:
        print("缺少封面，请通过以下方式之一提供:")
        print("  --thumb-image      指定本地封面图片路径（AI 生成的封面也用此参数）")
        print("  --thumb-media-id   指定已上传的封面素材 ID")
        sys.exit(1)

    # 5. 创建草稿
    token = get_access_token()
    digest = args.digest

    print("[5/5] 创建草稿 ...")
    media_id = add_draft(token, args.title, html, thumb_media_id, args.author, digest)
    print(f"草稿创建成功! media_id: {media_id}")

    # 6. 可选：自动发布
    if args.publish:
        print("正在发布 ...")
        result = publish_draft(token, media_id)
        print(f"发布结果: {result}")
    else:
        print("提示: 加 --publish 参数可自动发布，或在公众号后台手动发布此草稿")


if __name__ == "__main__":
    main()
