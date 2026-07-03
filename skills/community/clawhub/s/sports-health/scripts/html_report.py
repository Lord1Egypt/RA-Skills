#!/usr/bin/env python3
"""
HTML 运动报告生成器
- 日报 / 周报 / 月报
- 交互式图表（Chart.js）
- 消耗统计 + 趋势分析 + AI 建议
"""

import json
from pathlib import Path
from datetime import date, timedelta
try:
    from .calorie_calc import CalorieCalc
    from .plan_gen import PlanGenerator
except ImportError:
    from calorie_calc import CalorieCalc
    from plan_gen import PlanGenerator


def generate_daily_report(calc: CalorieCalc, dt: date = None) -> str:
    """生成单日运动报告 HTML"""
    if dt is None:
        dt = date.today()

    daily = calc.calc_daily(dt)
    streak = calc.get_streak()
    profile = calc.load_profile()
    weight = calc.get_weight()

    # 评分
    score = _rate_daily(daily)
    score_color = _score_color(score)

    # 运动列表
    exercises_html = ""
    for ex in daily["exercises"]:
        exercises_html += f"""
        <div class="exercise-card">
            <div class="ex-header">
                <span class="ex-type">{_category_icon(ex.get('category', ''))} {ex['type']}</span>
                <span class="ex-time">{ex.get('time', '')}</span>
            </div>
            <div class="ex-stats">
                <div class="ex-stat"><span class="ex-label">时长</span><span class="ex-value">{ex['duration_min']}分钟</span></div>
                <div class="ex-stat"><span class="ex-label">消耗</span><span class="ex-value">{ex['calories']:.0f} kcal</span></div>
                <div class="ex-stat"><span class="ex-label">分类</span><span class="ex-value">{ex.get('category', '-')}</span></div>
            </div>
        </div>"""

    # 食物等同
    food_html = ""
    if daily["total_calories"] > 0:
        from .motion_db import get_food_equivalent
        foods = get_food_equivalent(daily["total_calories"])
        for f in foods[:3]:
            food_html += f'<div class="food-item">🍽️ {f["equivalent"]}份{f["food"]}</div>'

    # 建议
    tips = _generate_daily_tips(daily, profile)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>运动日报 - {dt.strftime('%Y年%m月%d日')}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif; background: linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%); padding: 16px; min-height: 100vh; }}
.container {{ max-width: 520px; margin: 0 auto; }}

.header {{ text-align: center; padding: 20px 0; }}
.header h1 {{ font-size: 24px; color: #1e3a5f; font-weight: 800; }}
.header .date {{ color: #6b7280; font-size: 14px; margin-top: 4px; }}

.card {{ background: white; border-radius: 16px; padding: 20px; margin-bottom: 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}

.score-section {{ display: flex; align-items: center; gap: 16px; }}
.score-circle {{ display: flex; align-items: center; justify-content: center; width: 72px; height: 72px; border-radius: 50%; background: {score_color}; color: white; font-size: 28px; font-weight: bold; flex-shrink: 0; }}
.score-info {{ flex: 1; }}
.score-info .title {{ font-size: 15px; font-weight: 600; color: #1e3a5f; }}
.score-info .subtitle {{ font-size: 13px; color: #6b7280; margin-top: 2px; }}

.stats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }}
.stat-item {{ background: #f8fafc; border-radius: 12px; padding: 14px; text-align: center; }}
.stat-value {{ font-size: 22px; font-weight: 800; color: #1e3a5f; }}
.stat-label {{ font-size: 12px; color: #6b7280; margin-top: 2px; }}

.card-title {{ font-size: 16px; font-weight: 700; color: #1e3a5f; margin-bottom: 14px; display: flex; align-items: center; gap: 6px; }}

.exercise-card {{ background: #f8fafc; border-radius: 10px; padding: 12px; margin-bottom: 8px; border-left: 3px solid #3b82f6; }}
.ex-header {{ display: flex; justify-content: space-between; font-size: 14px; }}
.ex-type {{ font-weight: 600; color: #374151; }}
.ex-time {{ color: #9ca3af; font-size: 12px; }}
.ex-stats {{ display: flex; gap: 16px; margin-top: 8px; }}
.ex-stat {{ display: flex; flex-direction: column; }}
.ex-label {{ font-size: 11px; color: #9ca3af; }}
.ex-value {{ font-size: 13px; font-weight: 600; color: #374151; }}

.food-item {{ background: #fef3c7; border-radius: 8px; padding: 8px 12px; margin-bottom: 6px; font-size: 13px; color: #92400e; }}

.tip-item {{ background: #f0fdf4; border-radius: 8px; padding: 8px 12px; margin-bottom: 6px; font-size: 13px; color: #166534; border-left: 2px solid #22c55e; }}

.streak-badge {{ display: inline-flex; align-items: center; gap: 4px; background: linear-gradient(135deg, #f97316, #ef4444); color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }}

.no-data {{ text-align: center; padding: 30px; color: #9ca3af; font-size: 14px; }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>🏃 运动日报</h1>
        <div class="date">{dt.strftime('%Y年%m月%d日 %A')}</div>
        {f'<div style="margin-top:8px;"><span class="streak-badge">🔥 连续运动 {streak} 天</span></div>' if streak > 0 else ''}
    </div>

    <div class="card">
        <div class="score-section">
            <div class="score-circle">{score}</div>
            <div class="score-info">
                <div class="title">{_score_title(score)}</div>
                <div class="subtitle">今日消耗 {daily['total_calories']:.0f} kcal | 运动 {daily['total_duration_min']:.0f} 分钟</div>
            </div>
        </div>
    </div>

    <div class="card">
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-value">{daily['total_calories']:.0f}</div>
                <div class="stat-label">消耗 kcal</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{daily['total_duration_min']:.0f}</div>
                <div class="stat-label">运动分钟</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{daily['exercise_count']}</div>
                <div class="stat-label">运动次数</div>
            </div>
        </div>
    </div>

    <div class="card">
        <div class="card-title">📝 今日运动</div>
        {exercises_html if exercises_html else '<div class="no-data">今天还没有运动记录 💤<br>试试说"今天跑步5公里" 📱</div>'}
    </div>

    {f'''<div class="card">
        <div class="card-title">🍽️ 消耗相当于</div>
        {food_html}
    </div>''' if food_html else ''}

    <div class="card">
        <div class="card-title">💡 运动建议</div>
        {tips}
    </div>
</div>
</body>
</html>"""
    return html


def generate_weekly_report(calc: CalorieCalc) -> str:
    """生成周运动报告 HTML"""
    stats = calc.calc_weekly_stats()
    trend = calc.calc_trend(7)
    today = date.today()
    week_start = today - timedelta(days=6)

    chart_data = json.dumps({
        "labels": trend["dates"],
        "calories": trend["calories"],
        "durations": trend["durations"],
        "counts": trend["exercise_counts"],
    }, ensure_ascii=False)

    # 分类统计
    cat_html = ""
    cat_colors = {"有氧": "#3b82f6", "力量": "#f97316", "柔韧": "#22c55e", "球类": "#8b5cf6", "户外": "#06b6d4", "日常": "#eab308", "格斗": "#ef4444"}
    for cat, calories in sorted(stats.get("categories", {}).items(), key=lambda x: -x[1]):
        color = cat_colors.get(cat, "#6b7280")
        cat_html += f'<div class="cat-item"><span class="cat-dot" style="background:{color}"></span>{cat} <span class="cat-cal">{calories:.0f} kcal</span></div>'

    # 建议
    insights = _generate_weekly_insights(stats, trend)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>运动周报</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif; background: linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%); padding: 16px; }}
.container {{ max-width: 560px; margin: 0 auto; }}

.header {{ text-align: center; padding: 20px 0; }}
.header h1 {{ font-size: 24px; color: #1e3a5f; font-weight: 800; }}
.header .sub {{ color: #6b7280; font-size: 14px; }}

.card {{ background: white; border-radius: 16px; padding: 20px; margin-bottom: 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
.card-title {{ font-size: 16px; font-weight: 700; color: #1e3a5f; margin-bottom: 14px; }}

.stats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }}
.stat-item {{ background: #f8fafc; border-radius: 12px; padding: 14px; text-align: center; }}
.stat-value {{ font-size: 22px; font-weight: 800; color: #1e3a5f; }}
.stat-label {{ font-size: 12px; color: #6b7280; margin-top: 2px; }}

.progress-bar {{ height: 10px; background: #e5e7eb; border-radius: 5px; overflow: hidden; margin-top: 12px; }}
.progress-fill {{ height: 100%; border-radius: 5px; background: linear-gradient(90deg, #22c55e, #3b82f6); transition: width 1s; }}

.chart-box {{ height: 250px; }}

.cat-item {{ display: flex; align-items: center; gap: 8px; font-size: 13px; padding: 4px 0; }}
.cat-dot {{ width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }}
.cat-cal {{ margin-left: auto; color: #6b7280; }}

.insight-item {{ background: #f0fdf4; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; font-size: 13px; color: #166534; border-left: 3px solid #22c55e; }}

.streak-highlight {{ background: linear-gradient(135deg, #fef3c7, #fde68a); border-radius: 12px; padding: 16px; text-align: center; margin-bottom: 14px; }}
.streak-highlight .streak-num {{ font-size: 36px; font-weight: 900; color: #f97316; }}
.streak-highlight .streak-text {{ font-size: 14px; color: #92400e; margin-top: 4px; }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>📈 运动周报</h1>
        <div class="sub">{week_start.strftime('%m/%d')} - {today.strftime('%m/%d')}</div>
    </div>

    {f'''<div class="streak-highlight">
        <div class="streak-num">🔥 {stats['streak_days']}天</div>
        <div class="streak-text">连续运动天数</div>
    </div>''' if stats['streak_days'] > 0 else ''}

    <div class="card">
        <div class="card-title">📊 本周概览</div>
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-value">{stats['active_days']}/7</div>
                <div class="stat-label">运动天数</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{stats['total_calories']:.0f}</div>
                <div class="stat-label">总消耗 kcal</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{stats['total_duration_min']:.0f}</div>
                <div class="stat-label">总时长 分钟</div>
            </div>
        </div>
        <div class="progress-bar" style="margin-top:14px;">
            <div class="progress-fill" style="width:{min(stats['who_progress_pct'], 100)}%"></div>
        </div>
        <div style="font-size:12px;color:#6b7280;margin-top:6px;text-align:center;">
            WHO建议 150分钟/周 — {stats['guideline_status']}
        </div>
    </div>

    <div class="card">
        <div class="card-title">📈 每日消耗趋势</div>
        <div class="chart-box">
            <canvas id="calorieChart"></canvas>
        </div>
    </div>

    <div class="card">
        <div class="card-title">📈 运动时长趋势</div>
        <div class="chart-box">
            <canvas id="durationChart"></canvas>
        </div>
    </div>

    {f'''<div class="card">
        <div class="card-title">🏷️ 运动分类</div>
        {cat_html if cat_html else '<div style="color:#9ca3af;font-size:13px;">本周暂无记录</div>'}
    </div>''' if stats.get('categories') else ''}

    <div class="card">
        <div class="card-title">💡 本周洞察</div>
        {''.join([f'<div class="insight-item">{i}</div>' for i in insights])}
    </div>
</div>

<script>
const data = {chart_data};
new Chart(document.getElementById('calorieChart'), {{
    type: 'bar',
    data: {{
        labels: data.labels,
        datasets: [{{
            label: '消耗 (kcal)',
            data: data.calories,
            backgroundColor: data.calories.map(v => v > 0 ? '#3b82f6' : '#e5e7eb'),
            borderRadius: 6,
        }}]
    }},
    options: {{
        responsive: true, maintainAspectRatio: false,
        plugins: {{ legend: {{ display: false }} }},
        scales: {{
            y: {{ beginAtZero: true, grid: {{ color: '#f3f4f6' }} }},
            x: {{ grid: {{ display: false }} }}
        }}
    }}
}});
new Chart(document.getElementById('durationChart'), {{
    type: 'line',
    data: {{
        labels: data.labels,
        datasets: [{{
            label: '时长 (分钟)',
            data: data.durations,
            borderColor: '#22c55e',
            backgroundColor: 'rgba(34,197,94,0.1)',
            fill: true,
            tension: 0.3,
            pointRadius: 5,
            pointBackgroundColor: '#22c55e',
        }}]
    }},
    options: {{
        responsive: true, maintainAspectRatio: false,
        plugins: {{ legend: {{ display: false }} }},
        scales: {{
            y: {{ beginAtZero: true, grid: {{ color: '#f3f4f6' }} }},
            x: {{ grid: {{ display: false }} }}
        }}
    }}
}});
</script>
</body>
</html>"""
    return html


def _rate_daily(daily: dict) -> int:
    """评分 0-100"""
    if daily["total_calories"] == 0:
        return 0
    score = 50  # 基础分（有运动）
    # 时长加分
    dur = daily["total_duration_min"]
    if dur >= 60:
        score += 30
    elif dur >= 30:
        score += 20
    elif dur >= 15:
        score += 10
    # 次数加分
    if daily["exercise_count"] >= 2:
        score += 15
    elif daily["exercise_count"] >= 1:
        score += 10
    # 多样性加分
    cats = daily.get("categories", {})
    if len(cats) >= 2:
        score += 5
    return min(score, 100)


def _score_color(score: int) -> str:
    if score >= 80:
        return "#22c55e"
    elif score >= 60:
        return "#3b82f6"
    elif score >= 30:
        return "#f59e0b"
    return "#9ca3af"


def _score_title(score: int) -> str:
    if score >= 80:
        return "太棒了！运动达人 🏆"
    elif score >= 60:
        return "不错哦，继续保持 💪"
    elif score >= 30:
        return "动起来了，好开始 👍"
    elif score > 0:
        return "刚开始，加油！🌟"
    return "今天还没运动哦 💤"


def _category_icon(cat: str) -> str:
    icons = {
        "有氧": "🏃", "力量": "💪", "柔韧": "🧘",
        "球类": "⚽", "户外": "🏔️", "日常": "🚶",
        "格斗": "🥊",
    }
    return icons.get(cat, "🏋️")


def _generate_daily_tips(daily: dict, profile: dict) -> str:
    tips = []
    if daily["total_calories"] == 0:
        tips.append("今天还没运动哦！哪怕散步20分钟也是很好的开始 🚶")
        tips.append("建议每天至少30分钟中等强度运动，对心血管健康非常有益")
        return "\n".join([f'<div class="tip-item">{t}</div>' for t in tips])

    if daily["total_duration_min"] < 30:
        tips.append("运动时长偏少，明天争取达到30分钟吧！")
    if len(daily.get("categories", {})) == 1 and daily["exercise_count"] >= 2:
        tips.append("建议增加运动种类多样化，比如力量+有氧结合效果更好")

    tips.append("运动后记得补充水分！体重每减轻1kg需要补充1-1.5L水 💧")
    tips.append("今晚保证7-8小时睡眠，肌肉修复和体能恢复主要在睡眠中进行")

    goal = (profile or {}).get("goal", "")
    if goal == "减脂":
        tips.append("减脂建议：运动后30分钟内补充蛋白质，帮助肌肉修复且不易转化为脂肪")
    elif goal == "增肌":
        tips.append("增肌建议：训练后补充碳水和蛋白质（比如香蕉+蛋白粉），促进肌肉合成")

    return "\n".join([f'<div class="tip-item">{t}</div>' for t in tips])


def _generate_weekly_insights(stats: dict, trend: dict) -> list:
    insights = []
    
    if stats["active_days"] == 0:
        return ["本周还没有运动记录，从下周开始行动起来吧！🏁"]

    if stats["active_days"] >= 5:
        insights.append("🌟 太棒了！本周运动天数达到5天以上，非常自律")
    elif stats["active_days"] >= 3:
        insights.append("👍 运动频率不错，3天以上的规律运动对健康有明显益处")
    else:
        insights.append("📌 运动天数偏少，建议增加到每周至少3次")

    if stats["streak_days"] >= 7:
        insights.append(f"🔥 连续运动{stats['streak_days']}天！你已经养成了运动习惯")
    elif stats["streak_days"] >= 3:
        insights.append(f"💪 连续运动{stats['streak_days']}天，继续保持这个势头")
    
    if stats["who_progress_pct"] >= 100:
        insights.append("✅ 已达到WHO建议的每周150分钟运动标准")
    elif stats["who_progress_pct"] >= 50:
        insights.append(f"📊 完成WHO标准的{stats['who_progress_pct']}%，继续加油！")
    else:
        insights.append("🎯 距离WHO每周150分钟建议还有差距，可以从增加每次运动时长开始")

    # 趋势分析
    cals = trend.get("calories", [])
    if len(cals) >= 3 and all(c > 0 for c in cals[-3:]):
        if cals[-1] > cals[-2] > cals[-3]:
            insights.append("📈 近3天消耗量持续上升，运动状态越来越好！")
    elif len(cals) >= 5 and sum(1 for c in cals[-5:] if c > 0) >= 3:
        insights.append("📊 本周运动较为均匀，规律性是长期效果的关键")

    insights.append("💡 下周建议：尝试一个新的运动类型，打破适应性平台期")
    
    return insights


if __name__ == "__main__":
    calc = CalorieCalc()
    report = generate_daily_report(calc)
    Path("test_sports_report.html").write_text(report, encoding="utf-8")
    print("测试报告已生成: test_sports_report.html")
