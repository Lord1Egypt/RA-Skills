# -*- coding: utf-8 -*-
"""
log_query.py — 记录查询历史到 log.md（轻量留痕，失败不阻塞）

用法：
    python3 log_query.py --open_id ou_xxx --question "有没有关于力控制的文献"

输出单行 JSON：{"success": true} （即使日志写入失败也返回 success，
因为查询历史不是关键路径，不应影响查询本身。）
"""
from __future__ import annotations

import argparse
import json

import kb_common as kb


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--open_id", required=True)
    parser.add_argument("--question", required=True)
    args = parser.parse_args()

    user = kb.get_user_by_open_id(args.open_id)
    if user is None:
        print(json.dumps({"success": True, "logged": False,
                          "note": "用户未注册，跳过记录"}, ensure_ascii=False))
        return

    question = args.question.strip()
    if len(question) > 100:
        question = question[:100] + "…"
    kb.append_log(user["gitea_username"], "query", question)
    print(json.dumps({"success": True, "logged": True}, ensure_ascii=False))


if __name__ == "__main__":
    main()
