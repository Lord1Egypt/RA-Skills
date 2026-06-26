#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
monitor.py - 监控已发布文章状态并给出发布建议
Usage: python monitor.py [command]
"""

import os
import re
import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
NC = "\033[0m"
BOLD = "\033[1m"

TRACK_FILE = os.path.expanduser("~/.openclaw/workspace/wechat-monitor.json")


def load_tracked():
    if os.path.exists(TRACK_FILE):
        with open(TRACK_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_tracked(data):
    with open(TRACK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def search_sogou(title):
    try:
        query = urllib.parse.quote(title)
        url = "https://weixin.sogou.com/weixin?type=2&query=" + query + "&ie=utf8"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            },
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        title_pat = re.compile(r'<h3[^>]*>(.*?)</h3>', re.DOTALL)
        link_pat = re.compile(r'href="(https://mp\.weixin\.qq\.com/s/[^"]+)"')
        date_pat = re.compile(r'(\d{4}-\d{2}-\d{2})')

        titles = title_pat.findall(html)
        links = link_pat.findall(html)
        dates = date_pat.findall(html)

        results = []
        for t, l, d in zip(titles[:10], links[:10], dates[:10]):
            clean_title = re.sub(r'<[^>]+>', '', t).strip()
            results.append({"title": clean_title, "link": l, "date": d})

        found = any(title[:15] in r["title"] for r in results)
        return {"found": found, "count": len(results), "results": results}

    except Exception as e:
        return {"found": False, "error": str(e), "results": []}


def check_article(title):
    print(BOLD + "\U0001f50d " + title + NC + "\n")
    result = search_sogou(title)

    if result.get("error"):
        print(RED + "X 搜索失败：" + result["error"] + NC)
        return result

    if result["found"]:
        print(GREEN + "[OK] 文章已被搜狗收录！" + NC)
        print("   找到 " + str(result["count"]) + " 条相关结果：\n")
        for i, r in enumerate(result["results"][:5], 1):
            print("   " + str(i) + ". " + BOLD + r["title"][:40] + NC)
            print("      " + r["link"][:60] + "...")
            print("      日期: " + r["date"])
            print()
        return result
    else:
        print(YELLOW + "[等待] 文章尚未被搜狗收录" + NC)
        print("   （新文章通常需要 24-72 小时被索引）")
        print("   尝试用更短关键词搜索...")
        return result


def track_article(title, media_id=""):
    data = load_tracked()
    key = title[:30]
    now = datetime.now().isoformat()

    if key not in data:
        data[key] = {
            "title": title,
            "media_id": media_id,
            "first_checked": now,
            "last_checked": now,
            "status": "pending",
            "check_count": 0,
        }
    else:
        data[key]["last_checked"] = now
        data[key]["check_count"] = data[key].get("check_count", 0) + 1

    save_tracked(data)
    print(GREEN + "[OK] 已添加到追踪列表：" + title[:40] + NC)


def show_status():
    data = load_tracked()
    if not data:
        print(YELLOW + "暂无追踪文章。用 python monitor.py add 添加。" + NC)
        return

    print(BOLD + "\U0001f4ca 公众号文章追踪状态 (" + str(len(data)) + " 篇)" + NC + "\n")
    sep = "=" * 60
    print(sep)

    for i, (key, info) in enumerate(data.items(), 1):
        icons = {"indexed": GREEN + "[OK]", "pending": YELLOW + "[等待]", "failed": RED + "[X]"}

        status_icon = icons.get(info.get("status", "pending"), icons["pending"])
        first = info.get("first_checked", "")[:10]
        last = info.get("last_checked", "")[:10]
        checks = info.get("check_count", 0)

        print(str(i) + ". " + status_icon + " " + info["title"][:35] + NC)
        print("   首次: " + first + " | 最近: " + last + " | 查询: " + str(checks) + "次")
        print()


def generate_recommendations():
    data = load_tracked()
    print(BOLD + "\U0001f4dd 下一篇文章选题建议" + NC + "\n")

    suggestions = [
        {
            "topic": "AI 提问技巧进阶",
            "subtitle": "如何用结构化提问获得 AI 最佳答案",
            "angle": "上篇文章「为什么你问AI总得不到好答案」发出后很多人追问怎么练。",
            "target": "已读那篇但还没行动的读者，做内容承接",
            "titles": [
                "拿着这5个问题去问AI，效果立竿见影",
                "我问了这5个问题，AI的回答质量翻了两倍",
            ],
        },
        {
            "topic": "独立开发者工具链",
            "subtitle": "程序员一人公司的效率神器清单",
            "angle": "luisclaw 自己用 AI 工具跑通 OPC 的实战经验。",
            "target": "程序员、独立开发者群体",
            "titles": [
                "我用了这些工具，一个人顶一个团队",
                "程序员一人公司，这10个工具必备",
            ],
        },
        {
            "topic": "OPC 创业实录",
            "subtitle": "AI 赋能一人公司的真实记录",
            "angle": "luisclaw 的 OPC 创业经历，记录真实踩坑和突破。",
            "target": "有创业想法的技术人",
            "titles": [
                "做 OPC 三个月，我踩了这些坑",
                "从 0 到月入过万：一个程序员的 OPC 之路",
            ],
        },
    ]

    for i, s in enumerate(suggestions, 1):
        print(BOLD + "建议 " + str(i) + "：" + s["topic"] + NC)
        print("   副标题：" + s["subtitle"])
        print("   角度：" + s["angle"])
        print("   目标读者：" + s["target"])
        print("   候选标题：")
        for t in s["titles"]:
            print("     - " + t)
        print()

    # 节奏建议
    print(BOLD + "\U0001f4c5 发布节奏建议" + NC + "\n")
    indexed = len([v for v in data.values() if v.get("status") == "indexed"])
    pending = len([v for v in data.values() if v.get("status") == "pending"])

    if pending > 0:
        print("   有 " + str(pending) + " 篇文章待收录，建议先等收录完成再发新文章")
    print("   已收录 " + str(indexed) + " 篇，保持周更节奏即可\n")

    print(BOLD + "\U0001f527 下一步行动" + NC + "\n")
    print("   1. 去 mp.weixin.qq.com 草稿箱审核并发布今天的文章")
    print("   2. 等待 24-48 小时搜狗收录")
    print("   3. 收录后用 python monitor.py add 添加到追踪")
    print("   4. 定期用 python monitor.py status 查看数据\n")


def show_help():
    msg = """
{0}公众号文章监控工具{1}

命令：
  python monitor.py check "标题"   - 检查文章收录状态
  python monitor.py add "标题" [media_id]  - 添加到追踪列表
  python monitor.py status             - 查看所有追踪文章
  python monitor.py recommend           - 获取下一篇文章建议
  python monitor.py help               - 显示帮助

工作流程：
  1. 发布文章到草稿箱（用 publish_and_verify.py）
  2. 用 monitor.py add "标题" 加入追踪
  3. 定期用 monitor.py status 查看收录状态
  4. 收录后用 monitor.py recommend 获取下一篇文章建议
"""
    print(msg.format(BOLD, NC))


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    cmd = sys.argv[1]

    if cmd == "check":
        if len(sys.argv) < 3:
            print(RED + "请提供文章标题" + NC)
            return
        title = " ".join(sys.argv[2:])
        result = check_article(title)
        if result.get("found"):
            d = load_tracked()
            key = title[:30]
            if key in d:
                d[key]["status"] = "indexed"
                save_tracked(d)
                print(GREEN + "[OK] 追踪状态已更新为「已收录」" + NC)

    elif cmd == "add":
        if len(sys.argv) < 3:
            print(RED + "请提供文章标题" + NC)
            return
        title = " ".join(sys.argv[2:])
        media_id = sys.argv[3] if len(sys.argv) > 3 else ""
        track_article(title, media_id)

    elif cmd == "status":
        show_status()

    elif cmd == "recommend":
        generate_recommendations()

    elif cmd in ("help", "--help", "-h"):
        show_help()

    else:
        print(RED + "未知命令：" + cmd + NC)
        show_help()


if __name__ == "__main__":
    main()
