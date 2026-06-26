#!/usr/bin/env python3
"""一键发布：Markdown → 上传图片 → 转HTML → 创建草稿"""

import json
import os
import sys

# 确保能导入同目录模块
sys.path.insert(0, os.path.dirname(__file__))

from wechat_mp import upload_image, upload_article_image, create_draft
from md2html import md_to_html, find_local_images, replace_image_urls


def publish(md_path, cover_path, title, author="", digest="", theme="default"):
    """
    一键发布流程
    返回草稿 media_id 或 None
    """
    # 1. 读取markdown
    with open(md_path, encoding="utf-8") as f:
        md_text = f.read()
    md_dir = os.path.dirname(os.path.abspath(md_path))

    # 2. 扫描文内图片并上传
    local_images = find_local_images(md_text)
    url_map = {}
    for img_path in local_images:
        abs_path = img_path if os.path.isabs(img_path) else os.path.join(md_dir, img_path)
        if not os.path.exists(abs_path):
            print(f"⚠️ 图片不存在，跳过: {img_path}", file=sys.stderr)
            continue
        new_url = upload_article_image(abs_path)
        if new_url:
            url_map[img_path] = new_url
    if url_map:
        md_text = replace_image_urls(md_text, url_map)

    # 3. 上传封面图
    print(f"📸 上传封面图: {cover_path}")
    cover = upload_image(cover_path)
    if not cover:
        print("❌ 封面图上传失败", file=sys.stderr)
        return None
    thumb_media_id = cover["media_id"]

    # 4. Markdown → HTML
    html_content = md_to_html(md_text, theme)

    # 5. 创建草稿
    article = {
        "title": title,
        "author": author,
        "content": html_content,
        "thumb_media_id": thumb_media_id,
        "digest": digest or title,
    }
    media_id = create_draft([article])
    if media_id:
        print(f"\n🎉 发布成功！草稿 media_id: {media_id}")
    return media_id


def main():
    if len(sys.argv) < 4:
        print("用法: publish.py <markdown文件> <封面图> <标题> [作者] [摘要] [主题]")
        print("示例: publish.py article.md cover.jpg '我的文章' '作者' '文章摘要' elegant")
        sys.exit(1)
    md_path = sys.argv[1]
    cover_path = sys.argv[2]
    title = sys.argv[3]
    author = sys.argv[4] if len(sys.argv) > 4 else ""
    digest = sys.argv[5] if len(sys.argv) > 5 else ""
    theme = sys.argv[6] if len(sys.argv) > 6 else "default"
    result = publish(md_path, cover_path, title, author, digest, theme)
    if result:
        print(json.dumps({"media_id": result}))
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
