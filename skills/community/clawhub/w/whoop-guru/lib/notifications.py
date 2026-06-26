#!/usr/bin/env python3
import os
"""
Smart Notifications System
"""
import os
import json
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed', 'latest.json')

def check_notifications():
    """Check for health alerts and generate notifications"""
    with open(DATA_FILE) as f:
        data = json.load(f)
    
    processed = data.get('processed', {})
    recovery = processed.get('recovery', [])
    sleep = processed.get('sleep', [])
    
    notifications = []
    
    # Check latest recovery
    if recovery:
        latest = recovery[0]
        rec = latest.get('recovery_score', 0)
        
        if rec < 40:
            notifications.append({
                "type": "critical",
                "title": "恢复过低",
                "message": f"今日恢复仅{rec}%，建议完全休息",
                "priority": "high"
            })
        elif rec < 50:
            notifications.append({
                "type": "warning",
                "title": "恢复偏低",
                "message": f"恢复{rec}%，建议低强度活动",
                "priority": "medium"
            })
    
    # Check sleep debt
    if len(sleep) >= 7:
        sleep_hours = [s.get('total_in_bed_hours', 0) for s in sleep[:7]]
        debt = 7 * 8 - sum(sleep_hours)
        
        if debt > 10:
            notifications.append({
                "type": "critical",
                "title": "严重睡眠债务",
                "message": f"累计睡眠不足{debt:.0f}小时",
                "priority": "high"
            })
        elif debt > 5:
            notifications.append({
                "type": "warning",
                "title": "睡眠债务",
                "message": f"建议今晚多睡{debt:.0f}小时",
                "priority": "medium"
            })
    
    # Good news
    if recovery:
        rec = recovery[0].get('recovery_score', 0)
        if rec >= 70:
            notifications.append({
                "type": "success",
                "title": "状态良好",
                "message": f"恢复{rec}%，可以正常训练",
                "priority": "low"
            })
    
    result = {
        "notifications": notifications,
        "count": len(notifications),
        "checked_at": datetime.now().isoformat()
    }
    
    # Save
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed', 'notifications.json'), 'w') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    return result

result = check_notifications()
print(f"通知: {result['count']}条")
for n in result['notifications']:
    print(f"  [{n['type']}] {n['title']}: {n['message']}")
