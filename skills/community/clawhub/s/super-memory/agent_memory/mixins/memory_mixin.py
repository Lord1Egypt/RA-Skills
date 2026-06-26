from __future__ import annotations

import hashlib
import logging
import time
import uuid

from ..resilience import CircuitOpenError
from ..friendly_errors import get_friendly_error

logger = logging.getLogger(__name__)


class MemoryMixin:
    def remember(
        self,
        content: str,
        importance: str = None,
        topics: list[str] = None,
        nature: str = None,
        force: bool = False,
        auto_write: bool = True,
        context: str = None,
        return_result: bool = False,
        **kwargs,
    ) -> dict:
        """
        写入一条记忆。

        自动执行：过滤 → 清洗 → 去重 → 编码 → 存储 → 向量索引

        参数:
            content: 记忆内容
            importance: 重要度（None 则自动评估）
            topics: 主题列表（None 则自动检测）
            nature: 性质（None 则自动检测）
            force: 跳过过滤强制写入
            auto_write: 是否直接写入（False 则返回待审核状态，需再次调用 auto_write=True 确认）
            context: 上下文信息（传递给引擎）
            return_result: 如果为 True，返回 RememberResult dataclass 而非 dict

        返回: {"written": bool, "memory_id": str, "reason": str, "status": str}
              或 RememberResult dataclass（当 return_result=True 时）
        """
        if getattr(self, '_shutting_down', False):
            raise RuntimeError("AgentMemory is shutting down")

        # Feature flag: memory_ingestion
        if not self._is_feature_enabled("memory_ingestion", default=True):
            return _wrap({"written": False, "memory_id": None, "status": "disabled", "reason": "Feature 'memory_ingestion' is disabled by feature flag"})

        # Optional consent check
        if self.store and hasattr(self.store, '_consent_manager') and self.store._consent_manager:
            try:
                consent = self.store._consent_manager.check(
                    agent_id=kwargs.get("agent_id", "default"),
                )
                if not consent:
                    from ..result_types import SaveResult
                    return _wrap({
                        "written": False,
                        "memory_id": "",
                        "status": "consent_denied",
                        "reason": "写入被拒绝：未获得数据存储同意",
                        "message": "写入被拒绝：未获得数据存储同意",
                        "tip": "请先通过 consent manager 授权记忆存储",
                    })
            except Exception:
                pass  # Consent check failure should not block writes

        def _wrap(result_dict: dict):
            """If return_result is True, convert dict to RememberResult."""
            if return_result:
                from ..result_types import RememberResult
                return RememberResult.from_dict(result_dict)
            return result_dict

        # ── v10 Engine 路径 ──────────────────────────────────
        if getattr(self, '_ingest_engine', None) is not None:
            # Optional PII detection on write
            if self.store and hasattr(self.store, '_pii_check_on_write') and self.store._pii_check_on_write:
                try:
                    from agent_memory.privacy.guard import PrivacyGuard
                    guard = PrivacyGuard()
                    pii_result = guard.detect_pii(content)
                    if pii_result.get("has_pii"):
                        logger.warning(
                            "PII detected in memory content",
                            extra={"event": "pii_detected", "pii_types": pii_result.get("types", [])}
                        )
                        # Don't block, just warn and tag
                        kwargs.setdefault("metadata", {})
                        kwargs["metadata"]["pii_detected"] = True
                        kwargs["metadata"]["pii_types"] = pii_result.get("types", [])
                except Exception:
                    pass  # PII detection failure should not block writes

            engine_kwargs = dict(kwargs)
            if importance is not None:
                engine_kwargs["importance"] = importance
            if topics is not None:
                engine_kwargs["topics"] = topics
            if nature is not None:
                engine_kwargs["nature_code"] = nature
            engine_kwargs["force"] = force
            engine_kwargs["auto_write"] = auto_write

            # 传递功能开关：当 filter/dedup 被禁用时，跳过对应步骤
            if not getattr(self, '_enable_filter', True):
                engine_kwargs["skip_filter"] = True
            if not getattr(self, '_enable_dedup', True):
                engine_kwargs["skip_dedup"] = True

            try:
                result = self._llm_breaker.call(
                    self._ingest_engine.remember, content, context=context, **engine_kwargs
                )
            except CircuitOpenError as e:
                logger.warning("remember: LLM 断路器已打开，降级为直接存储: %s", e)
                friendly = get_friendly_error("circuit_open", str(e))
                result = {"written": False, "memory_id": None, "status": "circuit_open", "reason": str(e),
                          "message": friendly["message"], "tip": friendly["tip"]}

            # 统一返回格式为 dict，确保包含 status / memory_id / written
            if hasattr(result, "to_dict"):
                result = result.to_dict()

            if isinstance(result, dict):
                # 添加降级警告
                warnings = self.get_degradation_warnings()
                if warnings:
                    result["_warnings"] = warnings
                status = result.get("status")
                if status == "stored":
                    result["written"] = True
                    if "reason" not in result:
                        result["reason"] = "ok"
                    return _wrap(result)
                elif status == "pending_review":
                    result["written"] = False
                    return _wrap(result)
                else:
                    result["written"] = False
                    if "memory_id" not in result:
                        result["memory_id"] = None
                    # Add friendly error messages for common error statuses
                    if status == "filtered" and "message" not in result:
                        friendly = get_friendly_error("filtered", result.get("reason", ""))
                        result["message"] = friendly["message"]
                        result["tip"] = friendly["tip"]
                    elif status == "duplicate" and "message" not in result:
                        friendly = get_friendly_error("duplicate_skipped", result.get("reason", ""))
                        result["message"] = friendly["message"]
                        result["tip"] = friendly["tip"]
                    elif status == "cooldown" and "message" not in result:
                        friendly = get_friendly_error("cooldown_active", result.get("reason", ""))
                        result["message"] = friendly["message"]
                        result["tip"] = friendly["tip"]
                    elif status == "circuit_open" and "message" not in result:
                        friendly = get_friendly_error("circuit_open", result.get("reason", ""))
                        result["message"] = friendly["message"]
                        result["tip"] = friendly["tip"]
                    elif status == "error" and "message" not in result:
                        friendly = get_friendly_error(status, result.get("reason", ""))
                        result["message"] = friendly["message"]
                        result["tip"] = friendly["tip"]
                    return _wrap(result)

            return _wrap({"written": False, "memory_id": None, "status": "error", "reason": f"意外的结果类型: {type(result)}"})

        # ── Fallback：直接调用 store.insert_memory ──────────
        logger.warning(
            "IngestEngine not available - using direct store insertion. "
            "Filter/cleaner/dedup/pipeline steps are SKIPPED. "
            "This may result in lower data quality."
        )

        if not content or not content.strip():
            logger.warning("Empty content rejected in fallback path")
            friendly = get_friendly_error("empty_content")
            return _wrap({"written": False, "memory_id": None, "status": "filtered", "reason": "内容为空",
                          "message": friendly["message"], "tip": friendly["tip"]})

        content = content.strip()
        if len(content) > 10000:
            content = content[:10000]
            logger.warning("Content truncated to 10000 chars in fallback path")

        if not auto_write:
            preview = content[:200] + ("..." if len(content) > 200 else "")
            return _wrap({
                "written": False,
                "memory_id": None,
                "status": "pending_review",
                "reason": "pending_review",
                "preview": preview,
                "content_length": len(content),
                "message": "记忆待人工审核。设置 auto_write=True 可跳过审核直接写入（仅限受信任环境）。",
            })

        try:
            ts = int(time.time())
            memory_id = f"mem_{uuid.uuid4().hex[:12]}"
            content_hash = hashlib.md5(content.encode()).hexdigest()[:12]
            result = self.store.insert_memory(
                memory_id=memory_id,
                time_id=f"T{ts}",
                time_ts=ts,
                person_id=self.agent_id or "_system",
                nature_id=nature or "note",
                content=content,
                content_hash=content_hash,
                topics=topics or [],
                tools=[],
                knowledge_types=[],
                importance=importance or "medium",
                owner_agent_id=self.agent_id or "_system",
                visibility="team" if self.agent_id else "private",
            )
            # Handle duplicate content dedup result from store
            if isinstance(result, dict) and result.get("reason") == "内容重复":
                friendly = get_friendly_error("duplicate_skipped", "内容重复")
                return _wrap({
                    "written": False,
                    "status": "duplicate",
                    "memory_id": result["memory_id"],
                    "reason": "内容重复",
                    "message": friendly["message"],
                    "tip": friendly["tip"],
                })
            return _wrap({
                "written": True,
                "status": "stored",
                "memory_id": memory_id,
                "reason": "ok (fallback)",
                "topics": topics or [],
                "nature": nature or "",
                "importance": importance or "medium",
            })
        except Exception as e:
            logger.warning("memory_mixin fallback insert failed: %s", e)
            friendly = get_friendly_error("error", str(e))
            result = {"written": False, "memory_id": None, "status": "error", "reason": str(e),
                      "message": friendly["message"], "tip": friendly["tip"]}
            warnings = self.get_degradation_warnings()
            if warnings:
                result["_warnings"] = warnings
            return _wrap(result)

    def batch_remember(self, items: list[dict]) -> list[dict]:
        """
        批量写入记忆。

        参数:
            items: 记忆列表，每项包含 content 及可选的 importance/topics 等

        返回: 结果列表
        """
        if getattr(self, '_ingest_engine', None) is not None and hasattr(self._ingest_engine, 'batch_remember'):
            return self._ingest_engine.batch_remember(items)
        return []

    def purge_cascade(self, memory_id: str) -> dict:
        """
        级联清除：删除指定记忆及其所有蒸馏派生内容。

        当一条记忆被删除或标记为不可信时，应调用此方法防止级联污染。
        同时清除：主题摘要、知识实体、关系、百科条目。

        参数:
            memory_id: 要清除的原始记忆 ID

        返回: {"purged": bool, "deleted": {table: count}, "memory_id": str}
        """
        result = self.distiller.purge_by_source(memory_id)
        result["memory_id"] = memory_id
        return result

    def purge_cascade_batch(self, memory_ids: list[str]) -> dict:
        """
        批量级联清除。

        参数:
            memory_ids: 要清除的原始记忆 ID 列表

        返回: {"purged": bool, "deleted": {table: count}, "count": int}
        """
        return self.distiller.purge_by_sources(memory_ids)

    def remember_image(
        self,
        image_path: str,
        description: str = None,
        importance: str = "medium",
        topics: list[str] = None,
        prompt: str = None,
    ) -> dict:
        """
        记住一张图片。

        如果配置了 vision_fn（GPT-4o / Qwen-VL / MiMo Omni 等），会自动：
        - 理解图片内容并生成描述
        - 提取图中文字（OCR）
        - 分析图表/代码/配置截图

        如果有 CLIP，还会生成图片 embedding（支持以图搜图）。

        否则降级为基本元数据提取。

        参数:
            image_path: 图片文件路径
            description: 手动描述（可选，模型描述会追加）
            importance: 重要度
            topics: 主题列表
            prompt: 给视觉模型的提示词（默认自动）

        返回: {"written": bool, "memory_id": str, "model_description": str, "has_clip_embedding": bool}
        """
        from media_processor import IMAGE_FORMATS
        return self._remember_media(image_path, IMAGE_FORMATS, "image", description, importance, topics, prompt)

    def remember_audio(
        self,
        audio_path: str,
        description: str = None,
        importance: str = "medium",
        topics: list[str] = None,
    ) -> dict:
        """
        记住一段音频。

        如果配置了 audio_fn（Whisper / MiMo Omni 等），会自动转写语音为文字。

        参数:
            audio_path: 音频文件路径
            description: 手动描述（可选）
            importance: 重要度
            topics: 主题列表

        返回: {"written": bool, "memory_id": str, "transcript": str}
        """
        from ..media_processor import AUDIO_FORMATS
        return self._remember_media(audio_path, AUDIO_FORMATS, "audio", description, importance, topics, None)

    def remember_video(
        self,
        video_path: str,
        description: str = None,
        importance: str = "medium",
        topics: list[str] = None,
        prompt: str = None,
    ) -> dict:
        """
        记住一个视频。

        如果同时配置了 vision_fn + audio_fn + ffmpeg，会自动：
        - 提取关键帧并用视觉模型分析
        - 提取音频并转写
        - 合并为完整的视频描述

        参数:
            video_path: 视频文件路径
            description: 手动描述（可选）
            importance: 重要度
            topics: 主题列表
            prompt: 给视觉模型的提示词

        返回: {"written": bool, "memory_id": str, "description": str}
        """
        from ..media_processor import VIDEO_FORMATS
        return self._remember_media(video_path, VIDEO_FORMATS, "video", description, importance, topics, prompt)

    def remember_media(
        self,
        file_path: str,
        description: str = None,
        importance: str = "medium",
        topics: list[str] = None,
        prompt: str = None,
    ) -> dict:
        """
        万能入口：自动识别图片/音频/视频并处理。

        用法：
            memory.remember_media("/path/to/screenshot.png")
            memory.remember_media("/path/to/meeting.mp3")
            memory.remember_media("/path/to/demo.mp4")
        """
        from ..media_processor import ALL_FORMATS
        return self._remember_media(file_path, ALL_FORMATS, None, description, importance, topics, prompt)

    def _remember_media(
        self,
        file_path: str,
        allowed_formats: set,
        expected_type: str = None,
        description: str = None,
        importance: str = "medium",
        topics: list[str] = None,
        prompt: str = None,
    ) -> dict:
        """内部统一处理入口，支持 DocumentParser 不可用时的降级模式"""
        import os

        if not os.path.exists(file_path):
            return {"written": False, "memory_id": None, "description": "", "reason": "文件不存在"}

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in allowed_formats:
            return {"written": False, "memory_id": None, "description": "", "reason": f"不支持的格式: {ext}"}

        filename = os.path.basename(file_path)

        # Try full processing with DocumentParser enhancement
        try:
            from ..document_parser import DocumentParser

            # 用 MediaProcessor 处理
            if self.media_processor:
                result = self.media_processor.process(file_path, prompt=prompt)
                model_desc = result.get("description", "")
                metadata = result.get("metadata", {})
                media_type = result.get("media_type", expected_type or "unknown")
            else:
                model_desc = ""
                metadata = {"filename": filename}
                media_type = expected_type or "unknown"

            # DocumentParser enhancement: try to extract text from document-type files
            doc_parser = DocumentParser()
            if ext in doc_parser.SUPPORTED_FORMATS:
                try:
                    parsed = doc_parser.parse(file_path)
                    if parsed.sections:
                        doc_text = "\n".join(
                            s.content for s in parsed.sections if s.content
                        )[:2000]
                        if doc_text:
                            if model_desc:
                                model_desc = model_desc + "\n\n[文档内容]\n" + doc_text
                            else:
                                model_desc = "[文档内容]\n" + doc_text
                            metadata["doc_sections"] = len(parsed.sections)
                            metadata["doc_title"] = parsed.title
                except Exception as e:
                    logger.debug("DocumentParser enhancement failed: %s", e)

        except ImportError:
            # DocumentParser not available — degraded mode
            logger.info(
                "DocumentParser未安装，%s记忆将使用降级模式（仅存储元数据）",
                expected_type or "媒体",
            )

            # Store basic metadata without content extraction
            content_parts = [f"[{(expected_type or 'MEDIA').upper()}] "]
            metadata = {}

            if os.path.exists(file_path):
                content_parts.append(f"文件: {filename}")
                metadata["file_path"] = file_path
                metadata["file_size"] = os.path.getsize(file_path)
                # Compute file hash for dedup
                try:
                    with open(file_path, "rb") as f:
                        metadata["file_hash"] = hashlib.sha256(f.read()).hexdigest()[:16]
                except Exception:
                    pass
            if description:
                content_parts.append(f"描述: {description}")

            metadata["media_type"] = expected_type or "unknown"
            metadata["degraded"] = True
            metadata["degradation_note"] = "DocumentParser未安装，仅存储基本元数据"

            content = " ".join(content_parts)

            # Determine topics
            if topics is None:
                type_topics = {
                    "image": "media.image",
                    "audio": "media.audio",
                    "video": "media.video",
                }
                topics = [type_topics.get(expected_type, "media")]

            result = self.remember(
                content=content,
                importance=importance,
                topics=topics,
                nature="note",
            )

            # Add degradation info to result
            if isinstance(result, dict):
                result["degraded"] = True
                result["degradation_note"] = metadata["degradation_note"]
                result["media_type"] = expected_type or "unknown"
                result["metadata"] = metadata
                result["description"] = ""
                result["has_clip_embedding"] = False

            return result

        # 组合内容
        content_parts = []
        if description:
            content_parts.append(description)
        content_parts.append(f"📁 {filename}")

        if metadata:
            meta_strs = []
            for k, v in metadata.items():
                if k != "filename":
                    meta_strs.append(f"{k}: {v}")
            if meta_strs:
                content_parts.append(" | ".join(meta_strs))

        if model_desc:
            content_parts.append(f"\n{model_desc}")

        content = "\n".join(content_parts)

        # 确定主题
        if topics is None:
            type_topics = {
                "image": "media.image",
                "audio": "media.audio",
                "video": "media.video",
            }
            topics = [type_topics.get(media_type, "media")]

        # 写入记忆
        write_result = self.remember(
            content=content,
            importance=importance,
            topics=topics,
            nature="note",
        )

        # CLIP 图片 embedding（支持以图搜图）
        has_clip = False
        if media_type == "image" and self.embedding_store and write_result.get("written"):
            try:
                self.embedding_store.add_image(
                    memory_id=write_result["memory_id"],
                    image_path=file_path,
                    text_description=model_desc or description or "",
                    metadata={
                        "media_type": "image",
                        "importance": importance,
                        "source_file": filename,
                    },
                )
                has_clip = True
            except Exception as e:
                logger.debug(f"CLIP embedding 失败: {e}")

        write_result["description"] = model_desc
        write_result["media_type"] = media_type
        write_result["metadata"] = metadata
        write_result["has_clip_embedding"] = has_clip
        return write_result

    def compress(self, topic: str = None, smart: bool = True) -> dict:
        """
        压缩记忆。

        参数:
            topic: 指定主题
            smart: 使用智能压缩（向量聚类区分核心/边缘）
        """
        if smart:
            return self.compressor.smart_compress(
                embedding_store=self.embedding_store,
                topic_code=topic,
            )
        return self.compressor.compress(topic_code=topic)

    def deduplicate(self) -> dict:
        """批量去重"""
        if self.dedup:
            return self.dedup.deduplicate_batch()
        return {"error": "去重功能未启用"}