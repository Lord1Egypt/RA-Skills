#!/usr/bin/env python3
"""
播客创作机会报告生成器 — 综合榜单数据 + 订阅追踪 + 小宇宙详情，
生成完整的播客创作机会分析报告

用法:
  python3 scripts/generate_report.py --genre 个人成长
  python3 scripts/generate_report.py --custom-query "AI创业"
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

SCRIPT_DIR = Path(__file__).parent
TRACK_FILE = SCRIPT_DIR / "subscription_data.json"
TRACK_RANKING_FILE = SCRIPT_DIR / "tracking_data.json"
TREND_API_BASE = "https://api.xyzrank.top/v1"

# 内容形式关键词
FORMAT_HINTS = {
    "访谈": 0, "对话": 0, "单口": 0, "圆桌": 0,
    "盘点": 0, "复盘": 0, "故事": 0, "观察": 0,
    "问答": 0, "独白": 0, "对谈": 0,
}

TOPIC_BUCKETS = [
    "AI", "科技", "商业", "创业", "投资", "职场",
    "管理", "社会", "文化", "历史", "女性", "教育",
    "健康", "情感", "喜剧", "幽默", "电影", "音乐",
    "媒体", "国际", "旅行", "体育", "艺术",
]


def run_xyz(query, list_type="hot-podcasts", limit=30):
    args = [
        sys.executable, str(SCRIPT_DIR / "fetch_xyz_rank.py"),
        "--list", list_type,
        "--query", query,
        "--limit", str(limit),
    ]
    result = subprocess.run(args, capture_output=True, text=True)
    try:
        return json.loads(result.stdout).get("items", [])
    except Exception:
        return []


def load_tracked():
    """加载订阅追踪数据"""
    if not TRACK_FILE.exists():
        return {}
    return json.load(open(TRACK_FILE)).get("podcasts", {})


def load_ranked():
    """加载排名追踪数据"""
    if not TRACK_RANKING_FILE.exists():
        return {}
    return json.load(open(TRACK_RANKING_FILE)).get("podcasts", {})


def calc_weekly_growth(history):
    if len(history) < 2:
        return None, None
    first = history[0].get("subscribers", 0)
    last = history[-1].get("subscribers", 0)
    weeks = len(history)
    return last - first, (last - first) / weeks


def fetch_trend_metrics(podcast_id):
    """从 api.xyzrank.top 获取播客历史订阅趋势 /v1/metrics/{id}"""
    try:
        url = f"{TREND_API_BASE}/metrics/{podcast_id}"
        req = Request(url, headers={"User-Agent": "podcast-radar-cn/1.0"})
        with urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        return None


def fetch_trend_stats():
    """从 api.xyzrank.top 获取所有播客最新订阅统计 /v1/stats"""
    try:
        url = f"{TREND_API_BASE}/stats"
        req = Request(url, headers={"User-Agent": "podcast-radar-cn/1.0"})
        with urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except Exception:
        return None


def calc_trend_growth(metrics_data):
    """从历史趋势数据计算增长率"""
    if not metrics_data or "data" not in metrics_data:
        return None, None, None
    data = metrics_data["data"]
    if len(data) < 2:
        return None, None, None
    # 按日期排序（最新的在前）
    sorted_data = sorted(data, key=lambda x: x.get("crawl_date", ""), reverse=True)
    latest = sorted_data[0].get("subscriber_count", 0)
    oldest = sorted_data[-1].get("subscriber_count", 0)
    days = len(sorted_data)
    total_growth = latest - oldest
    daily_avg = total_growth / days if days > 0 else 0
    growth_rate = (total_growth / oldest * 100) if oldest > 0 else 0
    return latest, total_growth, growth_rate


def extract_formats(episodes):
    """统计单集标题中的内容形式"""
    counts = dict(FORMAT_HINTS)
    durations = []
    for ep in episodes:
        title = ep.get("title", "")
        for fmt in FORMAT_HINTS:
            if fmt in title:
                counts[fmt] += 1
        dur = ep.get("durationMinutes") or ep.get("duration")
        if dur:
            durations.append(float(dur))
    return counts, durations


def extract_topic_keywords(episodes):
    """提取标题中的话题关键词"""
    keyword_counts = {k: 0 for k in TOPIC_BUCKETS}
    for ep in episodes:
        title = (ep.get("title") or "").lower()
        for kw in TOPIC_BUCKETS:
            if kw.lower() in title:
                keyword_counts[kw] += 1
    return keyword_counts


def find_top_guests(episodes, limit=10):
    """从标题中提取高频嘉宾/对谈对象"""
    guest_pattern = re.compile(r"(?:对话|对谈|访谈|with)\s*([^｜|:：!！?？]+)")
    guests = []
    for ep in episodes:
        for m in guest_pattern.finditer(ep.get("title", "")):
            name = m.group(1).strip()[:16]
            if name:
                guests.append(name)
    from collections import Counter
    return [g for g, _ in Counter(guests).most_common(limit)]


def print_divider(char="─", width=60):
    print(char * width)


def generate_report(genre_query):
    """主报告生成函数"""
    print(f"\n{'🎙️ '*20}")
    print(f"播客创作机会报告")
    print(f"关键词: {genre_query}")
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print_divider()

    # 1. 数据收集
    hot_podcasts = run_xyz(genre_query, "hot-podcasts", 30)
    new_podcasts = run_xyz(genre_query, "new-podcasts", 20)
    hot_episodes = run_xyz(genre_query, "hot-episodes", 20)
    new_episodes = run_xyz(genre_query, "new-episodes", 20)

    tracked = load_tracked()
    tracked_pids = {v.get("pid") for v in tracked.values()}

    all_episodes = hot_episodes + new_episodes
    all_podcasts = hot_podcasts + new_podcasts

    # 2. 领域概览
    print(f"\n📈 领域概览")
    print_divider()
    print(f"  热门播客进入视线: {len(hot_podcasts)} 档")
    print(f"  新锐播客进入视线: {len(new_podcasts)} 档")
    print(f"  热门单集:         {len(hot_episodes)} 期")
    print(f"  新锐单集:         {len(new_episodes)} 期")

    # 3. 订阅增长分析（来自 batch_track 数据）
    print(f"\n📊 订阅增长分析 (来自订阅追踪数据)")
    print_divider()
    hot_with_growth = []
    for p in hot_podcasts:
        xyz_url = p.get("links", {}).get("xyz", "") if isinstance(p.get("links"), dict) else ""
        pid = xyz_url.split("/")[-1] if xyz_url else ""
        for tname, tinfo in tracked.items():
            if tinfo.get("pid") == pid or tname == p.get("title"):
                history = tinfo.get("history", [])
                if len(history) >= 2:
                    total, weekly = calc_weekly_growth(history)
                    hot_with_growth.append({
                        **p,
                        "track_name": tname,
                        "pid": pid,
                        "total_growth": total,
                        "weekly_growth": weekly,
                        "weeks": len(history),
                        "current_subs": history[-1].get("subscribers", 0),
                    })
                break

    if hot_with_growth:
        hot_with_growth.sort(key=lambda x: x["weekly_growth"] or 0, reverse=True)
        for i, p in enumerate(hot_with_growth[:5], 1):
            wg = p["weekly_growth"] or 0
            tg = p["total_growth"] or 0
            subs = p.get("current_subs", 0)
            bar = "█" * min(int(wg / 300), 18)
            print(f"  {i}. {p['title']}")
            print(f"     订阅量: {subs:>10,}  周均: +{wg:>7,.0f} {bar}")
            print(f"     总增长: +{tg:>9,} ({p['weeks']}周数据)")
    else:
        print(f"  📭 暂无本地订阅追踪数据（需先运行 batch_track.py init）")

    # 3.5 趋势 API 数据（xyzrank 官方趋势）
    print(f"\n📈 趋势 API 数据 (api.xyzrank.top)")
    print_divider()
    trend_data_found = False
    trend_results = []

    for p in hot_podcasts[:10]:  # 只查前10个，避免API请求过多
        xyz_url = p.get("links", {}).get("xyz", "") if isinstance(p.get("links"), dict) else ""
        pid = xyz_url.split("/")[-1] if xyz_url else ""
        if pid and len(pid) == 24:  # 小宇宙PID是24位
            metrics = fetch_trend_metrics(pid)
            if metrics and metrics.get("data"):
                latest, total_growth, growth_rate = calc_trend_growth(metrics)
                if latest:
                    trend_results.append({
                        **p,
                        "pid": pid,
                        "latest_subs": latest,
                        "total_growth": total_growth,
                        "growth_rate": growth_rate,
                        "data_points": len(metrics["data"]),
                    })
                    trend_data_found = True

    if trend_results:
        trend_results.sort(key=lambda x: x["growth_rate"] or 0, reverse=True)
        print(f"  成功获取 {len(trend_results)} 档播客的趋势数据\n")
        for i, p in enumerate(trend_results[:5], 1):
            gr = p["growth_rate"] or 0
            tg = p["total_growth"] or 0
            subs = p["latest_subs"] or 0
            bar = "█" * min(int(abs(gr) / 5), 15)
            arrow = "📈" if gr > 0 else "📉" if gr < 0 else "➡️"
            print(f"  {i}. {p['title']}")
            print(f"     当前订阅: {subs:>10,}  总增长: {tg:>+9,}  ({arrow}{gr:+.1f}%) {bar}")
            print(f"     数据来源: api.xyzrank.top ({p['data_points']}个数据点)")
    else:
        print(f"  📭 暂无趋势 API 数据（可能这些播客未被 xyzrank 收录）")

    # 4. 竞争格局
    print(f"\n⚔️ 竞争格局")
    print_divider()
    plays = [p["avgPlayCount"] for p in hot_podcasts if p.get("avgPlayCount")]
    comments = [p["avgCommentCount"] for p in hot_podcasts if p.get("avgCommentCount")]
    concentration = None

    if plays:
        sorted_plays = sorted(plays, reverse=True)
        top10_plays_list = sorted_plays[:10]
        mid_val = sorted_plays[len(sorted_plays) // 2]
        avg = sum(plays) / len(plays)
        top10_avg = sum(top10_plays_list) / len(top10_plays_list)
        concentration = top10_avg / avg if avg > 0 else 1

        print(f"  头部门槛(前10%): {top10_plays_list[0]:>12,} 播放量")
        print(f"  均播量中位值:   {mid_val:>12,}")
        print(f"  整体平均值:     {avg:>12,.0f}")
        print(f"  头部集中系数:   {concentration:.2f}x  {'🔴 头部高度集中' if concentration > 3 else '🟡 中度集中' if concentration > 2 else '🟢 相对分散'}")
        print(f"  创作者机会:     ", end="")
        if concentration > 3:
            print("空间在细分垂直领域，长尾有利")
        elif concentration > 2:
            print("仍有差异化空间，关注细分人群")
        else:
            print("竞争分散，容易切入")

    if comments and plays:
        avg_c = sum(comments) / len(comments)
        avg_p = sum(plays) / len(plays)
        print(f"  平均评论率:     {avg_c/avg_p*100:.2f}%  {'💬 互动强' if avg_c/avg_p > 0.005 else '🔇 互动弱' if avg_c/avg_p < 0.001 else '💬 互动中'}")

    # 5. 内容模式分析
    print(f"\n🔥 内容模式分析 (基于热门单集)")
    print_divider()
    format_counts, durations = extract_formats(all_episodes)
    active_formats = {k: v for k, v in sorted(format_counts.items(), key=lambda x: x[1], reverse=True) if v > 0}
    if active_formats:
        top_fmt = list(active_formats.items())[0]
        print(f"  最常见形式:     {top_fmt[0]} ({top_fmt[1]}期)")
        print(f"  形式分布:       " + "  ".join(f"{k}:{v}" for k, v in list(active_formats.items())[:5]))

    if durations:
        avg_dur = sum(durations) / len(durations)
        long_pct = sum(1 for d in durations if d > 60) / len(durations) * 100
        print(f"  平均时长:       {avg_dur:.0f}min  {'📊 长内容主导' if avg_dur > 55 else '📰 中短内容主导'}")
        print(f"  长单集(>60min): {long_pct:.0f}%")

    # 话题关键词
    topic_counts = extract_topic_keywords(all_episodes)
    hot_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:6]
    hot_topics = [(k, v) for k, v in hot_topics if v > 0]
    if hot_topics:
        print(f"  高频话题:       " + "  ".join(f"{k}({v})" for k, v in hot_topics))

    # 高频嘉宾
    top_guests = find_top_guests(all_episodes)
    if top_guests:
        print(f"  高频对谈嘉宾:   " + "  ".join(top_guests[:5]))

    # 6. 推荐对标案例
    print(f"\n📚 推荐对标案例 (Top 5)")
    print_divider()
    sorted_hot = sorted(hot_podcasts, key=lambda x: x.get("avgPlayCount", 0), reverse=True)
    for i, p in enumerate(sorted_hot[:5], 1):
        xyz_url = p.get("links", {}).get("xyz", "") if isinstance(p.get("links"), dict) else ""
        pid = xyz_url.split("/")[-1] if xyz_url else ""
        is_tracked = pid in tracked_pids or p.get("title") in tracked
        mark = "✅已追踪" if is_tracked else "➕可追踪"
        plays_i = p.get("avgPlayCount", 0)
        comments_i = p.get("avgCommentCount", 0)
        genre_i = p.get("genre", "—")
        tracks = p.get("trackCount", "—")
        dur_i = p.get("avgDurationMinutes", 0)
        dur_str = f"{dur_i:.0f}min" if dur_i else "—"
        print(f"  {i}. {p['title']}")
        print(f"     均播:{plays_i:>10,}  评论:{comments_i:>6}  时长:{dur_str}  更新:{tracks}期")
        print(f"     分类:{genre_i}  {mark}")

    # 7. 新锐机会
    if new_podcasts:
        print(f"\n🆕 新锐入场机会")
        print_divider()
        sorted_new = sorted(new_podcasts, key=lambda x: x.get("avgPlayCount", 0), reverse=True)
        for i, p in enumerate(sorted_new[:5], 1):
            plays_n = p.get("avgPlayCount", 0)
            freshness_n = p.get("freshnessDays", 0)
            print(f"  {i}. {p['title']}  均播:{plays_n:>8,}  {freshness_n:.0f}天前更新")

    # 8. 创作切入点建议
    print(f"\n💡 创作切入点建议")
    print_divider()
    suggestions = []

    if active_formats:
        top_fmt_name = list(active_formats.keys())[0]
        if top_fmt_name in ("访谈", "对谈", "对话"):
            suggestions.append(f"  · 嘉宾选择：寻找「已有流量但未高频出镜」的人物，避免同质化串台")
        elif top_fmt_name in ("盘点", "复盘"):
            suggestions.append(f"  · 时效性强，适合做年终/季度/事件盘点，可制造话题热度")
        elif top_fmt_name in ("圆桌"):
            suggestions.append(f"  · 圆桌讨论参与感强，利于拉新；注意控制人数(3-4人最佳)")

    if durations:
        if avg_dur > 60:
            suggestions.append(f"  · 时长参考：{avg_dur:.0f}min 长单集是主流，深度内容有壁垒，可做2-3小时超级内容")
        elif avg_dur > 40:
            suggestions.append(f"  · 时长参考：中长单集({avg_dur:.0f}min)最常见，适合通勤场景")
        else:
            suggestions.append(f"  · 时长参考：短单集({avg_dur:.0f}min)为主，适合碎片时间，高频更新可增加曝光")

    if len(new_podcasts) > 8:
        suggestions.append(f"  · 新人机会：新锐榜有{len(new_podcasts)}档入场，证明需求未被完全满足，是入场窗口期")

    if concentration and concentration > 2.5:
        suggestions.append(f"  · 差异化方向：头部集中系数{concentration:.1f}x说明市场被头部垄断，垂直细分+独特人设是破局点")
    elif concentration and concentration < 2:
        suggestions.append(f"  · 差异化方向：市场分散，机会在整合与规模化，建立清晰的品牌认知比内容更重要")

    if hot_topics:
        top_topic = hot_topics[0]
        suggestions.append(f"  · 蹭话题策略：「{top_topic[0]}」出现{top_topic[1]}次，但要有独特切入角度，避免泛泛而谈")

    # 参考标杆
    suggestions.append(f"  · 品牌参考：GIADA《岩中花述》证明高端IP+优质内容可破圈；泡泡玛特IP联名思路值得借鉴")
    suggestions.append(f"  · 下一步：先用 analyze_genre.py 深入分析，再做最终方向决策")

    for s in suggestions:
        print(s)

    print(f"\n{'='*56}")
    print(f"报告完毕 · {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*56}\n")


def main():
    parser = argparse.ArgumentParser(description="生成播客创作机会完整报告")
    parser.add_argument("--genre", help="分析分类名称")
    parser.add_argument("--custom-query", help="自定义关键词搜索")
    args = parser.parse_args()
    q = args.genre or args.custom_query or "个人成长"
    generate_report(q)


if __name__ == "__main__":
    main()
