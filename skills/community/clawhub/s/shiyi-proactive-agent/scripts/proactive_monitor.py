#!/usr/bin/env python3
"""
主动监控器 - 持续监控环境并触发行动
"""
import json
import time
from datetime import datetime
from pathlib import Path
import sys

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from context_analyzer import ContextAnalyzer
from action_suggester import ActionSuggester

class ProactiveMonitor:
    def __init__(self, base_path=None):
        self.base_path = base_path or Path(__file__).parent.parent.parent
        self.context_analyzer = ContextAnalyzer(self.base_path)
        self.action_suggester = ActionSuggester(self.base_path)
        self.log_file = self.base_path / "memory" / "logs" / "proactive_monitor.log"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 监控配置
        self.check_interval = 300  # 5分钟检查一次
        self.last_alert_time = {}
        self.alert_cooldown = 1800  # 30分钟冷却
        
    def check_and_alert(self):
        """检查并生成提醒"""
        context = self.context_analyzer.get_current_context()
        suggestions = self.action_suggester.suggest_actions(context)
        
        alerts = []
        now = datetime.now()
        
        for suggestion in suggestions:
            action_type = suggestion['type']
            
            # 检查冷却时间
            if action_type in self.last_alert_time:
                elapsed = (now - self.last_alert_time[action_type]).total_seconds()
                if elapsed < self.alert_cooldown:
                    continue
            
            # 高优先级立即提醒
            if suggestion['priority'] == 'high':
                alerts.append(suggestion)
                self.last_alert_time[action_type] = now
                self._log_alert(suggestion)
        
        return alerts
    
    def _log_alert(self, alert):
        """记录提醒日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": alert['type'],
            "priority": alert['priority'],
            "action": alert['action'],
            "suggestion": alert['suggestion']
        }
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def run_once(self):
        """运行一次检查"""
        alerts = self.check_and_alert()
        if alerts:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 发现 {len(alerts)} 个需要注意的事项:")
            for alert in alerts:
                print(f"  - [{alert['priority'].upper()}] {alert['action']}")
                print(f"    建议: {alert['suggestion']}")
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 一切正常，无需行动")
        return alerts
    
    def run_daemon(self, interval=None):
        """作为守护进程持续运行"""
        interval = interval or self.check_interval
        print(f"启动主动监控器，每 {interval} 秒检查一次...")
        print("按 Ctrl+C 停止")
        
        try:
            while True:
                self.run_once()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n监控器已停止")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="主动监控器")
    parser.add_argument("--daemon", action="store_true", help="作为守护进程运行")
    parser.add_argument("--interval", type=int, default=300, help="检查间隔（秒）")
    parser.add_argument("--status", action="store_true", help="只检查当前状态")
    args = parser.parse_args()
    
    monitor = ProactiveMonitor()
    
    if args.status:
        analyzer = ContextAnalyzer()
        summary = analyzer.analyze()
        print("=== 当前状态 ===")
        for key, value in summary.items():
            print(f"{key}: {value}")
    elif args.daemon:
        monitor.run_daemon(args.interval)
    else:
        monitor.run_once()
