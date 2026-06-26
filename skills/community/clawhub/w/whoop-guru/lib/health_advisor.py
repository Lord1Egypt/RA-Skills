#!/usr/bin/env python3
"""
AI Health Advisor - Intelligent health consultation
"""
import os
import json
from datetime import datetime, timedelta

# 路径配置 - 使用环境变量
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_DIR = os.environ.get("OPENCLAW_WORKSPACE", os.path.dirname(os.path.dirname(SKILL_DIR)))
PROCESSED_DIR = os.environ.get("WHOOP_DATA_DIR", os.path.join(WORKSPACE_DIR, "data", "processed"))

DATA_FILE = os.path.join(PROCESSED_DIR, 'latest.json')
PATTERNS_FILE = os.path.join(PROCESSED_DIR, 'patterns.json')

def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)

def analyze_current_state():
    """Analyze current health state"""
    data = load_data()
    processed = data.get('processed', {})
    
    recovery = processed.get('recovery', [])
    sleep = processed.get('sleep', [])
    cycles = processed.get('cycles', [])
    workouts = processed.get('workouts', [])
    
    # Get recent 7 days
    recent_rec = recovery[:7]
    recent_sleep = sleep[:7]
    recent_cycles = cycles[:7]
    
    # Calculate averages
    rec_scores = [r.get('recovery_score', 0) for r in recent_rec if r.get('recovery_score')]
    hrv_values = [r.get('hrv', 0) for r in recent_rec if r.get('hrv')]
    rhr_values = [r.get('rhr', 0) for r in recent_rec if r.get('rhr')]
    
    sleep_hours = [s.get('total_in_bed_hours', 0) for s in recent_sleep if s.get('total_in_bed_hours')]
    sleep_perf = [s.get('sleep_performance', 0) for s in recent_sleep if s.get('sleep_performance')]
    
    strain_values = [c.get('strain', 0) for c in recent_cycles if c.get('strain')]
    
    return {
        "recovery": {
            "avg": sum(rec_scores)/len(rec_scores) if rec_scores else 0,
            "current": rec_scores[0] if rec_scores else 0,
            "hrv": sum(hrv_values)/len(hrv_values) if hrv_values else 0,
            "rhr": sum(rhr_values)/len(rhr_values) if rhr_values else 0,
            "trend": "up" if len(rec_scores) > 1 and rec_scores[0] > rec_scores[1] else "down"
        },
        "sleep": {
            "avg_hours": sum(sleep_hours)/len(sleep_hours) if sleep_hours else 0,
            "avg_perf": sum(sleep_perf)/len(sleep_perf) if sleep_perf else 0,
            "sleep_debt": max(0, 7*8 - sum(sleep_hours))
        },
        "training": {
            "avg_strain": sum(strain_values)/len(strain_values) if strain_values else 0,
            "workout_count": len(workouts)
        }
    }

def get_training_recommendation(state):
    """Get training recommendation based on recovery and sleep"""
    rec = state["recovery"]["avg"]
    sleep_hours = state["sleep"]["avg_hours"]
    hrv = state["recovery"]["hrv"]
    
    if rec >= 70 and sleep_hours >= 7:
        return {
            "level": "high",
            "message": "状态良好，可以进行正常强度训练",
            "activities": ["跑步 10-15km", "力量训练", "HIIT"],
            "emoji": "💪"
        }
    elif rec >= 50 and sleep_hours >= 6:
        return {
            "level": "medium",
            "message": "状态一般，建议低强度活动",
            "activities": ["轻松跑步 5-8km", "瑜伽", "拉伸"],
            "emoji": "🟡"
        }
    elif rec >= 30:
        return {
            "level": "low",
            "message": "需要休息，建议轻度活动",
            "activities": ["散步", "轻度拉伸"],
            "emoji": "🔴"
        }
    else:
        return {
            "level": "rest",
            "message": "身体需要恢复，建议完全休息",
            "activities": ["充足睡眠", "避免运动"],
            "emoji": "😴"
        }

def get_sleep_advice(state):
    """Get personalized sleep advice"""
    sleep_hours = state["sleep"]["avg_hours"]
    sleep_debt = state["sleep"]["sleep_debt"]
    sleep_perf = state["sleep"]["avg_perf"]
    
    advice = []
    
    if sleep_debt > 10:
        advice.append("🔴 严重睡眠债务: 建议连续2-3天8小时睡眠")
    elif sleep_debt > 5:
        advice.append("🟡 存在睡眠债务: 建议今晚提前1小时入睡")
    
    if sleep_hours < 6:
        advice.append("🟡 睡眠时长不足: 目标每晚7-8小时")
    
    if sleep_perf < 70:
        advice.append("🟡 睡眠质量欠佳: 睡前1小时远离电子设备")
    
    if not advice:
        advice.append("✅ 睡眠状态良好，保持当前作息")
    
    return advice

def generate_health_report():
    """Generate comprehensive health report"""
    state = analyze_current_state()
    
    # Get recommendations
    training_rec = get_training_recommendation(state)
    sleep_advice = get_sleep_advice(state)
    
    # Determine overall health score
    rec_score = state["recovery"]["avg"]
    sleep_score = state["sleep"]["avg_perf"]
    hrv = state["recovery"]["hrv"]
    
    # Calculate composite score
    if hrv >= 50 and rec_score >= 70:
        overall = 90
    elif hrv >= 40 and rec_score >= 60:
        overall = 75
    elif rec_score >= 50:
        overall = 60
    else:
        overall = 40
    
    report = {
        "generated_at": datetime.now().isoformat(),
        "overall_score": overall,
        "state": state,
        "training_recommendation": training_rec,
        "sleep_advice": sleep_advice,
        "insights": generate_insights(state)
    }
    
    # Save
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed', 'health_advisor.json'), 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    return report

def generate_insights(state):
    """Generate personalized insights"""
    insights = []
    
    # Recovery insights
    rec = state["recovery"]["avg"]
    if rec < 50:
        insights.append(f"恢复状态偏低({rec:.0f}%)，注意身体休息")
    elif rec > 70:
        insights.append(f"恢复状态良好({rec:.0f}%)，可以保持当前训练")
    
    # HRV insights
    hrv = state["recovery"]["hrv"]
    if hrv < 30:
        insights.append(f"HRV偏低({hrv:.0f}ms)，建议减少压力")
    elif hrv > 50:
        insights.append(f"HRV优秀({hrv:.0f}ms)，心肺功能良好")
    
    # Training insights
    strain = state["training"]["avg_strain"]
    if strain > 15:
        insights.append(f"近期训练强度偏高(strain {strain:.1f})，注意轮休")
    elif strain < 5:
        insights.append("活动量较低，可适当增加运动")
    
    return insights

def ask_question(question):
    """Answer health questions"""
    report = generate_health_report()
    state = report["state"]
    
    q = question.lower()
    
    # Recovery related
    if "恢复" in q or "recovery" in q:
        if "今天" in q or "现在" in q or "current" in q:
            rec = state["recovery"]["current"]
            return f"今日恢复: {rec:.0f}%"
        return f"近期平均恢复: {state['recovery']['avg']:.0f}%"
    
    # Training related
    if "训练" in q or "运动" in q or "跑" in q:
        rec = get_training_recommendation(state)
        return f"{rec['emoji']} {rec['message']} - 推荐: {', '.join(rec['activities'])}"
    
    # Sleep related
    if "睡眠" in q or "sleep" in q:
        return f"平均睡眠: {state['sleep']['avg_hours']:.1f}h, 睡眠债务: {state['sleep']['sleep_debt']:.1f}h"
    
    # HRV related
    if "hrv" in q:
        return f"平均HRV: {state['recovery']['hrv']:.1f}ms"
    
    # Overall
    if "怎么样" in q or "如何" in q or "how" in q:
        return f"综合健康分: {report['overall_score']}/100\n" + "\n".join(report["insights"])
    
    return "抱歉，我不太明白。你可以直接问:恢复、训练、睡眠、HRV等"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        answer = ask_question(question)
        print(f"Q: {question}")
        print(f"A: {answer}")
    else:
        report = generate_health_report()
        print(f"综合健康分: {report['overall_score']}/100")
        print(f"训练建议: {report['training_recommendation']['message']}")
