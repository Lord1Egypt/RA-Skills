"""annual_report.py — Memory Annual Report Generator (Spotify Wrapped style)"""

from __future__ import annotations

import json
import time
import logging
from collections import Counter
from datetime import datetime

logger = logging.getLogger(__name__)


class AnnualReportGenerator:
    """Generate shareable annual/periodic memory reports (like Spotify Wrapped)."""

    def __init__(self, store, spirit=None):
        self.store = store
        self.spirit = spirit

    def generate_report(self, year: int = None, tenant_id: str = 'default') -> dict:
        """Generate a comprehensive annual report."""
        year = year or datetime.now().year
        start = int(datetime(year, 1, 1).timestamp())
        end = int(datetime(year, 12, 31, 23, 59, 59).timestamp())

        stats = self._compute_stats(start, end, tenant_id)
        return {
            "year": year,
            "title": f"Your {year} Memory Journey",
            "total_memories": stats["total"],
            "top_topics": stats["topics"][:5],
            "emotion_trajectory": stats["emotions"],
            "knowledge_growth": stats["knowledge_growth"],
            "peak_day": stats["peak_day"],
            "memory_streak": stats["streak"],
            "highlights": self._generate_highlights(stats),
        }

    def _compute_stats(self, start: int, end: int, tenant_id: str) -> dict:
        """Compute annual statistics from the store."""
        try:
            memories = self.store.query(
                time_from=start,
                time_to=end,
                limit=5000,
            )
        except Exception as e:
            logger.warning("AnnualReport: query failed: %s", e)
            memories = []

        total = len(memories)

        # Topic distribution
        topic_counter = Counter()
        for m in memories:
            for t in m.get("topics", []):
                code = t.get("code", t) if isinstance(t, dict) else t
                if code:
                    root = code.split(".")[0]
                    topic_counter[root] += 1

        topics = [
            {"topic": t, "count": c}
            for t, c in topic_counter.most_common(20)
        ]

        # Emotion trajectory (monthly averages)
        emotions = self._compute_emotion_trajectory(memories)

        # Knowledge growth (monthly memory counts)
        knowledge_growth = self._compute_knowledge_growth(memories)

        # Peak day
        day_counter = Counter()
        for m in memories:
            ts = m.get("time_ts", 0)
            if ts:
                day = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                day_counter[day] += 1
        peak_day = day_counter.most_common(1)[0] if day_counter else (None, 0)

        # Streak (consecutive days with memories)
        streak = self._compute_streak(day_counter)

        # Importance distribution
        importance_dist = Counter(m.get("importance", "medium") for m in memories)

        # Nature distribution
        nature_dist = Counter(m.get("nature_id", "") for m in memories if m.get("nature_id"))

        return {
            "total": total,
            "topics": topics,
            "emotions": emotions,
            "knowledge_growth": knowledge_growth,
            "peak_day": {"date": peak_day[0], "count": peak_day[1]},
            "streak": streak,
            "importance_dist": dict(importance_dist),
            "nature_dist": dict(nature_dist),
            "day_counter": dict(day_counter),
        }

    def _compute_emotion_trajectory(self, memories: list[dict]) -> list[dict]:
        """Compute monthly emotion averages."""
        monthly = {}
        for m in memories:
            ts = m.get("time_ts", 0)
            if not ts:
                continue
            month = datetime.fromtimestamp(ts).strftime("%Y-%m")
            monthly.setdefault(month, {"valence": [], "arousal": []})
            v = m.get("valence")
            a = m.get("arousal")
            if v is not None:
                monthly[month]["valence"].append(float(v))
            if a is not None:
                monthly[month]["arousal"].append(float(a))

        trajectory = []
        for month in sorted(monthly):
            vals = monthly[month]
            trajectory.append({
                "month": month,
                "avg_valence": round(sum(vals["valence"]) / len(vals["valence"]), 3) if vals["valence"] else 0,
                "avg_arousal": round(sum(vals["arousal"]) / len(vals["arousal"]), 3) if vals["arousal"] else 0,
                "count": len(vals["valence"]),
            })
        return trajectory

    def _compute_knowledge_growth(self, memories: list[dict]) -> list[dict]:
        """Compute monthly memory counts (knowledge growth curve)."""
        monthly = Counter()
        for m in memories:
            ts = m.get("time_ts", 0)
            if ts:
                month = datetime.fromtimestamp(ts).strftime("%Y-%m")
                monthly[month] += 1

        return [
            {"month": m, "count": c}
            for m, c in sorted(monthly.items())
        ]

    def _compute_streak(self, day_counter: Counter) -> dict:
        """Compute longest consecutive-day streak."""
        if not day_counter:
            return {"longest": 0, "current": 0}

        sorted_days = sorted(day_counter.keys())
        longest = 1
        current = 1

        for i in range(1, len(sorted_days)):
            prev = datetime.strptime(sorted_days[i - 1], "%Y-%m-%d")
            curr = datetime.strptime(sorted_days[i], "%Y-%m-%d")
            if (curr - prev).days == 1:
                current += 1
                longest = max(longest, current)
            else:
                current = 1

        # Check if current streak extends to today
        today_str = datetime.now().strftime("%Y-%m-%d")
        current_streak = 0
        check_date = datetime.now()
        while True:
            check_str = check_date.strftime("%Y-%m-%d")
            if check_str in day_counter:
                current_streak += 1
                check_date = datetime.fromtimestamp(
                    check_date.timestamp() - 86400
                )
            else:
                break

        return {"longest": longest, "current": current_streak}

    def _generate_highlights(self, stats: dict) -> list[dict]:
        """Generate data-driven highlights, not template-based."""
        highlights = []

        total = stats.get("total", 0)
        if total > 0:
            highlights.append({
                "type": "milestone",
                "icon": "📊",
                "text": f"全年共记录 {total} 条记忆",
            })

        # Most active topic
        topics = stats.get("topics", [])
        if topics:
            top_topic = topics[0]
            highlights.append({
                "type": "top_topic",
                "icon": "📚",
                "text": f"最关注的话题: {top_topic['topic']} ({top_topic['count']}条)",
            })

        # Growth trend
        knowledge_growth = stats.get("knowledge_growth", [])
        if len(knowledge_growth) >= 4:
            first_count = knowledge_growth[0].get("count", 0)
            last_count = knowledge_growth[-1].get("count", 0)
            trend = "上升" if last_count > first_count else "下降"
            highlights.append({
                "type": "trend",
                "icon": "📈",
                "text": f"记忆增长趋势: {trend}",
            })

        # High importance ratio
        imp = stats.get("importance_dist", {})
        if imp:
            high_ratio = imp.get("high", 0) / max(sum(imp.values()), 1)
            if high_ratio > 0.3:
                highlights.append({
                    "type": "quality",
                    "icon": "⭐",
                    "text": f"高质量记忆占比 {high_ratio:.0%}，信息密度优秀",
                })
            elif high_ratio < 0.1:
                highlights.append({
                    "type": "quality",
                    "icon": "💡",
                    "text": f"高质量记忆仅占 {high_ratio:.0%}，建议多记录关键决策",
                })

        # Peak day
        peak = stats.get("peak_day", {})
        if peak.get("date"):
            highlights.append({
                "type": "peak",
                "icon": "📈",
                "text": f"最活跃的一天: {peak['date']} ({peak['count']} 条记忆)",
            })

        # Streak
        streak = stats.get("streak", {})
        if streak.get("longest", 0) >= 7:
            highlights.append({
                "type": "streak",
                "icon": "🔥",
                "text": f"最长连续记录: {streak['longest']} 天",
            })

        return highlights

    def generate_html_report(self, year: int = None, tenant_id: str = 'default') -> str:
        """Generate a beautiful HTML report page."""
        report = self.generate_report(year, tenant_id)
        year_val = report["year"]

        # Build topic bars
        topic_bars_html = ""
        max_topic_count = max(
            (t["count"] for t in report["top_topics"]), default=1
        )
        for t in report["top_topics"]:
            pct = int(t["count"] / max_topic_count * 100)
            topic_bars_html += f"""
            <div class="topic-row">
                <span class="topic-name">{t['topic']}</span>
                <div class="topic-bar-bg">
                    <div class="topic-bar-fill" style="width:{pct}%"></div>
                </div>
                <span class="topic-count">{t['count']}</span>
            </div>"""

        # Build emotion chart (simple SVG sparkline)
        emotion_svg = self._render_emotion_svg(report.get("emotion_trajectory", []))

        # Build knowledge growth chart
        growth_svg = self._render_growth_svg(report.get("knowledge_growth", []))

        # Build highlights
        highlights_html = ""
        for h in report.get("highlights", []):
            highlights_html += f"""
            <div class="highlight-card">
                <span class="highlight-icon">{h['icon']}</span>
                <span class="highlight-text">{h['text']}</span>
            </div>"""

        peak = report.get("peak_day", {})
        streak = report.get("memory_streak", {})

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{report['title']}</title>
<style>
  :root {{
    --bg: #0d1117;
    --card: #161b22;
    --border: #30363d;
    --text: #e6edf3;
    --text-muted: #8b949e;
    --accent: #58a6ff;
    --accent2: #f78166;
    --green: #3fb950;
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    line-height: 1.6;
    padding: 2rem;
    max-width: 800px;
    margin: 0 auto;
  }}
  h1 {{ font-size: 2rem; margin-bottom: 0.5rem; }}
  .subtitle {{ color: var(--text-muted); margin-bottom: 2rem; }}
  .stat-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
  }}
  .stat-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
  }}
  .stat-value {{ font-size: 2rem; font-weight: 700; color: var(--accent); }}
  .stat-label {{ font-size: 0.85rem; color: var(--text-muted); margin-top: 0.3rem; }}
  .section {{ margin-bottom: 2rem; }}
  .section-title {{
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
  }}
  .topic-row {{ display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.6rem; }}
  .topic-name {{ width: 100px; text-align: right; font-size: 0.9rem; color: var(--text-muted); }}
  .topic-bar-bg {{
    flex: 1;
    height: 20px;
    background: var(--border);
    border-radius: 10px;
    overflow: hidden;
  }}
  .topic-bar-fill {{
    height: 100%;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    border-radius: 10px;
    transition: width 0.5s ease;
  }}
  .topic-count {{ width: 40px; font-size: 0.85rem; color: var(--text-muted); }}
  .highlight-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
  }}
  .highlight-icon {{ font-size: 1.5rem; }}
  .highlight-text {{ font-size: 0.95rem; }}
  .chart-container {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
  }}
  .chart-container svg {{ width: 100%; height: auto; }}
  .watermark {{
    text-align: center;
    color: var(--text-muted);
    font-size: 0.75rem;
    margin-top: 3rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
  }}
</style>
</head>
<body>
<h1>{report['title']}</h1>
<p class="subtitle">Powered by Agent Memory V12</p>

<div class="stat-grid">
  <div class="stat-card">
    <div class="stat-value">{report['total_memories']}</div>
    <div class="stat-label">Total Memories</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">{peak.get('count', 0)}</div>
    <div class="stat-label">Peak Day</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">{streak.get('longest', 0)}</div>
    <div class="stat-label">Longest Streak</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">{len(report['top_topics'])}</div>
    <div class="stat-label">Top Topics</div>
  </div>
</div>

<div class="section">
  <div class="section-title">📚 Top Topics</div>
  {topic_bars_html}
</div>

<div class="section">
  <div class="section-title">📈 Knowledge Growth</div>
  <div class="chart-container">{growth_svg}</div>
</div>

<div class="section">
  <div class="section-title">😊 Emotion Trajectory</div>
  <div class="chart-container">{emotion_svg}</div>
</div>

<div class="section">
  <div class="section-title">✨ Highlights</div>
  {highlights_html}
</div>

<div class="watermark">Powered by Agent Memory V12 &mdash; No PII included</div>
</body>
</html>"""
        return html

    def generate_share_card(self, year: int = None, tenant_id: str = 'default') -> str:
        """Generate a compact share card as HTML (600x400)."""
        report = self.generate_report(year, tenant_id)
        peak = report.get("peak_day", {})
        streak = report.get("memory_streak", {})
        top_topic = report["top_topics"][0] if report["top_topics"] else {"topic": "N/A", "count": 0}

        highlights_text = ""
        for h in report.get("highlights", [])[:3]:
            highlights_text += f"<div class='hl'>{h['icon']} {h['text']}</div>"

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  :root {{
    --bg: #0d1117; --card: #161b22; --border: #30363d;
    --text: #e6edf3; --muted: #8b949e; --accent: #58a6ff; --accent2: #f78166;
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    background: var(--bg); color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    width: 600px; height: 400px; overflow: hidden;
    padding: 2rem; display: flex; flex-direction: column;
  }}
  .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }}
  .title {{ font-size: 1.5rem; font-weight: 700; }}
  .year {{ font-size: 2.5rem; font-weight: 800; color: var(--accent); }}
  .stats {{ display: flex; gap: 1.5rem; margin-bottom: 1.5rem; }}
  .stat {{ text-align: center; }}
  .stat-val {{ font-size: 1.8rem; font-weight: 700; color: var(--accent2); }}
  .stat-lbl {{ font-size: 0.7rem; color: var(--muted); }}
  .highlights {{ flex: 1; }}
  .hl {{ font-size: 0.85rem; margin-bottom: 0.5rem; }}
  .footer {{
    text-align: center; color: var(--muted); font-size: 0.65rem;
    margin-top: auto; padding-top: 0.5rem; border-top: 1px solid var(--border);
  }}
</style>
</head>
<body>
<div class="header">
  <div class="title">Memory Journey</div>
  <div class="year">{report['year']}</div>
</div>
<div class="stats">
  <div class="stat"><div class="stat-val">{report['total_memories']}</div><div class="stat-lbl">MEMORIES</div></div>
  <div class="stat"><div class="stat-val">{streak.get('longest', 0)}</div><div class="stat-lbl">STREAK</div></div>
  <div class="stat"><div class="stat-val">{peak.get('count', 0)}</div><div class="stat-lbl">PEAK DAY</div></div>
  <div class="stat"><div class="stat-val">{top_topic['count']}</div><div class="stat-lbl">{top_topic['topic'][:8]}</div></div>
</div>
<div class="highlights">{highlights_text}</div>
<div class="footer">Powered by Agent Memory V12 &mdash; No PII included</div>
</body>
</html>"""
        return html

    def _render_emotion_svg(self, trajectory: list[dict]) -> str:
        """Render emotion trajectory as a simple SVG line chart."""
        if not trajectory:
            return "<p style='color:#8b949e;text-align:center'>No emotion data</p>"

        width = 700
        height = 150
        padding = 30
        chart_w = width - 2 * padding
        chart_h = height - 2 * padding

        points_valence = []
        points_arousal = []
        n = len(trajectory)
        for i, t in enumerate(trajectory):
            x = padding + (i / max(n - 1, 1)) * chart_w
            # Valence: -1 to 1 → chart area
            vy = padding + chart_h / 2 - (t.get("avg_valence", 0)) * chart_h / 2
            points_valence.append(f"{x:.1f},{vy:.1f}")
            # Arousal: 0 to 1 → chart area
            ay = padding + chart_h - t.get("avg_arousal", 0) * chart_h
            points_arousal.append(f"{x:.1f},{ay:.1f}")

        valence_line = " ".join(points_valence)
        arousal_line = " ".join(points_arousal)

        # Month labels
        labels = ""
        step = max(1, n // 6)
        for i in range(0, n, step):
            x = padding + (i / max(n - 1, 1)) * chart_w
            month = trajectory[i].get("month", "")[5:]  # Just MM
            labels += f'<text x="{x:.0f}" y="{height - 5}" fill="#8b949e" font-size="10" text-anchor="middle">{month}</text>'

        return f"""<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <line x1="{padding}" y1="{padding + chart_h / 2}" x2="{width - padding}" y2="{padding + chart_h / 2}" stroke="#30363d" stroke-width="1" stroke-dasharray="4"/>
  <polyline points="{valence_line}" fill="none" stroke="#58a6ff" stroke-width="2"/>
  <polyline points="{arousal_line}" fill="none" stroke="#f78166" stroke-width="2" stroke-dasharray="4"/>
  <circle cx="{width - padding - 60}" cy="15" r="4" fill="#58a6ff"/>
  <text x="{width - padding - 50}" y="19" fill="#8b949e" font-size="10">Valence</text>
  <circle cx="{width - padding - 60}" cy="30" r="4" fill="#f78166"/>
  <text x="{width - padding - 50}" y="34" fill="#8b949e" font-size="10">Arousal</text>
  {labels}
</svg>"""

    def _render_growth_svg(self, growth: list[dict]) -> str:
        """Render knowledge growth as a simple SVG bar chart."""
        if not growth:
            return "<p style='color:#8b949e;text-align:center'>No growth data</p>"

        width = 700
        height = 150
        padding = 30
        chart_w = width - 2 * padding
        chart_h = height - 2 * padding

        max_count = max(g["count"] for g in growth) or 1
        bar_width = max(4, chart_w / len(growth) - 2)

        bars = ""
        labels = ""
        for i, g in enumerate(growth):
            x = padding + (i / len(growth)) * chart_w
            bar_h = (g["count"] / max_count) * chart_h
            y = padding + chart_h - bar_h
            bars += f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width:.1f}" height="{bar_h:.1f}" fill="url(#growthGrad)" rx="2"/>'
            # Labels: show every few months
            if len(growth) <= 12 or i % max(1, len(growth) // 6) == 0:
                month = g.get("month", "")[5:]
                labels += f'<text x="{x + bar_width / 2:.0f}" y="{height - 5}" fill="#8b949e" font-size="10" text-anchor="middle">{month}</text>'

        return f"""<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="growthGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#58a6ff"/>
      <stop offset="100%" stop-color="#f78166"/>
    </linearGradient>
  </defs>
  {bars}
  {labels}
</svg>"""
