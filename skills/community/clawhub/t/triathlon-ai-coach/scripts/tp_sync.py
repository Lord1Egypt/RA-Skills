#!/usr/bin/env python3
"""
TP 数据同步脚本
自动从 TrainingPeaks 同步训练数据并更新 AI 教练配置
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# 路径配置（相对于 skill 目录）
SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = SKILL_DIR / "config.json"
TP_SCRIPT = SKILL_DIR / "scripts" / "tp.py"
PYTHON = Path.home() / ".miniconda3/bin/python3"


def sync_workouts():
    """同步最近90天的 workouts"""
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    
    cmd = f"{PYTHON} {TP_SCRIPT} workouts {start_date} {end_date} --json"
    result = os.popen(cmd).read()
    
    output_file = AI_COACH_DIR / "data" / "tp_workouts.json"
    output_file.parent.mkdir(exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(result)
    
    return json.loads(result) if result else []


def sync_fitness():
    """同步体能数据 (CTL/ATL/TSB)"""
    cmd = f"{PYTHON} {TP_SCRIPT} fitness --days 90 --json"
    result = os.popen(cmd).read()
    
    output_file = AI_COACH_DIR / "data" / "tp_fitness.json"
    with open(output_file, 'w') as f:
        f.write(result)
    
    return json.loads(result) if result else {}


def analyze_training_load(workouts):
    """分析训练负荷"""
    total_tss = 0
    total_hours = 0
    
    swim_count = 0
    bike_count = 0
    run_count = 0
    
    swim_distance = 0
    bike_distance = 0
    run_distance = 0
    
    for w in workouts:
        total_tss += w.get('tss', 0) or 0
        
        # 时长（分钟）
        duration = w.get('totalTime', 0) or 0
        total_hours += duration / 60
        
        # 按运动类型统计
        sport = (w.get('sport', '') or '').lower()
        distance = (w.get('distance', 0) or 0) / 1000  # km
        
        if 'swim' in sport:
            swim_count += 1
            swim_distance += distance
        elif 'bike' in sport or 'cycl' in sport:
            bike_count += 1
            bike_distance += distance
        elif 'run' in sport:
            run_count += 1
            run_distance += distance
    
    return {
        "total_tss": total_tss,
        "total_hours": round(total_hours, 1),
        "swim": {"count": swim_count, "distance": round(swim_distance, 2)},
        "bike": {"count": bike_count, "distance": round(bike_distance, 2)},
        "run": {"count": run_count, "distance": round(run_distance, 2)}
    }


def update_config_with_tp_data():
    """更新 AI 教练配置，融入 TP 数据"""
    
    # 同步数据
    print("正在同步 TrainingPeaks 数据...")
    workouts = sync_workouts()
    fitness = sync_fitness()
    
    print(f"✅ 同步完成: {len(workouts)} 条训练记录")
    
    # 分析训练负荷
    analysis = analyze_training_load(workouts)
    print(f"📊 统计: TSS={analysis['total_tss']}, 时长={analysis['total_hours']}h")
    print(f"🏊 游泳: {analysis['swim']['count']}次, {analysis['swim']['distance']}km")
    print(f"🚴 骑行: {analysis['bike']['count']}次, {analysis['bike']['distance']}km")
    print(f"🏃 跑步: {analysis['run']['count']}次, {analysis['run']['distance']}km")
    
    # 更新配置
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    
    config['tp_sync'] = {
        "last_sync": datetime.now().isoformat(),
        "workouts_count": len(workouts),
        "analysis": analysis,
        "fitness": fitness[:14] if isinstance(fitness, list) else []  # 最近14天
    }
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"✅ AI 教练配置已更新")
    return analysis


if __name__ == "__main__":
    update_config_with_tp_data()
