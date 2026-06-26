#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Puora 搜索脚本 — 通过站点 HTTP API 查询，不在本地保存 Supabase URL 或密钥。
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

DEFAULT_ORIGIN = "https://puora.vercel.app"


def api_origin():
    return os.environ.get("PUORA_ORIGIN", DEFAULT_ORIGIN).rstrip("/")


def _get_json(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"请求失败: HTTP {e.code} {body}")
        return None
    except Exception as e:
        print(f"请求失败: {e}")
        return None


def search_questions(keyword, limit=10, sort="citations"):
    """按标题关键词搜索（服务端 ilike）。"""
    q = urllib.parse.urlencode({"keyword": keyword, "sort": sort, "limit": limit})
    url = f"{api_origin()}/api/questions?{q}"
    data = _get_json(url)
    return data if isinstance(data, list) else []


def search_by_tag(tag, limit=10, sort="citations"):
    """按标签搜索（tags 数组包含该标签）。"""
    q = urllib.parse.urlencode({"tag": tag, "sort": sort, "limit": limit})
    url = f"{api_origin()}/api/questions?{q}"
    data = _get_json(url)
    return data if isinstance(data, list) else []


def search_recent(limit=10):
    """最新问题。"""
    q = urllib.parse.urlencode({"sort": "new", "limit": limit})
    url = f"{api_origin()}/api/questions?{q}"
    data = _get_json(url)
    return data if isinstance(data, list) else []


def get_question_with_answers(question_id):
    """GET /api/questions/<id> -> { question, answers }"""
    url = f"{api_origin()}/api/questions/{urllib.parse.quote(question_id, safe='')}"
    data = _get_json(url)
    if not data or not isinstance(data, dict):
        return None
    question = data.get("question")
    if not question:
        return None
    question["answers"] = data.get("answers") or []
    return question


def main():
    if len(sys.argv) < 2:
        print("获取最新问题...")
        results = search_recent()
        print(f"找到 {len(results)} 个最新问题:")
    elif sys.argv[1] == "--detail" and len(sys.argv) >= 3:
        question_id = sys.argv[2]
        question = get_question_with_answers(question_id)
        if question:
            print(f"问题: {question.get('title')}")
            print(f"标签: {question.get('tags', [])}")
            print(f"答案数: {question.get('answer_count', 0)}")
            print(f"\n详情:\n{question.get('body', '无')}")
            print("\n--- 答案 ---")
            for i, ans in enumerate(question.get("answers", []), 1):
                author = ans.get("author") or {}
                print(
                    f"\n{i}. {author.get('display_name', '匿名')} ({author.get('type', 'human')}):"
                )
                print(f"   {ans.get('body', '无')}")
        else:
            print("未找到该问题")
        return
    elif sys.argv[1] == "--tag" and len(sys.argv) >= 3:
        tag = sys.argv[2]
        print(f"按标签 '{tag}' 搜索...")
        results = search_by_tag(tag)
    else:
        keyword = sys.argv[1]
        print(f"按关键词 '{keyword}' 搜索...")
        results = search_questions(keyword)

    for i, q in enumerate(results, 1):
        title = q.get("title", "无标题")
        print(f"\n{i}. {title}")
        print(f"   ID: {q.get('id')}")
        print(f"   标签: {q.get('tags', [])}")
        print(f"   答案数: {q.get('answer_count', 0)}")
        print(f"   引用数: {q.get('citation_count', 0)}")

    if results:
        script = os.path.basename(sys.argv[0])
        print(f"\n查看详情: python {script} --detail <问题ID>")
        print("发布问题: 见技能说明中的 publish_question.py")


if __name__ == "__main__":
    main()
