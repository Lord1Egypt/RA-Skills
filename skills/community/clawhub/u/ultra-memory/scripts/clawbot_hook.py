#!/usr/bin/env python3
"""
ultra-memory clawbot auto-hook

在 clawbot 的对话循环中自动触发 ultra-memory 记录，
不依赖模型主动调用，保证任何模型（Claude/Gemini/MiniMax等）记忆都完整。

用法（在 clawbot 的 skill_runner 或对话循环中导入）：
    from clawbot_hook import UltraMemoryHook
    hook = UltraMemoryHook()
    # 每轮对话结束后：
    hook.on_turn_end(session_id, model_name, user_msg, assistant_msg)

此模块放置在 clawbot/core/ 或作为 ultra-memory 技能的一部分。
"""

import subprocess
import re
import os
import json
from pathlib import Path
from datetime import datetime, timezone

# ── 路径配置 ──────────────────────────────────────────────────────────────

def _get_skill_dir():
    """获取 SKILL_DIR，优先级：环境变量 > 默认安装路径"""
    env = os.environ.get("SKILL_DIR")
    if env:
        return Path(env)
    # 尝试常见安装路径
    for p in [
        Path.home() / ".openclaw" / "workspace" / "skills" / "ultra-memory",
        Path(__file__).parent.parent,
    ]:
        if (p / "scripts" / "init.py").exists():
            return p
    return Path(__file__).parent


SKILL_DIR = _get_skill_dir()
LOG_SCRIPT = SKILL_DIR / "scripts" / "log_op.py"
INIT_SCRIPT = SKILL_DIR / "scripts" / "init.py"
SUMMARIZE_SCRIPT = SKILL_DIR / "scripts" / "summarize.py"
ULTRA_MEMORY_HOME = Path(os.environ.get("ULTRA_MEMORY_HOME", Path.home() / ".ultra-memory"))


# ── 核心 Hook 类 ──────────────────────────────────────────────────────────

class UltraMemoryHook:
    """
    ultra-memory 自动 hook。

    在每轮对话结束后自动记录，模型不需要主动调用。
    所有失败静默跳过，不影响主对话流程。
    """

    def __init__(self):
        self._session_id = None  # 当前 session_id

    # ── 对话轮次 Hook ───────────────────────────────────────────────────

    def on_turn_end(
        self,
        session_id: str | None,
        model_name: str,
        user_msg: str,
        assistant_msg: str,
        project: str = "default",
    ):
        """
        每轮对话结束后自动调用。

        Args:
            session_id: 当前会话 ID（未初始化则传入 None）
            model_name: 当前模型名称（claude/gemini/minimax 等）
            user_msg: 本轮用户消息
            assistant_msg: 本轮模型输出
            project: 项目名（从用户消息提取，无法提取用 default）
        """
        # 1. 确保有 session_id
        if not session_id and not self._session_id:
            sid = self._init_session(project)
            if sid:
                self._session_id = sid
            return  # 首次初始化，等待下一轮再记录

        sid = session_id or self._session_id
        if not sid:
            return

        # 2. 自动记录本轮交互
        self._log_turn(sid, model_name, user_msg, assistant_msg)

        # 3. 检查压缩信号
        self._check_compress(sid)

    def _init_session(self, project: str) -> str | None:
        """初始化会话，返回 session_id，失败返回 None"""
        if not INIT_SCRIPT.exists():
            return None

        try:
            result = subprocess.run(
                ["python3", str(INIT_SCRIPT), "--project", project, "--resume"],
                capture_output=True,
                text=True,
                timeout=10,
                errors="replace",
            )
            # 从输出中提取 session_id
            match = re.search(r"session_id:\s*(sess_\w+)", result.stdout)
            if match:
                sid = match.group(1)
                # 读取历史摘要注入上下文（供模型使用）
                self._inject_context(sid)
                return sid
        except Exception:
            pass
        return None

    def _log_turn(
        self,
        session_id: str,
        model_name: str,
        user_msg: str,
        assistant_msg: str,
    ):
        """记录本轮交互，失败静默跳过"""
        if not LOG_SCRIPT.exists():
            return

        summary = f"[{model_name}] 用户: {user_msg[:60]}{'...' if len(user_msg) > 60 else ''}"
        detail = {
            "model": model_name,
            "user_msg_len": len(user_msg),
            "assistant_msg_len": len(assistant_msg),
            "user_preview": user_msg[:100],
            "turn_ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }

        try:
            result = subprocess.run(
                [
                    "python3", str(LOG_SCRIPT),
                    "--session", session_id,
                    "--type", "tool_call",
                    "--summary", summary,
                    "--detail", json.dumps(detail, ensure_ascii=False),
                    "--tags", f"model:{model_name},auto",
                ],
                capture_output=True,
                text=True,
                timeout=5,
                errors="replace",
            )
            # 检查压缩信号
            if "COMPRESS_SUGGESTED" in result.stdout:
                self._auto_summarize(session_id)
        except Exception:
            pass  # 静默跳过，不影响主流程

    def _auto_summarize(self, session_id: str):
        """自动触发摘要压缩"""
        if not SUMMARIZE_SCRIPT.exists():
            return
        try:
            subprocess.run(
                ["python3", str(SUMMARIZE_SCRIPT), "--session", session_id],
                capture_output=True,
                text=True,
                timeout=30,
                errors="replace",
            )
        except Exception:
            pass

    def _inject_context(self, session_id: str):
        """
        从 init.py 输出中读取历史摘要，注入到上下文供模型使用。
        由 clawbot skill_runner 在模型调用前注入。
        """
        # 读取 session 目录下的 summary.md（最近一次压缩结果）
        session_dir = ULTRA_MEMORY_HOME / "sessions" / session_id
        summary_file = session_dir / "summary.md"
        if not summary_file.exists():
            return ""

        try:
            with open(summary_file, encoding="utf-8") as f:
                content = f.read()
            # 只取最后一个摘要块
            blocks = content.split("---")
            return blocks[-1].strip() if blocks else content.strip()
        except Exception:
            return ""

    # ── 工具调用 Hook（可选）─────────────────────────────────────────────

    def on_tool_call(
        self,
        session_id: str | None,
        tool_name: str,
        tool_input: dict,
        tool_output: str,
    ):
        """
        每次工具调用后自动记录（可选，需要 clawbot 支持 post_tool_call hook）。

        Args:
            session_id: 当前会话 ID
            tool_name: 工具名称
            tool_input: 工具输入参数
            tool_output: 工具输出（截断到前200字）
        """
        sid = session_id or self._session_id
        if not sid or not LOG_SCRIPT.exists():
            return

        summary = f"工具调用: {tool_name}"
        detail = {
            "tool": tool_name,
            "input": str(tool_input)[:200],
            "output_preview": tool_output[:200] if tool_output else "",
        }

        try:
            subprocess.run(
                [
                    "python3", str(LOG_SCRIPT),
                    "--session", sid,
                    "--type", "tool_call",
                    "--summary", summary,
                    "--detail", json.dumps(detail, ensure_ascii=False),
                    "--tags", f"tool:{tool_name},auto",
                ],
                capture_output=True,
                timeout=5,
                errors="replace",
            )
        except Exception:
            pass

    # ── 会话管理 ───────────────────────────────────────────────────────

    def get_session_id(self) -> str | None:
        """获取当前 session_id"""
        return self._session_id

    def set_session_id(self, session_id: str):
        """手动设置 session_id（clawbot 恢复会话时调用）"""
        self._session_id = session_id

    def clear(self):
        """清除当前会话（开始新会话时调用）"""
        self._session_id = None
