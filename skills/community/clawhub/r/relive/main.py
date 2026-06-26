import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

from core.orchestrator import Orchestrator
from core.engines.video_gen_engine import VideoGenEngine
from core.utils.config_loader import load_settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ReliveSkill:
    def __init__(self, skill_root: Optional[str] = None):
        if skill_root is None:
            skill_root = os.path.dirname(os.path.abspath(__file__))
        self.skill_root = Path(skill_root)
        
        self.config_dir = self.skill_root / "config"
        self.storage_root = self.skill_root / "storage"
        
        self.settings = load_settings(self.config_dir / "settings.yaml")
        self.video_gen_engine = VideoGenEngine(
            self.settings.get("video_generation", {})
        )
        self.orchestrator = Orchestrator(
            config_dir=self.config_dir,
            storage_root=self.storage_root,
            settings=self.settings,
            video_gen_engine=self.video_gen_engine,
        )
        
    def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        # 允许调用方省略 user_id，默认视为单用户场景
        user_id = message.get("user_id") or "default"
        target_id = message.get("target_id")
        content = message.get("content", "")
        message_type = message.get("type", "text")
        
        if message_type not in ("video_generation_create", "video_generation_wait"):
            if not user_id or not target_id:
                return {
                    "success": False,
                    "error": "Missing user_id or target_id"
                }

        if message_type == "init":
            return self._handle_init(user_id, target_id)
        elif message_type == "upload":
            return self._handle_upload(user_id, target_id, message)
        elif message_type == "get_context":
            return self._handle_get_context(user_id, target_id, content)
        elif message_type == "synthesize":
            return self._handle_synthesize(user_id, target_id, message)
        elif message_type == "export_md":
            return self._handle_export_md(user_id, target_id, message)
        elif message_type == "video_generation_create":
            return self._handle_video_generation_create(message)
        elif message_type == "video_generation_wait":
            return self._handle_video_generation_wait(message)
        else:
            return self._handle_get_context(user_id, target_id, content)
            
    def _handle_init(self, user_id: str, target_id: str) -> Dict:
        storage_path = self.storage_root / f"{user_id}_{target_id}"
        storage_path.mkdir(parents=True, exist_ok=True)
        
        (storage_path / "source").mkdir(exist_ok=True)
        (storage_path / "runtime").mkdir(exist_ok=True)
        (storage_path / "vector_db" / "source_index").mkdir(parents=True, exist_ok=True)
        (storage_path / "vector_db" / "runtime_index").mkdir(parents=True, exist_ok=True)
        (storage_path / "voice_profile").mkdir(exist_ok=True)
        (storage_path / "cache").mkdir(exist_ok=True)
        
        return {
            "success": True,
            "message": f"Storage initialized for {target_id}",
            "storage_path": str(storage_path)
        }
        
    def _handle_get_context(self, user_id: str, target_id: str, user_message: str) -> Dict:
        context = self.orchestrator.build_prompt_context(user_id, target_id, user_message)
        
        return {
            "success": True,
            "context": context
        }
        
    def _handle_synthesize(self, user_id: str, target_id: str, message: Dict) -> Dict:
        # content = 要合成的 AI 回复正文（语音/视频时作为 text 传给引擎）；兼容旧字段 text
        response_text = message.get("content", message.get("text", ""))
        output_mode = message.get("output_mode")
        user_message = message.get("user_message", "")

        # prompt_text 不再要求调用方传入，而是从
        # storage/{user_id}_{target_id}/voice_profile/corresponding.txt 读取
        prompt_text: Optional[str] = None
        voice_profile_dir = self.storage_root / f"{user_id}_{target_id}" / "voice_profile"
        corresponding_path = voice_profile_dir / "corresponding.txt"
        if corresponding_path.exists():
            try:
                with open(corresponding_path, "r", encoding="utf-8") as f:
                    prompt_text = f.read().strip()
            except Exception as e:
                logger.warning(f"Failed to read prompt_text from {corresponding_path}: {e}")

        # 视频模式：参考图使用 URL。优先用请求里的 reference_image_url，否则读角色目录下的 reference_image_url.txt
        reference_image_url: Optional[str] = (message.get("reference_image_url") or "").strip() or None
        if not reference_image_url and output_mode == "video":
            storage_path = self.storage_root / f"{user_id}_{target_id}"
            url_file = storage_path / "reference_image_url.txt"
            if url_file.exists():
                try:
                    with open(url_file, "r", encoding="utf-8") as f:
                        reference_image_url = f.read().strip() or None
                except Exception as e:
                    logger.warning(f"Failed to read reference_image_url from {url_file}: {e}")

        result = self.orchestrator.process(
            user_id=user_id,
            target_id=target_id,
            response_text=response_text,
            output_mode=output_mode,
            prompt_text=prompt_text,
            user_message=user_message,
            reference_image_url=reference_image_url,
            video_wait=message.get("video_wait", False),
        )
        # video 模式下若返回了 video_task_id，自动生成 video_wait.json，无需再复制 task_id
        if result.get("success") and result.get("video_task_id"):
            wait_json = {
                "type": "video_generation_wait",
                "user_id": user_id,
                "target_id": target_id,
                "task_id": result["video_task_id"],
                "poll_interval_seconds": 5,
                "poll_timeout_seconds": 600,
            }
            wait_path = self.skill_root / "video_wait.json"
            try:
                with open(wait_path, "w", encoding="utf-8") as f:
                    json.dump(wait_json, f, ensure_ascii=False, indent=2)
                result["video_wait_json"] = str(wait_path)
            except Exception as e:
                logger.warning("Failed to write video_wait.json: %s", e)
        return result

    def _handle_export_md(self, user_id: str, target_id: str, message: Dict) -> Dict:
        storage_path = self.storage_root / f"{user_id}_{target_id}"
        source_dir = storage_path / "source"
        
        chat_file = None
        if source_dir.exists():
            files = list(source_dir.glob("*.json"))
            if files:
                chat_file = files[0]
        
        if not chat_file or not chat_file.exists():
            return {"success": False, "error": "No chat file found"}
        
        with open(chat_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        messages = data.get("messages", [])
        
        meta_file = storage_path / "chat_meta.json"
        self_name = "我"
        target_name = "对方"
        if meta_file.exists():
            with open(meta_file, 'r', encoding='utf-8') as f:
                meta = json.load(f)
                self_name = meta.get("self_name", self_name)
                target_name = meta.get("target_name", target_name)
        
        md_content = f"# {target_name} 的聊天记录\n\n"
        md_content += f"- **对话者**: {self_name} (我)\n"
        md_content += f"- **对方**: {target_name}\n"
        md_content += f"- **消息数**: {len(messages)}\n\n"
        md_content += "---\n\n"
        
        current_date = ""
        for msg in messages:
            sender = msg.get("sender", {})
            sender_name = sender.get("name", "未知")
            msg_time = msg.get("time", "")
            content = msg.get("content", {})
            text = content.get("text", "")
            
            msg_date = msg_time.split(" ")[0] if msg_time else ""
            if msg_date and msg_date != current_date:
                current_date = msg_date
                md_content += f"\n## {current_date}\n\n"
            
            speaker = target_name if sender_name == target_name else self_name
            md_content += f"**{speaker}** {msg_time.split(' ')[1] if ' ' in msg_time else ''}\n"
            md_content += f"{text}\n\n"
        
        output_file = storage_path / "chat.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        return {
            "success": True,
            "message": f"Exported to {output_file}",
            "output_path": str(output_file)
        }

    def _handle_video_generation_create(self, message: Dict) -> Dict:
        """创建视频生成任务（Seedance 等 API）。"""
        if not self.video_gen_engine.enabled:
            return {"success": False, "error": "视频生成 API 未启用，请在 config/settings.yaml 中设置 video_generation.enabled: true"}
        text = message.get("text", "").strip()
        image_url = (message.get("image_url") or "").strip() or None
        content = message.get("content")
        if content is not None:
            # 直接传 content 列表时使用
            result = self.video_gen_engine.create_task(
                content,
                generate_audio=message.get("generate_audio", True),
                ratio=message.get("ratio", "adaptive"),
                duration=message.get("duration", 5),
                watermark=message.get("watermark", False),
            )
        else:
            if not text:
                return {"success": False, "error": "缺少 text 或 content"}
            result = self.video_gen_engine.create_task_from_prompt(
                text,
                image_url=image_url,
                generate_audio=message.get("generate_audio", True),
                ratio=message.get("ratio", "adaptive"),
                duration=message.get("duration", 5),
                watermark=message.get("watermark", False),
            )
        return result

    def _handle_video_generation_wait(self, message: Dict) -> Dict:
        """轮询视频生成任务直到完成或超时，成功后自动下载到该角色目录下 cache/。"""
        task_id = message.get("task_id", "").strip()
        if not task_id:
            return {"success": False, "error": "缺少 task_id"}
        user_id = message.get("user_id") or "default"
        target_id = message.get("target_id")
        if not target_id:
            return {"success": False, "error": "缺少 target_id，视频会保存到 storage/{user_id}_{target_id}/cache/"}
        result = self.video_gen_engine.wait_for_task(
            task_id,
            poll_interval=message.get("poll_interval_seconds"),
            timeout=message.get("poll_timeout_seconds"),
        )
        if not result.get("success") or result.get("status") != "succeeded":
            return result
        content = result.get("content") or {}
        video_url = content.get("video_url")
        if not video_url:
            return {**result, "success": False, "error": "任务成功但无 video_url"}
        cache_dir = self.storage_root / f"{user_id}_{target_id}" / "cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        video_path = cache_dir / f"{task_id}.mp4"
        try:
            import requests as req
            r = req.get(video_url, stream=True, timeout=120)
            r.raise_for_status()
            with open(video_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        except Exception as e:
            logger.warning("Video download failed: %s", e)
            return {**result, "video_url": video_url, "video_download_error": str(e)}
        result["video_path"] = str(video_path)
        result["video_url"] = video_url
        return result

    def _handle_upload(self, user_id: str, target_id: str, message: Dict) -> Dict:
        file_path = message.get("file_path")
        file_type = message.get("file_type", "unknown")
        self_name = message.get("self_name")
        target_name = message.get("target_name")
        
        if not file_path:
            return {
                "success": False,
                "error": "Missing file_path"
            }
            
        storage_root = self.storage_root / f"{user_id}_{target_id}"
        storage_path = storage_root / "source"
        
        try:
            from pathlib import Path
            from core.importer.factory import ImporterFactory

            importer = ImporterFactory.get_importer(file_type)
            result = importer.import_file(Path(file_path), storage_path)
            
            # 如果提供了“自己/目标”的名字，保存到元数据文件，供后续建模使用
            if self_name or target_name:
                meta = {
                    "self_name": self_name,
                    "target_name": target_name,
                }
                meta_file = storage_root / "chat_meta.json"
                with open(meta_file, "w", encoding="utf-8") as f:
                    json.dump(meta, f, ensure_ascii=False, indent=2)
            
            if result.get("success"):
                self.orchestrator.index_source_data(user_id, target_id, storage_path)
                
            return result
        except Exception as e:
            logger.error(f"Upload failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }


def _warn_if_not_in_venv() -> None:
    """
    Print a gentle reminder to use a virtual environment when running this skill.
    This does not abort execution; it only warns, to avoid accidental model
    installs into the global Python environment.
    """
    import sys

    in_venv = (
        # Standard venv / virtualenv
        getattr(sys, "base_prefix", sys.prefix) != sys.prefix
        or getattr(sys, "real_prefix", None) is not None
        # Conda env
        or os.environ.get("CONDA_DEFAULT_ENV")
        # Generic indicator
        or os.environ.get("VIRTUAL_ENV")
    )

    if not in_venv:
        print(
            "[Re:Live] WARNING: It looks like you are not running inside a virtual "
            "environment. For stable dependencies and to avoid model issues, "
            "please activate a venv (typically named `.venv`) in this "
            "skill directory before running `python main.py ...`."
        )


def main():
    _warn_if_not_in_venv()

    skill = ReliveSkill()
    
    import sys
    if len(sys.argv) > 1:
        message_file = sys.argv[1]
        with open(message_file, 'r', encoding='utf-8') as f:
            message = json.load(f)
        result = skill.handle_message(message)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Re:Live skill initialized. Waiting for messages...")


if __name__ == "__main__":
    main()
