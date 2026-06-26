#!/usr/bin/env python3
import os
"""
Enhanced Health Report - Full features
"""
import json
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed', 'latest.json')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')

def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)

def calculate_health_score(recovery, sleep):
    """Calculate overall health score"""
    if not recovery or not sleep:
        return 0, "N/A"
    
    rec_avg = sum(r.get('recovery_score', 0) for r in recovery[:7]) / min(7, len(recovery))
    sleep_avg = sum(s.get('sleep_performance', 0) for s in sleep[:7]) / min(7, len(sleep))
    hrv_avg = sum(r.get('hrv', 0) for r in recovery[:7]) / min(7, len(recovery))
    rhr_avg = sum(r.get('rhr', 0) for r in recovery[:7]) / min(7, len(recovery))
    
    hrv_score = min(100, hrv_avg * 2)
    rhr_score = max(0, 100 - (rhr_avg - 50) * 5)
    
    total = rec_avg * 0.4 + sleep_avg * 0.3 + hrv_score * 0.2 + rhr_score * 0.1
    
    if total >= 90: grade = "A+"
    elif total >= 85: grade = "A"
    elif total >= 80: grade = "A-"
    elif total >= 70: grade = "B"
    elif total >= 60: grade = "C"
    else: grade = "D"
    
    return round(total, 1), grade

def get_heart_zone_emoji(zone):
    """Get emoji for heart rate zone"""
    zones = {
        "zone0": "🟢 Zone 0 (恢复)",
        "zone1": "🟢 Zone 1 (轻松)",
        "zone2": "🟡 Zone 2 (有氧)",
        "zone3": "🟠 Zone 3 (混氧)",
        "zone4": "🔴 Zone 4 (无氧)",
        "zone5": "🔴 Zone 5 (极限)"
    }
    return zones.get(zone, zone)

def generate_morning_report():
    """Generate comprehensive morning report"""
    data = load_data()
    processed = data.get('processed', {})
    
    recovery = processed.get('recovery', [])
    sleep = processed.get('sleep', [])
    cycles = processed.get('cycles', [])
    workouts = processed.get('workouts', [])
    
    # Latest data
    latest_rec = recovery[0] if recovery else {}
    latest_sleep = sleep[0] if sleep else {}
    latest_cycle = cycles[0] if cycles else {}
    
    # Health Score
    score, grade = calculate_health_score(recovery, sleep)
    
    # Sleep debt
    sleep_hours = [s.get('total_in_bed_hours', 0) for s in sleep[:14]]
    debt = 14 * 8 - sum(sleep_hours)
    
    # Heart rate zones
    zones = {"zone0": 0, "zone1": 0, "zone2": 0, "zone3": 0, "zone4": 0, "zone5": 0}
    for w in workouts[:7]:
        for z in range(6):
            zones[f"zone{z}"] += w.get(f"zone{z}_min", 0)
    total_zone = sum(zones.values())
    zone_pcts = {k: round(v/total_zone*100, 1) if total_zone > 0 else 0 for k, v in zones.items()}
    
    # Sleep stages
    light = sum(s.get('light_sleep_hours', 0) for s in sleep[:7])
    deep = sum(s.get('deep_sleep_hours', 0) for s in sleep[:7])
    rem = sum(s.get('rem_sleep_hours', 0) for s in sleep[:7])
    total_sleep_hours = light + deep + rem
    if total_sleep_hours > 0:
        light_pct = round(light/total_sleep_hours*100, 1)
        deep_pct = round(deep/total_sleep_hours*100, 1)
        rem_pct = round(rem/total_sleep_hours*100, 1)
    
    # Body battery
    rec = latest_rec.get('recovery_score', 50)
    sp = latest_sleep.get('sleep_performance', 70)
    battery = round(rec * 0.6 + sp * 0.4, 1)
    if battery >= 80: battery_level = "满格 🟢"
    elif battery >= 60: battery_level = "良好 🟡"
    elif battery >= 40: battery_level = "一般 🟠"
    else: battery_level = "需充电 🔴"
    
    # Respiratory rate
    rr = latest_sleep.get('respiratory_rate', 0)
    
    # Generate report
    date = datetime.now().strftime("%Y-%m-%d")
    report = f"""📊 **健康日报** - {date}

---

### 🔋 身体电量

**{battery_level}** ({battery}%)

---

### 🫀 今日状态

| 指标 | 数值 | 状态 |
|------|------|------|
| 恢复分数 | {latest_rec.get('recovery_score', 'N/A')}% | {'✅' if latest_rec.get('recovery_score', 0) >= 60 else '⚠️'} |
| HRV | {latest_rec.get('hrv', 'N/A')} ms | {'✅' if latest_rec.get('hrv', 0) >= 40 else '⚠️'} |
| 静息心率 | {latest_rec.get('rhr', 'N/A')} bpm | ✅ |
| 血氧 | {latest_rec.get('spo2', 'N/A')}% | ✅ |
| 皮肤温度 | {latest_rec.get('skin_temp', 'N/A')}°C | ✅ |

---

### 😴 睡眠分析

| 指标 | 数值 |
|------|------|
| 睡眠时长 | {latest_sleep.get('total_in_bed_hours', 'N/A')} h |
| 睡眠效率 | {latest_sleep.get('sleep_efficiency', 'N/A')}% |
| 呼吸率 | {rr} ({"正常" if 12 <= rr <= 20 else "异常"}) |

**睡眠结构:**
- 浅睡: {light_pct if total_sleep_hours > 0 else 0}% ({round(light/7, 1) if total_sleep_hours > 0 else 0}h)
- 深睡: {deep_pct if total_sleep_hours > 0 else 0}% ({round(deep/7, 1) if total_sleep_hours > 0 else 0}h)
- REM: {rem_pct if total_sleep_hours > 0 else 0}% ({round(rem/7, 1) if total_sleep_hours > 0 else 0}h)

**睡眠债务:** {round(debt, 1)} 小时

---

### 💪 训练分析

**今日 Strain:** {latest_cycle.get('strain', 'N/A')}
**消耗:** {latest_cycle.get('kilojoules', 'N/A')} kJ

**心率区间 (近7次训练):**
| 区间 | 比例 |
|------|------|
| Zone 0-1 (恢复/轻松) | {zone_pcts.get('zone0', 0) + zone_pcts.get('zone1', 0)}% |
| Zone 2-3 (有氧/混氧) | {zone_pcts.get('zone2', 0) + zone_pcts.get('zone3', 0)}% |
| Zone 4-5 (无氧/极限) | {zone_pcts.get('zone4', 0) + zone_pcts.get('zone5', 0)}% |

---

### 📈 健康评分

| 维度 | 分数 |
|------|------|
| 恢复 | {round(sum(r.get('recovery_score', 0) for r in recovery[:7])/min(7, len(recovery)), 1) if recovery else 0} |
| 睡眠 | {round(sum(s.get('sleep_performance', 0) for s in sleep[:7])/min(7, len(sleep)), 1) if sleep else 0} |
| HRV | {round(min(100, sum(r.get('hrv', 0) for r in recovery[:7])/min(7, len(recovery)) * 2), 1) if recovery else 0} |
| 心率 | {round(max(0, 100 - (sum(r.get('rhr', 0) for r in recovery[:7])/min(7, len(recovery)) - 50) * 5), 1) if recovery else 0} |

**总分: {score}/100 ({grade})**

---

### 💡 建议

"""
    
    # Recommendations based on data
    if rec >= 70:
        report += "- ✅ 恢复良好，可以正常训练\n"
    elif rec >= 50:
        report += "- 🟡 恢复一般，建议低强度活动\n"
    else:
        report += "- 🔴 恢复偏低，建议休息\n"
    
    if debt > 10:
        report += f"- 🔴 睡眠债务较重 ({round(debt, 1)}h)，注意补觉\n"
    
    if zone_pcts.get('zone4', 0) + zone_pcts.get('zone5', 0) > 10:
        report += "- 🟡 无氧训练比例较高，注意恢复\n"
    
    report += "\n---\n_数据来源: WHOOP | 健康糕_"
    
    return report

def generate_detailed_report():
    """Generate detailed report"""
    # Similar but more detailed version
    return generate_morning_report()  # For now, same as morning

if __name__ == "__main__":
    import sys
    
    report_type = sys.argv[1] if len(sys.argv) > 1 else "morning"
    date = datetime.now().strftime("%Y-%m-%d")
    
    if report_type == "morning":
        content = generate_morning_report()
        filename = f"{OUTPUT_DIR}/report_morning_{date}.md"
    else:
        content = generate_detailed_report()
        filename = f"{OUTPUT_DIR}/report_detailed_{date}.md"
    
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"✅ Report saved: {filename}")
