#!/usr/bin/env python3
"""
分类竞争分析脚本 — 评估某分类的竞争强度，输出增长机会和对标案例

用法:
  python3 scripts/analyze_genre.py --genre 商业
  python3 scripts/analyze_genre.py --genre 科技 --compare-genres 商业 个人成长
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from urllib.request import Request, urlopen

SCRIPT_DIR = Path(__file__).parent
TRACK_FILE = SCRIPT_DIR / "subscription_data.json"
TREND_API_BASE = "https://api.xyzrank.top/v1"


def load_tracked():
    """加载本地订阅追踪数据，返回 {podcast_name: {pid, history}}"""
    if not TRACK_FILE.exists():
        return {}
    raw = json.load(open(TRACK_FILE))
    podcasts = raw.get("podcasts", {})
    # 标准化：兼容 name-keyed 和 pid-keyed 两种格式
    return podcasts


def fetch_xyz(genre, list_type="hot-podcasts", limit=100):
    """从 xyzrank 获取某分类的播客列表"""
    args = [
        sys.executable, str(SCRIPT_DIR / "fetch_xyz_rank.py"),
        "--list", list_type,
        "--genre", genre,
        "--limit", str(limit),
    ]
    result = subprocess.run(args, capture_output=True, text=True)
    try:
        return json.loads(result.stdout).get("items", [])
    except Exception:
        return []


def fetch_new_podcasts(genre, limit=20):
    return fetch_xyz(genre, "new-podcasts", limit)


def fetch_trend_metrics(podcast_id):
    """从 api.xyzrank.top 获取播客历史订阅趋势 /v1/metrics/{id}"""
    try:
        url = f"{TREND_API_BASE}/metrics/{podcast_id}"
        req = Request(url, headers={"User-Agent": "podcast-radar-cn/1.0"})
        with urlopen(req, timeout=10) as r:
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
    sorted_data = sorted(data, key=lambda x: x.get("crawl_date", ""), reverse=True)
    latest = sorted_data[0].get("subscriber_count", 0)
    oldest = sorted_data[-1].get("subscriber_count", 0)
    days = len(sorted_data)
    total_growth = latest - oldest
    growth_rate = (total_growth / oldest * 100) if oldest > 0 else 0
    return latest, total_growth, growth_rate


def calc_weekly_growth(name, history):
    """从订阅历史计算周均增长率"""
    if len(history) < 2:
        return None, None
    first = history[0].get("subscribers", 0)
    last = history[-1].get("subscribers", 0)
    weeks = len(history)
    total = last - first
    weekly = total / weeks if weeks > 0 else 0
    return total, weekly


def score_competition(podcasts):
    """评分竞争强度，返回 0-100（越高=竞争越激烈）"""
    plays = [p["avgPlayCount"] for p in podcasts if p.get("avgPlayCount")]
    if not plays:
        return None, None

    avg = sum(plays) / len(plays)
    top10 = sorted(plays, reverse=True)[:10]
    top10_avg = sum(top10) / len(top10) if top10 else avg
    concentration = top10_avg / avg if avg > 0 else 1

    # 竞争激烈度 = 头部集中系数（权重0.6）+ 头部门槛系数（权重0.4）
    threshold_ratio = top10[0] / avg if avg > 0 else 1
    score = min(100, concentration * 35 + threshold_ratio * 15)
    return round(score, 1), round(concentration, 2)


def analyze_genre(genre):
    """主分析函数"""
    print(f"\n{'='*56}")
    print(f"📊 分类竞争分析: {genre}")
    print(f"{'='*56}")

    hot = fetch_xyz(genre, "hot-podcasts", 100)
    new = fetch_new_podcasts(genre, 20)
    tracked = load_tracked()

    if not hot:
        print(f"❌ 未找到分类「{genre}」的播客，请检查分类名称")
        return

    # 播放量分析
    plays = [p["avgPlayCount"] for p in hot if p.get("avgPlayCount")]
    comments = [p["avgCommentCount"] for p in hot if p.get("avgCommentCount")]
    durations = [p["avgDurationMinutes"] for p in hot if p.get("avgDurationMinutes")]
    freshness = [p["freshnessDays"] for p in hot if p.get("freshnessDays")]

    sorted_hot = sorted(hot, key=lambda x: x.get("avgPlayCount", 0), reverse=True)
    top10 = sorted_hot[:10]

    print(f"\n🏆 竞争规模")
    print(f"  热门播客总数:   {len(hot)} 档")
    print(f"  新锐播客数量:   {len(new)} 档")

    if plays:
        top10_plays = [p["avgPlayCount"] for p in top10]
        mid_idx = len(plays) // 2
        competition_score, concentration = score_competition(hot)
        print(f"\n⚔️  竞争格局")
        print(f"  平均播放量:     {sum(plays)/len(plays):>10,.0f}")
        print(f"  中位播放量:     {sorted(plays)[mid_idx]:>10,.0f}")
        print(f"  最高播放量:     {max(plays):>10,}")
        print(f"  Top10均值:      {sum(top10_plays)/len(top10_plays):>10,.0f}")
        print(f"  头部集中系数:   {concentration:.2f}x  {'🔴 高度集中' if concentration > 3 else '🟡 中度集中' if concentration > 2 else '🟢 相对分散'}")
        if competition_score:
            print(f"  竞争激烈度:     {competition_score}/100  {'🔴 强竞争' if competition_score > 70 else '🟡 中等' if competition_score > 40 else '🟢 低竞争'}")

    if comments:
        avg_comment = sum(comments) / len(comments)
        avg_play = sum(plays) / len(plays) if plays else 1
        comment_rate = avg_comment / avg_play * 100
        print(f"  平均评论率:     {comment_rate:.2f}%")

    if durations:
        avg_dur = sum(durations) / len(durations)
        print(f"  平均时长:       {avg_dur:.0f}min  {'📊 长内容主导' if avg_dur > 50 else '📰 中短内容主导'}")

    if freshness:
        avg_fresh = sum(freshness) / len(freshness)
        print(f"  平均更新间隔:   {avg_fresh:.1f}天   {'⚡ 高频更新' if avg_fresh < 7 else '📅 中频更新' if avg_fresh < 14 else '🐢 低频更新'}")

    # 增长最快的播客（来自订阅追踪数据）
    tracked_pids = {v.get("pid"): name for name, v in tracked.items()}
    hot_with_growth = []
    for p in sorted_hot:
        xyz_url = p.get("links", {}).get("xyz", "") if isinstance(p.get("links"), dict) else ""
        pid = xyz_url.split("/")[-1] if xyz_url else ""
        for tname, tinfo in tracked.items():
            if tinfo.get("pid") == pid or tname == p.get("title"):
                history = tinfo.get("history", [])
                if len(history) >= 2:
                    total, weekly = calc_weekly_growth(tname, history)
                    hot_with_growth.append({
                        **p,
                        "track_name": tname,
                        "total_growth": total,
                        "weekly_growth": weekly,
                        "history_len": len(history),
                    })
                    break

    if hot_with_growth:
        hot_with_growth.sort(key=lambda x: x["weekly_growth"] or 0, reverse=True)
        print(f"\n📈 订阅增长最快的播客 (来自订阅追踪数据)")
        for i, p in enumerate(hot_with_growth[:3], 1):
            wg = p["weekly_growth"] or 0
            tg = p["total_growth"] or 0
            bar = "█" * min(int(wg / 200), 20)
            print(f"  {i}. {p['title']}")
            print(f"     周均: +{wg:>6,.0f} {bar}")
            print(f"     总增长: +{tg:>8,} ({p['history_len']}周数据)")

    # 趋势 API 数据（xyzrank 官方）
    print(f"\n📈 趋势 API 数据 (api.xyzrank.top)")
    trend_results = []
    for p in sorted_hot[:8]:  # 查前8个
        xyz_url = p.get("links", {}).get("xyz", "") if isinstance(p.get("links"), dict) else ""
        pid = xyz_url.split("/")[-1] if xyz_url else ""
        if pid and len(pid) == 24:
            metrics = fetch_trend_metrics(pid)
            if metrics and metrics.get("data"):
                latest, total_growth, growth_rate = calc_trend_growth(metrics)
                if latest:
                    trend_results.append({
                        **p,
                        "latest_subs": latest,
                        "growth_rate": growth_rate,
                        "total_growth": total_growth,
                    })
    if trend_results:
        trend_results.sort(key=lambda x: x["growth_rate"] or 0, reverse=True)
        print(f"  成功获取 {len(trend_results)} 档播客趋势数据\n")
        for i, p in enumerate(trend_results[:3], 1):
            gr = p["growth_rate"] or 0
            tg = p["total_growth"] or 0
            subs = p["latest_subs"] or 0
            arrow = "📈" if gr > 0 else "📉"
            print(f"  {i}. {p['title']}")
            print(f"     订阅: {subs:>10,}  增长: {tg:>+9,} ({arrow}{gr:+.1f}%)")
    else:
        print(f"  📭 暂无趋势数据")

    # 新锐榜
    if new:
        print(f"\n🆕 新锐榜 Top 5 (快速崛起机会)")
        sorted_new = sorted(new, key=lambda x: x.get("avgPlayCount", 0), reverse=True)
        for i, p in enumerate(sorted_new[:5], 1):
            plays_n = p.get("avgPlayCount", 0)
            print(f"  {i}. {p['title']}  均播:{plays_n:>8,}  更新:{p.get('freshnessDays', 0):.0f}天前")

    # 对标案例
    print(f"\n📚 推荐对标案例 Top 5")
    for i, p in enumerate(sorted_hot[:5], 1):
        xyz_url = p.get("links", {}).get("xyz", "") if isinstance(p.get("links"), dict) else ""
        pid = xyz_url.split("/")[-1] if xyz_url else ""
        is_tracked = pid in tracked_pids or p.get("title") in tracked
        mark = "✅已追踪" if is_tracked else "➕可追踪"
        plays_i = p.get("avgPlayCount", 0)
        comments_i = p.get("avgCommentCount", 0)
        genre_i = p.get("genre", "—")
        print(f"  {i}. {p['title']}  [{mark}]")
        print(f"     均播:{plays_i:>10,}  评论:{comments_i:>6}  分类:{genre_i}")


def main():
    parser = argparse.ArgumentParser(description="分析某分类的播客竞争格局")
    parser.add_argument("--genre", required=True, help="要分析的分类名称")
    parser.add_argument("--compare-genres", nargs="+", help="对比多个分类")
    args = parser.parse_args()

    analyze_genre(args.genre)
    if args.compare_genres:
        print("\n")
        for g in args.compare_genres:
            analyze_genre(g)


if __name__ == "__main__":
    main()
