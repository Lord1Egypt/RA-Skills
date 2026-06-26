#!/usr/bin/env python3
"""Token 消耗追踪系统 - 全局自动追踪版
每次对话自动追踪，单次消耗报告，总数按需查询
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

# Token 阈值
SMALL_TASK_THRESHOLD = 100000
LARGE_TASK_THRESHOLD = 500000

# 状态文件
TOKEN_STATE_FILE = Path.home() / ".openclaw" / "workspace" / "memory" / "token-state.json"

class TokenTracker:
    """全局 Token 追踪器"""
    
    def __init__(self):
        self.state_file = TOKEN_STATE_FILE
        self.load_state()
        # 每次初始化检查是否需要启动新任务
        self._check_session()
    
    def load_state(self):
        """加载状态"""
        if self.state_file.exists():
            self.state = json.loads(self.state_file.read_text())
        else:
            self.state = self._default_state()
    
    def _default_state(self) -> dict:
        return {
            "current_session": None,
            "session_start_time": None,
            "session_input_tokens": 0,
            "session_output_tokens": 0,
            "total_tokens": 0,
            "small_tasks": [],
            "large_tasks": [],
            "session_history": [],
            "last_report_time": None
        }
    
    def _check_session(self):
        """检查会话"""
        now = datetime.now()
        # 如果没有当前会话或距离上次报告超过5分钟，开启新会话
        if not self.state.get("current_session"):
            self.start_session()
    
    def start_session(self, session_name: Optional[str] = None):
        """开始新会话"""
        import uuid
        self.state["current_session"] = session_name or f"session_{uuid.uuid4().hex[:8]}"
        self.state["session_start_time"] = now_str()
        self.state["session_input_tokens"] = 0
        self.state["session_output_tokens"] = 0
        self.save_state()
    
    def record_session_tokens(self, input_tokens: int, output_tokens: int):
        """记录本会话 Token 消耗（自动从环境/上下文获取）"""
        self.state["session_input_tokens"] += input_tokens
        self.state["session_output_tokens"] += output_tokens
        self.state["total_tokens"] += (input_tokens + output_tokens)
        self.save_state()
    
    def save_state(self):
        """保存状态"""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(self.state, indent=2))
    
    def end_session(self) -> dict:
        """结束当前会话，返回单次报告"""
        session_name = self.state.get("current_session", "unknown")
        input_t = self.state.get("session_input_tokens", 0)
        output_t = self.state.get("session_output_tokens", 0)
        total = input_t + output_t
        
        start_time = self.state.get("session_start_time")
        duration = 0
        if start_time:
            from datetime import datetime
            start = datetime.fromisoformat(start_time)
            duration = int((datetime.now() - start).total_seconds())
        
        # 判断任务大小
        if total < SMALL_TASK_THRESHOLD:
            task_type = "small"
            icon = "📊"
        elif total > LARGE_TASK_THRESHOLD:
            task_type = "large"
            icon = "💎"
        else:
            task_type = "medium"
            icon = "📋"
        
        # 保存到历史
        record = {
            "name": session_name,
            "input_tokens": input_t,
            "output_tokens": output_t,
            "total_tokens": total,
            "type": task_type,
            "duration": duration,
            "timestamp": now_str()
        }
        
        if task_type == "small":
            self.state["small_tasks"].append(record)
            self.state["small_tasks"] = self.state["small_tasks"][-100:]
        elif task_type == "large":
            self.state["large_tasks"].append(record)
            self.state["large_tasks"] = self.state["large_tasks"][-50:]
        
        self.state["session_history"].append(record)
        self.state["session_history"] = self.state["session_history"][-20:]
        if "session_history" not in self.state:
            self.state["session_history"] = []
        self.state["current_session"] = None
        self.state["session_start_time"] = None
        self.state["session_input_tokens"] = 0
        self.state["session_output_tokens"] = 0
        self.state["last_report_time"] = now_str()
        self.save_state()
        
        return record
    
    def format_single_report(self, record: dict) -> str:
        """格式化单次报告"""
        total = record["total_tokens"]
        task_type = record["type"]
        duration = record.get("duration", 0)
        icon = {"small": "📊", "medium": "📋", "large": "💎"}.get(task_type, "📋")
        
        return f"""{icon} 任务完成: {record['name']}

📥 输入: {record['input_tokens']:,} tokens
📤 输出: {record['output_tokens']:,} tokens
💎 总计: {total:,} tokens ({task_type})
⏱️ 耗时: {duration}s"""
    
    def get_total_stats(self) -> dict:
        """获取累计统计"""
        return {
            "total_tokens": self.state.get("total_tokens", 0),
            "small_tasks_count": len(self.state.get("small_tasks", [])),
            "large_tasks_count": len(self.state.get("large_tasks", [])),
            "all_sessions_count": len(self.state.get("session_history", []))
        }
    
    def format_total_report(self) -> str:
        """格式化累计报告"""
        total = self.state.get("total_tokens", 0)
        small = self.state.get("small_tasks", [])
        large = self.state.get("large_tasks", [])
        
        small_total = sum(t["total_tokens"] for t in small)
        large_total = sum(t["total_tokens"] for t in large)
        
        cost = total / 1_000_000 * 0.1
        
        return f"""💰 Token 累计报告

📊 小任务: {len(small)}个, {small_total:,} tokens
💎 大任务: {len(large)}个, {large_total:,} tokens
💎 总消耗: {total:,} tokens (≈ ${cost:.4f})"""


def now_str() -> str:
    return datetime.now().isoformat()


# 全局实例（延迟初始化）
_tracker = None

def get_tracker() -> TokenTracker:
    global _tracker
    if _tracker is None:
        _tracker = TokenTracker()
    return _tracker

def auto_record(input_tokens: int, output_tokens: int):
    """自动记录（全局规则）"""
    get_tracker().record_session_tokens(input_tokens, output_tokens)

def end_and_report() -> Optional[str]:
    """结束会话并报告"""
    tracker = get_tracker()
    if tracker.state.get("current_session"):
        record = tracker.end_session()
        return tracker.format_single_report(record)
    return None

def get_total() -> str:
    """获取累计报告"""
    return get_tracker().format_total_report()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 token_reporter.py record <输入> <输出>")
        print("  python3 token_reporter.py end")
        print("  python3 token_reporter.py total")
        print("  python3 token_reporter.py status")
        sys.exit(1)
    
    cmd = sys.argv[1]
    tracker = get_tracker()
    
    if cmd == "record":
        input_t = int(sys.argv[2])
        output_t = int(sys.argv[3])
        tracker.record_session_tokens(input_t, output_t)
        print(f"✅ 已记录: 输入{input_t} + 输出{output_t}")
    
    elif cmd == "end":
        report = end_and_report()
        if report:
            print(report)
        else:
            print("❌ 没有进行中的任务")
    
    elif cmd == "total":
        print(get_total())
    
    elif cmd == "status":
        stats = tracker.get_total_stats()
        print(f"📊 当前状态:")
        print(f"  进行中: {tracker.state.get('current_session', '无')}")
        print(f"  本会话: 输入{tracker.state.get('session_input_tokens',0):,} + 输出{tracker.state.get('session_output_tokens',0):,}")
        print(f"  总消耗: {stats['total_tokens']:,}")
    
    else:
        print(f"❓ 未知命令: {cmd}")
