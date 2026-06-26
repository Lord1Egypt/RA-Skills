#!/usr/bin/env python3
"""
Check-in Reminder Push - 20:00
训练打卡提醒

推送内容包含：
- 今日训练状态
- 打卡重要性说明
- 打卡格式示例
- 恢复提示
"""

import os
import sys
import json
import subprocess
from datetime import datetime

sys.path.insert(0, "/root/.openclaw/workspace-healthgao/skill/whoop-guru")

from lib.pusher import CoachPushMessage

SKILL_DIR = "/root/.openclaw/workspace-healthgao/skill/whoop-guru"
WORKSPACE_DIR = "/root/.openclaw/workspace-healthgao"
PROCESSED_DIR = os.path.join(WORKSPACE_DIR, "data", "processed")
OUTPUT_FILE = os.path.join(SKILL_DIR, "data", "logs", "checkin_push.json")


def refresh_whoop_data():
    """拉取WHOOP最新数据并写入latest.json"""
    try:
        result = subprocess.run(
            ["python3", f"{SKILL_DIR}/scripts/whoop_data.py", "summary", "--days", "7"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            return False
        
        api_data = json.loads(result.stdout)
        
        recovery_records = api_data.get("recovery", {}).get("records", [])
        processed_recovery = []
        for r in recovery_records:
            score = r.get("score", {})
            # recovery has no start field, use created_at
            created_at = r.get("created_at", "") or r.get("start", "")
            date = created_at[:10] if created_at else "Unknown"
            hrv_val = score.get("hrv_rmssd_milli")
            skin_val = score.get("skin_temp_celsius")
            processed_recovery.append({
                "date": date,
                "datetime": created_at,
                "recovery_score": score.get("recovery_score", 0),
                "hrv": round(hrv_val, 1) if hrv_val is not None else None,
                "rhr": score.get("resting_heart_rate", 0),
                "spo2": score.get("spo2_percentage", 0),
                "skin_temp": round(skin_val, 1) if skin_val is not None else None,
                "user_calibrating": score.get("user_calibrating", False)
            })
        
        sleep_records = api_data.get("sleep", {}).get("records", [])
        processed_sleep = []
        for r in sleep_records:
            score = r.get("score", {})
            stage = score.get("stage_summary", {})
            start = r.get("start", "")
            date = start[:10] if start else "Unknown"
            in_bed_ms = stage.get("total_in_bed_time_milli", 0)
            awake_ms = stage.get("total_awake_time_milli", 0)
            processed_sleep.append({
                "date": date,
                "total_in_bed_hours": round((in_bed_ms - awake_ms) / 3600000, 1),
                "sleep_performance": score.get("sleep_performance_percentage", 0),
                "sleep_efficiency": score.get("sleep_efficiency_percentage", 0),
                "respiratory_rate": score.get("respiratory_rate", 0),
                "light_sleep_hours": round(stage.get("total_light_sleep_time_milli", 0) / 3600000, 1),
                "deep_sleep_hours": round(stage.get("total_slow_wave_sleep_time_milli", 0) / 3600000, 1),
                "rem_sleep_hours": round(stage.get("total_rem_sleep_time_milli", 0) / 3600000, 1),
                "disturbances": stage.get("disturbance_count", 0)
            })
        
        cycle_records = api_data.get("cycles", {}).get("records", [])
        processed_cycles = []
        for r in cycle_records:
            score = r.get("score", {})
            start = r.get("start", "")
            date = start[:10] if start else "Unknown"
            processed_cycles.append({
                "date": date,
                "strain": score.get("strain", 0),
                "kilojoules": score.get("kilojoule", 0),
                "avg_hr": score.get("average_heart_rate", 0),
                "max_hr": score.get("max_heart_rate", 0)
            })
        
        rec_scores = [r["recovery_score"] for r in processed_recovery if r["recovery_score"]]
        hrv_vals = [r["hrv"] for r in processed_recovery if r["hrv"]]
        rhr_vals = [r["rhr"] for r in processed_recovery if r["rhr"]]
        sleep_perfs = [r["sleep_performance"] for r in processed_sleep if r["sleep_performance"]]
        
        metrics = {
            "avg_recovery": round(sum(rec_scores)/len(rec_scores), 1) if rec_scores else 0,
            "avg_hrv": round(sum(hrv_vals)/len(hrv_vals), 1) if hrv_vals else 0,
            "avg_rhr": round(sum(rhr_vals)/len(rhr_vals), 1) if rhr_vals else 0,
            "avg_sleep_performance": round(sum(sleep_perfs)/len(sleep_perfs), 1) if sleep_perfs else 0,
            "recovery_count": len(processed_recovery),
            "sleep_count": len(processed_sleep),
        }
        
        output = {
            "date": processed_recovery[0]["date"] if processed_recovery else None,
            "processed": {
                "recovery": processed_recovery,
                "sleep": processed_sleep,
                "cycles": processed_cycles,
            },
            "metrics": metrics,
            "updated_at": datetime.now().isoformat()
        }
        
        os.makedirs(PROCESSED_DIR, exist_ok=True)
        with open(os.path.join(PROCESSED_DIR, "latest.json"), "w") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"Data refresh error: {e}", file=sys.stderr)
        return False


def generate_checkin_push():
    """生成打卡提醒"""
    
    # 先刷新WHOOP数据
    refresh_whoop_data()
    
    # 使用增强版的推送消息
    message = CoachPushMessage.checkin_reminder()
    
    # 保存推送记录
    result = {
        "type": "checkin_reminder",
        "timestamp": datetime.now().isoformat(),
        "message": message
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # 打印消息供Telegram发送
    print(message)
    
    return result


if __name__ == "__main__":
    generate_checkin_push()
