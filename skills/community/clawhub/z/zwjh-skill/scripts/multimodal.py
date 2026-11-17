# -*- coding: utf-8 -*-
"""
多模态记忆 —— 图片 / 音频 / 文件的记忆关联。

功能：
  - 图片记忆：理解图片内容、拍摄时间、关联事件
  - 音频记忆：会议录音摘要、关键决策关联
  - 文件记忆：文档摘要、存在路径、关联实体
  - 实体关联：媒体文件与知识图谱实体自动链接

设计原则：
  - 理解能力可插拔（本地模型 / LLM API / 手动描述）
  - 仅存储描述和关联，不存储原始二进制
  - 零密钥默认（未配置 LLM 时退化为手动描述）
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from datetime import datetime

from . import config, store


# ── 媒体理解适配器（可插拔） ──────────────────────────────────────────────
class MediaProvider:
    """媒体理解适配器接口。"""

    def describe_image(self, image_path: str) -> str:
        """生成图片描述。"""
        return "⚠️ 图片理解未配置，请配置 LLM API 或本地模型"

    def transcribe_audio(self, audio_path: str) -> str:
        """转录音频内容。"""
        return "⚠️ 音频转录未配置，请配置 LLM API 或本地模型"

    def summarize_file(self, file_path: str) -> str:
        """生成文件摘要。"""
        return "⚠️ 文件摘要未配置，请配置 LLM API 或本地模型"


class ManualMediaProvider(MediaProvider):
    """手动模式：将文件路径和基础信息作为描述，供用户手动补充。"""

    def describe_image(self, image_path: str) -> str:
        stat = os.stat(image_path)
        mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
        return f"[图片 {image_path}，拍摄时间 {mtime}]"

    def transcribe_audio(self, audio_path: str) -> str:
        size = os.path.getsize(audio_path)
        size_mb = size / (1024 * 1024)
        return f"[音频 {audio_path}，大小 {size_mb:.1f}MB]"

    def summarize_file(self, file_path: str) -> str:
        size = os.path.getsize(file_path)
        ext = os.path.splitext(file_path)[1]
        mtime = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M")
        return f"[文件 {file_path}，类型 {ext}，大小 {size} 字节，修改时间 {mtime}]"


# ── 全局媒体适配器 ────────────────────────────────────────────────────────
_media_provider: MediaProvider = ManualMediaProvider()


def set_media_provider(provider: MediaProvider) -> None:
    """注册全局媒体理解适配器。"""
    global _media_provider
    _media_provider = provider


def get_media_provider() -> MediaProvider:
    """获取当前媒体适配器。"""
    return _media_provider


# ── 多模态记忆管理器 ──────────────────────────────────────────────────────
class MultimodalManager:
    """多模态记忆管理器。"""

    def __init__(self, media_provider: MediaProvider | None = None):
        self.provider = media_provider or get_media_provider()
        self._ensure_media_table()

    def _ensure_media_table(self) -> None:
        """确保媒体记忆表存在。"""
        conn = store.get_conn()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS media_memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                media_type TEXT NOT NULL,        -- image / audio / file
                file_path TEXT NOT NULL,
                file_hash TEXT,                   -- 文件 MD5（用于去重）
                description TEXT NOT NULL,        -- AI 生成的描述 / 手动描述
                associated_entity_id INTEGER,     -- 关联的图谱实体
                associated_memory_id INTEGER,     -- 关联的记忆
                metadata_json TEXT DEFAULT '{}',  -- 拍摄时间 / GPS / 时长等
                created_at TEXT NOT NULL,
                FOREIGN KEY(associated_entity_id) REFERENCES entities(id),
                FOREIGN KEY(associated_memory_id) REFERENCES memories(id)
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_media_path ON media_memories(file_path)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_media_hash ON media_memories(file_hash)")
        conn.commit()

    def index_image(self, image_path: str, entity_name: str | None = None,
                    memory_text: str | None = None) -> dict:
        """索引一张图片。"""
        if not os.path.exists(image_path):
            return {"status": "error", "reason": f"文件不存在: {image_path}"}

        description = self.provider.describe_image(image_path)
        file_hash = self._compute_hash(image_path)
        entity_id = None
        memory_id = None

        # 关联实体
        if entity_name:
            entity = store.find_entity(None, entity_name)
            if entity:
                entity_id = entity["id"]

        # 关联记忆
        if memory_text:
            from . import embeddings
            toks = embeddings.tokenize(memory_text)
            h = embeddings.norm_hash(toks)
            mid = store.add_memory(
                config.today_str(), "multimodal:image",
                memory_text, h, toks, importance=0.6
            )
            memory_id = mid

        conn = store.get_conn()
        now = datetime.now().isoformat(timespec="seconds")
        conn.execute(
            "INSERT INTO media_memories(media_type, file_path, file_hash, description, "
            "associated_entity_id, associated_memory_id, metadata_json, created_at) "
            "VALUES(?,?,?,?,?,?,?,?)",
            ("image", image_path, file_hash, description, entity_id, memory_id,
             "{}", now),
        )
        conn.commit()

        return {
            "status": "ok",
            "media_type": "image",
            "path": image_path,
            "description": description,
            "entity_id": entity_id,
        }

    def index_audio(self, audio_path: str, entity_name: str | None = None,
                    project_name: str | None = None) -> dict:
        """索引一段音频。"""
        if not os.path.exists(audio_path):
            return {"status": "error", "reason": f"文件不存在: {audio_path}"}

        description = self.provider.transcribe_audio(audio_path)
        file_hash = self._compute_hash(audio_path)
        entity_id = None
        memory_id = None

        # 关联实体（如会议参与人）
        if entity_name:
            entity = store.find_entity(None, entity_name)
            if entity:
                entity_id = entity["id"]

        # 关联项目记忆
        if project_name:
            from . import embeddings
            text = f"音频关联项目：{project_name}"
            if description:
                text += f"\n\n{description}"
            toks = embeddings.tokenize(text)
            h = embeddings.norm_hash(toks)
            mid = store.add_memory(
                config.today_str(), "multimodal:audio",
                text, h, toks, importance=0.6
            )
            memory_id = mid

        conn = store.get_conn()
        now = datetime.now().isoformat(timespec="seconds")
        conn.execute(
            "INSERT INTO media_memories(media_type, file_path, file_hash, description, "
            "associated_entity_id, associated_memory_id, metadata_json, created_at) "
            "VALUES(?,?,?,?,?,?,?,?)",
            ("audio", audio_path, file_hash, description, entity_id, memory_id,
             "{}", now),
        )
        conn.commit()

        return {
            "status": "ok",
            "media_type": "audio",
            "path": audio_path,
            "description": description,
            "entity_id": entity_id,
        }

    def index_file(self, file_path: str, entity_name: str | None = None,
                   project_name: str | None = None) -> dict:
        """索引一个文档文件。"""
        if not os.path.exists(file_path):
            return {"status": "error", "reason": f"文件不存在: {file_path}"}

        description = self.provider.summarize_file(file_path)
        file_hash = self._compute_hash(file_path)
        entity_id = None
        memory_id = None

        # 关联实体
        if entity_name:
            entity = store.find_entity(None, entity_name)
            if entity:
                entity_id = entity["id"]

        # 关联项目记忆
        if project_name:
            from . import embeddings
            text = f"文件关联项目：{project_name}\n路径：{file_path}"
            if description:
                text += f"\n\n{description}"
            toks = embeddings.tokenize(text)
            h = embeddings.norm_hash(toks)
            memory_id = store.add_memory(
                config.today_str(), "multimodal:file",
                text, h, toks, importance=0.5
            )

        conn = store.get_conn()
        now = datetime.now().isoformat(timespec="seconds")
        conn.execute(
            "INSERT INTO media_memories(media_type, file_path, file_hash, description, "
            "associated_entity_id, associated_memory_id, metadata_json, created_at) "
            "VALUES(?,?,?,?,?,?,?,?)",
            ("file", file_path, file_hash, description, entity_id, memory_id,
             "{}", now),
        )
        conn.commit()

        return {
            "status": "ok",
            "media_type": "file",
            "path": file_path,
            "description": description,
            "entity_id": entity_id,
            "memory_id": memory_id,
        }

    def list_media(self, media_type: str | None = None,
                   entity_name: str | None = None) -> list[dict]:
        """列出媒体记忆。"""
        conn = store.get_conn()
        sql = "SELECT * FROM media_memories WHERE 1=1"
        args: list = []
        if media_type:
            sql += " AND media_type=?"
            args.append(media_type)
        if entity_name:
            sql += " AND associated_entity_id = (SELECT id FROM entities WHERE name=?)"
            args.append(entity_name)
        sql += " ORDER BY created_at DESC"
        rows = conn.execute(sql, args).fetchall()
        return [dict(r) for r in rows]

    def get_media(self, media_id: int) -> dict | None:
        """获取单个媒体记忆。"""
        conn = store.get_conn()
        row = conn.execute("SELECT * FROM media_memories WHERE id=?", (media_id,)).fetchone()
        return dict(row) if row else None

    def associate_entity(self, media_id: int, entity_name: str) -> dict:
        """将媒体记忆关联到实体。"""
        entity = store.find_entity(None, entity_name)
        if not entity:
            return {"status": "error", "reason": f"实体 {entity_name} 不存在"}

        conn = store.get_conn()
        conn.execute(
            "UPDATE media_memories SET associated_entity_id=? WHERE id=?",
            (entity["id"], media_id),
        )
        conn.commit()
        return {"status": "ok", "entity_id": entity["id"]}

    def _compute_hash(self, file_path: str) -> str:
        """计算文件 MD5（用于去重）。"""
        h = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()


# ── 便捷函数 ──────────────────────────────────────────────────────────────
def index_image(image_path: str, entity_name: str | None = None,
                memory_text: str | None = None) -> dict:
    """索引一张图片。"""
    mgr = MultimodalManager()
    return mgr.index_image(image_path, entity_name, memory_text)


def index_audio(audio_path: str, entity_name: str | None = None,
                project_name: str | None = None) -> dict:
    """索引一段音频。"""
    mgr = MultimodalManager()
    return mgr.index_audio(audio_path, entity_name, project_name)


def index_file(file_path: str, entity_name: str | None = None,
               project_name: str | None = None) -> dict:
    """索引一个文件。"""
    mgr = MultimodalManager()
    return mgr.index_file(file_path, entity_name, project_name)


def list_media(media_type: str | None = None, entity_name: str | None = None) -> list[dict]:
    """列出媒体记忆。"""
    mgr = MultimodalManager()
    return mgr.list_media(media_type, entity_name)


if __name__ == "__main__":
    print("=== 媒体记忆功能 ===")
    print("list:", list_media())
