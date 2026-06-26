"""Shared utilities for CLI sub-modules — argument helpers, formatters, and common imports."""

from __future__ import annotations

import sys
import os
import json
import sqlite3
import logging
from argparse import Namespace
from datetime import datetime

# 项目目录
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(PROJECT_DIR, "memory.db")
_MODEL_SERVER_WARNED = False

try:
    from document_parser import DocumentParser
    _HAS_DOCUMENT_PARSER = True
except ImportError:
    _HAS_DOCUMENT_PARSER = False

try:
    from semantic_chunker import SemanticChunker
    _HAS_SEMANTIC_CHUNKER = True
except ImportError:
    _HAS_SEMANTIC_CHUNKER = False

try:
    from chunk_indexer import ChunkIndexer
    _HAS_CHUNK_INDEXER = True
except ImportError:
    _HAS_CHUNK_INDEXER = False

try:
    from chunk_retriever import ChunkRetriever
    _HAS_CHUNK_RETRIEVER = True
except ImportError:
    _HAS_CHUNK_RETRIEVER = False

try:
    from chat_parser import ChatParser
    from personality_analyzer import PersonalityAnalyzer
    from personality_memory import PersonalityMemory
    _HAS_PERSONALITY = True
except ImportError:
    _HAS_PERSONALITY = False


def get_memory():
    """获取 AgentMemory 实例"""
    from agent_memory.memory_system import AgentMemory
    return AgentMemory(
        db_path=DB_PATH,
        project_dir=PROJECT_DIR,
        enable_semantic=True,
    )


def _check_model_server():
    """检测 model_server 是否在运行，未运行则自动启动"""
    global _MODEL_SERVER_WARNED
    if _MODEL_SERVER_WARNED:
        return
    _MODEL_SERVER_WARNED = True

    # 只有 local 后端需要守护进程（hash/openai/cohere/voyage 不需要）
    backend = os.environ.get("AGENT_MEMORY_EMBEDDING_BACKEND", "local").lower()
    if backend != "local":
        return

    # 检查守护进程是否已经在运行
    try:
        from model_server import is_running
        if is_running():
            return  # 已在线，直接返回
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.warning("cli: %s", e)

    # 自动启动守护进程
    try:
        print("⏳ 模型守护进程未启动，正在后台加载模型...", file=sys.stderr, flush=True)
        from model_server import start_server
        start_server(daemon=True)
        print("✅ 模型守护进程已启动", file=sys.stderr, flush=True)
    except Exception as e:
        print(
            f"⚠️  守护进程启动失败 ({e})，回退到冷启动模式（首次操作约 10-15s）。\n"
            f"   手动启动: python3 {os.path.join(PROJECT_DIR, 'model_server.py')} start",
            file=sys.stderr,
        )
