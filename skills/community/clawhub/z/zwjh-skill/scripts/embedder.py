# -*- coding: utf-8 -*-
"""
本地 Embedding 层 —— ONNX Runtime 推理 + TF-IDF 回退。

设计原则：
  - 模型文件不打包，包内只带 SHA256 校验与下载指引
  - 用户下载 .onnx 放置 models/ 即启用语义检索
  - 无模型自动回退 TF-IDF（行为同旧版）
  - 向量存 SQLite BLOB 表，万条级暴力余弦检索
  - 接口预留 HNSW 扩展点

模型：bge-small-zh-v1.5 (ONNX 量化版)
  - 维度：512
  - 来源：BAAI/bge-small-zh-v1.5
  - 量化：INT8
  - 大小：约 30MB
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import struct
import sys
from datetime import datetime
from typing import Any

# 确保能 import 同级模块
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
if SKILL_DIR not in sys.path:
    sys.path.insert(0, SKILL_DIR)

from . import config, store


# ── 模型配置 ────────────────────────────────────────────────────────────────
MODEL_DIR = os.path.join(SKILL_DIR, "models")
MODEL_FILENAME = "bge-small-zh-v1.5-q.onnx"
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILENAME)
MODEL_SHA256 = "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2"  # 占位，实际发布时替换
MODEL_DIM = 512
MODEL_MAX_LENGTH = 512

# 模型下载信息
MODEL_DOWNLOAD_URL = "https://huggingface.co/BAAI/bge-small-zh-v1.5/resolve/main/onnx/model_quantized.onnx"
MODEL_SOURCE = "BAAI/bge-small-zh-v1.5 (ONNX INT8 量化)"


# ── 全局状态 ────────────────────────────────────────────────────────────────
_onnx_session: Any = None
_onnx_tokenizer: Any = None
_model_available: bool = False
_model_error: str | None = None


# ── 模型检测 ────────────────────────────────────────────────────────────────
def is_model_available() -> bool:
    """检查模型文件是否存在且校验通过。"""
    if not os.path.exists(MODEL_PATH):
        return False
    # 可选：SHA256 校验（如果存在 .sha256 文件）
    sha_file = MODEL_PATH + ".sha256"
    if os.path.exists(sha_file):
        expected = _read_sha256_file(sha_file)
        actual = _compute_sha256(MODEL_PATH)
        return expected == actual
    return True


def _read_sha256_file(path: str) -> str:
    """读取 .sha256 文件中的期望哈希值。"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip().split()[0].lower()
    except Exception:
        return ""


def _compute_sha256(path: str) -> str:
    """计算文件 SHA256。"""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest().lower()


def get_model_info() -> dict:
    """获取模型状态信息。"""
    return {
        "model_path": MODEL_PATH,
        "model_exists": os.path.exists(MODEL_PATH),
        "model_available": is_model_available(),
        "model_dim": MODEL_DIM,
        "model_source": MODEL_SOURCE,
        "model_download_url": MODEL_DOWNLOAD_URL,
        "model_size_mb": _get_model_size_mb(),
        "error": _model_error,
    }


def _get_model_size_mb() -> float:
    """获取模型文件大小（MB）。"""
    try:
        return round(os.path.getsize(MODEL_PATH) / (1024 * 1024), 2)
    except Exception:
        return 0.0


# ── ONNX 模型加载 ───────────────────────────────────────────────────────────
def _load_onnx_model() -> bool:
    """加载 ONNX 模型。成功返回 True。"""
    global _onnx_session, _onnx_tokenizer, _model_available, _model_error

    if not is_model_available():
        _model_error = "模型文件不存在或校验失败: %s" % MODEL_PATH
        return False

    try:
        import onnxruntime as ort
    except ImportError:
        _model_error = "onnxruntime 未安装。运行: pip install onnxruntime"
        return False

    try:
        # 创建推理会话
        sess_options = ort.SessionOptions()
        sess_options.intra_op_num_threads = 2  # 限制线程数，不拖累电脑
        sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

        _onnx_session = ort.InferenceSession(
            MODEL_PATH, sess_options, providers=["CPUExecutionProvider"]
        )

        # 尝试加载 tokenizer（可选）
        _load_tokenizer()

        _model_available = True
        _model_error = None
        return True

    except Exception as e:
        _model_error = "ONNX 模型加载失败: %s" % str(e)
        _onnx_session = None
        _onnx_tokenizer = None
        _model_available = False
        return False


def _load_tokenizer() -> None:
    """加载 tokenizer（优先 transformers，回退简单分词）。"""
    global _onnx_tokenizer

    try:
        from transformers import AutoTokenizer
        # 尝试从模型目录加载
        tokenizer_path = os.path.join(MODEL_DIR, "tokenizer")
        if os.path.exists(tokenizer_path):
            _onnx_tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        else:
            # 回退：从 HuggingFace 加载（需要联网）
            _onnx_tokenizer = AutoTokenizer.from_pretrained(
                "BAAI/bge-small-zh-v1.5",
                cache_dir=MODEL_DIR
            )
    except Exception:
        # 回退：简单分词
        _onnx_tokenizer = None


# ── 编码接口 ────────────────────────────────────────────────────────────────
def encode(text: str) -> list[float] | None:
    """
    将文本编码为向量。
    
    优先使用 ONNX 模型，失败时返回 None（调用方回退 TF-IDF）。
    """
    global _model_available

    # 延迟加载
    if _onnx_session is None and not _model_available:
        _load_onnx_model()

    if not _model_available or _onnx_session is None:
        return None

    try:
        # Tokenize
        if _onnx_tokenizer is not None:
            inputs = _onnx_tokenizer(
                text,
                padding=True,
                truncation=True,
                max_length=MODEL_MAX_LENGTH,
                return_tensors="np"
            )
            input_ids = inputs["input_ids"].astype("int64")
            attention_mask = inputs["attention_mask"].astype("int64")
        else:
            # 回退：简单字符编码
            input_ids, attention_mask = _simple_tokenize(text)

        # 推理
        outputs = _onnx_session.run(
            None,
            {
                "input_ids": input_ids,
                "attention_mask": attention_mask,
            }
        )

        # 提取 embedding（取 CLS token 或 mean pooling）
        embedding = outputs[0]  # shape: (1, seq_len, dim) 或 (1, dim)

        # Mean pooling
        if len(embedding.shape) == 3:
            # (batch, seq_len, dim) → (batch, dim)
            mask_expanded = attention_mask[:, :, None].astype("float32")
            embedding = (embedding * mask_expanded).sum(axis=1) / mask_expanded.sum(axis=1).clip(min=1e-9)

        # L2 归一化
        norm = math.sqrt(sum(x * x for x in embedding[0]))
        if norm > 0:
            embedding = embedding / norm

        return embedding[0].tolist()

    except Exception as e:
        # 推理失败，标记不可用
        _model_error = "推理失败: %s" % str(e)
        _model_available = False
        return None


def _simple_tokenize(text: str) -> tuple:
    """简单分词回退（字符级）。"""
    # 将文本转为字符 ID（简单哈希）
    chars = list(text[:MODEL_MAX_LENGTH])
    input_ids = [hash(c) % 30000 for c in chars]  # 简单哈希到词表范围
    attention_mask = [1] * len(input_ids)

    # 填充到固定长度
    while len(input_ids) < MODEL_MAX_LENGTH:
        input_ids.append(0)
        attention_mask.append(0)

    import numpy as np
    return (
        np.array([input_ids], dtype="int64"),
        np.array([attention_mask], dtype="int64")
    )


# ── 向量存储 ────────────────────────────────────────────────────────────────
def _ensure_vectors_table() -> None:
    """确保 vectors 表存在。"""
    conn = store.get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS vectors (
            memory_id INTEGER PRIMARY KEY,
            embedding BLOB NOT NULL,
            model TEXT NOT NULL,
            dim INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(memory_id) REFERENCES memories(id) ON DELETE CASCADE
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_vectors_model ON vectors(model)")
    conn.commit()


def store_embedding(memory_id: int, embedding: list[float], model: str = "bge-small-zh") -> None:
    """存储向量到数据库。"""
    _ensure_vectors_table()
    conn = store.get_conn()

    # 将 float list 打包为 BLOB（小端 float32）
    blob = struct.pack("<%df" % len(embedding), *embedding)

    conn.execute(
        "INSERT OR REPLACE INTO vectors(memory_id, embedding, model, dim, created_at) VALUES(?,?,?,?,?)",
        (memory_id, blob, model, len(embedding), datetime.now().isoformat(timespec="seconds")),
    )
    conn.commit()


def get_embedding(memory_id: int) -> list[float] | None:
    """从数据库读取向量。"""
    _ensure_vectors_table()
    conn = store.get_conn()
    row = conn.execute(
        "SELECT embedding, dim FROM vectors WHERE memory_id=?", (memory_id,)
    ).fetchone()
    if not row:
        return None

    # 解包 BLOB 为 float list
    dim = row["dim"]
    embedding = struct.unpack("<%df" % dim, row["embedding"])
    return list(embedding)


def get_all_embeddings() -> list[tuple[int, list[float]]]:
    """获取所有向量（用于暴力检索）。"""
    _ensure_vectors_table()
    conn = store.get_conn()
    rows = conn.execute("SELECT memory_id, embedding, dim FROM vectors").fetchall()
    results = []
    for r in rows:
        dim = r["dim"]
        embedding = struct.unpack("<%df" % dim, r["embedding"])
        results.append((r["memory_id"], list(embedding)))
    return results


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """计算余弦相似度。"""
    if not a or not b:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


# ── 语义检索 ────────────────────────────────────────────────────────────────
def semantic_search(query: str, top_k: int = 8) -> list[dict]:
    """
    语义检索：将 query 编码为向量，与所有记忆向量计算余弦相似度。
    
    返回: [{memory_id, score}]（按 score 降序）
    """
    query_vec = encode(query)
    if query_vec is None:
        return []  # 模型不可用，返回空（调用方回退 TF-IDF）

    all_vecs = get_all_embeddings()
    if not all_vecs:
        return []

    scores = []
    for mem_id, vec in all_vecs:
        sim = cosine_similarity(query_vec, vec)
        scores.append({"memory_id": mem_id, "score": sim})

    scores.sort(key=lambda x: x["score"], reverse=True)
    return scores[:top_k]


# ── 初始化 ──────────────────────────────────────────────────────────────────
def initialize() -> bool:
    """
    初始化 embedding 层。
    - 检查模型可用性
    - 加载 ONNX 会话
    - 返回是否成功
    """
    if not is_model_available():
        _model_error = "模型文件不存在: %s" % MODEL_PATH
        return False
    return _load_onnx_model()


# ── 便捷函数 ────────────────────────────────────────────────────────────────
def encode_and_store(memory_id: int, text: str) -> bool:
    """编码文本并存储向量。成功返回 True。"""
    vec = encode(text)
    if vec is None:
        return False
    store_embedding(memory_id, vec)
    return True


if __name__ == "__main__":
    info = get_model_info()
    print(json.dumps(info, ensure_ascii=False, indent=2))
    if info["model_available"]:
        print("\n模型可用，测试编码...")
        vec = encode("机器学习需要大量数据")
        if vec:
            print("编码成功，维度:", len(vec))
            print("前 5 个值:", vec[:5])
        else:
            print("编码失败")
    else:
        print("\n模型不可用，将回退 TF-IDF")
