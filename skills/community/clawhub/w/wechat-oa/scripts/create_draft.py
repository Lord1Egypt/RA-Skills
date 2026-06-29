# -*- coding: utf-8 -*-
"""
创建微信公众号草稿文章
支持：标题、作者、摘要、正文HTML、封面图
"""
import json
import os
import sys
import urllib.request
import urllib.error
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from get_token import get_access_token

DRAFT_API = "https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"


def wrap_content(content):
    """将正文内容包装为微信图文消息所需的HTML格式"""
    if not content.strip().startswith("<"):
        paragraphs = content.strip().split("\n")
        html_parts = []
        for p in paragraphs:
            p = p.strip()
            if not p:
                continue
            html_parts.append(f"<p>{p}</p>")
        body = "\n".join(html_parts)
    else:
        body = content

    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'></head><body>"
        + body
        + "</body></html>"
    )


def create_draft(title, content, author=None, digest=None, thumb_media_id=None):
    token = get_access_token()
    url = DRAFT_API.format(token=token)

    wrapped = wrap_content(content)

    article = {
        "title": title,
        "content": wrapped,
        "thumb_media_id": thumb_media_id or "",
        "content_source_url": "",
        "need_open_comment": 0,
        "only_fans_can_comment": 0,
    }
    if author:
        article["author"] = author
    if digest:
        article["digest"] = digest

    payload = json.dumps({"articles": [article]}, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8") if e.fp else str(e)
        print(f"HTTP错误 {e.code}: {err}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"网络错误: {e}", file=sys.stderr)
        sys.exit(1)

    if "media_id" in result:
        print(f"草稿创建成功！")
        print(f"标题：{title}")
        print(f"media_id：{result['media_id']}")
        return result["media_id"]
    else:
        print(f"创建失败: {result}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="创建微信公众号草稿")
    parser.add_argument("--title", required=True, help="文章标题")
    parser.add_argument("--content", required=True, help="正文内容（HTML或纯文本）")
    parser.add_argument("--author", default=None, help="作者名")
    parser.add_argument("--digest", default=None, help="文章摘要")
    parser.add_argument("--thumb-image", default=None, help="封面图路径")
    args = parser.parse_args()

    thumb_media_id = None
    if args.thumb_image:
        from upload_thumb import upload_thumb
        thumb_media_id = upload_thumb(args.thumb_image)

    create_draft(
        title=args.title,
        content=args.content,
        author=args.author,
        digest=args.digest,
        thumb_media_id=thumb_media_id,
    )


if __name__ == "__main__":
    main()
