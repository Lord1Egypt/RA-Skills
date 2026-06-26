"""
图可丽视觉 API Skill — 配置管理

管理：API Key、端点 URL、输出目录。

重要：图可丽 API 请求域名为 picupapi.tukeli.net，与官网 www.tukeli.net 不同。
"""
from __future__ import annotations

import os
from pathlib import Path

# ── 路径 ─────────────────────────────────────────────────────────────────────

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"
DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = DATA_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── API 配置 ──────────────────────────────────────────────────────────────────

# 注意：API 请求域名与官网不同
API_BASE = "https://picupapi.tukeli.net"
USER_AGENT = "TukeliSkill/1.0"

ENDPOINTS = {
    # 通用抠图 — 二进制响应（mattingType 作为 URL 参数）
    "matting_binary": "/api/v1/matting",
    # 通用抠图 — Base64 响应
    "matting_base64": "/api/v1/matting2",
    # 通用抠图 — 图片URL模式
    "matting_url": "/api/v1/mattingByUrl",
    # 人脸变清晰 — 与抠图共用端点，mattingType=18
    "face_clear_binary": "/api/v1/matting",
    "face_clear_base64": "/api/v1/matting2",
    "face_clear_url": "/api/v1/mattingByUrl",
    # AI背景更换 — 异步接口
    "ai_bg_submit": "/api/v1/paintAsync",
    "ai_bg_query": "/api/v1/getPaintResult",
}

# mattingType 映射
MATTING_TYPE = {
    "matting": None,   # 由 --matting-type 参数决定，默认 6
    "face-clear": 18,  # 人脸变清晰固定为 18
}

# 抠图类型说明
MATTING_TYPE_DESC = {
    1: "人像抠图（发丝级精度）",
    2: "物体抠图",
    3: "头像抠图",
    6: "通用抠图（默认）",
}

# ── 输出配置 ──────────────────────────────────────────────────────────────────

OUTPUT_SETTINGS = {
    "format": "png",
    "save_metadata": True,
}

# ── 工具函数 ──────────────────────────────────────────────────────────────────


def _parse_env_file(env_path: Path) -> dict[str, str]:
    """解析 .env 文件，返回 key=value 字典。"""
    result: dict[str, str] = {}
    if not env_path.exists():
        return result
    try:
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k and v:
                    result[k] = v
    except (OSError, UnicodeDecodeError):
        pass
    return result


def get_api_key() -> str | None:
    """按优先级获取 API Key：环境变量 > .env 文件。"""
    key = os.environ.get("TUKELI_API_KEY")
    if key:
        return key
    env_data = _parse_env_file(ROOT_DIR / ".env")
    return env_data.get("TUKELI_API_KEY")


def validate_image_file(filepath: str | Path, api: str = "matting") -> Path:
    """验证图片文件存在且格式受支持。"""
    if api == "matting":
        supported = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}
        max_size_mb = 25
    else:  # face-clear
        supported = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}
        max_size_mb = 15

    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在：{path}")
    if not path.is_file():
        raise ValueError(f"不是文件：{path}")
    if path.suffix.lower() not in supported:
        raise ValueError(
            f"不支持的格式：{path.suffix}。支持：{', '.join(supported)}"
        )
    if path.stat().st_size == 0:
        raise ValueError(f"文件为空：{path}")
    if path.stat().st_size > max_size_mb * 1024 * 1024:
        raise ValueError(
            f"文件过大（{path.stat().st_size / 1024 / 1024:.1f}MB），最大 {max_size_mb}MB"
        )
    return path
