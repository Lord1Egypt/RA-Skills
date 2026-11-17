#!/usr/bin/env python3
"""
听懂了服务监控脚本
每小时检查一次，异常时发送飞书告警
"""
import requests, json, os, sys
from datetime import datetime, timedelta

# 配置
API_BASE = os.environ.get("TINGDONG_API_URL", "http://111.229.22.145:8092/api/v1").rstrip("/")
API_TOKEN = os.environ.get("TINGDONG_API_TOKEN", "")
FEISHU_WEBHOOK = os.environ.get("FEISHU_WEBHOOK", "")  # 需要配置
DISK_THRESHOLD = 90  # 磁盘使用率告警阈值


def api_get(endpoint: str, timeout: int = 10):
    """带认证的 GET 请求"""
    url = f"{API_BASE}{endpoint}"
    headers = {}
    if API_TOKEN:
        headers["Authorization"] = f"Bearer {API_TOKEN}"
    return requests.get(url, headers=headers, timeout=timeout)


class Monitor:
    def __init__(self):
        self.alerts = []
    
    def check_api_health(self):
        """检查API是否可用"""
        try:
            r = api_get("/health", timeout=10)
            if r.status_code != 200:
                self.alerts.append(f"API健康检查失败: HTTP {r.status_code}")
            return r.status_code == 200
        except Exception as e:
            self.alerts.append(f"API无法访问: {str(e)[:100]}")
            return False
    
    def check_disk_space(self):
        """检查磁盘空间"""
        try:
            import shutil
            stat = shutil.disk_usage("/")
            used_percent = (stat.used / stat.total) * 100
            if used_percent > DISK_THRESHOLD:
                self.alerts.append(f"磁盘使用率 {used_percent:.1f}% (阈值 {DISK_THRESHOLD}%)")
            return used_percent
        except Exception as e:
            self.alerts.append(f"磁盘检查失败: {e}")
            return 0
    
    def check_recent_failures(self):
        """检查最近1小时是否有任务失败"""
        # 需要通过API或日志检查，目前简化为占位
        pass
    
    def send_alert(self):
        """发送告警（如果有）"""
        if not self.alerts:
            print(f"[{datetime.now()}] 一切正常")
            return
        
        message = "🚨 听懂了服务告警\n\n" + "\n".join(f"• {a}" for a in self.alerts)
        print(f"[{datetime.now()}] ALERT: {message}")
        
        # 如果有飞书webhook，发送消息
        if FEISHU_WEBHOOK:
            try:
                requests.post(FEISHU_WEBHOOK, json={
                    "msg_type": "text",
                    "content": {"text": message}
                }, timeout=10)
            except Exception as e:
                print(f"发送告警失败: {e}")
    
    def run(self):
        """运行所有检查"""
        self.check_api_health()
        self.check_disk_space()
        self.check_recent_failures()
        self.send_alert()

if __name__ == "__main__":
    monitor = Monitor()
    monitor.run()
