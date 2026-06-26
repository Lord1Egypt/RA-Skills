"""multimodal_memory.py — 多模态记忆系统 (v9.0)

在现有 media_processor.py 的基础上，将图片/音频/视频内容作为一等记忆公民：
1. 多模态写入 — 图片/音频/视频 → 记忆条目（含描述 + 元数据 + embedding）
2. 跨模态检索 — 文本查询可匹配图片描述，图片查询可匹配文本记忆
3. 媒体特征提取 — 颜色直方图 / 音频指纹 / 关键帧签名
4. 模态感知存储 — 自动标记 media_type 和媒体路径

零外部依赖的核心层，可选 PIL（图片元数据）/ ffmpeg（视频/音频元数据）。
"""

from __future__ import annotations

import base64
import hashlib
import json
import logging
import os
import struct

logger = logging.getLogger(__name__)

SUPPORTED_IMAGE = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff"}
SUPPORTED_AUDIO = {".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac", ".wma"}
SUPPORTED_VIDEO = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv", ".wmv"}
SUPPORTED_ALL = SUPPORTED_IMAGE | SUPPORTED_AUDIO | SUPPORTED_VIDEO


class MediaDescriptor:
    __slots__ = ("media_type", "format", "size_bytes", "width", "height",
                 "duration_sec", "color_histogram", "audio_fingerprint",
                 "description", "ocr_text", "transcript")

    def __init__(self):
        self.media_type: str = ""
        self.format: str = ""
        self.size_bytes: int = 0
        self.width: int = 0
        self.height: int = 0
        self.duration_sec: float = 0.0
        self.color_histogram: list[int] | None = None
        self.audio_fingerprint: list[float] | None = None
        self.description: str = ""
        self.ocr_text: str = ""
        self.transcript: str = ""

    def to_dict(self) -> dict:
        d = {
            "media_type": self.media_type,
            "format": self.format,
            "size_bytes": self.size_bytes,
        }
        if self.width:
            d["width"] = self.width
            d["height"] = self.height
        if self.duration_sec:
            d["duration_sec"] = self.duration_sec
        if self.color_histogram:
            d["color_histogram_bins"] = len(self.color_histogram)
        if self.description:
            d["description"] = self.description[:500]
        if self.ocr_text:
            d["ocr_text"] = self.ocr_text[:200]
        if self.transcript:
            d["transcript"] = self.transcript[:500]
        return d


class MultimodalMemory:
    """多模态记忆系统 — 将图片/音频/视频作为一等记忆存储和检索。

    用法:
        mm = MultimodalMemory(store, embedder=my_embed_fn)
        mm.ingest_media("/path/to/image.png", agent_id="alice", topics=["ai.vision"])
        results = mm.search("架构图", media_types=["image"], top_k=5)
    """

    def __init__(self, store=None, media_processor=None, embedder=None,
                 encoder=None):
        self.store = store
        self.media_processor = media_processor
        self.embedder = embedder
        self.encoder = encoder

        self._media_index: dict[str, MediaDescriptor] = {}
        self._text_to_media: dict[str, list[str]] = {}

    def ingest_media(self, file_path: str, agent_id: str = "default",
                     person_id: str = "", topics: list[str] = None,
                     importance: str = "medium", prompt: str = "",
                     tags: list[str] = None) -> dict:
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in SUPPORTED_ALL:
            return {"success": False, "error": f"不支持媒体格式: {ext}"}

        if not os.path.exists(file_path):
            return {"success": False, "error": "文件不存在"}

        file_size = os.path.getsize(file_path)
        if file_size > 100 * 1024 * 1024:
            return {"success": False, "error": "文件超过 100MB 上限"}

        descriptor = MediaDescriptor()
        descriptor.format = ext
        descriptor.size_bytes = file_size

        if ext in SUPPORTED_IMAGE:
            descriptor.media_type = "image"
            self._analyze_image(file_path, descriptor, prompt)
        elif ext in SUPPORTED_AUDIO:
            descriptor.media_type = "audio"
            self._analyze_audio(file_path, descriptor)
        elif ext in SUPPORTED_VIDEO:
            descriptor.media_type = "video"
            self._analyze_video(file_path, descriptor, prompt)

        content = self._build_content(descriptor, file_path, topics or [], tags or [])

        embedding = None
        if self.embedder:
            try:
                embedding = self.embedder(content)
            except Exception as e:
                logger.debug("Embedding generation failed: %s", e)

        memory_entry = {
            "agent_id": agent_id,
            "person_id": person_id,
            "content": content,
            "nature": "multimodal_ingest",
            "importance": importance,
            "media_type": descriptor.media_type,
            "media_path": file_path,
            "media_descriptor": descriptor.to_dict(),
            "tags": json.dumps(tags or []),
        }

        if self.encoder:
            try:
                memory_entry["nature_id"] = self.encoder.encode_nature("multimodal_ingest")
                memory_entry["person_id"] = self.encoder.encode_person(person_id) if person_id else ""
                if topics:
                    topic_codes = [self.encoder.encode_topic(t) if hasattr(self.encoder, "encode_topic") else t
                                   for t in topics]
                    memory_entry["topics"] = [{"code": c} for c in topic_codes]
                memory_entry["memory_id"] = self.encoder.generate_memory_id(
                    memory_entry.get("time_ts", 0),
                    memory_entry.get("person_id", ""),
                    memory_entry.get("nature_id", ""),
                    content,
                )
            except Exception as e:
                logger.debug("Encoder failed: %s", e)

        if self.store:
            try:
                self.store.insert_memory(**memory_entry)
                if embedding:
                    try:
                        self.store.insert_embedding(
                            memory_entry.get("memory_id", ""), embedding, content
                        )
                    except Exception as e:
                        logger.warning("multimodal_memory: %s", e)
            except Exception as e:
                logger.debug("Store insert failed: %s", e)

        self._media_index[memory_entry.get("memory_id", file_path)] = descriptor

        for keyword in self._extract_keywords(content):
            if keyword not in self._text_to_media:
                self._text_to_media[keyword] = []
            self._text_to_media[keyword].append(memory_entry.get("memory_id", file_path))

        return {
            "success": True,
            "memory_id": memory_entry.get("memory_id", ""),
            "media_type": descriptor.media_type,
            "content": content,
            "descriptor": descriptor.to_dict(),
        }

    def _analyze_image(self, file_path: str, descriptor: MediaDescriptor, prompt: str):
        try:
            from PIL import Image
            img = Image.open(file_path)
            descriptor.width = img.width
            descriptor.height = img.height

            if img.mode in ("RGB", "RGBA"):
                small = img.resize((64, 64))
                pixels = list(small.getdata())
                bins = [0] * 16
                for px in pixels:
                    r, g, b = px[0], px[1], px[2]
                    brightness = (r + g + b) // 3
                    bin_idx = min(brightness // 16, 15)
                    bins[bin_idx] += 1
                descriptor.color_histogram = bins

            img.close()
        except ImportError as e:
            logger.debug("multimodal_memory: PIL not available: %s", e)
        except Exception as e:
            logger.debug("PIL analysis failed: %s", e)

        if self.media_processor and self.media_processor.vision_fn:
            try:
                result = self.media_processor.process(file_path, prompt or None)
                if result.get("success"):
                    descriptor.description = result.get("description", "")
            except Exception as e:
                logger.debug("Vision processing failed: %s", e)

    def _analyze_audio(self, file_path: str, descriptor: MediaDescriptor):
        try:
            import wave
            if file_path.endswith(".wav"):
                with wave.open(file_path, "r") as w:
                    descriptor.duration_sec = round(
                        w.getnframes() / w.getframerate(), 1
                    )
                    descriptor.audio_fingerprint = self._extract_audio_fingerprint(
                        w.readframes(min(w.getnframes(), w.getframerate() * 5)),
                        w.getframerate(),
                    )
        except ImportError as e:
            logger.debug("multimodal_memory: wave module not available: %s", e)
        except Exception as e:
            logger.debug("Audio analysis failed: %s", e)

        if self.media_processor and self.media_processor.audio_fn:
            try:
                result = self.media_processor.process(file_path)
                if result.get("success"):
                    descriptor.transcript = result.get("description", "")
            except Exception as e:
                logger.debug("Audio processing failed: %s", e)

    def _analyze_video(self, file_path: str, descriptor: MediaDescriptor, prompt: str):
        if self.media_processor:
            try:
                result = self.media_processor.process(file_path, prompt or None)
                if result.get("success"):
                    descriptor.description = result.get("description", "")
                    metadata = result.get("metadata", {})
                    descriptor.duration_sec = metadata.get("duration_sec", 0.0)
            except Exception as e:
                logger.debug("Video processing failed: %s", e)

    def _build_content(self, descriptor: MediaDescriptor, file_path: str,
                       topics: list[str], tags: list[str]) -> str:
        parts = []

        filename = os.path.basename(file_path)
        type_emoji = {"image": "🖼️", "audio": "🎵", "video": "🎬"}.get(
            descriptor.media_type, "📎"
        )

        parts.append(f"{type_emoji} [{descriptor.media_type.upper()}] {filename}")

        if descriptor.width and descriptor.height:
            parts.append(f"尺寸: {descriptor.width}x{descriptor.height}")
        if descriptor.duration_sec:
            parts.append(f"时长: {descriptor.duration_sec:.1f}s")
        if descriptor.size_bytes:
            parts.append(f"大小: {descriptor.size_bytes // 1024}KB")

        if descriptor.description:
            parts.append(f"\n描述: {descriptor.description}")
        if descriptor.transcript:
            parts.append(f"\n转录: {descriptor.transcript}")
        if descriptor.ocr_text:
            parts.append(f"\nOCR: {descriptor.ocr_text}")

        if topics:
            parts.append(f"\n主题: {', '.join(topics)}")
        if tags:
            parts.append(f"\n标签: {', '.join(tags)}")

        return "\n".join(parts)

    def search(self, query: str, media_types: list[str] = None,
               top_k: int = 10, use_embedding: bool = True) -> list[dict]:
        results = []

        if use_embedding and self.embedder and self.store:
            try:
                q_emb = self.embedder(query)
                vec_results = self.store.search_embedding(q_emb, top_k * 2)
                for r in vec_results:
                    if media_types and r.get("media_type") not in media_types:
                        continue
                    results.append({
                        "memory_id": r.get("memory_id", ""),
                        "score": r.get("score", 0),
                        "content": r.get("content", ""),
                        "media_type": r.get("media_type", ""),
                        "source": "vector",
                    })
            except Exception as e:
                logger.debug("Vector search failed: %s", e)

        q_keywords = self._extract_keywords(query)
        for kw in q_keywords:
            for mid in self._text_to_media.get(kw, [])[:top_k]:
                desc = self._media_index.get(mid)
                if desc and media_types and desc.media_type not in media_types:
                    continue
                if not any(r.get("memory_id") == mid for r in results):
                    results.append({
                        "memory_id": mid,
                        "score": 0.7,
                        "content": desc.description if desc else "",
                        "media_type": desc.media_type if desc else "",
                        "source": "keyword",
                    })

        # 图片颜色直方图匹配
        if "image" in (media_types or []) or not media_types:
            hist_results = self._search_by_color(query, top_k)
            for r in hist_results:
                if not any(existing.get("memory_id") == r["memory_id"] for existing in results):
                    results.append(r)

        results.sort(key=lambda x: -x.get("score", 0))
        return results[:top_k]

    def _search_by_color(self, query: str, top_k: int) -> list[dict]:
        results = []
        color_keywords = {
            "红色": (200, 30, 30), "蓝色": (30, 30, 200), "绿色": (30, 200, 30),
            "黄色": (200, 200, 30), "白色": (220, 220, 220), "黑色": (20, 20, 20),
            "暗": (50, 50, 50), "亮": (200, 200, 200), "暖色": (200, 100, 50),
            "冷色": (50, 100, 200),
        }
        matched_colors = []
        for name, rgb in color_keywords.items():
            if name in query:
                matched_colors.append((name, rgb))

        if not matched_colors:
            return results

        for mid, desc in self._media_index.items():
            if desc.color_histogram and desc.media_type == "image":
                avg_brightness = sum(
                    i * c for i, c in enumerate(desc.color_histogram or [])
                ) / max(sum(desc.color_histogram), 1)
                for cname, crgb in matched_colors:
                    target_brightness = sum(crgb) / (3 * 256) * 15
                    sim = 1.0 - abs(avg_brightness - target_brightness) / 15.0
                    if sim > 0.6:
                        results.append({
                            "memory_id": mid,
                            "score": round(sim, 4),
                            "content": desc.description or desc.format,
                            "media_type": "image",
                            "source": f"color_{cname}",
                        })
                        break

        return sorted(results, key=lambda x: -x["score"])[:top_k]

    def cross_modal_search(self, query: str, source_modality: str = "text",
                           target_modalities: list[str] = None) -> list[dict]:
        all_modalities = ["image", "audio", "video"]
        if source_modality in all_modalities:
            all_modalities.remove(source_modality)
        targets = target_modalities or all_modalities

        return self.search(query, media_types=targets)

    def get_media_info(self, memory_id: str) -> dict | None:
        desc = self._media_index.get(memory_id)
        if desc:
            return desc.to_dict()
        return None

    def get_stats(self) -> dict:
        type_counts = {"image": 0, "audio": 0, "video": 0}
        for desc in self._media_index.values():
            if desc.media_type in type_counts:
                type_counts[desc.media_type] += 1

        return {
            "total_media": len(self._media_index),
            "by_type": type_counts,
            "keyword_index_size": len(self._text_to_media),
        }

    def _extract_audio_fingerprint(self, audio_data: bytes, sample_rate: int) -> list[float]:
        if not audio_data:
            return []
        try:
            samples = struct.unpack(f"{len(audio_data) // 2}h", audio_data[:2000])
            step = max(len(samples) // 16, 1)
            energy = []
            for i in range(0, len(samples) - step, step):
                chunk = samples[i:i + step]
                avg = sum(abs(s) for s in chunk) / len(chunk)
                energy.append(avg)
            if energy:
                max_e = max(energy) or 1
                energy = [e / max_e for e in energy]
            return energy[:16]
        except Exception:
            return []

    @staticmethod
    def _extract_keywords(text: str) -> list[str]:
        keywords = []
        for word in text.replace("\n", " ").split():
            word = word.strip(",.!?;:，。！？；：\"'（）()[]{}")
            if len(word) >= 2 and not word.isdigit():
                keywords.append(word.lower())
        return list(dict.fromkeys(keywords))

    @staticmethod
    def detect_media_type(file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()
        if ext in SUPPORTED_IMAGE:
            return "image"
        elif ext in SUPPORTED_AUDIO:
            return "audio"
        elif ext in SUPPORTED_VIDEO:
            return "video"
        return "unknown"


class MediaMemoryBridge:
    """多模态 ↔ 文本记忆桥接 — 使多模态记忆参与常规 RRF 检索。

    用法:
        bridge = MediaMemoryBridge(store, multimodal_memory)
        bridge.link_media_to_topic("mem_img_001", "ai.architecture")
        enriched = bridge.enrich_recall(recall_results, query)
    """

    def __init__(self, store=None, multimodal_memory: MultimodalMemory = None):
        self.store = store
        self.mm = multimodal_memory

    def link_media_to_text(self, media_memory_id: str, text_memory_id: str,
                           link_type: str = "multimodal_context", weight: float = 0.7):
        if self.store and hasattr(self.store, "create_link"):
            self.store.create_link(media_memory_id, text_memory_id, link_type, weight,
                                   "cross-modal link")

    def enrich_recall(self, recall_results: list[dict], query: str,
                      include_media: bool = True, max_media: int = 3) -> list[dict]:
        if not include_media or not self.mm:
            return recall_results

        seen_ids = {r.get("memory_id", "") for r in recall_results}
        media_results = self.mm.search(query, top_k=max_media)

        for mr in media_results:
            if mr.get("memory_id") not in seen_ids:
                mr["score"] = mr.get("score", 0) * 0.6
                mr["source"] = "cross_modal"
                recall_results.append(mr)

        recall_results.sort(key=lambda x: -x.get("score", 0))
        return recall_results