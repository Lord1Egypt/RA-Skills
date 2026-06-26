#!/usr/bin/env python3
"""
embed_backends.py - 统一 Embedding 后端（OpenAI / 硅基流动 / 智谱 GLM）

支持后端：
  openai       — OpenAI text-embedding-ada-002 (1536维)
  siliconflow  — 硅基流动 BGE-M3 (1024维，免费)
  zhipu        — 智谱 glm-embedding-3 (1024维)

配置优先级：
  1. 环境变量  EMBED_BACKEND / OPENAI_API_KEY / SILICONFLOW_API_KEY / ZHIPU_API_KEY
  2. 配置文件  .memory_config.json（与 .memory_vectors.db 同目录）

用法：
  from embed_backends import get_embedding, list_backends, get_backend_info

  # 单条
  vec = get_embedding("你好世界")

  # 批量（自动分批）
  vecs = get_embeddings(["text1", "text2"])

  # 获取当前后端信息
  info = get_backend_info()
  print(info["dim"], info["name"])
"""

import os
import json
import sqlite3
from pathlib import Path
from typing import List, Optional, Dict, Any, Union

try:
    import numpy as np
except ImportError:
    np = None

try:
    from openai import OpenAI as _OpenAI
except ImportError:
    _OpenAI = None

# ── 后端定义 ──────────────────────────────────────────────

BACKENDS = {
    "openai": {
        "name": "OpenAI text-embedding-ada-002",
        "dim": 1536,
        "model": "text-embedding-ada-002",
        "batch_size": 100,
        "key_env": "OPENAI_API_KEY",
        "base_url": None,  # 使用 OpenAI 默认
    },
    "siliconflow": {
        "name": "SiliconFlow BGE-M3",
        "dim": 1024,
        "model": "BGE-M3",
        "batch_size": 50,
        "key_env": "SILICONFLOW_API_KEY",
        "base_url": "https://api.siliconflow.cn/v1",
    },
    "zhipu": {
        "name": "智谱 GLM-embedding-3",
        "dim": 1024,
        "model": "glm-embedding-3",
        "batch_size": 50,
        "key_env": "ZHIPU_API_KEY",
        "base_url": "https://open.bigmodel.cn/api/paas/v4/embeddings",
    },
}


def _load_config(db_path):
    """从 .memory_config.json 读取后端配置"""
    cfg_file = str(Path(db_path).with_name(".memory_config.json"))
    if os.path.exists(cfg_file):
        try:
            with open(cfg_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def _resolve_backend(db_path=None):
    """
    解析使用哪个后端。
    优先级：环境变量 EMBED_BACKEND > .memory_config.json > 默认 openai
    """
    backend = os.environ.get("EMBED_BACKEND", "").lower()
    if not backend:
        cfg = _load_config(db_path) if db_path else {}
        backend = cfg.get("backend", "openai")

    if backend not in BACKENDS:
        raise ValueError(
            f"未知后端: {backend}，可用: {', '.join(BACKENDS.keys())}"
        )
    return backend


def _get_api_key(backend_key_env):
    """获取 API key，支持多个环境变量名"""
    for env_var in [backend_key_env, "OPENAI_API_KEY", "ANTHROPIC_API_KEY"]:
        key = os.environ.get(env_var)
        if key:
            return key
    return None


# ── 向量维度查询 ──────────────────────────────────────────

def get_embedding_dim(db_path=None, backend=None):
    """获取当前后端的向量维度（不调用 API）"""
    if backend is None:
        backend = _resolve_backend(db_path)
    return BACKENDS[backend]["dim"]


def get_backend_info(db_path=None):
    """获取当前后端的元信息"""
    backend = _resolve_backend(db_path)
    info = BACKENDS[backend].copy()
    info["backend"] = backend
    # 不暴露 key
    info.pop("key_env", None)
    return info


# ── Embed 调用 ────────────────────────────────────────────

def get_embedding(text: str, db_path: Optional[str] = None, backend: Optional[str] = None):
    """
    获取单条文本的 embedding 向量（numpy array, float32）
    """
    vecs = get_embeddings([text], db_path=db_path, backend=backend)
    return vecs[0]


def get_embeddings(texts: List[str], db_path: Optional[str] = None, backend: Optional[str] = None) -> List:
    """
    批量获取 embeddings。

    返回: List[numpy.ndarray]，每个向量 dtype=float32

    自动分批：按 backend["batch_size"] 分批调用 API。
    支持 OpenAI 兼容接口（siliconflow、zhipu 均可用 base_url 切换）。
    """
    if not texts:
        return []

    if np is None:
        raise RuntimeError("需要安装 numpy: pip install numpy")

    # 解析后端
    if backend is None:
        backend = _resolve_backend(db_path)
    cfg = BACKENDS[backend]

    api_key = _get_api_key(cfg["key_env"])
    if not api_key:
        raise RuntimeError(
            f"需要设置 API key：环境变量 {cfg['key_env']}，"
            f"或创建 .memory_config.json {{'backend': '{backend}'}}"
        )

    # 构建 client（OpenAI 兼容接口）
    if _OpenAI is None:
        raise RuntimeError("需要安装 openai: pip install openai")

    client_kwargs = {"api_key": api_key}
    if cfg["base_url"]:
        client_kwargs["base_url"] = cfg["base_url"]

    client = _OpenAI(**client_kwargs)

    all_embeddings = []
    batch_size = cfg["batch_size"]

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        resp = client.embeddings.create(
            model=cfg["model"],
            input=batch,
        )
        for item in resp.data:
            vec = np.array(item.embedding, dtype=np.float32)
            # 归一化（余弦相似度搜索时更快）
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            all_embeddings.append(vec)

        done = min(i + batch_size, len(texts))
        print(f"    embedded {done}/{len(texts)}...")

    return all_embeddings


def list_backends():
    """列出所有可用后端"""
    return {
        bid: {k: v for k, v in info.items() if k != "key_env"}
        for bid, info in BACKENDS.items()
    }
