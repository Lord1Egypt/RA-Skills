#!/usr/bin/env python3
"""
ML Prediction Model - Advanced prediction using simple ML
"""
import os
import json
import math
from datetime import datetime, timedelta

# 路径配置 - 使用环境变量
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_DIR = os.environ.get("OPENCLAW_WORKSPACE", os.path.dirname(os.path.dirname(SKILL_DIR)))
PROCESSED_DIR = os.environ.get("WHOOP_DATA_DIR", os.path.join(WORKSPACE_DIR, "data", "processed"))

DATA_FILE = os.path.join(PROCESSED_DIR, 'latest.json')

def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)

def prepare_features(data):
    """Prepare features for ML model"""
    processed = data.get('processed', {})
    recovery = processed.get('recovery', [])
    sleep = processed.get('sleep', [])
    cycles = processed.get('cycles', [])
    
    # Build feature matrix
    X = []  # Features: [prev_recovery, prev_sleep, prev_strain, day_of_week]
    y = []  # Target: next_day_recovery
    
    # Align by date
    sleep_dict = {s['date']: s for s in sleep}
    cycle_dict = {c['date']: c for c in cycles}
    
    for i in range(1, len(recovery)):
        prev = recovery[i-1]
        curr = recovery[i]
        
        date = curr.get('date', '')
        
        # Features
        prev_rec = prev.get('recovery_score', 50)
        prev_sleep = sleep_dict.get(date, {}).get('total_in_bed_hours', 7)
        prev_strain = cycle_dict.get(date, {}).get('strain', 5)
        
        # Day of week (0=Monday)
        try:
            dow = datetime.strptime(date, "%Y-%m-%d").weekday()
        except:
            dow = 3
        
        X.append([prev_rec, prev_sleep, prev_strain, dow])
        y.append(curr.get('recovery_score', 50))
    
    return X, y

def predict_linear_regression(X, y, features):
    """Simple linear regression prediction"""
    if len(X) < 3:
        return 50  # Not enough data
    
    # Simple moving average with weights
    n = min(5, len(y))
    weights = [0.4, 0.25, 0.15, 0.1, 0.1]  # Recent weights
    
    pred = 0
    for i in range(n):
        idx = len(y) - n + i
        pred += y[idx] * weights[i]
    
    return max(0, min(100, pred))

def predict_next_day():
    """Predict next day's recovery"""
    data = load_data()
    X, y = prepare_features(data)
    
    if not y:
        return {"prediction": 50, "confidence": "low", "reason": "数据不足"}
    
    # Get latest features
    processed = data.get('processed', {})
    recovery = processed.get('recovery', [])
    sleep = processed.get('sleep', [])
    cycles = processed.get('cycles', [])
    
    if recovery:
        prev_rec = recovery[0].get('recovery_score', 50)
        prev_sleep = sleep[0].get('total_in_bed_hours', 7) if sleep else 7
        prev_strain = cycles[0].get('strain', 5) if cycles else 5
        
        prediction = predict_linear_regression(X[-5:] if len(X) >= 5 else X, 
                                             y[-5:] if len(y) >= 5 else y,
                                             [prev_rec, prev_sleep, prev_strain, 3])
        
        # Determine confidence
        if len(y) >= 14:
            confidence = "high"
        elif len(y) >= 7:
            confidence = "medium"
        else:
            confidence = "low"
        
        # Generate reason
        if prediction >= 70:
            reason = "身体状态良好，预计恢复不错"
        elif prediction >= 50:
            reason = "状态一般，需要注意"
        else:
            reason = "恢复偏低，建议休息"
        
        return {
            "prediction": round(prediction, 1),
            "confidence": confidence,
            "reason": reason,
            "based_on_data": len(y)
        }
    
    return {"prediction": 50, "confidence": "low", "reason": "数据不足"}

def get_training_advice(prediction):
    """Get training advice based on prediction"""
    if prediction >= 70:
        return "可以进行正常强度训练"
    elif prediction >= 50:
        return "建议低强度活动或休息"
    else:
        return "建议完全休息"

if __name__ == "__main__":
    result = predict_next_day()
    print(f"预测恢复: {result['prediction']}%")
    print(f"置信度: {result['confidence']}")
    print(f"原因: {result['reason']}")
    print(f"训练建议: {get_training_advice(result['prediction'])}")
