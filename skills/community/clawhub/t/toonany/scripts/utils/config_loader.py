"""Configuration loader with friendly onboarding for missing API keys."""

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


class ConfigError(Exception):
    """Raised when configuration is invalid or incomplete."""
    pass


# Provider-specific onboarding guides
PROVIDER_GUIDES = {
    "deepseek": {
        "name": "DeepSeek",
        "apply_url": "https://platform.deepseek.com/api_keys",
        "guide": (
            "1. 访问 https://platform.deepseek.com 注册账号\n"
            "2. 进入 API Keys 页面创建密钥\n"
            "3. 复制密钥并执行: export DEEPSEEK_API_KEY=sk-xxx"
        ),
        "env_var": "DEEPSEEK_API_KEY",
    },
    "volcengine": {
        "name": "火山引擎",
        "apply_url": "https://console.volcengine.com/ark/",
        "guide": (
            "1. 访问 https://console.volcengine.com 注册账号\n"
            "2. 开通方舟大模型服务\n"
            "3. 创建 API Key\n"
            "4. 执行: export VOLC_API_KEY=你的密钥"
        ),
        "env_var": "VOLC_API_KEY",
    },
    "kling": {
        "name": "可灵",
        "apply_url": "https://klingai.com/",
        "guide": (
            "1. 访问 https://klingai.com/ 注册账号\n"
            "2. 进入开发者中心创建 API Key\n"
            "3. 执行: export KLING_API_KEY=你的密钥"
        ),
        "env_var": "KLING_API_KEY",
    },
    "vidu": {
        "name": "Vidu",
        "apply_url": "https://www.vidu.com/",
        "guide": (
            "1. 访问 https://www.vidu.com/ 注册账号\n"
            "2. 申请 API 权限\n"
            "3. 执行: export VIDU_API_KEY=你的密钥"
        ),
        "env_var": "VIDU_API_KEY",
    },
    "gemini": {
        "name": "Google Gemini",
        "apply_url": "https://aistudio.google.com/app/apikey",
        "guide": (
            "1. 访问 https://aistudio.google.com/app/apikey\n"
            "2. 创建 API Key\n"
            "3. 执行: export GEMINI_API_KEY=你的密钥"
        ),
        "env_var": "GEMINI_API_KEY",
    },
    "openai": {
        "name": "OpenAI",
        "apply_url": "https://platform.openai.com/api-keys",
        "guide": (
            "1. 访问 https://platform.openai.com 注册账号\n"
            "2. 进入 API Keys 页面创建密钥\n"
            "3. 执行: export OPENAI_API_KEY=sk-xxx"
        ),
        "env_var": "OPENAI_API_KEY",
    },
    "anthropic": {
        "name": "Anthropic",
        "apply_url": "https://console.anthropic.com/settings/keys",
        "guide": (
            "1. 访问 https://console.anthropic.com 注册账号\n"
            "2. 进入 API Keys 页面创建密钥\n"
            "3. 执行: export ANTHROPIC_API_KEY=sk-ant-xxx"
        ),
        "env_var": "ANTHROPIC_API_KEY",
    },
    "aliyun": {
        "name": "阿里云",
        "apply_url": "https://www.aliyun.com/product/nls",
        "guide": (
            "1. 访问阿里云官网开通语音合成服务\n"
            "2. 创建 Access Key\n"
            "3. 执行: export ALIYUN_ACCESS_KEY_ID=xxx\n"
            "   export ALIYUN_ACCESS_KEY_SECRET=xxx"
        ),
        "env_var": "ALIYUN_ACCESS_KEY_ID",
    },
    "edge-tts": {
        "name": "Edge TTS",
        "apply_url": None,
        "guide": (
            "Edge TTS 是免费服务，无需 API Key。\n"
            "确保已安装 edge-tts: pip install edge-tts"
        ),
        "env_var": None,
    },
}


@dataclass
class ModelConfig:
    """Configuration for a single AI model."""
    provider: str
    model: str
    api_key: str
    base_url: Optional[str] = None


@dataclass
class ProjectConfig:
    """Complete project configuration."""
    name: str
    project_type: str
    art_style: str
    video_ratio: str
    episode_count: int
    style_reference: Optional[str] = None
    versions: dict = field(default_factory=dict)
    text_model: Optional[ModelConfig] = None
    image_model: Optional[ModelConfig] = None
    video_model: Optional[ModelConfig] = None
    audio_model: Optional[ModelConfig] = None
    characters: list = field(default_factory=list)
    scenes: list = field(default_factory=list)
    props: list = field(default_factory=list)


class ConfigLoader:
    """Load and validate project configuration with friendly onboarding."""

    ENV_VAR_PATTERN = re.compile(r"^\$\{(.+)\}$")

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.config_file = self.project_path / "project.json"

    def load(self, resolve_env: bool = True) -> ProjectConfig:
        """Load project configuration from project.json.

        Args:
            resolve_env: Whether to resolve ${ENV_VAR} syntax from environment.

        Returns:
            ProjectConfig instance.

        Raises:
            ConfigError: If project.json is missing or invalid.
        """
        if not self.config_file.exists():
            raise ConfigError(
                f"项目配置文件不存在: {self.config_file}\n"
                f"请先执行 '/toonany new <name>' 创建项目。"
            )

        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigError(f"project.json 格式错误: {e}")

        # Resolve environment variables
        if resolve_env:
            data = self._resolve_env_vars(data)

        # Parse model configs
        models = data.get("models", {})
        text_model = self._parse_model_config(models.get("text"))
        image_model = self._parse_model_config(models.get("image"))
        video_model = self._parse_model_config(models.get("video"))
        audio_model = self._parse_model_config(models.get("audio"))

        return ProjectConfig(
            name=data.get("name", "untitled"),
            project_type=data.get("type", "都市"),
            art_style=data.get("artStyle", "2D动漫风格"),
            video_ratio=data.get("videoRatio", "16:9"),
            episode_count=data.get("episodeCount", 1),
            style_reference=data.get("styleReference"),
            versions=data.get("versions", {}),
            text_model=text_model,
            image_model=image_model,
            video_model=video_model,
            audio_model=audio_model,
            characters=data.get("characters", []),
            scenes=data.get("scenes", []),
            props=data.get("props", []),
        )

    def check_required_models(self, *model_types: str) -> list[dict]:
        """Check if required model types are configured.

        Args:
            *model_types: Model types to check ('text', 'image', 'video', 'audio').

        Returns:
            List of missing model guides. Empty if all are configured.
        """
        try:
            config = self.load(resolve_env=True)
        except ConfigError:
            return []

        model_map = {
            "text": config.text_model,
            "image": config.image_model,
            "video": config.video_model,
            "audio": config.audio_model,
        }

        missing = []
        for model_type in model_types:
            model = model_map.get(model_type)
            if not model or not model.api_key:
                # Try to get provider from raw config for better guidance
                raw_provider = self._get_raw_provider(model_type)
                guide = self._get_missing_guide(raw_provider or "volcengine")
                missing.append({
                    "type": model_type,
                    "provider": raw_provider or "未知",
                    "guide": guide,
                })

        return missing

    def _get_raw_provider(self, model_type: str) -> Optional[str]:
        """Get provider name from raw config without env resolution."""
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("models", {}).get(model_type, {}).get("provider")
        except Exception:
            return None

    @staticmethod
    def _get_missing_guide(provider: str) -> dict:
        """Get onboarding guide for a provider."""
        guide = PROVIDER_GUIDES.get(provider.lower())
        if not guide:
            return {
                "name": provider,
                "apply_url": None,
                "guide": "请查阅该 provider 的官方文档获取 API Key。",
                "env_var": None,
            }
        return guide

    def _resolve_env_vars(self, data):
        """Recursively resolve ${ENV_VAR} syntax in dict/list/str."""
        if isinstance(data, dict):
            return {k: self._resolve_env_vars(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._resolve_env_vars(v) for v in data]
        elif isinstance(data, str):
            match = self.ENV_VAR_PATTERN.match(data)
            if match:
                env_var = match.group(1)
                env_value = os.environ.get(env_var, "")
                return env_value
            return data
        return data

    @staticmethod
    def _parse_model_config(config: Optional[dict]) -> Optional[ModelConfig]:
        """Parse a single model config dict."""
        if not config:
            return None
        return ModelConfig(
            provider=config.get("provider", ""),
            model=config.get("model", ""),
            api_key=config.get("apiKey", ""),
            base_url=config.get("baseUrl"),
        )

    @staticmethod
    def format_missing_guide(missing: list[dict]) -> str:
        """Format missing model guides into user-friendly message."""
        if not missing:
            return ""

        lines = ["=" * 50, "检测到以下 API Key 未配置", "=" * 50, ""]

        for item in missing:
            guide = item["guide"]
            lines.append(f"\n【{guide['name']}】- 用于 {item['type']} 生成")
            if guide["apply_url"]:
                lines.append(f"申请地址: {guide['apply_url']}")
            lines.append("配置步骤:")
            lines.append(guide["guide"])
            if guide["env_var"]:
                lines.append(f"环境变量名: {guide['env_var']}")
            lines.append("")

        lines.extend([
            "=" * 50,
            "配置完成后，请告诉我\"已配置\"，我会继续执行。",
            "=" * 50,
        ])

        return "\n".join(lines)
