"""
memory.py — SpecQ v2.0 三层记忆模块
ChromaDB 连接管理 + 智谱 embedding + 工作记忆 JSON 读写
"""
import json
import os
from pathlib import Path

# 模块级缓存，避免重复初始化
_collection = None


def get_memory_dir() -> str:
    """数据存储根目录。"""
    return os.getenv("SPECQ_DATA_DIR", os.path.expanduser("~/.specq_data"))


def get_chroma_dir() -> str:
    """ChromaDB 持久化目录。"""
    return os.path.join(get_memory_dir(), "chromadb")


def get_embedding_config() -> dict:
    """通用 Embedding API 配置，用户可配任何兼容 OpenAI embedding 格式的 API。"""
    return {
        "url": os.getenv("EMBEDDING_API_URL", "https://api.deepseek.com/v1/embeddings"),
        "key": os.getenv("EMBEDDING_API_KEY", ""),
        "model": os.getenv("EMBEDDING_MODEL", "deepseek-embed"),
    }


def get_chroma_collection():
    """获取或创建 specq_memory collection（懒加载，模块级缓存）。"""
    global _collection
    if _collection is not None:
        return _collection
    import chromadb
    chroma_dir = get_chroma_dir()
    Path(chroma_dir).mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=chroma_dir, settings=chromadb.Settings(anonymized_telemetry=False))
    _collection = client.get_or_create_collection(name="specq_memory")
    return _collection


def embed_text(text: str) -> list[float]:
    """文本向量化。有 Embedding API Key 时走 API，无 Key 时降级为本地简单哈希向量。"""
    cfg = get_embedding_config()
    if cfg["key"]:
        import httpx
        try:
            resp = httpx.post(
                cfg["url"],
                json={"model": cfg["model"], "input": text},
                headers={"Authorization": f"Bearer {cfg['key']}", "Content-Type": "application/json"},
                timeout=10,
            )
            if resp.status_code == 200:
                data = resp.json()
                return data["data"][0]["embedding"]
        except Exception:
            pass  # API 失败，走降级
    # 降级：基于词频的简单哈希向量
    return _hash_embed(text)


def _hash_embed(text: str, dim: int = 768) -> list[float]:
    """本地哈希向量化。无需任何 API，作为 Embedding 的降级方案。"""
    import hashlib
    import re
    words = re.findall(r'[\w\u4e00-\u9fff]+', text.lower())
    if not words:
        return [0.0] * dim
    vec = [0.0] * dim
    for i, word in enumerate(words[:200]):
        h = int(hashlib.md5(word.encode()).hexdigest(), 16)
        idx = h % dim
        vec[idx] += 1.0
    # 归一化
    norm = sum(v * v for v in vec) ** 0.5
    if norm > 0:
        vec = [v / norm for v in vec]
    return vec


def load_working_memory(uid: str) -> dict:
    """读取用户工作记忆 JSON，不存在时返回空结构。"""
    memory_dir = Path(get_memory_dir())
    memory_dir.mkdir(parents=True, exist_ok=True)
    filepath = memory_dir / f"specq_working_memory_{uid}.json"
    if not filepath.exists():
        return {"goal": None, "plan": [], "current_step": 0, "results": {}}
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_working_memory(uid: str, data: dict) -> None:
    """保存用户工作记忆 JSON。"""
    memory_dir = Path(get_memory_dir())
    memory_dir.mkdir(parents=True, exist_ok=True)
    filepath = memory_dir / f"specq_working_memory_{uid}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
