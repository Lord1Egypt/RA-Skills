#!/usr/bin/env python3
"""
API使用自动检查器
智能判断"够用/不够用"并显示剩余量
"""

import os
import sys
import json
import datetime
import argparse
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# 添加工具模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
from log_parser import LogParser

@dataclass
class UsageStatus:
    """使用状态"""
    is_enough: bool              # 是否够用
    remaining_percent: float     # 剩余百分比
    remaining_calls: int         # 剩余调用次数
    remaining_tokens: int        # 剩余令牌数
    remaining_days: int          # 剩余天数
    message: str                # 状态消息
    color: str                  # 显示颜色
    
    def to_dict(self) -> Dict:
        return {
            "is_enough": self.is_enough,
            "remaining_percent": round(self.remaining_percent, 2),
            "remaining_calls": self.remaining_calls,
            "remaining_tokens": self.remaining_tokens,
            "remaining_days": self.remaining_days,
            "message": self.message,
            "color": self.color,
        }

class APIAutoChecker:
    """API自动检查器"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.parser = LogParser()
        
        # 默认配额配置（可根据实际情况调整）
        self.quotas = {
            "daily": {
                "calls": 1000,      # 每日调用次数
                "tokens": 1000000,  # 每日令牌数（1百万）
                "cost": 10.0,       # 每日成本上限（元）
            },
            "weekly": {
                "calls": 5000,      # 每周调用次数
                "tokens": 5000000,  # 每周令牌数（5百万）
                "cost": 50.0,       # 每周成本上限
            },
            "monthly": {
                "calls": 20000,     # 每月调用次数
                "tokens": 20000000, # 每月令牌数（2千万）
                "cost": 200.0,      # 每月成本上限
            }
        }
        
        # 模型成本配置（元/百万令牌）
        self.model_costs = {
            "deepseek-ai": 0.001,
            "glm-5": 0.0015,
            "gpt-4": 0.03,
            "gpt-3.5-turbo": 0.001,
            "claude-3": 0.015,
            "default": 0.002,
        }
    
    def get_current_usage(self, days: int = 1) -> Dict:
        """获取当前使用情况"""
        from collections import defaultdict
        
        usage = defaultdict(lambda: {
            "calls": 0,
            "tokens": 0,
            "cost": 0.0,
            "models": defaultdict(lambda: {"calls": 0, "tokens": 0, "cost": 0.0}),
        })
        
        # 获取日志文件
        log_files = []
        log_path = os.path.join(os.path.expanduser("~"), ".openclaw", "logs")
        if os.path.exists(log_path):
            cutoff_time = datetime.datetime.now() - datetime.timedelta(days=days)
            for filename in os.listdir(log_path):
                if filename.endswith('.log'):
                    filepath = os.path.join(log_path, filename)
                    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
                    if mtime >= cutoff_time:
                        log_files.append(filepath)
        
        # 解析日志文件
        for log_file in log_files:
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        
                        # 简单解析（实际应使用更复杂的解析）
                        if '"model"' in line:
                            usage["total"]["calls"] += 1
                            
                            # 提取模型名
                            import re
                            model_match = re.search(r'"model"\s*:\s*"([^"]+)"', line)
                            if model_match:
                                model = model_match.group(1)
                                usage["total"]["models"][model]["calls"] += 1
                                
                                # 估算令牌数（假设平均500令牌/次）
                                tokens = 500
                                usage["total"]["tokens"] += tokens
                                usage["total"]["models"][model]["tokens"] += tokens
                                
                                # 计算成本
                                cost_per_million = self.model_costs.get(model, self.model_costs["default"])
                                cost = (tokens / 1000000) * cost_per_million
                                usage["total"]["cost"] += cost
                                usage["total"]["models"][model]["cost"] += cost
            except Exception as e:
                if self.debug:
                    print(f"解析日志文件失败 {log_file}: {e}")
        
        # 转换为普通字典
        result = {
            "period_days": days,
            "total_calls": usage["total"]["calls"],
            "total_tokens": usage["total"]["tokens"],
            "total_cost": round(usage["total"]["cost"], 4),
            "models": dict(usage["total"]["models"]),
            "check_time": datetime.datetime.now().isoformat(),
        }
        
        return result
    
    def check_daily_status(self) -> UsageStatus:
        """检查每日使用状态"""
        usage = self.get_current_usage(days=1)
        quota = self.quotas["daily"]
        
        calls = usage["total_calls"]
        tokens = usage["total_tokens"]
        cost = usage["total_cost"]
        
        # 计算剩余量
        remaining_calls = max(0, quota["calls"] - calls)
        remaining_tokens = max(0, quota["tokens"] - tokens)
        remaining_cost = max(0, quota["cost"] - cost)
        
        # 计算剩余百分比（取最小值）
        calls_percent = (remaining_calls / quota["calls"]) * 100
        tokens_percent = (remaining_tokens / quota["tokens"]) * 100
        cost_percent = (remaining_cost / quota["cost"]) * 100
        
        remaining_percent = min(calls_percent, tokens_percent, cost_percent)
        
        # 判断是否够用
        is_enough = remaining_percent > 20  # 剩余20%以上为够用
        
        # 生成状态消息 - Windows兼容版本
        if remaining_percent >= 80:
            message = "[OK] 充足 - 剩余量充足，可放心使用"
            color = "green"
        elif remaining_percent >= 50:
            message = "[OK] 充足 - 剩余量良好，继续使用"
            color = "green"
        elif remaining_percent >= 20:
            message = "[WARN] 紧张 - 剩余量一般，建议适度使用"
            color = "yellow"
        elif remaining_percent > 0:
            message = "[WARN] 不足 - 剩余量较低，请谨慎使用"
            color = "orange"
        else:
            message = "[ERROR] 耗尽 - 配额已用完，请停止使用"
            color = "red"
        
        # 计算剩余天数（基于当前使用速率）
        if calls > 0:
            avg_daily_calls = calls
            remaining_days = remaining_calls / avg_daily_calls if avg_daily_calls > 0 else 999
        else:
            remaining_days = 999
        
        return UsageStatus(
            is_enough=is_enough,
            remaining_percent=remaining_percent,
            remaining_calls=remaining_calls,
            remaining_tokens=remaining_tokens,
            remaining_days=int(remaining_days),
            message=message,
            color=color,
        )
    
    def check_weekly_status(self) -> UsageStatus:
        """检查每周使用状态"""
        usage = self.get_current_usage(days=7)
        quota = self.quotas["weekly"]
        
        calls = usage["total_calls"]
        tokens = usage["total_tokens"]
        cost = usage["total_cost"]
        
        # 计算剩余量
        remaining_calls = max(0, quota["calls"] - calls)
        remaining_tokens = max(0, quota["tokens"] - tokens)
        remaining_cost = max(0, quota["cost"] - cost)
        
        # 计算剩余百分比
        remaining_percent = min(
            (remaining_calls / quota["calls"]) * 100,
            (remaining_tokens / quota["tokens"]) * 100,
            (remaining_cost / quota["cost"]) * 100,
        )
        
        # 判断是否够用
        is_enough = remaining_percent > 20
        
        # 生成状态消息 - Windows兼容版本
        if remaining_percent >= 80:
            message = "[OK] 充足 - 本周剩余量充足"
            color = "green"
        elif remaining_percent >= 50:
            message = "[OK] 充足 - 本周剩余量良好"
            color = "green"
        elif remaining_percent >= 20:
            message = "[WARN] 紧张 - 本周剩余量一般"
            color = "yellow"
        elif remaining_percent > 0:
            message = "[WARN] 不足 - 本周剩余量较低"
            color = "orange"
        else:
            message = "[ERROR] 耗尽 - 本周配额已用完"
            color = "red"
        
        # 计算剩余天数
        avg_daily_calls = calls / 7 if calls > 0 else 1
        remaining_days = remaining_calls / avg_daily_calls if avg_daily_calls > 0 else 999
        
        return UsageStatus(
            is_enough=is_enough,
            remaining_percent=remaining_percent,
            remaining_calls=remaining_calls,
            remaining_tokens=remaining_tokens,
            remaining_days=int(remaining_days),
            message=message,
            color=color,
        )
    
    def generate_report(self, period: str = "daily") -> str:
        """生成详细报告"""
        if period == "daily":
            usage = self.get_current_usage(days=1)
            quota = self.quotas["daily"]
            status = self.check_daily_status()
            period_name = "今日"
        else:  # weekly
            usage = self.get_current_usage(days=7)
            quota = self.quotas["weekly"]
            status = self.check_weekly_status()
            period_name = "本周"
        
        # 构建报告 - Windows兼容版本
        report = []
        report.append(f"== API使用状态检查报告 - {period_name} ==")
        report.append("=" * 50)
        report.append("")
        
        # 状态摘要
        report.append(f"状态: {status.message}")
        report.append(f"颜色指示: {status.color}")
        report.append(f"剩余百分比: {status.remaining_percent:.1f}%")
        report.append(f"预计可用天数: {status.remaining_days}天")
        report.append("")
        
        # 详细使用情况
        report.append(f"{period_name}使用情况:")
        report.append(f"  调用次数: {usage['total_calls']} / {quota['calls']}")
        report.append(f"  剩余次数: {status.remaining_calls}")
        report.append(f"  使用令牌: {usage['total_tokens']:,} / {quota['tokens']:,}")
        report.append(f"  剩余令牌: {status.remaining_tokens:,}")
        report.append(f"  估计成本: ¥{usage['total_cost']:.4f} / ¥{quota['cost']:.2f}")
        report.append(f"  剩余成本: ¥{quota['cost'] - usage['total_cost']:.2f}")
        report.append("")
        
        # 模型分布
        if usage["models"]:
            report.append("按模型分布:")
            for model, data in usage["models"].items():
                calls = data.get("calls", 0)
                tokens = data.get("tokens", 0)
                cost = data.get("cost", 0)
                report.append(f"  • {model}: {calls}次, {tokens:,}令牌, ¥{cost:.4f}")
        else:
            report.append("按模型分布: 无数据")
        
        report.append("")
        
        # 建议
        report.append("== 使用建议 ==")
        if status.is_enough:
            report.append("  [OK] 配额充足，可正常使用")
            if status.remaining_percent < 50:
                report.append("  [NOTE] 建议关注使用频率，避免突增")
        else:
            report.append("  [WARN] 配额紧张，建议:")
            report.append("      1. 优先使用低成本模型")
            report.append("      2. 减少不必要的API调用")
            report.append("      3. 优化查询内容以减少令牌数")
            if status.remaining_percent <= 0:
                report.append("      4. 立即停止新调用，等待配额重置")
        
        report.append("")
        report.append(f"检查时间: {usage['check_time']}")
        report.append("=" * 50)
        
        return "\n".join(report)
    
    def check_and_alert(self) -> Dict:
        """检查并返回告警信息"""
        daily_status = self.check_daily_status()
        weekly_status = self.check_weekly_status()
        
        alerts = []
        
        # 检查每日告警
        if not daily_status.is_enough:
            alerts.append({
                "level": "warning",
                "period": "daily",
                "message": f"每日配额紧张: 剩余{daily_status.remaining_percent:.1f}%",
                "status": daily_status.to_dict(),
            })
        
        # 检查每周告警
        if not weekly_status.is_enough:
            alerts.append({
                "level": "warning",
                "period": "weekly",
                "message": f"每周配额紧张: 剩余{weekly_status.remaining_percent:.1f}%",
                "status": weekly_status.to_dict(),
            })
        
        # 严重告警（剩余量极低）
        if daily_status.remaining_percent <= 10:
            alerts.append({
                "level": "critical",
                "period": "daily",
                "message": f"每日配额即将耗尽: 仅剩{daily_status.remaining_percent:.1f}%",
                "status": daily_status.to_dict(),
            })
        
        # 构建结果
        result = {
            "timestamp": datetime.datetime.now().isoformat(),
            "daily": daily_status.to_dict(),
            "weekly": weekly_status.to_dict(),
            "alerts": alerts,
            "summary": {
                "overall_enough": daily_status.is_enough and weekly_status.is_enough,
                "has_alerts": len(alerts) > 0,
                "alert_count": len(alerts),
            }
        }
        
        return result

def main():
    # Windows编码兼容性处理
    import locale
    try:
        # 尝试设置控制台编码为UTF-8
        if sys.platform == "win32":
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except:
        pass
    
    parser = argparse.ArgumentParser(description="API使用自动检查器")
    parser.add_argument("--period", choices=["daily", "weekly", "both"],
                       default="both", help="检查周期")
    parser.add_argument("--report", action="store_true", help="生成详细报告")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    parser.add_argument("--alerts", action="store_true", help="仅显示告警")
    parser.add_argument("--simple", action="store_true", help="简化输出")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    
    args = parser.parse_args()
    
    # 创建检查器
    checker = APIAutoChecker(debug=args.debug)
    
    try:
        if args.alerts:
            # 仅显示告警
            result = checker.check_and_alert()
            if args.json:
                print(json.dumps(result["alerts"], indent=2, ensure_ascii=False))
            else:
                if result["alerts"]:
                    print("[ALERT] 告警信息:")
                    for alert in result["alerts"]:
                        print(f"  {alert['level'].upper()}: {alert['message']}")
                else:
                    print("[OK] 无告警信息")
        
        elif args.report:
            # 生成详细报告 - Windows兼容版本
            if args.period == "daily" or args.period == "both":
                print(checker.generate_report("daily"))
                if args.period == "both":
                    print("\n" + "="*60 + "\n")
            if args.period == "weekly" or args.period == "both":
                print(checker.generate_report("weekly"))
        
        elif args.simple:
            # 简化输出 - Windows兼容版本
            if args.period == "daily" or args.period == "both":
                status = checker.check_daily_status()
                print(f"[今日] {status.message} (剩余{status.remaining_percent:.1f}%)")
            if args.period == "weekly" or args.period == "both":
                status = checker.check_weekly_status()
                print(f"[本周] {status.message} (剩余{status.remaining_percent:.1f}%)")
        
        elif args.json:
            # JSON格式输出
            result = checker.check_and_alert()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        else:
            # 默认输出 - Windows兼容版本
            if args.period == "daily" or args.period == "both":
                daily_status = checker.check_daily_status()
                print("== 今日API使用状态检查 ==")
                print(f"  状态: {daily_status.message}")
                print(f"  剩余百分比: {daily_status.remaining_percent:.1f}%")
                print(f"  预计可用天数: {daily_status.remaining_days}天")
                print(f"  剩余调用次数: {daily_status.remaining_calls}")
                print(f"  剩余令牌数: {daily_status.remaining_tokens:,}")
                print(f"  是否够用: {'是' if daily_status.is_enough else '否'}")
                
            if args.period == "weekly" or args.period == "both":
                weekly_status = checker.check_weekly_status()
                print("\n== 本周API使用状态检查 ==")
                print(f"  状态: {weekly_status.message}")
                print(f"  剩余百分比: {weekly_status.remaining_percent:.1f}%")
                print(f"  预计可用天数: {weekly_status.remaining_days}天")
                print(f"  剩余调用次数: {weekly_status.remaining_calls}")
                print(f"  剩余令牌数: {weekly_status.remaining_tokens:,}")
                print(f"  是否够用: {'是' if weekly_status.is_enough else '否'}")
                
            # 显示结论
            if args.period == "both":
                daily_status = checker.check_daily_status()
                weekly_status = checker.check_weekly_status()
                overall_enough = daily_status.is_enough and weekly_status.is_enough
                
                print("\n== 总体结论 ==")
                if overall_enough:
                    print("  [OK] API配额充足，可正常使用")
                else:
                    print("  [WARN] API配额紧张，建议:")
                    if not daily_status.is_enough:
                        print("    • 今日使用需谨慎")
                    if not weekly_status.is_enough:
                        print("    • 本周使用需优化")
    
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()