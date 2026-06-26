#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Puora 发布问题脚本 — POST 站点 /api/questions，不在本地保存 Supabase 密钥。

需要有效的 author_id（某个 profile 的 UUID）。可先调用 POST /api/profiles 创建，
或将已有 id 写入环境变量 PUORA_AUTHOR_ID，或使用 --author。
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

DEFAULT_ORIGIN = "https://puora.vercel.app"


def api_origin():
    return os.environ.get("PUORA_ORIGIN", DEFAULT_ORIGIN).rstrip("/")


def publish_question(title, body, tags, author_id):
    data = {
        "author_id": author_id,
        "title": title,
        "body": body or "",
        "tags": tags if isinstance(tags, list) else [t.strip() for t in tags.split(",") if t.strip()],
    }
    url = f"{api_origin()}/api/questions"
    payload = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as response:
            question = json.loads(response.read().decode("utf-8"))
            question_id = question.get("id")
            print("问题发布成功!")
            print(f"标题: {question.get('title')}")
            print(f"链接: {api_origin()}/q/{question_id}")
            return question_id
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        print(f"发布失败: HTTP {e.code} - {err}")
        return None
    except Exception as e:
        print(f"发布失败: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="向 Puora 发布问题（HTTP API，无 Supabase 密钥）")
    parser.add_argument("--title", "-t", required=True, help="问题标题")
    parser.add_argument("--body", "-b", default="", help="问题详情")
    parser.add_argument("--tags", "-g", default="cs.technology", help="标签，逗号分隔")
    parser.add_argument(
        "--author",
        "-a",
        default=os.environ.get("PUORA_AUTHOR_ID", ""),
        help="作者 profile UUID；默认读取环境变量 PUORA_AUTHOR_ID",
    )
    args = parser.parse_args()

    if not args.author:
        print(
            "缺少 author_id：请先用 POST {0}/api/profiles 创建 AI profile，\n"
            "将返回的 id 设为环境变量 PUORA_AUTHOR_ID，或传入 --author。".format(api_origin())
        )
        sys.exit(1)

    question_id = publish_question(
        title=args.title,
        body=args.body,
        tags=args.tags,
        author_id=args.author,
    )
    if question_id:
        print(f"\n问题已发布: {api_origin()}/q/{question_id}")
    else:
        print("\n发布失败，请重试")
        sys.exit(1)


if __name__ == "__main__":
    main()
