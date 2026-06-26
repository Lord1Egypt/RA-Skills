#!/usr/bin/env python3
"""
每日API使用检查脚本
自动运行并生成每日报告
"""

import os
import sys
import json
import datetime
import argparse
from pathlib import Path

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from scripts.api_monitor import APIMonitor

def ensure_directories():
    """确保必要的目录存在"""
    directories = [
        "reports/daily",
        "reports/weekly", 
        "reports/monthly",
        "logs",
    ]
    
    base_dir = Path(__file__).parent.parent
    for dir_name in directories:
        dir_path = base_dir / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        
    return base_dir

def get_date_range(period: str):
    """获取日期范围"""
    today = datetime.datetime.now()
    
    if period == "yesterday":
        date = today - datetime.timedelta(days=1)
        return date.strftime("%Y-%m-%d"), 1
    elif period == "week":
        days_ago = today - datetime.timedelta(days=7)
        return days_ago.strftime("%Y-%m-%d"), 7
    elif period == "month":
        days_ago = today - datetime.timedelta(days=30)
        return days_ago.strftime("%Y-%m-%d"), 30
    else:  # today
        return today.strftime("%Y-%m-%d"), 1

def generate_daily_report(monitor: APIMonitor, report_dir: Path):
    """生成每日报告"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # 收集今日统计
    stats, total_calls = monitor.collect_stats(days=1)
    
    # 生成文本报告
    text_report = monitor.format_report(stats, total_calls, days=1, mode="text")
    
    # 生成JSON报告
    json_report = monitor.format_report(stats, total_calls, days=1, mode="json")
    
    # 保存报告
    text_file = report_dir / f"daily_report_{today}.txt"
    json_file = report_dir / f"daily_report_{today}.json"
    
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(text_report)
    
    with open(json_file, 'w', encoding='utf-8') as f:
        f.write(json_report)
    
    print(f"📊 每日报告已生成:")
    print(f"  - 文本报告: {text_file}")
    print(f"  - JSON报告: {json_file}")
    
    return text_report

def generate_summary_report(monitor: APIMonitor, period: str, report_dir: Path):
    """生成周期汇总报告"""
    _, days = get_date_range(period)
    period_name = {"today": "今日", "week": "本周", "month": "本月"}.get(period, period)
    
    # 收集统计
    stats, total_calls = monitor.collect_stats(days=days)
    
    # 生成报告
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    report = monitor.format_report(stats, total_calls, days=days, mode="text")
    
    # 保存报告
    report_file = report_dir / f"{period}_summary_{today}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"📈 {period_name}汇总报告: {report_file}")
    
    return report

def check_alerts(monitor: APIMonitor, threshold_calls: int = 100, threshold_cost: float = 1.0):
    """检查告警条件"""
    stats, total_calls = monitor.collect_stats(days=1)
    total_cost = sum(data["cost"] for data in stats.values())
    
    alerts = []
    
    if total_calls > threshold_calls:
        alerts.append(f"⚠️ API调用频繁: {total_calls}次 (阈值: {threshold_calls}次)")
    
    if total_cost > threshold_cost:
        alerts.append(f"⚠️ 成本偏高: ¥{total_cost:.4f} (阈值: ¥{threshold_cost})")
    
    # 检查单个模型使用异常
    for model, data in stats.items():
        if data["calls"] > 50:  # 单个模型调用超过50次
            alerts.append(f"⚠️ 模型 {model} 使用频繁: {data['calls']}次")
    
    return alerts

def main():
    parser = argparse.ArgumentParser(description="每日API使用检查")
    parser.add_argument("--period", choices=["today", "yesterday", "week", "month"],
                       default="today", help="统计周期")
    parser.add_argument("--alerts", action="store_true", help="启用告警检查")
    parser.add_argument("--threshold-calls", type=int, default=100,
                       help="调用次数告警阈值")
    parser.add_argument("--threshold-cost", type=float, default=1.0,
                       help="成本告警阈值")
    parser.add_argument("--output-dir", type=str, help="自定义输出目录")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    
    args = parser.parse_args()
    
    # 确保目录存在
    base_dir = ensure_directories()
    
    # 设置输出目录
    if args.output_dir:
        report_dir = Path(args.output_dir)
    else:
        report_dir = base_dir / "reports" / "daily"
    
    report_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建监控器
    monitor = APIMonitor(debug=args.debug)
    
    print("🔍 开始API使用检查...")
    print(f"📅 统计周期: {args.period}")
    print(f"📁 报告目录: {report_dir}")
    print("-" * 50)
    
    try:
        # 生成每日报告
        if args.period == "today":
            report = generate_daily_report(monitor, report_dir)
            print(report)
        else:
            report = generate_summary_report(monitor, args.period, report_dir)
            print(report)
        
        print("-" * 50)
        
        # 检查告警
        if args.alerts:
            alerts = check_alerts(monitor, args.threshold_calls, args.threshold_cost)
            if alerts:
                print("🚨 告警检查结果:")
                for alert in alerts:
                    print(f"  {alert}")
            else:
                print("✅ 告警检查: 无异常")
        
        # 保存运行日志
        log_file = base_dir / "logs" / f"daily_check_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"运行时间: {datetime.datetime.now().isoformat()}\n")
            f.write(f"周期: {args.period}\n")
            f.write(f"报告目录: {report_dir}\n")
            f.write("\n" + report)
        
        print(f"\n📝 运行日志: {log_file}")
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()