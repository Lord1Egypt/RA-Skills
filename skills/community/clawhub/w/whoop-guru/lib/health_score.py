#!/usr/bin/env python3
"""
Health Score System - For Whoop Guru Skill
"""
import os
import json

# 路径配置 - 使用环境变量
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_DIR = os.environ.get("OPENCLAW_WORKSPACE", os.path.dirname(os.path.dirname(SKILL_DIR)))
PROCESSED_DIR = os.environ.get("WHOOP_DATA_DIR", os.path.join(WORKSPACE_DIR, "data", "processed"))

DATA_FILE = os.environ.get('WHOOP_DATA_DIR', os.path.join(PROCESSED_DIR, 'latest.json'))
OUTPUT_FILE = os.path.join(PROCESSED_DIR, 'health_score.json')

def calculate_health_score():
    try:
        with open(DATA_FILE) as f:
            data = json.load(f)
    except:
        return {"score": 0, "grade": "N/A"}
    
    processed = data.get('processed', {})
    recovery = processed.get('recovery', [])
    sleep = processed.get('sleep', [])
    
    recent_rec = [r.get('recovery_score', 0) for r in recovery[:7] if r.get('recovery_score')]
    recent_sleep = [s.get('sleep_performance', 0) for s in sleep[:7] if s.get('sleep_performance')]
    recent_hrv = [r.get('hrv', 0) for r in recovery[:7] if r.get('hrv')]
    recent_rhr = [r.get('rhr', 0) for r in recovery[:7] if r.get('rhr')]
    
    if not recent_rec:
        return {"score": 0, "grade": "N/A"}
    
    rec_score = sum(recent_rec) / len(recent_rec)
    sleep_score = sum(recent_sleep) / len(recent_sleep) if recent_sleep else 50
    avg_hrv = sum(recent_hrv) / len(recent_hrv) if recent_hrv else 40
    avg_rhr = sum(recent_rhr) / len(recent_rhr) if recent_rhr else 60
    
    hrv_score = min(100, avg_hrv * 2)
    rhr_score = max(0, 100 - (avg_rhr - 50) * 5)
    
    total_score = rec_score * 0.4 + sleep_score * 0.3 + hrv_score * 0.2 + rhr_score * 0.1
    
    if total_score >= 90: grade = "A+"
    elif total_score >= 85: grade = "A"
    elif total_score >= 80: grade = "A-"
    elif total_score >= 70: grade = "B"
    elif total_score >= 60: grade = "C"
    else: grade = "D"
    
    result = {
        "score": round(total_score, 1),
        "grade": grade,
        "breakdown": {
            "recovery": round(rec_score, 1),
            "sleep": round(sleep_score, 1),
            "hrv": round(hrv_score, 1),
            "rhr": round(rhr_score, 1)
        }
    }
    
    try:
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(result, f, indent=2)
    except:
        pass
    
    return result

if __name__ == "__main__":
    result = calculate_health_score()
    print(f"综合健康分: {result['score']}/100 ({result['grade']})")
    print(f"恢复: {result['breakdown']['recovery']} (40%)")
    print(f"睡眠: {result['breakdown']['sleep']} (30%)")
    print(f"HRV: {result['breakdown']['hrv']} (20%)")
    print(f"心率: {result['breakdown']['rhr']} (10%)")
