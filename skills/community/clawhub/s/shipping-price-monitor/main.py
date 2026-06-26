# -*- coding: utf-8 -*-
"""
海运报价监控助手 - 主入口
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.monitor import FileMonitor
from core.analyzer import PriceAnalyzer
from core.notifier import Notifier


class ShippingPriceMonitor:
    def __init__(self, default_target: str = "Liam"):
        self.monitor = FileMonitor()
        self.analyzer = PriceAnalyzer()
        self.notifier = Notifier(default_target)
        
        self.monitor.set_on_alert(self._on_file_change)
    
    def _on_file_change(self, excel_path: str):
        alerts = self.analyzer.analyze_all_rules(excel_path)
        if alerts:
            self._log(f"发现 {len(alerts)} 条预警")
            success, msg = self.notifier.send(alerts)
            if success:
                self._log(f"通知发送成功: {msg}")
            else:
                self._log(f"通知发送失败: {msg}")
        else:
            self._log("未发现低价预警")
    
    def _log(self, message: str):
        print(message)
    
    def enable(self) -> bool:
        return self.monitor.enable()
    
    def disable(self) -> bool:
        return self.monitor.disable()
    
    def is_enabled(self) -> bool:
        return self.monitor.is_enabled()
    
    def start(self) -> bool:
        if not self.is_enabled():
            self.enable()
        return self.monitor.start()
    
    def stop(self):
        self.monitor.stop()
    
    def check_now(self, excel_path: str = None) -> list:
        if excel_path is None:
            excel_path = self.monitor.get_excel_path()
            if not excel_path:
                excel_path = self.monitor.get_latest_excel()
        
        if not excel_path:
            self._log("未找到Excel文件")
            return []
        
        self._log(f"检查文件: {excel_path}")
        alerts = self.analyzer.analyze_all_rules(excel_path)
        
        if alerts:
            self._log(f"发现 {len(alerts)} 条预警")
            success, msg = self.notifier.send(alerts)
            if success:
                self._log(f"通知发送成功: {msg}")
            else:
                self._log(f"通知发送失败: {msg}")
        else:
            self._log("未发现低价预警")
        
        return alerts
    
    def set_watch_directory(self, directory: str):
        self.monitor.set_watch_directory(directory)
    
    def set_excel_path(self, path: str):
        self.monitor.set_excel_path(path)
    
    def set_webhook(self, channel: str, webhook: str):
        if channel == "feishu" or channel == "飞书":
            self.notifier.set_feishu_webhook(webhook)
            self.notifier.set_channel("feishu")
        else:
            self.notifier.set_wecom_webhook(webhook)
            self.notifier.set_channel("wecom")
    
    def set_target(self, target: str):
        self.notifier.set_target(target)
    
    def add_rule(self, rule: dict) -> str:
        return self.analyzer.add_rule(rule)
    
    def update_rule(self, rule_id: str, updates: dict) -> bool:
        return self.analyzer.update_rule(rule_id, updates)
    
    def delete_rule(self, rule_id: str) -> bool:
        return self.analyzer.delete_rule(rule_id)
    
    def get_rules(self) -> list:
        return self.analyzer.get_rule_summary()
    
    def test_notification(self, channel: str = None) -> tuple:
        return self.notifier.test(channel)
    
    def get_status(self) -> dict:
        return {
            "monitor": self.monitor.get_status(),
            "notification": self.notifier.get_status(),
            "rules": self.analyzer.get_rule_summary()
        }
    
    def print_status(self):
        status = self.get_status()
        
        print("\n" + "=" * 50)
        print("       海运报价监控助手 - 状态")
        print("=" * 50)
        
        m = status["monitor"]
        print(f"\n[监控状态]")
        print(f"  已启用: {'✅' if m['enabled'] else '❌'}")
        print(f"  运行中: {'✅' if m['running'] else '❌'}")
        print(f"  监控目录: {m['watch_directory'] or '未设置'}")
        print(f"  Excel路径: {m['excel_path'] or '未设置'}")
        print(f"  检查间隔: {m['check_interval']}秒")
        print(f"  启用规则数: {m['rules_count']}")
        
        n = status["notification"]
        print(f"\n[通知配置]")
        print(f"  当前渠道: {n['channel']}")
        print(f"  默认目标: {n['default_target']}")
        
        oc = n["openclaw_available"]
        print(f"  OpenClaw长连接:")
        print(f"    企业微信: {'✅ 可用' if oc['wecom'] else '❌ 不可用'}")
        print(f"    飞书: {'✅ 可用' if oc['feishu'] else '❌ 不可用'}")
        
        wh = n["webhook_configured"]
        print(f"  Webhook配置:")
        print(f"    企业微信: {'✅ 已配置' if wh['wecom'] else '❌ 未配置'}")
        print(f"    飞书: {'✅ 已配置' if wh['feishu'] else '❌ 未配置'}")
        
        rules = status["rules"]
        print(f"\n[预警规则] 共 {len(rules)} 条")
        for r in rules:
            status_text = "✅" if r["enabled"] else "❌"
            print(f"  {status_text} {r['name']} (ID: {r['id']})")
            print(f"      起运港: {r['pol_count']}个, 目的港: {r['pod_count']}个")
            print(f"      船司: {', '.join(r['carriers'])}")
            print(f"      阈值: 20GP=${r['thresholds'].get('20GP', 'N/A')}, "
                  f"40GP=${r['thresholds'].get('40GP', 'N/A')}, "
                  f"40HQ=${r['thresholds'].get('40HQ', 'N/A')}")
        
        print("\n" + "=" * 50 + "\n")


def main():
    app = ShippingPriceMonitor()
    
    if len(sys.argv) < 2:
        app.print_status()
        return
    
    cmd = sys.argv[1]
    
    if cmd == "start":
        app.start()
        print("✅ 监控已启动")
    elif cmd == "stop":
        app.stop()
        print("✅ 监控已停止")
    elif cmd == "enable":
        app.enable()
        print("✅ 监控已启用")
    elif cmd == "disable":
        app.disable()
        print("✅ 监控已禁用")
    elif cmd == "check":
        excel_path = sys.argv[2] if len(sys.argv) > 2 else None
        app.check_now(excel_path)
    elif cmd == "status":
        app.print_status()
    elif cmd == "test":
        channel = sys.argv[2] if len(sys.argv) > 2 else None
        success, msg = app.test_notification(channel)
        print(f"{'✅' if success else '❌'} {msg}")
    else:
        print(f"未知命令: {cmd}")
        print("用法: python main.py [start|stop|enable|disable|check|status|test]")


if __name__ == "__main__":
    main()
