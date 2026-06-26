#!/usr/bin/env python3
"""
OpenClaw 秘书式记忆系统 - 会话自动摘要
在会话结束时生成结构化摘要，写入 daily/YYYY-MM-DD.md

用法:
    python3 session_summary.py --session "会话内容..." --topics "话题1, 话题2"
    python3 session_summary.py --session "..." --topics "..." --dry-run
    python3 session_summary.py --test  # 干跑测试
    python3 session_summary.py --watch     # 持续监控模式（实时增量写入）
    python3 session_summary.py --append    # 追加模式：将内容追加到当日日志
"""

import os
import re
import json
import time
import signal
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import argparse

# ============== 配置 ==============
MEMORY_DIR = Path(os.environ.get("OPENCLAW_MEMORY_DIR", "/root/.openclaw/workspace/memory"))
DAILY_DIR = MEMORY_DIR / "daily"
SESSION_FILE = MEMORY_DIR / "session.log"  # 当前会话日志文件

# ============== 增量写入状态 ==============

class IncrementalWriter:
    """增量写入器 - 支持实时追加"""

    def __init__(self, daily_dir: Path):
        self.daily_dir = daily_dir
        self.daily_dir.mkdir(parents=True, exist_ok=True)
        self.last_position = 0

    def get_today_file(self) -> Path:
        """获取今日日志文件路径，不存在则创建"""
        today = datetime.now().strftime("%Y-%m-%d")
        f = self.daily_dir / f"{today}.md"
        if not f.exists():
            f.write_text(f"# {today}\n\n", encoding="utf-8")
        return f

    def append_incremental(self, content: str, session_id: str = "") -> Tuple[bool, str]:
        """增量追加内容到当日日志（立即刷盘）

        Args:
            content: 要追加的内容
            session_id: 会话ID（可选）

        Returns:
            (成功标志, 消息)
        """
        if not content.strip():
            return False, "空内容，无需写入"

        try:
            today_file = self.get_today_file()
            timestamp = datetime.now().strftime("%H:%M")

            # 构建写入内容
            lines = [f"\n## {timestamp}"]
            if session_id:
                lines.append(f" [会话: {session_id}]")
            lines.append(" - 会话摘要\n\n")
            lines.append(content.strip())
            lines.append("\n")

            entry = ''.join(lines)

            # 追加内容并立即刷盘
            with open(today_file, "a", encoding="utf-8") as f:
                f.write(entry)
                f.flush()
                os.fsync(f.fileno())  # 立即刷到磁盘

            return True, f"已增量追加到 {today_file.name} ({len(content)} 字符)"
        except Exception as e:
            return False, f"增量写入失败: {e}"

    def read_new_content(self, source_file: Path) -> Tuple[str, int]:
        """读取文件新增内容

        Returns:
            (新增内容, 新位置)
        """
        if not source_file.exists():
            return "", 0

        try:
            with open(source_file, "r", encoding="utf-8") as f:
                f.seek(self.last_position)
                new_content = f.read()
                f.seek(0, 2)
                new_position = f.tell()
            return new_content, new_position
        except Exception:
            return "", 0

    def watch_and_append(self, source_file: Path, interval: int = 2, session_id: str = "") -> bool:
        """持续监控源文件，实时增量追加到 daily/

        Args:
            source_file: 监控的源文件
            interval: 检查间隔（秒）
            session_id: 会话ID

        Returns:
            正常返回 True，收到停止信号返回 False
        """
        self.last_position = 0
        running = [True]  # 用列表包装以便在回调中修改

        def signal_handler(sig, frame):
            running[0] = False

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        print(f"[Watch] 开始监控 {source_file} (间隔 {interval}s)...")
        print(f"[Watch] 按 Ctrl+C 停止\n")

        # 如果源文件存在，读取已有内容长度（避免重复追加）
        if source_file.exists():
            try:
                with open(source_file, "r", encoding="utf-8") as f:
                    f.seek(0, 2)
                    self.last_position = f.tell()
            except Exception:
                pass

        last_content = ""
        consecutive_empty = 0

        while running[0]:
            try:
                new_content, new_position = self.read_new_content(source_file)

                if new_content.strip() and new_content != last_content:
                    # 检测到新内容
                    consecutive_empty = 0
                    last_content = new_content

                    # 追加到 daily/
                    success, msg = self.append_incremental(new_content, session_id)
                    if success:
                        print(f"[Watch] {datetime.now().strftime('%H:%M:%S')} - 已追加新内容")

                    self.last_position = new_position
                else:
                    consecutive_empty += 1

                time.sleep(interval)

            except Exception as e:
                print(f"[Watch] 监控异常: {e}")
                time.sleep(interval)

        print("[Watch] 监控已停止")
        return True


# ============== 工具函数 ==============

def ensure_daily_dir():
    """确保 daily 目录存在"""
    DAILY_DIR.mkdir(parents=True, exist_ok=True)


def get_today_file() -> Path:
    """获取今日日志文件路径，不存在则创建空文件"""
    ensure_daily_dir()
    today = datetime.now().strftime("%Y-%m-%d")
    f = DAILY_DIR / f"{today}.md"
    if not f.exists():
        f.write_text(f"# {today}\n\n", encoding="utf-8")
    return f


def get_timestamp() -> str:
    """获取当前时间戳"""
    return datetime.now().strftime("%H:%M")


def parse_session(session_text: str) -> Dict[str, any]:
    """解析会话内容，提取关键信息"""
    result = {
        "topics": [],
        "decisions": [],
        "tasks": [],
        "entities": []
    }

    if not session_text:
        return result

    # 提取话题（## 开头的或 --topics 传入的）
    topic_patterns = [
        r'(?:话题|topic|主题)[:：]\s*(.+?)(?:\n|$)',
        r'##\s+(.+)',
    ]
    for pattern in topic_patterns:
        matches = re.findall(pattern, session_text, re.IGNORECASE)
        result["topics"].extend([m.strip() for m in matches if len(m.strip()) > 1])

    # 提取决策
    decision_patterns = [
        r'(?:决定|决策|最终选择|采用|选择)[:：]\s*(.+?)(?:\n|$)',
        r'(?:决定|决策)[:：]\s*(.+?)(?:\n|$)',
    ]
    for pattern in decision_patterns:
        matches = re.findall(pattern, session_text)
        result["decisions"].extend([m.strip() for m in matches if len(m.strip()) > 2])

    # 提取任务（- [ ] 或 - [x] 格式）
    task_patterns = [
        r'(?:- \[.\]|\* \[.\])\s*(.+?)(?:\n|$)',
        r'(?:任务|task)[:：]\s*(.+?)(?:\n|$)',
    ]
    for pattern in task_patterns:
        matches = re.findall(pattern, session_text, re.IGNORECASE)
        result["tasks"].extend([m.strip() for m in matches if len(m.strip()) > 2])

    # 提取技术实体
    entity_patterns = [
        r'(React|Flask|LangGraph|RAG|OpenClaw|Claude|MiniMax|Stm32|Python|JavaScript)',
        r'([\u4e00-\u9fa5]{2,10}(?:框架|库|系统|架构|项目))',
    ]
    for pattern in entity_patterns:
        matches = re.findall(pattern, session_text)
        result["entities"].extend([m.strip() for m in matches if len(m.strip()) > 1])

    # 去重
    for key in result:
        result[key] = list(dict.fromkeys(result[key]))

    return result


def format_summary(session_text: str, topics_input: str = "") -> str:
    """生成格式化摘要"""
    parsed = parse_session(session_text)

    # 如果传入了 --topics 参数，合并到 topics
    if topics_input:
        additional_topics = [t.strip() for t in topics_input.split(",") if t.strip()]
        parsed["topics"].extend(additional_topics)
        parsed["topics"] = list(dict.fromkeys(parsed["topics"]))

    timestamp = get_timestamp()

    lines = [f"\n## {timestamp} - 会话摘要\n"]

    if parsed["topics"]:
        lines.append(f"- 话题: {', '.join(parsed['topics'][:5])}")

    if parsed["decisions"]:
        lines.append(f"- 决策: {', '.join(parsed['decisions'][:3])}")

    if parsed["tasks"]:
        lines.append(f"- 任务: {', '.join(parsed['tasks'][:3])}")

    if parsed["entities"]:
        lines.append(f"- 技术: {', '.join(parsed['entities'][:5])}")

    # 如果有原始会话内容，追加第一行作为摘要
    if session_text and not parsed["topics"] and not parsed["decisions"]:
        first_line = session_text.strip().split('\n')[0][:100]
        if first_line:
            lines.append(f"- 内容: {first_line}")

    return '\n'.join(lines)


def append_to_daily(summary: str) -> Tuple[bool, str]:
    """追加摘要到今日日志"""
    if not summary.strip():
        return False, "空摘要，无需写入"

    try:
        today_file = get_today_file()
        current_content = today_file.read_text(encoding="utf-8")
        current_content += summary + "\n"
        today_file.write_text(current_content, encoding="utf-8")
        return True, f"已追加到 {today_file.name}"
    except Exception as e:
        return False, f"写入失败: {e}"


def generate_json_output(session_text: str, topics_input: str) -> Dict:
    """生成 JSON 格式输出"""
    parsed = parse_session(session_text)

    if topics_input:
        additional_topics = [t.strip() for t in topics_input.split(",") if t.strip()]
        parsed["topics"].extend(additional_topics)
        parsed["topics"] = list(dict.fromkeys(parsed["topics"]))

    return {
        "timestamp": get_timestamp(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "topics": parsed["topics"][:10],
        "decisions": parsed["decisions"][:5],
        "tasks": parsed["tasks"][:5],
        "entities": parsed["entities"][:10],
        "raw_preview": session_text[:200] if session_text else ""
    }


# ============== 主程序 =============

def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw 秘书式记忆系统 - 会话摘要",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python3 session_summary.py --session "今天讨论了..." --topics "项目X,架构"
    python3 session_summary.py --session "..." --dry-run        # 预览不写入
    python3 session_summary.py --watch                         # 持续监控实时追加
    python3 session_summary.py --watch --session-id xxx        # 带会话ID的监控
    python3 session_summary.py --test                         # 测试模式
        """
    )
    parser.add_argument("--session", "-s", default="", help="会话内容")
    parser.add_argument("--topics", "-t", default="", help="话题列表（逗号分隔）")
    parser.add_argument("--dry-run", action="store_true", help="预览摘要，不写入文件")
    parser.add_argument("--json", "-j", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--test", action="store_true", help="测试模式")
    parser.add_argument("--watch", "-w", action="store_true", help="持续监控模式：实时增量追加")
    parser.add_argument("--session-id", default="", help="会话ID（用于追踪）")
    parser.add_argument("--interval", type=int, default=2, help="监控检查间隔秒数 (默认2)")

    args = parser.parse_args()

    # 持续监控模式
    if args.watch:
        ensure_daily_dir()
        writer = IncrementalWriter(DAILY_DIR)
        writer.watch_and_append(SESSION_FILE, interval=args.interval, session_id=args.session_id)
        return

    # 测试模式
    if args.test:
        test_session = """今天讨论了项目X的架构设计
        决定采用微服务架构
        任务：完成技术选型报告
        话题：架构设计、微服务、技术选型"""
        print("[Test] 测试会话摘要生成:")
        print(f"  输入: {test_session[:50]}...")
        summary = format_summary(test_session, "架构,微服务")
        print(f"  摘要:\n{summary}")
        return

    if not args.session and not args.topics:
        parser.print_help()
        print("\n[Error] 请提供 --session 或 --topics 参数")
        return

    summary = format_summary(args.session, args.topics)

    if args.json:
        output = generate_json_output(args.session, args.topics)
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    if args.dry_run:
        print("[Dry Run] 预览摘要:")
        print(summary)
        return

    success, msg = append_to_daily(summary)
    if success:
        print(f"[OK] {msg}")
    else:
        print(f"[Warning] {msg}")


if __name__ == "__main__":
    main()
