#!/usr/bin/env python3
"""
知乎内容搜索与分析 - zhida-content
搜索话题热度 + 问题分析 + 选题推荐

用法:
  python3 fetch_zhida.py --search "AI副业"
  python3 fetch_zhida.py --hot --limit 10
  python3 fetch_zhida.py --analyze "AI"
  python3 fetch_zhida.py --topic "AI" --limit 20
  python3 fetch_zhida.py --topic "AI" --json
"""

import json
import re
import sys
import ssl
import argparse
import time
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# SSL 配置
_SAFE_SSL_CTX = ssl.create_default_context()

def _urlopen(req, timeout=10):
    try:
        return urlopen(req, timeout=timeout, context=_SAFE_SSL_CTX)
    except URLError as e:
        reason = getattr(e, 'reason', None)
        if isinstance(reason, (ssl.SSLError, ssl.SSLCertVerificationError)):
            return urlopen(req, timeout=timeout, context=ssl.create_default_context())
        raise
    except Exception as e:
        if 'SSL' in str(type(e).__name__) or 'SSL' in str(e):
            return urlopen(req, timeout=timeout, context=ssl.create_default_context())
        raise

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
}


def search_zhihu(keyword, limit=20):
    """搜索知乎问题"""
    url = (
        "https://www.zhihu.com/api/v4/search_v3"
        "?t=general&q={}&correction=1&offset=0&limit={}"
        "&filter_fields=&lc_idx=0&show_all_topics=0"
    ).format(keyword, limit)
    headers = {**HEADERS, "Referer": "https://www.zhihu.com/search"}

    try:
        req = Request(url.format(keyword=keyword), headers=headers)
        with _urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print("  ⚠️ 知乎搜索失败: {}".format(e), file=sys.stderr)
        return []

    results = []
    data_items = data.get("data", [])
    if not isinstance(data_items, list):
        data_items = []

    for item in data_items:
        obj = item.get("object", {}) or item

        # 提取问题信息
        q_type = obj.get("type", "")
        if q_type != "question":
            continue

        qid = obj.get("id", "")
        title = (obj.get("title", "") or "").strip()
        if not title:
            continue

        question_stats = obj.get("question", {}) or obj
        follower_count = int(question_stats.get("follower_count", 0) or obj.get("follower_count", 0))
        answer_count = int(question_stats.get("answer_count", 0) or obj.get("answer_count", 0))
        comment_count = int(question_stats.get("comment_count", 0) or obj.get("comment_count", 0))

        # 浏览量（API不直接返回，从回答数和关注者估算）
        # 估算浏览量：关注者×10 + 回答数×1000 ≈ 最小浏览
        est_views = follower_count * 8 + answer_count * 800

        # 热度评估
        if est_views >= 1000000:
            heat_level = "🔥🔥🔥"
        elif est_views >= 100000:
            heat_level = "🔥🔥"
        elif est_views >= 10000:
            heat_level = "🔥"
        else:
            heat_level = "❄️"

        # 机会评估
        if answer_count == 0:
            opportunity = "🟢 蓝海（无回答）"
        elif answer_count < 10 and follower_count > 100:
            opportunity = "🟢 高机会"
        elif answer_count < 50 and follower_count > 500:
            opportunity = "🟡 中机会"
        elif answer_count > 200:
            opportunity = "🔴 竞争激烈"
        else:
            opportunity = "🟡 中等机会"

        results.append({
            "title": title,
            "qid": qid,
            "url": "https://www.zhihu.com/question/{}".format(qid),
            "follower_count": follower_count,
            "answer_count": answer_count,
            "comment_count": comment_count,
            "est_views": est_views,
            "heat_level": heat_level,
            "opportunity": opportunity,
        })

    return results


def get_hot_list(limit=10):
    """获取知乎热榜"""
    url = "https://api.zhihu.com/topstory/hot-lists/total?limit={}".format(limit)
    try:
        req = Request(url, headers=HEADERS)
        with _urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print("  ⚠️ 知乎热榜失败: {}".format(e), file=sys.stderr)
        return []

    results = []
    for item in data.get("data", []):
        target = item.get("target", {})
        title = (target.get("title", "") or "").strip()
        if not title:
            continue

        detail = item.get("detail_text", "")
        qid = target.get("id", "")
        answer_count = int(target.get("answer_count", 0))
        follower_count = int(target.get("follower_count", 0))

        # 提取热度数值
        heat_num = 0
        try:
            if "万" in detail:
                heat_num = float(re.sub(r"[^\d.]", "", detail)) * 10000
        except (ValueError, AttributeError):
            pass

        if heat_num >= 1000000:
            heat_level = "🔥🔥🔥"
        elif heat_num >= 100000:
            heat_level = "🔥🔥"
        else:
            heat_level = "🔥"

        results.append({
            "title": title,
            "qid": qid,
            "url": "https://www.zhihu.com/question/{}".format(qid),
            "heat": int(heat_num),
            "heat_display": detail,
            "heat_level": heat_level,
            "answer_count": answer_count,
            "follower_count": follower_count,
            "opportunity": "🟡 蹭热度机会" if answer_count < 100 else "🔴 竞争激烈",
        })
    return results


def topic_suggestions(keyword, limit=20):
    """选题推荐（搜索 + 分析）"""
    results = search_zhihu(keyword, limit)
    if not results:
        return []

    # 按机会评分排序
    def score(r):
        s = 0
        # 关注者多 + 回答少 = 机会大
        s += min(r["follower_count"] / 100, 50)
        # 回答少加分
        s += max(0, (50 - r["answer_count"]) * 0.5)
        # 浏览估算加分
        s += min(r["est_views"] / 50000, 30)
        return s

    scored = [(r, score(r)) for r in results]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [r for r, _ in scored]


def print_search_results(results, keyword):
    """打印搜索结果"""
    if not results:
        print("\n⚠️ 未找到「{}」相关问题".format(keyword))
        return

    print("\n" + "=" * 60)
    print("  🔍 知乎搜索结果 | 「{}」| {}个问题".format(keyword, len(results)))
    print("=" * 60)

    # 按机会排序
    scored = []
    def s(r):
        return min(r["follower_count"] / 100, 50) + max(0, (50 - r["answer_count"]) * 0.5)

    sorted_results = sorted(results, key=s, reverse=True)

    print("\n🎯 高价值选题推荐（按机会排序）")
    print("-" * 60)

    for i, r in enumerate(sorted_results[:10], 1):
        title = r["title"][:40]
        followers = _format_num(r["follower_count"])
        answers = r["answer_count"]
        opp = r["opportunity"]
        print("\n  {}. {} {}".format(i, title, r["heat_level"]))
        print("     👥 {}关注 | 💬 {}回答 | {}".format(followers, answers, opp))
        print("     🔗 https://www.zhihu.com/question/{}".format(r["qid"]))

    print("\n" + "-" * 60)
    print("📊 高热话题（按热度排序）")
    print("-" * 60)

    for i, r in enumerate(sorted(results, key=lambda x: x["est_views"], reverse=True)[:10], 1):
        title = r["title"][:40]
        followers = _format_num(r["follower_count"])
        answers = r["answer_count"]
        opp = r["opportunity"]
        print("\n  {}. {} {}".format(i, title, r["heat_level"]))
        print("     👥 {}关注 | 💬 {}回答 | {}".format(followers, answers, opp))

    print("\n" + "=" * 60)
    print("💡 说明：关注多+回答少 = 最佳选题机会")


def print_hot_list(results, keyword=None):
    """打印热榜"""
    if not results:
        print("\n⚠️ 热榜数据获取失败")
        return

    print("\n" + "🔥" * 18)
    keyword_str = " | 「{}」相关".format(keyword) if keyword else ""
    print("  知乎热榜TOP{} {}".format(len(results), keyword_str))
    print("🔥" * 18)

    for i, r in enumerate(results, 1):
        title = r["title"][:38]
        heat = r.get("heat_display", "")
        answers = r["answer_count"]
        opp = r["opportunity"]
        print("\n  {}. {} {}".format(i, title, r["heat_level"]))
        print("     💬 {}回答 | {} | {}".format(answers, heat, opp))
        print("     🔗 https://www.zhihu.com/question/{}".format(r["qid"]))

    # 推荐回答机会
    best_opportunities = [r for r in results if r["answer_count"] < 50][:3]
    if best_opportunities:
        print("\n🎯 高机会回答（回答少+热度高）")
        for r in best_opportunities:
            print("  • {} — {}回答 | 🔥{}".format(
                r["title"][:36], r["answer_count"], r.get("heat_display", "")))


def print_topic_suggestions(results, keyword):
    """打印选题推荐"""
    if not results:
        print("\n⚠️ 未能生成「{}」的选题建议".format(keyword))
        return

    print("\n" + "🎯" * 18)
    print("  选题推荐TOP10 | 「{}」".format(keyword))
    print("🎯" * 18)

    def calc_score(r):
        return min(r["follower_count"] / 100, 50) + max(0, (50 - r["answer_count"]) * 0.5)

    scored = [(r, calc_score(r)) for r in results]
    scored.sort(key=lambda x: x[1], reverse=True)

    for i, (r, sc) in enumerate(scored[:10], 1):
        title = r["title"][:38]
        stars = "⭐" * min(int(sc / 10), 5)
        print("\n  {}. {} {}".format(i, title, r["heat_level"]))
        print("     📊 机会评分: {} {}".format(int(sc), stars))
        print("     👥 {}关注 | 💬 {}回答".format(
            _format_num(r["follower_count"]), r["answer_count"]))
        print("     🏷️ {}".format(r["opportunity"]))
        print("     🔗 https://www.zhihu.com/question/{}".format(r["qid"]))

        # 内容建议
        suggestions = _content_suggestion(r)
        print("     💡 建议: {}".format(suggestions))

    print("\n" + "=" * 60)


def _content_suggestion(r):
    """生成内容方向建议"""
    title = r["title"]
    answers = r["answer_count"]
    title_lower = title.lower()

    # 检测话题类型
    if any(k in title_lower for k in ["怎么", "如何", "什么", "为什么", "是否", "好不好"]):
        base = "回答类（直接给答案+方法论）"
    elif any(k in title_lower for k in ["评价", "怎么看", "觉得", "感受"]):
        base = "观点类（立场鲜明+3个理由）"
    elif any(k in title_lower for k in ["推荐", "分享", "有没有"]):
        base = "清单类（列出具体项）"
    else:
        base = "深度分析类"

    if answers == 0:
        level = "无回答，蓝海，先发优势最大"
    elif answers < 20:
        level = "竞争小，回答质量一般，有机会脱颖而出"
    elif answers < 100:
        level = "竞争适中，需要差异化视角"
    else:
        level = "竞争激烈，需要独特切入点"

    return "{}，{}".format(base, level)


def _format_num(n):
    n = int(n)
    if n >= 100000000:
        return "{:.1f}亿".format(n / 100000000)
    elif n >= 10000:
        return "{:.1f}万".format(n / 10000)
    return str(n)


# ========== 主入口 ==========

def main():
    parser = argparse.ArgumentParser(description="🔍 知乎内容搜索与分析")
    parser.add_argument("--search", "-s",
                        help="搜索关键词")
    parser.add_argument("--hot", action="store_true",
                        help="获取知乎热榜")
    parser.add_argument("--topic", "-t",
                        help="选题推荐（基于关键词）")
    parser.add_argument("--limit", "-n", type=int, default=20,
                        help="搜索结果数量（默认20）")
    parser.add_argument("--json", action="store_true",
                        help="JSON格式输出")
    args = parser.parse_args()

    if args.hot:
        print("📡 正在获取知乎热榜...", file=sys.stderr)
        results = get_hot_list(args.limit)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print_hot_list(results)

    elif args.search:
        print("🔍 搜索「{}」...".format(args.search), file=sys.stderr)
        time.sleep(0.5)  # 礼貌延迟
        results = search_zhihu(args.search, args.limit)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print_search_results(results, args.search)

    elif args.topic:
        print("🎯 选题分析「{}」...".format(args.topic), file=sys.stderr)
        time.sleep(0.5)
        results = topic_suggestions(args.topic, args.limit)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print_topic_suggestions(results, args.topic)

    else:
        # 默认：显示热榜
        print("📡 正在获取知乎热榜（默认）...", file=sys.stderr)
        results = get_hot_list(args.limit)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print_hot_list(results)


if __name__ == "__main__":
    main()
