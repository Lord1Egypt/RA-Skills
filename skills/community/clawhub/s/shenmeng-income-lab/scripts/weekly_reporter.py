#!/usr/bin/env python3
"""
周度复盘报告生成器

用法:
    python weekly_reporter.py generate --week 2025-12
    python weekly_reporter.py analyze --experiment exp_001
"""

import argparse
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List

DATA_DIR = os.path.expanduser("~/.income-lab")
EXPERIMENTS_FILE = os.path.join(DATA_DIR, "experiments.json")


def load_experiments() -> Dict:
    """加载实验数据"""
    if not os.path.exists(EXPERIMENTS_FILE):
        return {}
    with open(EXPERIMENTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_weekly_report(week_str: str = None):
    """生成周度复盘报告"""
    experiments = load_experiments()
    
    if not experiments:
        print("[*] 暂无实验数据，请先添加实验")
        return
    
    # 计算本周数据
    total_income = 0
    total_hours = 0
    active_experiments = []
    completed_experiments = []
    
    for exp_id, exp in experiments.items():
        total_income += exp.get("total_income", 0)
        total_hours += exp.get("total_hours", 0)
        
        if exp.get("status") == "active":
            active_experiments.append(exp)
        elif exp.get("status") == "completed":
            completed_experiments.append(exp)
    
    avg_hourly = total_income / total_hours if total_hours > 0 else 0
    
    # 生成报告
    print("\n" + "="*70)
    print(f"📊 周度复盘报告")
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*70)
    
    print(f"\n💰 本周汇总")
    print(f"  总收入: ¥{total_income:.2f}")
    print(f"  总投入: {total_hours:.1f}小时")
    print(f"  平均时薪: ¥{avg_hourly:.2f}/小时")
    
    print(f"\n🟢 进行中实验 ({len(active_experiments)}个)")
    for exp in active_experiments:
        avg = exp["total_income"] / exp["total_hours"] if exp["total_hours"] > 0 else 0
        progress = len(exp.get("daily_logs", [])) / exp["duration_days"] * 100
        print(f"  • {exp['name']}")
        print(f"    进度: {progress:.0f}% | 时薪: ¥{avg:.2f}/小时")
    
    print(f"\n🔴 已完成实验 ({len(completed_experiments)}个)")
    for exp in completed_experiments:
        result = "✓" if exp.get("success") else "✗"
        print(f"  {result} {exp['name']} - ¥{exp['total_income']:.2f}")
    
    # 分析建议
    print(f"\n💡 分析与建议")
    
    # 找出最有效的实验
    if active_experiments:
        best_exp = max(active_experiments, 
                      key=lambda x: x["total_income"]/x["total_hours"] if x["total_hours"] > 0 else 0)
        best_hourly = best_exp["total_income"] / best_exp["total_hours"] if best_exp["total_hours"] > 0 else 0
        print(f"  ✓ 最有效实验: {best_exp['name']} (¥{best_hourly:.2f}/小时)")
        print(f"    建议: 考虑增加投入时间")
    
    # 找出最无效的实验
    if active_experiments:
        worst_exp = min(active_experiments, 
                       key=lambda x: x["total_income"]/x["total_hours"] if x["total_hours"] > 0 else float('inf'))
        worst_hourly = worst_exp["total_income"] / worst_exp["total_hours"] if worst_exp["total_hours"] > 0 else 0
        if worst_hourly < 20:  # 时薪低于20元
            print(f"  ✗ 最低效实验: {worst_exp['name']} (¥{worst_hourly:.2f}/小时)")
            print(f"    建议: 考虑减少投入或放弃")
    
    print(f"\n📋 下周行动计划")
    print("  1. 继续有效实验，适当放大")
    print("  2. 评估低效实验，决定是否放弃")
    print("  3. 考虑启动新实验分散风险")
    
    print("\n" + "="*70)


def analyze_experiment(exp_id: str):
    """分析单个实验"""
    experiments = load_experiments()
    
    if exp_id not in experiments:
        print(f"[×] 实验不存在: {exp_id}")
        return
    
    exp = experiments[exp_id]
    
    print(f"\n📊 实验分析报告: {exp['name']}")
    print("="*60)
    
    print(f"\n基本信息")
    print(f"  类型: {exp['type']}")
    print(f"  状态: {exp['status']}")
    print(f"  创建时间: {exp['created_at'][:10]}")
    print(f"  计划周期: {exp['duration_days']}天")
    
    print(f"\n投入产出")
    print(f"  总投入时间: {exp['total_hours']:.1f}小时")
    print(f"  总收入: ¥{exp['total_income']:.2f}")
    print(f"  平均时薪: ¥{exp['total_income']/exp['total_hours']:.2f}/小时" if exp['total_hours'] > 0 else "  平均时薪: N/A")
    
    print(f"\n目标完成度")
    if exp['income_target'] > 0:
        progress = exp['total_income'] / exp['income_target'] * 100
        print(f"  目标收入: ¥{exp['income_target']}")
        print(f"  完成度: {progress:.1f}%")
    
    print(f"\n每日趋势")
    logs = exp.get("daily_logs", [])
    if logs:
        print(f"  已记录天数: {len(logs)}")
        if len(logs) >= 7:
            recent_logs = logs[-7:]  # 最近7天
            recent_income = sum(log['income'] for log in recent_logs)
            recent_hours = sum(log['hours'] for log in recent_logs)
            recent_hourly = recent_income / recent_hours if recent_hours > 0 else 0
            print(f"  最近7天时薪: ¥{recent_hourly:.2f}/小时")
        
        # 趋势判断
        if len(logs) >= 3:
            recent = sum(logs[-3:][i]['income']/logs[-3:][i]['hours'] if logs[-3:][i]['hours'] > 0 else 0 for i in range(3)) / 3
            older = sum(logs[:3][i]['income']/logs[:3][i]['hours'] if logs[:3][i]['hours'] > 0 else 0 for i in range(min(3, len(logs)))) / min(3, len(logs))
            if recent > older * 1.2:
                print(f"  趋势: ↗️ 上升 (最近时薪比初期高 {(recent/older-1)*100:.0f}%)")
            elif recent < older * 0.8:
                print(f"  趋势: ↘️ 下降 (最近时薪比初期低 {(1-recent/older)*100:.0f}%)")
            else:
                print(f"  趋势: → 平稳")
    
    print(f"\n结论与建议")
    if exp['status'] == 'completed':
        success = "✓ 成功" if exp.get('success') else "✗ 失败"
        print(f"  实验结果: {success}")
        if exp.get('lessons_learned'):
            print(f"  经验总结: {exp['lessons_learned']}")
    else:
        hourly = exp['total_income'] / exp['total_hours'] if exp['total_hours'] > 0 else 0
        if hourly >= 50:
            print(f"  建议: ✓ 高效实验，建议增加投入")
        elif hourly >= 20:
            print(f"  建议: → 尚可，继续观察或优化")
        else:
            print(f"  建议: ✗ 低效，考虑减少投入或放弃")
    
    print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(description='周度复盘报告生成器')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # generate 命令
    generate_parser = subparsers.add_parser('generate', help='生成周度报告')
    generate_parser.add_argument('--week', type=str, help='周次 (格式: YYYY-WW)')
    
    # analyze 命令
    analyze_parser = subparsers.add_parser('analyze', help='分析单个实验')
    analyze_parser.add_argument('--experiment', type=str, required=True, help='实验ID')
    
    args = parser.parse_args()
    
    if args.command == 'generate':
        generate_weekly_report(args.week)
    elif args.command == 'analyze':
        analyze_experiment(args.experiment)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
