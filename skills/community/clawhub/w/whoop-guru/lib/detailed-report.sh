#!/bin/bash
# Detailed Report - 22:00 详细健康日报
# 包含完整洞察、建议和分析

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SKILL_DIR")"
cd "$SKILL_DIR"

python3 << 'PYEOF'
import sys
import os
sys.path.insert(0, 'lib')

from datetime import datetime
from lib.data_cleaner import WhoopDataProvider
from lib.ml import get_recovery_prediction, get_hrv_anomaly
from lib.reports.weekly import WeeklyReporter

p = WhoopDataProvider()
data = p.get_latest_data()
metrics = p.get_metrics()

processed = data.get('processed', {})
recovery_list = processed.get('recovery', [])
sleep_list = processed.get('sleep', [])
cycles_list = processed.get('cycles', [])
workouts_list = processed.get('workouts', [])

latest_rec = recovery_list[0] if recovery_list else {}
latest_sleep = sleep_list[0] if sleep_list else {}
latest_cycle = cycles_list[0] if cycles_list else {}

date = datetime.now().strftime("%Y年%m月%d日 %H:%M")

# ========== 身体电量 ==========
rec = latest_rec.get('recovery_score', 50)
sp = latest_sleep.get('sleep_performance', 70) if latest_sleep else 70
battery = rec * 0.6 + sp * 0.4
if battery >= 80:
    battery_level = "满格 🟢"
elif battery >= 60:
    battery_level = "良好 🟡"
elif battery >= 40:
    battery_level = "一般 🟠"
else:
    battery_level = "需充电 🔴"

# ========== 睡眠债务 ==========
sleep_hours_14 = [s.get('total_in_bed_hours', 0) for s in sleep_list[:14]]
debt = 14 * 8 - sum(sleep_hours_14)

# ========== 睡眠结构 ==========
light = sum(s.get('light_sleep_hours', 0) for s in sleep_list[:7])
deep = sum(s.get('deep_sleep_hours', 0) for s in sleep_list[:7])
rem = sum(s.get('rem_sleep_hours', 0) for s in sleep_list[:7])
total_sleep = light + deep + rem
if total_sleep > 0:
    light_pct = light / total_sleep * 100
    deep_pct = deep / total_sleep * 100
    rem_pct = rem / total_sleep * 100
else:
    light_pct = deep_pct = rem_pct = 0

# ========== 心率区间 ==========
zones = {"z0": 0, "z1": 0, "z2": 0, "z3": 0, "z4": 0, "z5": 0}
for w in workouts_list[:7]:
    for z in range(6):
        key = f"zone{z}_min"
        zones[f"z{z}"] += w.get(key, 0)
total_zone = sum(zones.values())
if total_zone > 0:
    z01_pct = (zones["z0"] + zones["z1"]) / total_zone * 100
    z23_pct = (zones["z2"] + zones["z3"]) / total_zone * 100
    z45_pct = (zones["z4"] + zones["z5"]) / total_zone * 100
else:
    z01_pct = z23_pct = z45_pct = 0

# ========== ML预测 ==========
pred = get_recovery_prediction()
anomaly = get_hrv_anomaly()

# ========== 周报 ==========
weekly = WeeklyReporter().generate_weekly_report()
weekly_stats = weekly.get('stats', {})

print(f"""
╔══════════════════════════════════════════════════════════════╗
║          🌙 WHOOP GURU 详细健康日报                      ║
║                    {date}                         ║
╚══════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔋 【身体电量】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⚡ {battery:.0f}% {battery_level}
  
  今日恢复: {rec:.0f}% × 0.6 = {rec * 0.6:.1f}
  今日睡眠: {sp:.0f}% × 0.4 = {sp * 0.4:.1f}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🫀 【今日数据】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ┌─────────────────┬──────────┬──────────────────┐
  │ 指标            │ 数值     │ 参考范围         │
  ├─────────────────┼──────────┼──────────────────┤
  │ 恢复分数        │ {rec:.0f}%      │ 60%+ 良好       │
  │ HRV             │ {latest_rec.get('hrv', 0):.0f} ms   │ 40ms+ 正常      │
  │ 静息心率        │ {latest_rec.get('rhr', 0):.0f} bpm   │ 50-60bpm 良好   │
  │ 血氧饱和度      │ {latest_rec.get('spo2', 0):.1f}%   │ 95%+ 正常       │
  │ 皮肤温度        │ {latest_rec.get('skin_temp', 0):.1f}°C   │ 33-36°C 正常    │
  └─────────────────┴──────────┴──────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

😴 【睡眠分析】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  今日睡眠: {latest_sleep.get('total_in_bed_hours', 0):.1f} 小时
  睡眠效率: {latest_sleep.get('sleep_efficiency', 0):.1f}%
  呼吸率: {latest_sleep.get('respiratory_rate', 0):.1f} 次/分钟

  睡眠结构 (近7天平均):
  ├─ 浅睡: {light_pct:.1f}% ({light/7:.1f}h)
  ├─ 深睡: {deep_pct:.1f}% ({deep/7:.1f}h) {'✅ 充足' if deep/7 >= 1 else '⚠️ 偏少'}
  └─ REM: {rem_pct:.1f}% ({rem/7:.1f}h)

  睡眠债务: {debt:.1f} 小时 {'⚠️ 需补觉' if debt > 2 else '✅ 正常'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💪 【训练分析】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  今日strain: {latest_cycle.get('strain', 0):.1f} {'✅ 完成目标' if latest_cycle.get('strain', 0) >= 10 else '⚠️ 未达标'}
  消耗能量: {latest_cycle.get('kilojoule', 0):.0f} kJ
  平均心率: {latest_cycle.get('average_heart_rate', 0):.0f} bpm
  最高心率: {latest_cycle.get('max_heart_rate', 0):.0f} bpm

  心率区间 (近7天):
  ├─ Zone 0-1 恢复/轻松: {z01_pct:.1f}% {'✅ 有氧基础' if z01_pct > 50 else '⚠️ 偏重'}
  ├─ Zone 2-3 有氧/混氧: {z23_pct:.1f}% {'✅ 训练主力' if z23_pct > 30 else '⚠️ 偏少'}
  └─ Zone 4-5 无氧/极限: {z45_pct:.1f}% {'⚠️ 比例偏高' if z45_pct > 10 else '✅ 正常'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔮 【ML恢复预测】(未来7天)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

for i, p_val in enumerate(pred['predictions'][:7], 1):
    bar = "█" * int(p_val / 5)
    status = "🟢" if p_val >= 60 else "🟡" if p_val >= 40 else "🔴"
    print(f"  第{i}天: {p_val:5.1f}% {bar} {status}")

print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ 【HRV异常检测】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  状态: {'⚠️ 异常' if anomaly.get('is_anomaly') else '✅ 正常'}
""")

if anomaly.get('is_anomaly'):
    print(f"  变化: {anomaly.get('change_pct', 0):+.1f}%")
    print(f"  原因: {anomaly.get('reason', 'N/A')}")
    print(f"  建议: {anomaly.get('suggestion', '注意休息')}")

print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 【本周总结】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  训练天数: {weekly_stats.get('training_days', 0)}天
  平均恢复: {weekly_stats.get('avg_recovery', 0):.0f}%
  平均HRV: {weekly_stats.get('avg_hrv', 0):.0f}ms
  平均静息心率: {weekly_stats.get('avg_rhr', 0):.0f}bpm
  总strain: {weekly_stats.get('total_strain', 0):.1f}
  睡眠债务: {weekly_stats.get('sleep_debt', 0):.1f}小时

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 【综合洞察】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

insights = []
if rec < 40:
    insights.append(("🔴", "恢复评分严重偏低，需要完全休息"))
elif rec < 60:
    insights.append(("🟡", "恢复评分一般，建议降低强度"))

if latest_rec.get('hrv', 0) < 25:
    insights.append(("🔴", "HRV过低，神经系统疲劳"))

if debt > 5:
    insights.append(("🔴", f"睡眠债务{debt:.1f}小时，需要补觉"))

if z45_pct > 15:
    insights.append(("🟡", "无氧训练比例偏高，注意恢复"))

if not insights:
    insights.append(("🟢", "各项指标正常，身体状态良好"))

for emoji, text in insights:
    print(f"  {emoji} {text}")

print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 【明日建议】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

if rec >= 70:
    print("  ✅ 明日可以正常训练，甚至挑战高强度")
elif rec >= 50:
    print("  🟡 建议中等强度训练，注意监控心率")
else:
    print("  🔴 强烈建议休息或仅进行轻度活动")

if debt > 3:
    print(f"  🔴 优先补觉，保证7-8小时睡眠")

print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 【长期趋势】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  近30天数据:
  ├─ 平均恢复: {metrics.get('avg_recovery', 0):.0f}%
  ├─ 平均HRV: {metrics.get('avg_hrv', 0):.0f}ms
  ├─ 静息心率: {metrics.get('avg_rhr', 0):.0f}bpm
  ├─ 训练天数: {metrics.get('workout_count', 0)}天
  └─ 平均strain: {metrics.get('avg_strain', 0):.1f}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_数据来源: WHOOP | 健康糕_
_报告生成: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_
""")

PYEOF

echo "✅ 详细日报生成完成 $(date '+%H:%M:%S')"
