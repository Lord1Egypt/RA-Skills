#!/usr/bin/env python3
"""
WorkTracker - 简单快速的工作日志系统
专为AI助手团队设计，解决助手忘记报告工作进展的问题
"""

import json
import os
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Any
import shutil

# 配置文件路径
CONFIG_DIR = os.path.expanduser("~/.openclaw/workspace/.worktracker")
WORK_STATUS_PATH = os.path.join(CONFIG_DIR, "work_status.json")
WORK_LOG_PATH = os.path.join(CONFIG_DIR, "work_log.md")
BACKUP_DIR = os.path.join(CONFIG_DIR, "backups")

# 默认助手配置
DEFAULT_ASSISTANTS = {
    "小新": {"role": "总协调助手", "email": ""},
    "小雅": {"role": "市场助手", "email": ""},
    "小锐": {"role": "销售助手", "email": ""},
    "小暖": {"role": "服务助手", "email": ""}
}

class WorkTracker:
    def __init__(self):
        self.ensure_directories()
        self.load_config()
    
    def ensure_directories(self):
        """确保目录存在"""
        os.makedirs(CONFIG_DIR, exist_ok=True)
        os.makedirs(BACKUP_DIR, exist_ok=True)
    
    def load_config(self):
        """加载配置"""
        self.config_path = os.path.join(CONFIG_DIR, "config.json")
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "version": "1.0.0",
                "assistants": DEFAULT_ASSISTANTS,
                "settings": {
                    "auto_backup": True,
                    "backup_days": 30,
                    "require_update_minutes": 30,
                    "min_work_minutes": 10
                }
            }
            self.save_config()
    
    def save_config(self):
        """保存配置"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def load_status(self):
        """加载工作状态"""
        if os.path.exists(WORK_STATUS_PATH):
            with open(WORK_STATUS_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                "assistants": {name: {
                    "current_work": "",
                    "status": "空闲",
                    "start_time": "",
                    "last_update": "",
                    "progress": 0,
                    "deadline": ""
                } for name in self.config["assistants"]},
                "last_updated": datetime.now().isoformat()
            }
    
    def save_status(self, status):
        """保存工作状态"""
        status["last_updated"] = datetime.now().isoformat()
        with open(WORK_STATUS_PATH, 'w', encoding='utf-8') as f:
            json.dump(status, f, ensure_ascii=False, indent=2)
    
    def log_work(self, assistant: str, action: str, details: str):
        """记录工作日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"## {timestamp} - {assistant} - {action}\n\n{details}\n\n"
        
        # 追加到日志文件
        with open(WORK_LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        # 备份日志
        self.backup_logs()
    
    def backup_logs(self):
        """备份日志"""
        if self.config["settings"]["auto_backup"]:
            date_str = datetime.now().strftime("%Y%m%d")
            backup_status = os.path.join(BACKUP_DIR, f"work_status_{date_str}.json")
            backup_log = os.path.join(BACKUP_DIR, f"work_log_{date_str}.md")
            
            # 备份状态文件
            if os.path.exists(WORK_STATUS_PATH):
                shutil.copy2(WORK_STATUS_PATH, backup_status)
            
            # 备份日志文件
            if os.path.exists(WORK_LOG_PATH):
                shutil.copy2(WORK_LOG_PATH, backup_log)
            
            # 清理旧备份
            self.clean_old_backups()
    
    def clean_old_backups(self):
        """清理旧备份"""
        backup_days = self.config["settings"]["backup_days"]
        cutoff_time = datetime.now().timestamp() - (backup_days * 24 * 60 * 60)
        
        for filename in os.listdir(BACKUP_DIR):
            filepath = os.path.join(BACKUP_DIR, filename)
            if os.path.isfile(filepath):
                if os.path.getmtime(filepath) < cutoff_time:
                    os.remove(filepath)
    
    def start_work(self, assistant: str, work: str, deadline: str = ""):
        """开始工作"""
        status = self.load_status()
        
        if assistant not in status["assistants"]:
            return f"❌ 助手 '{assistant}' 不存在"
        
        current_work = status["assistants"][assistant]["current_work"]
        if current_work:
            return f"❌ {assistant} 已有进行中的工作：{current_work}"
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        status["assistants"][assistant] = {
            "current_work": work,
            "status": "进行中",
            "start_time": timestamp,
            "last_update": timestamp,
            "progress": 0,
            "deadline": deadline
        }
        
        self.save_status(status)
        
        # 记录日志
        log_details = f"**工作内容**：{work}\n**截止时间**：{deadline if deadline else '未设置'}"
        self.log_work(assistant, "开始工作", log_details)
        
        return f"✅ {assistant} 已开始工作：{work}" + (f"（截止：{deadline}）" if deadline else "")
    
    def update_work(self, assistant: str, progress: int, update_text: str):
        """更新工作进展"""
        if progress < 0 or progress > 100:
            return "❌ 进度必须在0-100之间"
        
        status = self.load_status()
        
        if assistant not in status["assistants"]:
            return f"❌ 助手 '{assistant}' 不存在"
        
        current_work = status["assistants"][assistant]["current_work"]
        if not current_work:
            return f"❌ {assistant} 没有进行中的工作"
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        status["assistants"][assistant].update({
            "last_update": timestamp,
            "progress": progress,
            "status": "进行中" if progress < 100 else "已完成"
        })
        
        self.save_status(status)
        
        # 记录日志
        log_details = f"**工作内容**：{current_work}\n**当前进度**：{progress}%\n**更新内容**：{update_text}"
        self.log_work(assistant, "更新进展", log_details)
        
        return f"✅ {assistant} 工作进展更新：{progress}% - {update_text}"
    
    def complete_work(self, assistant: str, result: str, follow_up: str = ""):
        """完成工作"""
        status = self.load_status()
        
        if assistant not in status["assistants"]:
            return f"❌ 助手 '{assistant}' 不存在"
        
        current_work = status["assistants"][assistant]["current_work"]
        if not current_work:
            return f"❌ {assistant} 没有进行中的工作"
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        status["assistants"][assistant] = {
            "current_work": "",
            "status": "空闲",
            "start_time": "",
            "last_update": timestamp,
            "progress": 0,
            "deadline": ""
        }
        
        self.save_status(status)
        
        # 记录日志
        log_details = f"**完成工作**：{current_work}\n**完成结果**：{result}\n**后续事项**：{follow_up if follow_up else '无'}"
        self.log_work(assistant, "完成工作", log_details)
        
        return f"✅ {assistant} 工作完成：{result}" + (f"（后续：{follow_up}）" if follow_up else "")
    
    def show_status(self):
        """显示工作状态"""
        status = self.load_status()
        last_updated = datetime.fromisoformat(status["last_updated"]).strftime("%Y-%m-%d %H:%M")
        
        output = [f"📋 **工作状态报告**（{last_updated}）", ""]
        
        # 表头
        header = "| 助手 | 当前工作 | 进度 | 状态 | 开始时间 | 最后更新 | 截止时间 |"
        separator = "|------|----------|------|------|----------|----------|----------|"
        output.extend([header, separator])
        
        # 数据行
        for assistant, info in status["assistants"].items():
            current_work = info["current_work"][:20] + "..." if len(info["current_work"]) > 20 else info["current_work"]
            progress = f"{info['progress']}%"
            status_text = info["status"]
            start_time = info["start_time"] if info["start_time"] else "-"
            last_update = info["last_update"] if info["last_update"] else "-"
            deadline = info["deadline"] if info["deadline"] else "-"
            
            row = f"| {assistant} | {current_work} | {progress} | {status_text} | {start_time} | {last_update} | {deadline} |"
            output.append(row)
        
        output.append("")
        return "\n".join(output)
    
    def show_log(self, limit: int = 10):
        """显示工作日志"""
        if not os.path.exists(WORK_LOG_PATH):
            return "📝 暂无工作日志记录"
        
        with open(WORK_LOG_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 分割日志条目
        entries = content.split("## ")
        # 去掉空字符串
        entries = [e for e in entries if e.strip()]
        # 取最新的条目
        recent_entries = entries[-limit:] if limit > 0 else entries
        
        output = [f"📝 **最近{len(recent_entries)}条工作日志**", ""]
        for entry in reversed(recent_entries):
            output.append(f"## {entry.strip()}")
        
        return "\n".join(output)
    
    def add_assistant(self, name: str, role: str, email: str = ""):
        """添加助手"""
        if name in self.config["assistants"]:
            return f"❌ 助手 '{name}' 已存在"
        
        self.config["assistants"][name] = {"role": role, "email": email}
        self.save_config()
        
        # 更新状态文件
        status = self.load_status()
        status["assistants"][name] = {
            "current_work": "",
            "status": "空闲",
            "start_time": "",
            "last_update": "",
            "progress": 0,
            "deadline": ""
        }
        self.save_status(status)
        
        return f"✅ 已添加助手：{name}（{role}）"
    
    def remove_assistant(self, name: str):
        """移除助手"""
        if name not in self.config["assistants"]:
            return f"❌ 助手 '{name}' 不存在"
        
        del self.config["assistants"][name]
        self.save_config()
        
        # 更新状态文件
        status = self.load_status()
        if name in status["assistants"]:
            del status["assistants"][name]
        self.save_status(status)
        
        return f"✅ 已移除助手：{name}"
    
    def export_data(self, format: str = "json", output_path: str = ""):
        """导出数据"""
        status = self.load_status()
        
        if format == "json":
            if not output_path:
                output_path = os.path.join(CONFIG_DIR, f"work_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(status, f, ensure_ascii=False, indent=2)
            
            return f"✅ 数据已导出为JSON：{output_path}"
        
        elif format == "csv":
            if not output_path:
                output_path = os.path.join(CONFIG_DIR, f"work_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            
            import csv
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["助手", "当前工作", "进度", "状态", "开始时间", "最后更新", "截止时间"])
                
                for assistant, info in status["assistants"].items():
                    writer.writerow([
                        assistant,
                        info["current_work"],
                        info["progress"],
                        info["status"],
                        info["start_time"],
                        info["last_update"],
                        info["deadline"]
                    ])
            
            return f"✅ 数据已导出为CSV：{output_path}"
        
        else:
            return "❌ 不支持的导出格式，支持：json, csv"
    
    def run_test(self):
        """运行测试"""
        test_results = []
        
        # 测试1：开始工作
        result = self.start_work("小新", "测试工作", "今天完成")
        test_results.append(("开始工作", "✅" if "✅" in result else "❌", result))
        
        # 测试2：更新工作
        result = self.update_work("小新", 50, "测试更新")
        test_results.append(("更新工作", "✅" if "✅" in result else "❌", result))
        
        # 测试3：完成工作
        result = self.complete_work("小新", "测试完成", "无后续")
        test_results.append(("完成工作", "✅" if "✅" in result else "❌", result))
        
        # 测试4：显示状态
        result = self.show_status()
        test_results.append(("显示状态", "✅" if "📋" in result else "❌", "状态显示正常"))
        
        # 输出测试结果
        output = ["🧪 **WorkTracker测试结果**", ""]
        for test_name, status, message in test_results:
            output.append(f"{status} {test_name}: {message}")
        
        return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="WorkTracker - 简单快速的工作日志系统")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # start命令
    start_parser = subparsers.add_parser("start", help="开始工作")
    start_parser.add_argument("assistant", help="助手名称")
    start_parser.add_argument("work", help="工作内容")
    start_parser.add_argument("deadline", nargs="?", default="", help="截止时间")
    
    # update命令
    update_parser = subparsers.add_parser("update", help="更新工作进展")
    update_parser.add_argument("assistant", help="助手名称")
    update_parser.add_argument("progress", type=int, help="进度百分比 (0-100)")
    update_parser.add_argument("update_text", help="更新内容")
    
    # complete命令
    complete_parser = subparsers.add_parser("complete", help="完成工作")
    complete_parser.add_argument("assistant", help="助手名称")
    complete_parser.add_argument("result", help="完成结果")
    complete_parser.add_argument("follow_up", nargs="?", default="", help="后续事项")
    
    # status命令
    subparsers.add_parser("status", help="显示工作状态")
    
    # log命令
    log_parser = subparsers.add_parser("log", help="显示工作日志")
    log_parser.add_argument("--limit", type=int, default=10, help="显示条数限制")
    
    # config命令
    config_parser = subparsers.add_parser("config", help="配置管理")
    config_subparsers = config_parser.add_subparsers(dest="config_command")
    
    # config add-assistant
    add_parser = config_subparsers.add_parser("add-assistant", help="添加助手")
    add_parser.add_argument("name", help="助手名称")
    add_parser.add_argument("role", help="助手角色")
    add_parser.add_argument("--email", default="", help="邮箱地址")
    
    # config remove-assistant
    remove_parser = config_subparsers.add_parser("remove-assistant", help="移除助手")
    remove_parser.add_argument("name", help="助手名称")
    
    # config show
    config_subparsers.add_parser("show", help="显示配置")
    
    # export命令
    export_parser = subparsers.add_parser("export", help="导出数据")
    export_parser.add_argument("format", choices=["json", "csv"], help="导出格式")
    export_parser.add_argument("--output", default="", help="输出文件路径")
    
    # test命令
    subparsers.add_parser("test", help="运行测试")
    
    # version命令
    subparsers.add_parser("version", help="显示版本信息")
    
    # 解析参数
    args = parser.parse_args()
    
    # 创建WorkTracker实例
    tracker = WorkTracker()
    
    # 执行命令
    if args.command == "start":
        result = tracker.start_work(args.assistant, args.work, args.deadline)
        print(result)
    
    elif args.command == "update":
        result = tracker.update_work(args.assistant, args.progress, args.update_text)
        print(result)
    
    elif args.command == "complete":
        result = tracker.complete_work(args.assistant, args.result, args.follow_up)
        print(result)
    
    elif args.command == "status":
        result = tracker.show_status()
        print(result)
    
    elif args.command == "log":
        result = tracker.show_log(args.limit)
        print(result)
    
    elif args.command == "config":
        if args.config_command == "add-assistant":
            result = tracker.add_assistant(args.name, args.role, args.email)
            print(result)
        elif args.config_command == "remove-assistant":
            result = tracker.remove_assistant(args.name)
            print(result)
        elif args.config_command == "show":
            import json
            print(json.dumps(tracker.config, ensure_ascii=False, indent=2))
        else:
            config_parser.print_help()
    
    elif args.command == "export":
        result = tracker.export_data(args.format, args.output)
        print(result)
    
    elif args.command == "test":
        result = tracker.run_test()
        print(result)
    
    elif args.command == "version":
        print("WorkTracker v1.0.0")
        print("作者：iSenlink")
        print("描述：简单快速的工作日志系统")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
