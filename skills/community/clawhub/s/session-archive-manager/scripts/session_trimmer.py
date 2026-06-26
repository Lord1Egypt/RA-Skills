#!/usr/bin/env python3
"""
Session 裁剪式智能总结工具
对正在使用的大 session 文件进行裁剪：
1. 分析整个 session
2. 把旧内容提取总结并归档
3. 只保留最近 N 条消息在原文件中
"""

import json
import os
import sys
import gzip
import shutil
from datetime import datetime
from pathlib import Path
from collections import defaultdict


class SessionTrimmer:
    def __init__(self, session_file, keep_recent=100):
        self.session_file = session_file
        self.keep_recent = keep_recent  # 保留最近多少条消息
        self.messages = []
        self.old_messages = []
        self.recent_messages = []
        
    def load_session(self):
        """加载 session 文件"""
        print(f"加载文件: {self.session_file}")
        print(f"文件大小: {os.path.getsize(self.session_file) / (1024*1024):.2f} MB")
        
        # 处理 .gz 压缩文件
        if self.session_file.endswith('.gz'):
            open_func = gzip.open
            mode = 'rt'
        else:
            open_func = open
            mode = 'r'
        
        with open_func(self.session_file, mode, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                    self.messages.append(msg)
                except json.JSONDecodeError as e:
                    print(f"跳过无效 JSON 行: {e}")
                    continue
        
        print(f"总共加载了 {len(self.messages)} 条消息")
        
        # 分割旧消息和新消息
        if len(self.messages) > self.keep_recent:
            self.old_messages = self.messages[:-self.keep_recent]
            self.recent_messages = self.messages[-self.keep_recent:]
            print(f"将裁剪为: 保留最近 {self.keep_recent} 条，归档 {len(self.old_messages)} 条旧消息")
        else:
            print(f"消息数量 ({len(self.messages)}) 少于保留数量 ({self.keep_recent})，无需裁剪")
            self.recent_messages = self.messages
            self.old_messages = []
    
    def summarize_old_messages(self):
        """对旧消息生成总结"""
        if not self.old_messages:
            return None
        
        print(f"\n正在分析 {len(self.old_messages)} 条旧消息...")
        
        summary = {
            "trimmed_at": datetime.now().isoformat(),
            "original_file": self.session_file,
            "total_messages_trimmed": len(self.old_messages),
            "total_messages_kept": len(self.recent_messages),
            "time_range": {"start": None, "end": None},
            "topics": [],
            "key_actions": [],
            "files_accessed": [],
            "commands_run": [],
            "participants": set(),
            "message_count": {"user": 0, "assistant": 0, "tool_calls": 0},
            "summary_text": ""
        }
        
        # 提取时间信息
        timestamps = []
        for msg in self.old_messages:
            if "timestamp" in msg:
                try:
                    ts = datetime.fromisoformat(msg["timestamp"].replace('Z', '+00:00'))
                    timestamps.append(ts)
                except (ValueError, TypeError):
                    pass
        
        if timestamps:
            summary["time_range"]["start"] = min(timestamps).isoformat()
            summary["time_range"]["end"] = max(timestamps).isoformat()
        
        # 分析每条消息
        keywords = [
            "创建", "修改", "删除", "文件", "目录", "脚本", "代码",
            "错误", "问题", "解决", "安装", "配置", "部署", "测试",
            "归档", "备份", "压缩", "session", "cron", "定时任务",
            "create", "modify", "delete", "file", "directory", "script",
            "error", "problem", "fix", "install", "config", "deploy", "test"
        ]
        
        for msg in self.old_messages:
            msg_type = msg.get("type", "")
            
            if msg_type == "message":
                message_data = msg.get("message", {})
                role = message_data.get("role", "")
                
                if role == "user":
                    summary["message_count"]["user"] += 1
                elif role == "assistant":
                    summary["message_count"]["assistant"] += 1
                
                # 检查工具调用
                if "toolCalls" in message_data or "tool_calls" in message_data:
                    summary["message_count"]["tool_calls"] += 1
                
                # 提取内容
                content = message_data.get("content", [])
                if isinstance(content, str):
                    content = [{"type": "text", "text": content}]
                
                for item in content:
                    if item.get("type") == "text":
                        text = item.get("text", "")
                        # 提取关键词
                        for keyword in keywords:
                            if keyword in text and keyword not in summary["topics"]:
                                summary["topics"].append(keyword)
                        # 提取文件路径
                        import re
                        paths = re.findall(r'[\w\-\.\/]+\.(py|sh|js|json|md|txt|yaml|yml)', text)
                        for p in paths:
                            if p not in summary["files_accessed"]:
                                summary["files_accessed"].append(p)
                        abs_paths = re.findall(r'\/[\w\-\.\/]+', text)
                        for p in abs_paths:
                            if len(p) > 5 and p not in summary["files_accessed"]:
                                summary["files_accessed"].append(p)
        
        summary["participants"] = list(summary["participants"])
        
        # 生成文本总结
        parts = []
        parts.append(f"裁剪时间: {summary['trimmed_at']}")
        parts.append(f"裁剪消息数: {summary['total_messages_trimmed']} 条")
        parts.append(f"保留消息数: {summary['total_messages_kept']} 条")
        if summary["time_range"]["start"]:
            parts.append(f"旧消息时间范围: {summary['time_range']['start']} 至 {summary['time_range']['end']}")
        parts.append(f"消息统计: 用户 {summary['message_count']['user']} 条, "
                    f"助手 {summary['message_count']['assistant']} 条, "
                    f"工具调用 {summary['message_count']['tool_calls']} 次")
        if summary["topics"]:
            parts.append(f"话题: {', '.join(summary['topics'][:15])}")
        if summary["files_accessed"]:
            parts.append("涉及文件:")
            for f in summary["files_accessed"][:10]:
                parts.append(f"  - {f}")
        
        summary["summary_text"] = "\n".join(parts)
        
        return summary
    
    def trim_session(self, backup_dir=None, summary_dir=None):
        """执行裁剪操作"""
        if not self.old_messages:
            print("没有需要裁剪的旧消息")
            return None
        
        if backup_dir is None:
            backup_dir = Path(self.session_file).parent / "archive"
        if summary_dir is None:
            summary_dir = Path(self.session_file).parent / "summaries"
        
        backup_dir = Path(backup_dir)
        summary_dir = Path(summary_dir)
        backup_dir.mkdir(parents=True, exist_ok=True)
        summary_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. 生成总结
        print("\n=== 步骤 1: 生成旧消息总结 ===")
        summary = self.summarize_old_messages()
        
        if summary:
            base_name = Path(self.session_file).stem
            if base_name.endswith('.jsonl'):
                base_name = base_name[:-6]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 保存总结
            summary_file = summary_dir / f"{base_name}_trim_summary_{timestamp}.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
            print(f"总结已保存: {summary_file}")
            
            # 2. 备份完整的旧文件
            print("\n=== 步骤 2: 备份完整文件 ===")
            backup_file = backup_dir / f"{base_name}_full_{timestamp}.jsonl"
            shutil.copy2(self.session_file, backup_file)
            gzip_file = f"{backup_file}.gz"
            with open(backup_file, 'rb') as f_in:
                with gzip.open(gzip_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(backup_file)
            print(f"完整备份已保存: {gzip_file}")
            
            # 3. 只保留最近的消息
            print("\n=== 步骤 3: 裁剪原文件 ===")
            temp_file = f"{self.session_file}.tmp"
            with open(temp_file, 'w', encoding='utf-8') as f:
                for msg in self.recent_messages:
                    f.write(json.dumps(msg, ensure_ascii=False))
                    f.write('\n')
            
            # 安全替换
            bak_file = f"{self.session_file}.bak"
            if os.path.exists(bak_file):
                os.remove(bak_file)
            os.rename(self.session_file, bak_file)
            os.rename(temp_file, self.session_file)
            os.remove(bak_file)
            
            print(f"原文件已裁剪: 从 {len(self.messages)} 条减少到 {len(self.recent_messages)} 条")
            
            original_size = os.path.getsize(bak_file) if os.path.exists(bak_file) else 0
            new_size = os.path.getsize(self.session_file)
            if original_size > 0:
                reduction = 100 - new_size/original_size*100
                print(f"文件大小: {original_size/(1024*1024):.2f} MB → {new_size/(1024*1024):.2f} MB "
                      f"(减少 {reduction:.1f}%)")
            else:
                print(f"文件大小: {new_size/(1024*1024):.2f} MB")
            
            return {
                "summary_file": str(summary_file),
                "backup_file": str(gzip_file),
                "messages_trimmed": len(self.old_messages),
                "messages_kept": len(self.recent_messages),
                "summary": summary
            }
        
        return None


def main():
    if len(sys.argv) < 2:
        print("用法: python session_trimmer.py <session_file.jsonl> [keep_recent]")
        print("示例: python session_trimmer.py /path/to/session.jsonl 100")
        print("  保留最近 100 条消息，把旧消息总结后归档")
        sys.exit(1)
    
    session_file = sys.argv[1]
    keep_recent = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    
    if not os.path.exists(session_file):
        print(f"错误: 文件不存在: {session_file}")
        sys.exit(1)
    
    print("="*70)
    print("Session 裁剪式智能总结工具")
    print("="*70)
    
    trimmer = SessionTrimmer(session_file, keep_recent)
    trimmer.load_session()
    
    if trimmer.old_messages:
        result = trimmer.trim_session()
        
        if result:
            print("\n" + "="*70)
            print("裁剪完成！总结预览:")
            print("="*70)
            print(result["summary"]["summary_text"])
            print("="*70)
    else:
        print("\n无需裁剪，消息数量在保留限制内")


if __name__ == "__main__":
    main()
