from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import ImageGenerationConfig, ProviderConfig, SkillConfig, WeChatConfig, WorkspaceConfig


def _provider_config(data: dict[str, Any]) -> ProviderConfig:
    return ProviderConfig(
        api_key=(data.get("api_key") or "").strip(),
        model=(data.get("model") or "").strip(),
        base_url=(data.get("base_url") or "").strip(),
    )


def load_config(path: Path) -> SkillConfig:
    if not path.exists():
        raise RuntimeError(f"配置文件不存在: {path}")

    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw.get("platforms", {}).get("wechat"), dict):
        raw["wechat"] = raw["platforms"]["wechat"]

    wechat_raw = raw.get("wechat") or {}
    if not isinstance(wechat_raw, dict):
        raise RuntimeError("配置文件缺少 wechat 配置")

    image_raw = raw.get("image_generation") or {}
    workspace_raw = raw.get("workspace") or {}

    return SkillConfig(
        wechat=WeChatConfig(
            app_id=(wechat_raw.get("app_id") or "").strip(),
            app_secret=(wechat_raw.get("app_secret") or "").strip(),
            author=(wechat_raw.get("author") or "").strip(),
            default_template=(wechat_raw.get("default_template") or "standard").strip() or "standard",
            open_comment=bool(wechat_raw.get("open_comment", True)),
            fans_only_comment=bool(wechat_raw.get("fans_only_comment", False)),
        ),
        image_generation=ImageGenerationConfig(
            provider=(image_raw.get("provider") or "doubao").strip().lower(),
            size=(image_raw.get("size") or "1536x1024").strip(),
            quality=(image_raw.get("quality") or "standard").strip(),
            doubao=_provider_config(image_raw.get("doubao") or {}),
            qwen=_provider_config(image_raw.get("qwen") or {}),
        ),
        workspace=WorkspaceConfig(output_dir=(workspace_raw.get("output_dir") or "outputs").strip()),
    )
