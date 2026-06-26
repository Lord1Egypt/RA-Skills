#!/usr/bin/env python3
"""
收入实验追踪器 - 记录和管理各种赚钱尝试

用法:
    # 初始化实验室
    python experiment_tracker.py init --name "我的收入实验"
    
    # 添加新实验
    python experiment_tracker.py add --name "蜂鸟众包" --type tier1 --duration 7 --time-budget 2 --income-target 100
    
    # 记录每日数据
    python experiment_tracker.py log --experiment "蜂鸟众包" --date 2025-03-26 --hours 2 --income 35
    
    # 查看实验状态
    python experiment_tracker.py status
    
    # 结束实验并复盘
    python experiment_tracker.py complete --experiment "蜂鸟众包" --success true --lessons "时薪太低，需要转型"
"""

import argparse
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List
import csv

DATA_DIR = os.path.expanduser("~/.income-lab")
EXPERIMENTS_FILE = os.path.join(DATA_DIR, "experiments.json")
LOGS_FILE = os.path.join(DATA_DIR, "daily_logs.json")


def ensure_data_dir():
    """确保数据目录存在"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_data(filepath: str) -> dict:
    """加载JSON数据"""
    if not os.path.exists(filepath):
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_data(filepath: str, data: dict):
    """保存JSON数据"""
    ensure_data_dir()
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def init_lab(name: str):
    """初始化收入实验室"""
    ensure_data_dir()
    config = {
        "name": name,
        "created_at": datetime.now().isoformat(),
        "total_experiments": 0,
        "total_income": 0,
        "total_hours": 0
    }
    save_data(os.path.join(DATA_DIR, "config.json"), config)
    save_data(EXPERIMENTS_FILE, {})
    save_data(LOGS_FILE, {})
    print(f"[✓] 已创建收入实验室: {name}")
    print(f"[✓] 数据存储在: {DATA_DIR}")


def add_experiment(name: str, exp_type: str, duration: int, time_budget: float, income_target: float, notes: str = ""):
    """添加新实验"""
    experiments = load_data(EXPERIMENTS_FILE)
    
    experiment_id = f"exp_{len(experiments) + 1:03d}"
    
    experiments[experiment_id] = {
        "id": experiment_id,
        "name": name,
        "type": exp_type,
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "duration_days": duration,
        "time_budget_hours_per_day": time_budget,
        "income_target": income_target,
        "notes": notes,
        "total_hours": 0,
        "total_income": 0,
        "daily_logs": []
    }
    
    save_data(EXPERIMENTS_FILE, experiments)
    
    print(f"[✓] 已添加实验: {name}")
    print(f"  ID: {experiment_id}")
    print(f"  类型: {exp_type}")
    print(f"  周期: {duration}天")
    print(f"  每日时间预算: {time_budget}小时")
    print(f"  收入目标: ¥{income_target}")


def log_daily(experiment_id: str, date: str, hours: float, income: float, notes: str = ""):
    """记录每日数据"""
    experiments = load_data(EXPERIMENTS_FILE)
    
    if experiment_id not in experiments:
        print(f"[×] 实验不存在: {experiment_id}")
        return
    
    log_entry = {
        "date": date,
        "hours": hours,
        "income": income,
        "notes": notes,
        "timestamp": datetime.now().isoformat()
    }
    
    experiments[experiment_id]["daily_logs"].append(log_entry)
    experiments[experiment_id]["total_hours"] += hours
    experiments[experiment_id]["total_income"] += income
    
    save_data(EXPERIMENTS_FILE, experiments)
    
    # 计算实时数据
    total_logs = len(experiments[experiment_id]["daily_logs"])
    avg_hourly_income = experiments[experiment_id]["total_income"] / experiments[experiment_id]["total_hours"] if experiments[experiment_id]["total_hours"] > 0 else 0
    
    print(f"[✓] 已记录: {date}")
    print(f"  投入: {hours}小时")
    print(f"  收入: ¥{income}")
    print(f"  当日时薪: ¥{income/hours:.2f}/小时" if hours > 0 else "")
    print(f"  累计: {total_logs}天 | 总收入¥{experiments[experiment_id]['total_income']} | 平均时薪¥{avg_hourly_income:.2f}")


def show_status():
    """显示所有实验状态"""
    experiments = load_data(EXPERIMENTS_FILE)
    
    if not experiments:
        print("[*] 暂无实验，使用 'add' 命令添加")
        return
    
    print("\n" + "="*70)
    print("📊 收入实验看板")
    print("="*70)
    
    total_income = 0
    total_hours = 0
    
    for exp_id, exp in experiments.items():
        status_emoji = "🟢" if exp["status"] == "active" else "🔴"
        avg_hourly = exp["total_income"] / exp["total_hours"] if exp["total_hours"] > 0 else 0
        progress = len(exp["daily_logs"]) / exp["duration_days"] * 100
        
        print(f"\n{status_emoji} [{exp_id}] {exp['name']}")
        print(f"   类型: {exp['type']} | 状态: {exp['status']}")
        print(f"   进度: {len(exp['daily_logs'])}/{exp['duration_days']}天 ({progress:.0f}%)")
        print(f"   投入: {exp['total_hours']:.1f}小时")
        print(f"   收入: ¥{exp['total_income']:.2f}")
        print(f"   时薪: ¥{avg_hourly:.2f}/小时")
        
        if exp["income_target"] > 0:
            target_progress = exp["total_income"] / exp["income_target"] * 100
            print(f"   目标: ¥{exp['total_income']:.0f}/¥{exp['income_target']:.0f} ({target_progress:.0f}%)")
        
        total_income += exp["total_income"]
        total_hours += exp["total_hours"]
    
    print("\n" + "-"*70)
    print(f"💰 总计: {len(experiments)}个实验 | {total_hours:.1f}小时 | ¥{total_income:.2f}")
    if total_hours > 0:
        print(f"📈 平均时薪: ¥{total_income/total_hours:.2f}/小时")
    print("="*70)


def complete_experiment(experiment_id: str, success: bool, lessons: str = ""):
    """结束实验"""
    experiments = load_data(EXPERIMENTS_FILE)
    
    if experiment_id not in experiments:
        print(f"[×] 实验不存在: {experiment_id}")
        return
    
    experiments[experiment_id]["status"] = "completed"
    experiments[experiment_id]["completed_at"] = datetime.now().isoformat()
    experiments[experiment_id]["success"] = success
    experiments[experiment_id]["lessons_learned"] = lessons
    
    save_data(EXPERIMENTS_FILE, experiments)
    
    exp = experiments[experiment_id]
    avg_hourly = exp["total_income"] / exp["total_hours"] if exp["total_hours"] > 0 else 0
    
    print(f"[✓] 实验已结束: {exp['name']}")
    print(f"  结果: {'成功' if success else '失败'}")
    print(f"  总投入: {exp['total_hours']:.1f}小时")
    print(f"  总收入: ¥{exp['total_income']:.2f}")
    print(f"  时薪: ¥{avg_hourly:.2f}/小时")
    print(f"  经验总结: {lessons}")


def export_to_csv(output_file: str = "income_report.csv"):
    """导出数据到CSV"""
    experiments = load_data(EXPERIMENTS_FILE)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['实验ID', '名称', '类型', '状态', '天数', '总小时', '总收入', '时薪', '目标完成率'])
        
        for exp_id, exp in experiments.items():
            avg_hourly = exp["total_income"] / exp["total_hours"] if exp["total_hours"] > 0 else 0
            target_progress = exp["total_income"] / exp["income_target"] * 100 if exp["income_target"] > 0 else 0
            
            writer.writerow([
                exp_id,
                exp['name'],
                exp['type'],
                exp['status'],
                len(exp['daily_logs']),
                f"{exp['total_hours']:.1f}",
                f"{exp['total_income']:.2f}",
                f"{avg_hourly:.2f}",
                f"{target_progress:.0f}%"
            ])
    
    print(f"[✓] 数据已导出到: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='收入实验追踪器')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # init 命令
    init_parser = subparsers.add_parser('init', help='初始化实验室')
    init_parser.add_argument('--name', type=str, default='我的收入实验', help='实验室名称')
    
    # add 命令
    add_parser = subparsers.add_parser('add', help='添加新实验')
    add_parser.add_argument('--name', type=str, required=True, help='实验名称')
    add_parser.add_argument('--type', type=str, choices=['tier1', 'tier2', 'tier3', 'tier4'], required=True, help='实验类型')
    add_parser.add_argument('--duration', type=int, required=True, help='实验周期（天）')
    add_parser.add_argument('--time-budget', type=float, required=True, help='每日时间预算（小时）')
    add_parser.add_argument('--income-target', type=float, default=0, help='收入目标')
    add_parser.add_argument('--notes', type=str, default='', help='备注')
    
    # log 命令
    log_parser = subparsers.add_parser('log', help='记录每日数据')
    log_parser.add_argument('--experiment', type=str, required=True, help='实验ID')
    log_parser.add_argument('--date', type=str, default=datetime.now().strftime('%Y-%m-%d'), help='日期')
    log_parser.add_argument('--hours', type=float, required=True, help='投入时间')
    log_parser.add_argument('--income', type=float, default=0, help='收入金额')
    log_parser.add_argument('--notes', type=str, default='', help='备注')
    
    # status 命令
    subparsers.add_parser('status', help='查看实验状态')
    
    # complete 命令
    complete_parser = subparsers.add_parser('complete', help='结束实验')
    complete_parser.add_argument('--experiment', type=str, required=True, help='实验ID')
    complete_parser.add_argument('--success', type=lambda x: x.lower() == 'true', required=True, help='是否成功')
    complete_parser.add_argument('--lessons', type=str, default='', help='经验总结')
    
    # export 命令
    export_parser = subparsers.add_parser('export', help='导出数据')
    export_parser.add_argument('--output', type=str, default='income_report.csv', help='输出文件')
    
    args = parser.parse_args()
    
    if args.command == 'init':
        init_lab(args.name)
    elif args.command == 'add':
        add_experiment(args.name, args.type, args.duration, args.time_budget, args.income_target, args.notes)
    elif args.command == 'log':
        log_daily(args.experiment, args.date, args.hours, args.income, args.notes)
    elif args.command == 'status':
        show_status()
    elif args.command == 'complete':
        complete_experiment(args.experiment, args.success, args.lessons)
    elif args.command == 'export':
        export_to_csv(args.output)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
