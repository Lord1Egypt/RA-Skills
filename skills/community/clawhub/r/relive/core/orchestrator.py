import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

from jinja2 import Environment, FileSystemLoader

from core.memory.dual_rag import DualRAG
from core.engines.voice_engine import VoiceEngine

logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(
        self,
        config_dir: Path,
        storage_root: Path,
        settings: Dict[str, Any],
        video_gen_engine: Optional[Any] = None,
    ):
        self.config_dir = config_dir
        self.storage_root = storage_root
        self.settings = settings
        self.video_gen_engine = video_gen_engine

        self.prompts_dir = config_dir / "prompts"
        self.jinja_env = Environment(loader=FileSystemLoader(str(self.prompts_dir)))

        self.voice_engine = VoiceEngine(settings.get("voice", {}))
        
    def get_storage_path(self, user_id: str, target_id: str) -> Path:
        return self.storage_root / f"{user_id}_{target_id}"
    
    def get_profile(self, user_id: str, target_id: str) -> Dict[str, Any]:
        storage_path = self.get_storage_path(user_id, target_id)
        profile_file = storage_path / "profile.md"
        if profile_file.exists():
            with open(profile_file, "r", encoding="utf-8") as f:
                raw = f.read()
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return {"markdown_content": raw}
        return {}
    
    def retrieve_context(self, user_id: str, target_id: str, user_message: str) -> Dict[str, Any]:
        storage_path = self.get_storage_path(user_id, target_id)
        
        profile = self.get_profile(user_id, target_id)
        
        rag = DualRAG(
            storage_path=storage_path,
            settings=self.settings.get("rag", {})
        )
        
        memories = rag.retrieve(user_message)
        logger.info(f"RAG retrieve returned {len(memories)} memories for query: {user_message}")
        
        return {
            "profile": profile,
            "memories": memories
        }
    
    def build_prompt_context(self, user_id: str, target_id: str, user_message: str) -> str:
        storage_path = self.get_storage_path(user_id, target_id)
        
        profile = self.get_profile(user_id, target_id)
        target_name = profile.get("name", target_id)
        
        rag = DualRAG(
            storage_path=storage_path,
            settings=self.settings.get("rag", {})
        )
        
        memories = rag.retrieve(user_message)
        logger.info(f"RAG retrieve returned {len(memories)} memories for query: {user_message}")
        
        return self._build_system_prompt(
            target_name=target_name,
            profile=profile,
            memories=memories,
            context=user_message
        )
    
    def process(
        self,
        user_id: str,
        target_id: str,
        response_text: str,
        output_mode: str = None,
        prompt_text: Optional[str] = None,
        user_message: str = "",
        reference_image_url: Optional[str] = None,
        video_wait: bool = False,
    ) -> Dict[str, Any]:
        if output_mode is None:
            output_mode = self.settings.get("default_output_mode", "voice")

        storage_path = self.get_storage_path(user_id, target_id)

        result = {
            "success": True,
            "text": response_text,
            "mode": output_mode,
        }
        
        voice_profile_path = storage_path / "voice_profile"
        has_voice_profile = (
            voice_profile_path.exists() and 
            (list(voice_profile_path.glob("*.wav")) or 
             list(voice_profile_path.glob("*.mp3")) or 
             list(voice_profile_path.glob("*.m4a")))
        )
        
        # video 模式不走语音合成，只走视频 API；仅 voice 模式需要 TTS
        if output_mode == "voice" and has_voice_profile:
            if not (prompt_text and str(prompt_text).strip()):
                result["voice_skip_reason"] = "语音克隆需要 prompt_text：请填写与参考音频内容一致的逐字稿（参考音频里说的那句话的文本）"
                output_mode = "text"
            else:
                try:
                    voice_result = self.voice_engine.synthesize(
                        text=response_text,
                        voice_profile_path=voice_profile_path,
                        prompt_text=prompt_text,
                    )
                    if voice_result.get("success"):
                        result["audio"] = voice_result.get("audio_path")
                    else:
                        reason = voice_result.get("error", "unknown")
                        result["voice_skip_reason"] = reason
                        logger.warning(f"Voice synthesis failed: {reason}, falling back to text")
                        output_mode = "text"
                except Exception as e:
                    result["voice_skip_reason"] = str(e)
                    logger.warning(f"Voice synthesis error: {e}, falling back to text")
                    output_mode = "text"
        elif output_mode == "voice" and not has_voice_profile:
            result["voice_skip_reason"] = "未找到语音样本：请在 storage/{user_id}_{target_id}/voice_profile/ 下放入参考音频（.wav / .mp3 / .m4a）"
            logger.warning("No voice profile found, falling back to text")
            output_mode = "text"

        if output_mode == "video":
            if not self.video_gen_engine or not getattr(self.video_gen_engine, "enabled", False):
                logger.info("视频生成 API 未启用，回退为 text")
                result["mode"] = "text"
            else:
                try:
                    # 让画面中的主体说回复内容，避免生成“不说话”的视频
                    # 传递链：synthesize.content -> response_text -> video_prompt -> API content[0].text
                    video_prompt = f'画面中的主体说：「{response_text}」'
                    logger.info("视频生成 prompt 传给 API: %s", video_prompt)
                    create_result = self.video_gen_engine.create_task_from_prompt(
                        video_prompt,
                        image_url=reference_image_url.strip() if reference_image_url else None,
                    )
                    if create_result.get("success") and create_result.get("task_id"):
                        result["video_task_id"] = create_result["task_id"]
                        result["video_prompt"] = video_prompt  # 便于核对实际发给 API 的文案
                        result["mode"] = "video"
                        if video_wait:
                            wait_result = self.video_gen_engine.wait_for_task(create_result["task_id"])
                            if wait_result.get("success") and wait_result.get("status") == "succeeded":
                                content = wait_result.get("content") or {}
                                result["video_url"] = content.get("video_url")
                            else:
                                result["video_wait_error"] = wait_result.get("error", "轮询未完成")
                    else:
                        result["video_error"] = create_result.get("error", "创建任务失败")
                        result["mode"] = "text"
                except Exception as e:
                    logger.warning(f"Video generation failed: {e}, falling back to text")
                    result["video_error"] = str(e)
                    result["mode"] = "text"
        else:
            result["mode"] = output_mode

        self._save_runtime_log(user_id, target_id, user_message, response_text)
        self._index_runtime_turn(user_id, target_id, user_message, response_text)

        return result
        
    def _build_system_prompt(
        self,
        target_name: str,
        profile: Dict[str, Any],
        memories: List[Dict[str, Any]],
        context: str
    ) -> str:
        template = self.jinja_env.get_template("system_prompt.jinja2")
        
        prompt = template.render(
            target_name=target_name,
            profile=profile,
            memories=memories,
            context=context
        )
        
        return prompt
    
    def index_source_data(self, user_id: str, target_id: str, source_path: Path):
        storage_path = self.get_storage_path(user_id, target_id)
        
        chat_files = (
            list(source_path.glob("*.csv"))
            + list(source_path.glob("*.txt"))
            + list(source_path.glob("*.json"))
        )
        
        all_messages = []
        for chat_file in chat_files:
            try:
                from core.importer.factory import ImporterFactory
                ext = chat_file.suffix[1:]
                importer = ImporterFactory.get_importer(ext if ext else "json")
                messages = importer.parse(chat_file)
                all_messages.extend(messages)
            except Exception as e:
                logger.error(f"Failed to parse {chat_file}: {e}")
        
        if all_messages:
            # 读取上传阶段保存的“自己 / 目标”名字，用于给消息打 role
            chat_meta = {}
            meta_file = storage_path / "chat_meta.json"
            if meta_file.exists():
                try:
                    with open(meta_file, "r", encoding="utf-8") as f:
                        chat_meta = json.load(f)
                except Exception as e:
                    logger.warning(f"Failed to load chat_meta.json: {e}")

            self_name = (chat_meta.get("self_name") or "").strip()
            target_name = (chat_meta.get("target_name") or "").strip()

            for msg in all_messages:
                # 为画像 / 检索打上 role 标记：self / target / other
                role = "other"
                sender = (msg.sender or "").strip()
                if target_name and sender == target_name:
                    role = "target"
                elif self_name and sender == self_name:
                    role = "self"

                metadata = msg.metadata or {}
                metadata["role"] = role
                msg.metadata = metadata

            from core.engines.llm_engine import LLMEngine
            llm_engine = LLMEngine({})
            # 只用目标人物的消息来抽取画像；如没有 role，则回退为全部
            target_messages = [
                msg.to_dict()
                for msg in all_messages
                if msg.metadata and msg.metadata.get("role") == "target"
            ]
            profile_source = target_messages or [msg.to_dict() for msg in all_messages]

            profile = llm_engine.extract_profile(profile_source)
            
            profile_file = storage_path / "profile.md"
            with open(profile_file, 'w', encoding='utf-8') as f:
                json.dump(profile, f, ensure_ascii=False, indent=2)
                
            rag = DualRAG(
                storage_path=storage_path,
                settings=self.settings.get("rag", {})
            )
            rag.index_source_data([msg.to_dict() for msg in all_messages])
            
    def _save_runtime_log(self, user_id: str, target_id: str, user_message: str, response: str):
        storage_path = self.get_storage_path(user_id, target_id)
        log_file = storage_path / "runtime" / "conversation.jsonl"
        import datetime
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user": user_message,
            "assistant": response,
        }
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    def _index_runtime_turn(
        self, user_id: str, target_id: str, user_message: str, response: str
    ):
        if not user_message.strip() and not response.strip():
            return
        storage_path = self.get_storage_path(user_id, target_id)
        rag = DualRAG(
            storage_path=storage_path,
            settings=self.settings.get("rag", {}),
        )
        rag.index_runtime_data(user_message, response)
        logger.info("Indexed one runtime turn into RAG")
