from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Article:
    title: str
    markdown: str
    html: str
    digest: str
    source_url: str = ""
    author: str = ""
    cover_hint: str = ""


@dataclass
class WeChatConfig:
    app_id: str
    app_secret: str
    author: str = ""
    default_template: str = "standard"
    open_comment: bool = True
    fans_only_comment: bool = False


@dataclass
class ProviderConfig:
    api_key: str = ""
    model: str = ""
    base_url: str = ""


@dataclass
class ImageGenerationConfig:
    provider: str = "doubao"
    size: str = "1536x1024"
    quality: str = "standard"
    doubao: ProviderConfig = field(default_factory=ProviderConfig)
    qwen: ProviderConfig = field(default_factory=ProviderConfig)


@dataclass
class WorkspaceConfig:
    output_dir: str = "outputs"


@dataclass
class SkillConfig:
    wechat: WeChatConfig
    image_generation: ImageGenerationConfig = field(default_factory=ImageGenerationConfig)
    workspace: WorkspaceConfig = field(default_factory=WorkspaceConfig)

    def resolve_output_dir(self, project_root: Path) -> Path:
        output_dir = Path(self.workspace.output_dir)
        if output_dir.is_absolute():
            return output_dir
        return project_root / output_dir
