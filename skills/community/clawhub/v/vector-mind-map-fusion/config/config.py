#!/usr/bin/env python3
"""
全局配置
所有路径基于项目根目录，不依赖 /workspace/fusion
"""

import os

from pathlib import Path

# 项目根目录（自动推导）
PROJECT_ROOT = Path(__file__).parent.resolve()

# ===== 数据层路径 =====
MEMORY_ROOT = PROJECT_ROOT / "memory"
MEMORY_STATE = MEMORY_ROOT / "_state"
L2A_DIR = MEMORY_ROOT / "layers" / "l2a"
L2_DIR = MEMORY_ROOT / "layers" / "l2"
HNSW_DIR = MEMORY_ROOT / "layers" / "hnsw"
INFINITYDB_DIR = MEMORY_ROOT / "layers" / "infinitydb"

# ===== Brain.db（固定路径，不在项目内）=====
BRAIN_DB_DIR = os.environ.get("NEURALMEMORY_DIR", os.path.expanduser("~/.local/share/neural-memory"))
BRAIN_DB_PATH = Path(BRAIN_DB_DIR) / "brains.db"

# ===== OpenClaw 会话目录 =====
SESSIONS_DIR = Path(os.environ.get("SESSIONS_DIR", "~/.openclaw/agents/main/sessions")).expanduser()

# ===== Ollama =====
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "bge-m3")
OLLAMA_BATCH_SIZE = int(os.environ.get("OLLAMA_BATCH_SIZE", "20"))
OLLAMA_TIMEOUT_SEC = int(os.environ.get("OLLAMA_TIMEOUT_SEC", "30"))
OLLAMA_MAX_RETRIES = int(os.environ.get("OLLAMA_MAX_RETRIES", "3"))

# ===== 向量维度 =====
VECTOR_DIM = 1024

# ===== L1 配置 =====
MAX_CHUNK_CHARS = 250
OVERLAP_CHARS = 50
COSINE_THRESHOLD_L1 = 0.85
MAX_CONTENT_LENGTH = 5000
L1_RAW_CHUNKS_TMP = MEMORY_STATE / "l1_raw_chunks_tmp.jsonl"

# ===== L2 配置 =====
WINDOW_SIZE = 200
OVERLAP = 100
SQLITE_BATCH_SIZE = 200
MAX_CHUNKS_PER_RUN = 5000

# ===== L3 配置 =====
L3_SCHEMA_THRESHOLD = 5
L3_SCHEMA_PRIORITY = 4
HNSW_BATCH_SIZE = 500
HNSW_MAX_ELEMENTS = 10000

# ===== 召回配置 =====
MAX_SPREAD_HOPS = 3
ACTIVATION_THRESHOLD = 0.3
DIMINISHING_RETURNS_ENABLED = True
DIMINISHING_RETURNS_THRESHOLD = 0.15
