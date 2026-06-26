import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

from core.memory.vector_store import VectorStore

logger = logging.getLogger(__name__)


class DualRAG:
    def __init__(self, storage_path: Path, settings: Dict[str, Any]):
        self.storage_path = storage_path
        self.settings = settings
        
        source_db_path = storage_path / "vector_db" / "source_index"
        runtime_db_path = storage_path / "vector_db" / "runtime_index"
        
        self.source_store = VectorStore(
            persist_directory=str(source_db_path),
            collection_name="source_memory",
        )
        self.runtime_store = VectorStore(
            persist_directory=str(runtime_db_path),
            collection_name="runtime_memory",
        )
        
    def index_source_data(self, messages: List[Dict[str, Any]]):
        texts = []
        metadatas = []
        
        for msg in messages:
            content = msg.get("content", "")
            if content:
                texts.append(content)
                meta = msg.get("metadata") or {}
                metadatas.append({
                    "source": "chat_history",
                    "sender": msg.get("sender", "unknown"),
                    "timestamp": msg.get("timestamp", ""),
                    "role": meta.get("role", "")
                })
                
        if texts:
            ids = [f"source_{i}" for i in range(len(texts))]
            self.source_store.add_texts(texts, metadatas, ids)
            logger.info(f"Indexed {len(texts)} source messages")
            
    def index_runtime_data(self, user_message: str, assistant_message: str):
        texts = [user_message, assistant_message]
        metadatas = [
            {"source": "runtime", "role": "user"},
            {"source": "runtime", "role": "assistant"},
        ]
        log_file = self.storage_path / "runtime" / "conversation.jsonl"
        turn_id = 0
        if log_file.exists():
            with open(log_file, "r", encoding="utf-8") as f:
                turn_id = sum(1 for _ in f)
        ids = [f"runtime_user_{turn_id}", f"runtime_asst_{turn_id}"]
        self.runtime_store.add_texts(texts, metadatas, ids)
        
    def retrieve(self, query: str, top_k_source: Optional[int] = None, top_k_runtime: Optional[int] = None) -> List[Dict[str, Any]]:
        if top_k_source is None:
            top_k_source = self.settings.get("top_k_source", 5)
        if top_k_runtime is None:
            top_k_runtime = self.settings.get("top_k_runtime", 3)
            
        similarity_threshold = self.settings.get("similarity_threshold", 0.5)
        top_k_with_context = self.settings.get("top_k_with_context", 3)
        context_window = self.settings.get("context_window", 5)

        source_results = self.source_store.similarity_search(
            query=query,
            k=top_k_source
        )
        runtime_results = self.runtime_store.similarity_search(
            query=query,
            k=top_k_runtime
        )

        def distance_to_relevance(d: float) -> float:
            return 1.0 / (1.0 + d)

        def _fmt_msg(doc: Dict[str, Any]) -> str:
            """单条消息格式：时间 + 谁说的 + 内容。"""
            c = (doc.get("content") or "").strip()
            if not c:
                return ""
            meta = doc.get("metadata") or {}
            sender = meta.get("sender") or "未知"
            ts = (meta.get("timestamp") or "").strip()
            if ts:
                return f"[{ts}] {sender}: {c}"
            return f"{sender}: {c}"

        def with_context(hit_content: str, hit_meta: Dict, index: int, store: VectorStore, window: int) -> str:
            """取 index 前后各 window 条，带发送者和时间，拼成一条记忆。"""
            parts = []
            for i in range(index - window, index + window + 1):
                if i == index:
                    doc = {"content": hit_content, "metadata": hit_meta}
                else:
                    doc = store.get_document_at(i)
                if doc:
                    line = _fmt_msg(doc)
                    if line:
                        parts.append(line)
            return "\n".join(parts)

        all_results = []
        for rank, result in enumerate(source_results):
            relevance = distance_to_relevance(result["distance"])
            if relevance < similarity_threshold:
                continue
            content = result["content"]
            idx = result.get("index", -1)
            meta = result.get("metadata", {})
            if rank < top_k_with_context and idx >= 0:
                content = with_context(content, meta, idx, self.source_store, context_window)
            all_results.append({
                "content": content,
                "source": "source_memory",
                "relevance": round(relevance, 4),
            })
        for result in runtime_results:
            relevance = distance_to_relevance(result["distance"])
            if relevance >= similarity_threshold:
                all_results.append({
                    "content": result["content"],
                    "source": "runtime_memory",
                    "relevance": round(relevance, 4),
                })
        
        all_results.sort(key=lambda x: x["relevance"], reverse=True)
        return all_results[: top_k_source + top_k_runtime]
