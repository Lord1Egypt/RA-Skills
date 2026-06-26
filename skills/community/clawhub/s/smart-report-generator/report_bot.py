#!/usr/bin/env python3
"""
智能报告生成器
用途：AI 自动生成日报/周报/月报，支持多平台推送
"""

import os
import json
import yaml
import argparse
from datetime import datetime, timedelta
from openclaw import OpenClaw
import requests

class ReportGenerator:
    """报告生成器"""
    
    TEMPLATES = {
        "daily": """## 📅 {date} 日报
**姓名**：{name}
**部门**：{department}

### ✅ 今日完成
{completed}

### 📋 明日计划
{planned}

### 🚧 阻塞问题
{blockers}

---
生成时间：{generated_at}
""",
        "weekly": """## 📊 {week} 周报
**姓名**：{name}
**部门**：{department}

### 📈 本周成果
{achievements}

### 💡 关键数据
{metrics}

### 📌 下周计划
{next_week}

### ⚠️ 风险预警
{risks}

---
生成时间：{generated_at}
"""
    }
    
    def __init__(self, config_path="config.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.api_key = os.getenv("OPENCLAW_API_KEY")
    
    def generate_from_tasks(self, tasks, report_type="daily"):
        """根据任务列表生成报告"""
        if report_type == "daily":
            completed = [t for t in tasks if t["status"] == "done"]
            planned = [t for t in tasks if t["status"] == "todo"]
            
            return self.TEMPLATES["daily"].format(
                date=datetime.now().strftime("%Y-%m-%d"),
                name=self.config.get("name", ""),
                department=self.config.get("department", ""),
                completed="\n".join([f"- {t['title']}" for t in completed]) or "无",
                planned="\n".join([f"- {t['title']}" for t in planned]) or "无",
                blockers="",  # 可扩展
                generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        
        elif report_type == "weekly":
            # AI 生成周报总结
            prompt = f"""根据以下任务列表，生成专业的周报：
任务：{json.dumps(tasks, ensure_ascii=False)}

要求：
1. 总结本周成果
2. 提取关键数据
3. 制定下周计划
4. 识别潜在风险
"""
            
            client = OpenClaw(api_key=self.api_key)
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
    
    def send_to_platform(self, report):
        """发送到平台"""
        platform = self.config.get("platform")
        webhook = self.config.get("webhook")
        
        if not webhook:
            print("❌ 未配置 Webhook")
            return False
        
        if platform == "feishu":
            response = requests.post(webhook, json={"msg_type": "text", "content": {"text": report}})
        elif platform == "dingtalk":
            response = requests.post(webhook, json={"msgtype": "text", "text": {"content": report}})
        else:
            print(f"❌ 不支持的平台: {platform}")
            return False
        
        if response.status_code == 200:
            print(f"✅ 已发送到 {platform}")
            return True
        else:
            print(f"❌ 发送失败: {response.status_code}")
            return False

def main():
    parser = argparse.ArgumentParser(description="智能报告生成器")
    parser.add_argument("--config", default="config.yaml", help="配置文件")
    parser.add_argument("--type", default="daily", help="报告类型：daily/weekly/monthly")
    parser.add_argument("--tasks", help="任务 JSON 文件")
    args = parser.parse_args()
    
    gen = ReportGenerator(args.config)
    
    # 示例任务
    if args.tasks and os.path.exists(args.tasks):
        with open(args.tasks) as f:
            tasks = json.load(f)
    else:
        # 示例数据
        tasks = [
            {"title": "完成客户订单处理", "status": "done"},
            {"title": "编写产品文档", "status": "done"},
            {"title": "参加周会", "status": "done"},
            {"title": "跟进客户反馈", "status": "todo"},
            {"title": "准备下周演示", "status": "todo"}
        ]
    
    report = gen.generate_from_tasks(tasks, args.type)
    print("\n📋 生成的报告：\n")
    print(report)
    print("\n" + "=" * 50)
    
    # 发送
    if input("是否发送到平台？(y/n): ").strip().lower() == "y":
        gen.send_to_platform(report)

if __name__ == "__main__":
    main()