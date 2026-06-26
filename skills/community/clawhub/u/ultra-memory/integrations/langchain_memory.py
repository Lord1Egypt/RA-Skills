#!/usr/bin/env python3
"""
ultra-memory: LangChain Memory 集成
提供 UltraMemoryMemory 类，实现 LangChain BaseMemory 接口，
可直接用于 LC agents。

用法:
    from integrations.langchain_memory import UltraMemoryMemory
    memory = UltraMemoryMemory(session_id="sess_langchain_test", project="my-agent")
    agent = OpenAIAgent(..., memory=memory)
"""

import json
import os
import sys
from pathlib import Path
from typing import Any

try:
    from langchain.schema import BaseMemory
    from langchain.schema import HumanMessage, AIMessage
    HAS_LANGCHAIN = True
except ImportError:
    HAS_LANGCHAIN = False

ULTRA_MEMORY_HOME = Path(os.environ.get("ULTRA_MEMORY_HOME", Path.home() / ".ultra-memory"))
_SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"


class UltraMemoryMemory:
    """
    LangChain memory backed by ultra-memory's 5-layer system.
    Implements BaseMemory-compatible interface.
    """

    def __init__(
        self,
        session_id: str,
        project: str = "langchain",
        top_k: int = 5,
    ):
        self.session_id = session_id
        self.project = project
        self.top_k = top_k

    @property
    def memory_variables(self) -> list[str]:
        return ["ultra_memory_context"]

    def load_memory_variables(self, inputs: dict) -> dict:
        """加载与当前上下文相关的记忆"""
        query = inputs.get("query", "")

        if not self.session_id:
            return {"ultra_memory_context": ""}

        if query:
            # 使用 recall 获取相关记忆
            import subprocess, io
            recall_script = _SCRIPTS_DIR / "recall.py"
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            try:
                subprocess.run(
                    [sys.executable, str(recall_script),
                     "--session", self.session_id,
                     "--query", query,
                     "--top-k", str(self.top_k)],
                    capture_output=True,
                    timeout=30,
                )
                context = sys.stdout.getvalue()
            except Exception:
                context = ""
            finally:
                sys.stdout = old_stdout
        else:
            # 加载最新摘要
            summary_file = ULTRA_MEMORY_HOME / "sessions" / self.session_id / "summary.md"
            if summary_file.exists():
                context = summary_file.read_text(encoding="utf-8")
            else:
                context = ""

        return {"ultra_memory_context": context}

    def save_context(self, inputs: dict, outputs: dict) -> None:
        """保存一轮对话到 ultra-memory"""
        import subprocess

        input_text = inputs.get("input", "")[:200]
        output_text = outputs.get("output", "")[:200]

        detail = {
            "input": inputs.get("input", ""),
            "output": outputs.get("output", ""),
        }

        try:
            subprocess.run(
                [
                    sys.executable,
                    str(_SCRIPTS_DIR / "log_op.py"),
                    "--session", self.session_id,
                    "--type", "tool_call",
                    "--summary", f"LC: {input_text[:60]}",
                    "--detail", json.dumps(detail, ensure_ascii=False),
                    "--tags", "langchain",
                ],
                capture_output=True,
                timeout=5,
            )
        except Exception:
            pass

    def clear(self) -> None:
        """清除当前记忆（不删除 session）"""
        self.session_id = None
