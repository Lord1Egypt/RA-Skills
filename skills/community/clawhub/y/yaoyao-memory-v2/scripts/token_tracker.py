#!/usr/bin/env python3
"""Token 消耗追踪系统
按小任务和大任务分类统计 token 消耗
"""
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# 状态文件
TOKEN_STATE_FILE = Path.home() / ".openclaw" / "workspace" / "memory" / "token-state.json"

# Token 阈值
SMALL_TASK_THRESHOLD = 100000  # 10万 tokens 以下为小任务
LARGE_TASK_THRESHOLD = 500000  # 50万 tokens 以上为大任务

class TokenTracker:
    """Token 消耗追踪器"""
    
    def __init__(self):
        self.load_state()
    
    def load_state(self):
        """加载状态"""
        if TOKEN_STATE_FILE.exists():
            self.state = json.loads(TOKEN_STATE_FILE.read_text())
        else:
            self.state = {
                "small_tasks": [],
                "large_tasks": [],
                "total_tokens": 0,
                "session_start": datetime.now().isoformat()
            }
    
    def save_state(self):
        """保存状态"""
        TOKEN_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        TOKEN_STATE_FILE.write_text(json.dumps(self.state, indent=2))
    
    def record_task(self, task_name: str, input_tokens: int, output_tokens: int, 
                   task_type: str = "auto", duration_ms: int = 0):
        """记录任务消耗
        
        Args:
            task_name: 任务名称
            input_tokens: 输入 token 数
            output_tokens: 输出 token 数
            task_type: 任务类型 ("small", "large", "auto")
            duration_ms: 任务耗时(毫秒)
        """
        total = input_tokens + output_tokens
        
        # 自动判断任务大小
        if task_type == "auto":
            if total < SMALL_TASK_THRESHOLD:
                task_type = "small"
            elif total > LARGE_TASK_THRESHOLD:
                task_type = "large"
            else:
                task_type = "medium"
        
        task_record = {
            "name": task_name,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total,
            "type": task_type,
            "duration_ms": duration_ms,
            "timestamp": datetime.now().isoformat()
        }
        
        if task_type == "small":
            self.state["small_tasks"].append(task_record)
            # 只保留最近100条
            self.state["small_tasks"] = self.state["small_tasks"][-100:]
        elif task_type == "large":
            self.state["large_tasks"].append(task_record)
            # 只保留最近50条
            self.state["large_tasks"] = self.state["large_tasks"][-50:]
        else:
            # medium 任务也记录
            self.state.setdefault("medium_tasks", []).append(task_record)
        
        self.state["total_tokens"] += total
        self.save_state()
        
        return task_record
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        small_total = sum(t["total_tokens"] for t in self.state.get("small_tasks", []))
        large_total = sum(t["total_tokens"] for t in self.state.get("large_tasks", []))
        medium_total = sum(t["total_tokens"] for t in self.state.get("medium_tasks", []))
        
        return {
            "total_tokens": self.state.get("total_tokens", 0),
            "small_tasks": {
                "count": len(self.state.get("small_tasks", [])),
                "total_tokens": small_total,
                "avg_tokens": small_total // len(self.state.get("small_tasks", [1]))
            },
            "large_tasks": {
                "count": len(self.state.get("large_tasks", [])),
                "total_tokens": large_total,
                "avg_tokens": large_total // len(self.state.get("large_tasks", [1]))
            },
            "medium_tasks": {
                "count": len(self.state.get("medium_tasks", [])),
                "total_tokens": medium_total
            },
            "session_start": self.state.get("session_start")
        }
    
    def report(self) -> str:
        """生成报告"""
        stats = self.get_stats()
        
        total = stats["total_tokens"]
        small = stats["small_tasks"]
        large = stats["large_tasks"]
        medium = stats["medium_tasks"]
        
        # 估算成本（假设 $0.1/1M tokens）
        cost = total / 1_000_000 * 0.1
        
        report = f"""
💰 Token 消耗报告
{'='*40}
总消耗: {total:,} tokens (≈ ${cost:.4f})

📊 小任务 (≤{SMALL_TASK_THRESHOLD:,} tokens)
  数量: {small['count']} 个
  总消耗: {small['total_tokens']:,} tokens
  平均: {small['avg_tokens']:,} tokens/个

📊 大任务 (>{LARGE_TASK_THRESHOLD:,} tokens)
  数量: {large['count']} 个
  总消耗: {large['total_tokens']:,} tokens
  平均: {large['avg_tokens']:,} tokens/个
"""
        
        if medium['count'] > 0:
            report += f"""
📊 中等任务
  数量: {medium['count']} 个
  总消耗: {medium['total_tokens']:,} tokens
"""
        
        return report

# 全局实例
_tracker = None

def get_tracker() -> TokenTracker:
    """获取追踪器实例（单例）"""
    global _tracker
    if _tracker is None:
        _tracker = TokenTracker()
    return _tracker

def record_task(task_name: str, input_tokens: int, output_tokens: int,
               task_type: str = "auto", duration_ms: int = 0):
    """快捷记录任务"""
    tracker = get_tracker()
    return tracker.record_task(task_name, input_tokens, output_tokens, task_type, duration_ms)

def get_token_stats() -> Dict:
    """获取统计"""
    return get_tracker().get_stats()

def print_token_report():
    """打印报告"""
    print(get_tracker().report())

if __name__ == "__main__":
    # 测试
    print("=== Token Tracker 测试 ===")
    
    tracker = get_tracker()
    
    # 模拟小任务
    tracker.record_task("小查询", 1000, 500, "small", 100)
    
    # 模拟大任务
    tracker.record_task("大任务", 300000, 200000, "large", 5000)
    
    # 自动判断
    tracker.record_task("自动判断-小", 50000, 30000, "auto", 1000)
    tracker.record_task("自动判断-大", 400000, 300000, "auto", 10000)
    
    print(tracker.report())
    print(f"\nStats: {tracker.get_stats()}")
