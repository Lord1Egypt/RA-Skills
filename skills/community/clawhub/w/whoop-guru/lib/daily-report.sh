#!/bin/bash
# Daily Report - 08:00 早间健康报告
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
from lib.ml import get_recovery_prediction

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

# ========== HRV ==========
hrv = latest_rec.get('hrv', 0)
if hrv >= 60:
    hrv_status = "优秀"
elif hrv >= 40:
    hrv_status = "正常"
elif hrv >= 25:
    hrv_status = "偏低"
else:
    hrv_status = "过低"

# ========== 睡眠 ==========
sleep_hours = latest_sleep.get('total_in_bed_hours', 0) if latest_sleep else 0
sleep_eff = latest_sleep.get('sleep_efficiency', 0) if latest_sleep else 0
rr = latest_sleep.get('respiratory_rate', 0) if latest_sleep else 0

# 睡眠债务
sleep_hours_14 = [s.get('total_in_bed_hours', 0) for s in sleep_list[:14]]
debt = 14 * 8 - sum(sleep_hours_14)

# 睡眠结构
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

# ========== 健康评分 ==========
hrv_avg = sum(r.get('hrv', 0) for r in recovery_list[:7]) / min(7, len(recovery_list)) if recovery_list else 0
rhr_avg = sum(r.get('rhr', 0) for r in recovery_list[:7]) / min(7, len(recovery_list)) if recovery_list else 0
hrv_score = min(100, hrv_avg * 2)
rhr_score = max(0, 100 - (rhr_avg - 50) * 5)
rec_avg = metrics.get('avg_recovery', 0)
sleep_avg = metrics.get('avg_sleep_hours', 0)
total_score = rec_avg * 0.4 + sleep_avg * 0.3 + hrv_score * 0.2 + rhr_score * 0.1

print(f"""
╔══════════════════════════════════════════════════════════════╗
║          🏥 WHOOP GURU 每日健康简报                    ║
║                    {date}                         ║
╚══════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔋 【身体电量】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⚡ {battery:.0f}% {battery_level}
  
  恢复贡献: {rec:.0f}% × 0.6 = {rec * 0.6:.1f}
  睡眠贡献: {sp:.0f}% × 0.4 = {sp * 0.4:.1f}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🫀 【今日状态】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ┌─────────────────┬──────────┬──────────┐
  │ 指标            │ 数值     │ 状态     │
  ├─────────────────┼──────────┼──────────┤
  │ 恢复分数        │ {rec:.0f}%      │ {'✅ 良好' if rec >= 60 else '⚠️ 注意'} │
  │ HRV             │ {hrv:.0f} ms   │ {'✅ 正常' if hrv >= 40 else '⚠️ 偏低'} │
  │ 静息心率        │ {latest_rec.get('rhr', 0):.0f} bpm   │ ✅       │
  │ 血氧饱和度      │ {latest_rec.get('spo2', 0):.1f}%   │ {'✅ 正常' if latest_rec.get('spo2', 0) >= 95 else '⚠️ 低'} │
  │ 皮肤温度        │ {latest_rec.get('skin_temp', 0):.1f}°C   │ {'✅ 正常' if 33 <= latest_rec.get('skin_temp', 35) <= 36 else '⚠️ 异常'} │
  └─────────────────┴──────────┴──────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

😴 【睡眠分析】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  睡眠时长: {sleep_hours:.1f} 小时
  睡眠效率: {sleep_eff:.1f}%
  呼吸率: {rr:.1f} 次/分钟 ({'正常' if 12 <= rr <= 20 else '偏高/偏低'})

  睡眠结构 (近7天平均):
  ├─ 浅睡: {light_pct:.1f}% ({light/7:.1f}h)
  ├─ 深睡: {deep_pct:.1f}% ({deep/7:.1f}h)
  └─ REM: {rem_pct:.1f}% ({rem/7:.1f}h)

  睡眠债务: {debt:.1f} 小时 {'⚠️ 需补觉' if debt > 2 else '✅ 正常'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💪 【训练分析】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  今日strain: {latest_cycle.get('strain', 0):.1f}
  消耗能量: {latest_cycle.get('kilojoule', 0):.0f} kJ
  平均心率: {latest_cycle.get('average_heart_rate', 0):.0f} bpm
  最高心率: {latest_cycle.get('max_heart_rate', 0):.0f} bpm

  心率区间分布 (近7天):
  ├─ Zone 0-1 恢复/轻松: {z01_pct:.1f}%
  ├─ Zone 2-3 有氧/混氧: {z23_pct:.1f}%
  └─ Zone 4-5 无氧/极限: {z45_pct:.1f}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 【健康趋势】(7天平均)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  恢复评分: {rec_avg:.0f}% {'📈 上升' if rec_avg >= 60 else '📉 下降'}
  HRV: {hrv_avg:.0f}ms ({'✅ 正常' if hrv_avg >= 40 else '⚠️ 偏低'})
  静息心率: {rhr_avg:.0f}bpm ({'✅ 良好' if rhr_avg <= 60 else '⚠️ 偏高'})
  训练天数: {metrics.get('workout_count', 0)}天

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 【健康洞察】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

# 洞察
insights = []
if rec < 40:
    insights.append("🔴 恢复评分明显偏低，身体疲劳累积严重，建议增加休息")
elif rec < 60:
    insights.append("🟡 恢复评分一般，注意训练强度，适当降低")
else:
    insights.append("🟢 恢复评分良好，身体状态不错")

if hrv < 25:
    insights.append("🔴 HRV严重偏低，神经系统疲劳过度，需要完全休息")
elif hrv < 40:
    insights.append("🟡 HRV偏低，可能存在压力或恢复不足")

if debt > 5:
    insights.append(f"🔴 睡眠债务积累 {debt:.1f}小时，需要增加睡眠时间")
elif debt > 2:
    insights.append(f"🟡 存在 {debt:.1f}小时睡眠债务，建议适当补觉")

if latest_rec.get('rhr', 0) > 65:
    insights.append("🔴 静息心率偏高，可能存在过度训练")

for i in insights:
    print(f"  {i}")

print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 【今日建议】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

# 建议
if rec >= 70:
    print("  ✅ 身体状态优秀，可以进行高强度训练")
elif rec >= 50:
    print("  🟡 身体状态一般，建议进行中低强度训练")
else:
    print("  🔴 恢复不足，建议完全休息或仅进行轻度活动")

if debt > 5:
    print(f"  🔴 睡眠债务较重，优先保证充足睡眠")
elif debt > 2:
    print(f"  🟡 有一定睡眠债务，注意今晚睡眠时间")

print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 【数据说明】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  恢复评分: 基于HRV、静息心率、睡眠质量综合计算
  身体电量: 恢复60% + 睡眠40%的加权值
  HRV: 心率变异性，越高表示恢复越好
  睡眠债务: 近14天睡眠缺口累积

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

PYEOF

echo "✅ 早间报告生成完成 $(date '+%H:%M:%S')"
