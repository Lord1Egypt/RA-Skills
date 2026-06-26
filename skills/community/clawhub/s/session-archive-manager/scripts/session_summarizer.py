#!/usr/bin/env python3
"""
Session 智能总结提取工具
分析 session JSONL 文件，提取关键信息并生成可检索的总结
"""

import json
import os
import sys
import gzip
from datetime import datetime
from pathlib import Path
from collections import defaultdict


class SessionSummarizer:
    def __init__(self, session_file):
        self.session_file = session_file
        self.messages = []
        self.summary = {
            "session_id": "",
            "start_time": None,
            "end_time": None,
            "duration_minutes": 0,
            "total_messages": 0,
            "user_messages": 0,
            "assistant_messages": 0,
            "tool_calls": 0,
            "topics": [],
            "key_actions": [],
            "files_accessed": [],
            "commands_run": [],
            "participants": set(),
            "summary_text": "",
            "original_file": session_file,
            "original_size_mb": 0
        }

    def load_session(self):
        """加载 session 文件"""
        print(f"加载文件: {self.session_file}")
        
        # 获取文件大小
        self.summary["original_size_mb"] = os.path.getsize(self.session_file) / (1024 * 1024)
        
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
        
        self.summary["total_messages"] = len(self.messages)
        print(f"加载了 {len(self.messages)} 条消息")

    def analyze_messages(self):
        """分析消息内容"""
        if not self.messages:
            print("没有消息可分析")
            return
        
        # 提取时间信息
        timestamps = []
        for msg in self.messages:
            if "timestamp" in msg:
                try:
                    ts = datetime.fromisoformat(msg["timestamp"].replace('Z', '+00:00'))
                    timestamps.append(ts)
                except (ValueError, TypeError):
                    pass
        
        if timestamps:
            self.summary["start_time"] = min(timestamps).isoformat()
            self.summary["end_time"] = max(timestamps).isoformat()
            duration = (max(timestamps) - min(timestamps)).total_seconds()
            self.summary["duration_minutes"] = round(duration / 60, 1)
        
        # 分析每条消息
        for msg in self.messages:
            msg_type = msg.get("type", "")
            
            # 提取 session ID
            if msg_type == "session" and "id" in msg:
                self.summary["session_id"] = msg["id"]
            
            # 分析 message 类型
            if msg_type == "message":
                self._analyze_message_content(msg)
        
        # 转换 set 为 list 以便 JSON 序列化
        self.summary["participants"] = list(self.summary["participants"])

    def _analyze_message_content(self, msg):
        """分析单条消息的内容"""
        message_data = msg.get("message", {})
        role = message_data.get("role", "")
        
        if role == "user":
            self.summary["user_messages"] += 1
            # 提取发送者信息
            if "sender" in message_data:
                self.summary["participants"].add(message_data["sender"])
        
        elif role == "assistant":
            self.summary["assistant_messages"] += 1
        
        # 分析内容
        content = message_data.get("content", [])
        if isinstance(content, str):
            content = [{"type": "text", "text": content}]
        
        for item in content:
            if item.get("type") == "text":
                text = item.get("text", "")
                self._extract_topics(text)
                self._extract_file_refs(text)
        
        # 检查工具调用
        if "toolCalls" in message_data or "tool_calls" in message_data:
            self.summary["tool_calls"] += 1
            tool_calls = message_data.get("toolCalls", []) or message_data.get("tool_calls", [])
            for call in tool_calls:
                self._analyze_tool_call(call)

    def _extract_topics(self, text):
        """从文本中提取话题关键词"""
        # 简单的关键词提取（实际可以用 NLP 库）
        keywords = [
            "创建", "修改", "删除", "文件", "目录", "脚本", "代码",
            "错误", "问题", "解决", "安装", "配置", "部署", "测试",
            "归档", "备份", "压缩", "session", "cron", "定时任务",
            "create", "modify", "delete", "file", "directory", "script",
            "error", "problem", "fix", "install", "config", "deploy", "test"
        ]
        
        found_topics = []
        for keyword in keywords:
            if keyword in text:
                found_topics.append(keyword)
        
        # 添加到话题列表（去重）
        for topic in found_topics:
            if topic not in self.summary["topics"]:
                self.summary["topics"].append(topic)

    def _extract_file_refs(self, text):
        """提取文件引用"""
        # 简单提取带路径的文件引用
        import re
        # 匹配类路径的字符串
        path_patterns = [
            r'[\w\-\.\/]+\.(py|sh|js|json|md|txt|yaml|yml)',
            r'\/[\w\-\.\/]+'
        ]
        
        for pattern in path_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match) > 3 and match not in self.summary["files_accessed"]:
                    self.summary["files_accessed"].append(match)

    def _analyze_tool_call(self, call):
        """分析工具调用"""
        tool_name = call.get("name", call.get("toolName", ""))
        args = call.get("arguments", {})
        
        action = f"工具调用: {tool_name}"
        
        if tool_name in ["read", "write", "edit"]:
            if "path" in args:
                action += f" ({args['path']})"
                if args["path"] not in self.summary["files_accessed"]:
                    self.summary["files_accessed"].append(args["path"])
        
        elif tool_name == "exec":
            if "command" in args:
                cmd_preview = args["command"][:50] if len(args["command"]) > 50 else args["command"]
                action += f" ({cmd_preview}...)"
                self.summary["commands_run"].append(args["command"])
        
        self.summary["key_actions"].append(action)

    def generate_summary(self):
        """生成文本总结"""
        parts = []
        
        if self.summary["session_id"]:
            parts.append(f"会话 ID: {self.summary['session_id']}")
        
        if self.summary["start_time"]:
            parts.append(f"时间范围: {self.summary['start_time']} 至 {self.summary['end_time']}")
            parts.append(f"持续时间: {self.summary['duration_minutes']} 分钟")
        
        parts.append(f"消息统计: 共 {self.summary['total_messages']} 条 "
                    f"(用户: {self.summary['user_messages']}, "
                    f"助手: {self.summary['assistant_messages']})")
        
        if self.summary["tool_calls"]:
            parts.append(f"工具调用: {self.summary['tool_calls']} 次")
        
        if self.summary["topics"]:
            parts.append(f"话题: {', '.join(self.summary['topics'][:10])}")
        
        if self.summary["key_actions"]:
            parts.append("关键操作:")
            for action in self.summary["key_actions"][:5]:
                parts.append(f"  - {action}")
        
        if self.summary["files_accessed"]:
            parts.append("涉及文件:")
            for f in self.summary["files_accessed"][:10]:
                parts.append(f"  - {f}")
        
        self.summary["summary_text"] = "\n".join(parts)

    def save_summary(self, output_dir=None):
        """保存总结到文件"""
        if output_dir is None:
            output_dir = Path(self.session_file).parent / "summaries"
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成输出文件名
        base_name = Path(self.session_file).stem
        if base_name.endswith('.jsonl'):
            base_name = base_name[:-6]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        summary_file = output_dir / f"{base_name}_summary_{timestamp}.json"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(self.summary, f, ensure_ascii=False, indent=2)
        
        print(f"总结已保存到: {summary_file}")
        return summary_file


def main():
    if len(sys.argv) < 2:
        print("用法: python session_summarizer.py <session_file.jsonl> [output_dir]")
        print("示例: python session_summarizer.py /path/to/session.jsonl")
        sys.exit(1)
    
    session_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(session_file):
        print(f"错误: 文件不存在: {session_file}")
        sys.exit(1)
    
    summarizer = SessionSummarizer(session_file)
    summarizer.load_session()
    summarizer.analyze_messages()
    summarizer.generate_summary()
    
    print("\n" + "="*60)
    print("会话总结:")
    print("="*60)
    print(summarizer.summary["summary_text"])
    print("="*60)
    
    summarizer.save_summary(output_dir)


if __name__ == "__main__":
    main()
