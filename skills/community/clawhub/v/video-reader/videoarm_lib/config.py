"""VideoARM configuration — data paths and video database."""

import os
from pathlib import Path

PROJECT_ROOT = Path.home() / ".videoarm"
VIDEO_DATABASE_FOLDER = PROJECT_ROOT / "video_database"


def get_config():
    """Get configuration from environment variables.
    
    Loads .env file automatically. Uses VISION_* vars with OPENAI_* fallback.
    Supports OpenClaw (default), OpenAI, and Anthropic APIs.
    """
    from dotenv import load_dotenv
    load_dotenv()

    provider = os.getenv("VISION_PROVIDER", "openclaw").lower()
    
    return {
        "provider": provider,
        "openai_api_key": os.getenv("VISION_API_KEY") or os.getenv("OPENAI_API_KEY"),
        "openai_base_url": os.getenv("VISION_BASE_URL") or os.getenv("OPENAI_BASE_URL"),
        "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
        "anthropic_base_url": os.getenv("ANTHROPIC_BASE_URL"),
        "vision_model": os.getenv("VISION_MODEL") or os.getenv("VIDEOARM_VISION_MODEL", "default"),
    }


class VideoDatabase:
    """Video database and path management."""

    def __init__(self, base_dir=None, default_dataset="default"):
        self.base_dir = Path(base_dir) if base_dir else VIDEO_DATABASE_FOLDER
        self.default_dataset = default_dataset
        self.temp_dir = self.base_dir / "temp"
        self._ensure_structure()

    def _ensure_structure(self):
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        for sub in ("downloads", "processing"):
            (self.temp_dir / sub).mkdir(exist_ok=True)

    def get_video_id_from_path(self, video_path):
        video_path = Path(video_path)
        if (
            video_path.name == "source.mp4"
            and video_path.parent.parent.parent.name == "video_database"
        ):
            return video_path.parent.name, video_path.parent.parent.name
        return video_path.stem, self.default_dataset

    def get_temp_frames_dir(self, video_id, session_id=None, dataset=None):
        base = self.base_dir / (dataset or self.default_dataset) / video_id / "cache" / "temp_frames"
        return base / session_id if session_id else base


database = VideoDatabase()
