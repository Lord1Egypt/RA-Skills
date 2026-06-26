#!/usr/bin/env python3
"""
API自动监控器
定时检查API使用状态，自动判断"够用/不够用"
"""

import os
import sys
import json
import time
import datetime
import argparse
from pathlib import Path

sys.path.append(os.path.dirname(__file__))
from auto_checker import APIAutoChecker

class AutoMonitor:
    """自动监控器"""
    
    def __init__(self, config_file: str = None):
        self.checker = APIAutoChecker()
        
        # 加载配置
        self.config = self.load_config(config_file)
        
        # 状态记录
        self.state_file = Path(__file__).parent.parent / "state" / "monitor_state.json"
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 报告目录
        self.report_dir = Path(__file__).parent.parent / "reports" / "auto"
        self.report_dir.mkdir(parents=True, exist_ok=True)
    
    def load_config(self, config_file: str = None) -> dict:
        """加载配置"""
        default_config = {
            "check_interval_minutes": 30,      # 检查间隔（分钟）
            "alert_threshold_percent": 20,     # 告警阈值百分比
            "critical_threshold_percent": 10,  # 严重告警阈值百分比
            "enable_daily_report": True,       # 启用每日报告
            "enable_weekly_report": True,      # 启用每周报告
            "max_history_days": 30,            # 历史数据保留天数
            "notifications": {
                "enabled": False,
                "method": "log",  # log, email, webhook
                "webhook_url": "",
            }
        }
        
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
        
        return default_config
    
    def load_state(self) -> dict:
        """加载状态"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        
        return {
            "last_check": None,
            "last_alert": None,
            "daily_history": [],
            "weekly_history": [],
            "alerts_count": 0,
        }
    
    def save_state(self, state: dict):
        """保存状态"""
        state["last_update"] = datetime.datetime.now().isoformat()
        
        # 清理历史数据
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=self.config["max_history_days"])
        
        for key in ["daily_history", "weekly_history"]:
            if key in state:
                state[key] = [
                    item for item in state[key]
                    if datetime.datetime.fromisoformat(item["timestamp"]) > cutoff_date
                ]
        
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存状态失败: {e}")
    
    def perform_check(self) -> dict:
        """执行一次检查"""
        result = self.checker.check_and_alert()
        
        # 保存检查结果到历史
        state = self.load_state()
        state["last_check"] = datetime.datetime.now().isoformat()
        
        # 添加日检查历史
        daily_entry = {
            "timestamp": result["timestamp"],
            "remaining_percent": result["daily"]["remaining_percent"],
            "is_enough": result["daily"]["is_enough"],
            "remaining_calls": result["daily"]["remaining_calls"],
            "alerts": len([a for a in result["alerts"] if a["period"] == "daily"]),
        }
        state["daily_history"].append(daily_entry)
        
        # 添加周检查历史
        weekly_entry = {
            "timestamp": result["timestamp"],
            "remaining_percent": result["weekly"]["remaining_percent"],
            "is_enough": result["weekly"]["is_enough"],
            "remaining_calls": result["weekly"]["remaining_calls"],
            "alerts": len([a for a in result["alerts"] if a["period"] == "weekly"]),
        }
        state["weekly_history"].append(weekly_entry)
        
        # 更新告警计数
        if result["alerts"]:
            state["last_alert"] = result["timestamp"]
            state["alerts_count"] += len(result["alerts"])
        
        self.save_state(state)
        
        return result
    
    def generate_daily_summary(self):
        """生成每日摘要"""
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        state = self.load_state()
        
        # 获取今日检查记录
        today_checks = [
            check for check in state["daily_history"]
            if check["timestamp"].startswith(today)
        ]
        
        if not today_checks:
            return None
        
        # 计算统计信息
        total_checks = len(today_checks)
        enough_checks = sum(1 for c in today_checks if c["is_enough"])
        enough_percent = (enough_checks / total_checks) * 100 if total_checks > 0 else 0
        
        # 获取最新检查
        latest_check = max(today_checks, key=lambda x: x["timestamp"])
        
        # 生成摘要
        summary = {
            "date": today,
            "total_checks": total_checks,
            "enough_checks": enough_checks,
            "enough_percent": enough_percent,
            "latest_remaining_percent": latest_check["remaining_percent"],
            "latest_is_enough": latest_check["is_enough"],
            "alerts_today": sum(c["alerts"] for c in today_checks),
        }
        
        return summary
    
    def display_status(self, result: dict = None):
        """显示当前状态"""
        if result is None:
            result = self.perform_check()
        
        print("🚀 API自动监控系统 - 实时状态")
        print("=" * 60)
        
        # 显示每日状态
        daily = result["daily"]
        print(f"\n📅 今日状态:")
        print(f"  🏷️  {daily['message']}")
        print(f"  📊 剩余量: {daily['remaining_percent']:.1f}%")
        print(f"  📞 剩余调用: {daily['remaining_calls']}次")
        print(f"  🔤 剩余令牌: {daily['remaining_tokens']:,}")
        print(f"  📆 预计可用: {daily['remaining_days']}天")
        print(f"  ✅ 是否够用: {'✅ 够用' if daily['is_enough'] else '⚠️ 不够用'}")
        
        # 显示每周状态
        weekly = result["weekly"]
        print(f"\n📆 本周状态:")
        print(f"  🏷️  {weekly['message']}")
        print(f"  📊 剩余量: {weekly['remaining_percent']:.1f}%")
        print(f"  📞 剩余调用: {weekly['remaining_calls']}次")
        print(f"  🔤 剩余令牌: {weekly['remaining_tokens']:,}")
        print(f"  📆 预计可用: {weekly['remaining_days']}天")
        print(f"  ✅ 是否够用: {'✅ 够用' if weekly['is_enough'] else '⚠️ 不够用'}")
        
        # 显示告警
        if result["alerts"]:
            print(f"\n🚨 告警信息 ({len(result['alerts'])}条):")
            for alert in result["alerts"]:
                level_emoji = "🔴" if alert["level"] == "critical" else "🟠"
                print(f"  {level_emoji} [{alert['period'].upper()}] {alert['message']}")
        else:
            print("\n✅ 无告警信息")
        
        # 显示总体结论
        if result["summary"]["overall_enough"]:
            print(f"\n🎯 总体结论: ✅ API配额充足，可正常使用")
        else:
            print(f"\n🎯 总体结论: ⚠️  API配额紧张，建议优化使用")
        
        print(f"\n🕒 检查时间: {result['timestamp']}")
        print("=" * 60)
        
        return result
    
    def run_once(self):
        """运行一次检查"""
        print(f"🔄 开始API使用检查...")
        result = self.perform_check()
        
        # 显示状态
        self.display_status(result)
        
        # 保存报告
        self.save_report(result)
        
        return result
    
    def save_report(self, result: dict):
        """保存检查报告"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.report_dir / f"check_{timestamp}.json"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"📝 检查报告已保存: {report_file}")
        except Exception as e:
            print(f"保存报告失败: {e}")
    
    def run_continuous(self):
        """持续运行监控"""
        print("🚀 API自动监控系统启动")
        print(f"⏰ 检查间隔: {self.config['check_interval_minutes']}分钟")
        print(f"📊 告警阈值: {self.config['alert_threshold_percent']}%")
        print("=" * 60)
        
        try:
            check_count = 0
            
            while True:
                check_count += 1
                print(f"\n🔄 执行第 {check_count} 次检查")
                print(f"🕒 时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                result = self.run_once()
                
                # 检查是否需要生成每日摘要
                current_hour = datetime.datetime.now().hour
                if current_hour == 23:  # 每天23点生成当日摘要
                    summary = self.generate_daily_summary()
                    if summary:
                        summary_file = self.report_dir / f"daily_summary_{datetime.datetime.now().strftime('%Y%m%d')}.json"
                        with open(summary_file, 'w', encoding='utf-8') as f:
                            json.dump(summary, f, indent=2, ensure_ascii=False)
                        print(f"📊 当日摘要已保存: {summary_file}")
                
                # 等待下次检查
                interval_seconds = self.config["check_interval_minutes"] * 60
                print(f"\n⏳ 下次检查将在 {self.config['check_interval_minutes']} 分钟后...")
                
                for remaining in range(interval_seconds, 0, -60):
                    if remaining % 300 == 0:  # 每5分钟打印一次
                        mins = remaining // 60
                        print(f"⏰ 剩余 {mins} 分钟...", end='\r')
                    time.sleep(60)
                
                print("")  # 换行
                
        except KeyboardInterrupt:
            print("\n\n👋 监控已停止")
            return 0
        except Exception as e:
            print(f"\n❌ 监控失败: {e}")
            return 1

def main():
    parser = argparse.ArgumentParser(description="API自动监控器")
    parser.add_argument("--once", action="store_true", help="运行一次检查")
    parser.add_argument("--continuous", action="store_true", help="持续运行监控")
    parser.add_argument("--interval", type=int, help="检查间隔（分钟）")
    parser.add_argument("--config", type=str, help="配置文件路径")
    parser.add_argument("--status", action="store_true", help="显示当前状态")
    parser.add_argument("--summary", action="store_true", help="显示每日摘要")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    
    args = parser.parse_args()
    
    # 创建监控器
    monitor = AutoMonitor(config_file=args.config)
    
    if args.interval:
        monitor.config["check_interval_minutes"] = args.interval
    
    try:
        if args.once:
            # 运行一次检查
            monitor.run_once()
        
        elif args.continuous:
            # 持续运行监控
            monitor.run_continuous()
        
        elif args.status:
            # 显示当前状态
            result = monitor.perform_check()
            monitor.display_status(result)
        
        elif args.summary:
            # 显示每日摘要
            summary = monitor.generate_daily_summary()
            if summary:
                print("📊 当日摘要:")
                print(json.dumps(summary, indent=2, ensure_ascii=False))
            else:
                print("暂无当日检查数据")
        
        else:
            # 默认运行一次检查
            monitor.run_once()
    
    except KeyboardInterrupt:
        print("\n👋 操作已取消")
    except Exception as e:
        print(f"❌ 运行失败: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()