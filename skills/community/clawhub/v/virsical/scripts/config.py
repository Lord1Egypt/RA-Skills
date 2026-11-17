"""
Virsical 配置管理模块。

负责管理 Virsical API 的配置信息。
"""

import os


def _load_env():
    """从 virsical.env 加载配置，不存在则使用默认值。"""
    env = {}
    env_file = os.path.join(os.path.dirname(__file__), "virsical.env")
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    env[key.strip()] = value.strip().strip('"').strip("'")
    return env


_env = _load_env()

# 优先从 virsical.env 读取，不存在则使用默认值
DEFAULT_BASE_URL = _env.get(
    "VIRSICAL_BASE_URL", "https://cloud.virsical.cn"
)
DEFAULT_AGENT_AUTH_BASE_URL = _env.get(
    "VIRSICAL_AGENT_AUTH_BASE_URL", DEFAULT_BASE_URL
)


class VirsicalConfig:
    """Virsical 配置管理器。

    使用固定默认值，无需从环境变量或文件加载配置。
    """

    def __init__(self):
        """初始化配置 - 使用固定默认值。"""
        pass

    @property
    def base_url(self) -> str:
        """Base URL，固定默认值。"""
        return DEFAULT_BASE_URL

    @property
    def agent_auth_base_url(self) -> str:
        """Agent 认证服务地址，固定默认值。"""
        return DEFAULT_AGENT_AUTH_BASE_URL

    @property
    def agent_auth_token(self) -> str:
        """Agent 授权令牌 - 未使用，保留空值。"""
        return ""

    @property
    def has_agent_auth_token(self) -> bool:
        """是否配置了 agent 授权令牌 - 始终返回 False。"""
        return False

    @property
    def is_configured(self) -> bool:
        """检查配置是否完整 - 始终返回 True。"""
        return True

    @property
    def has_custom_base_url(self) -> bool:
        """是否配置了自定义 base_url - 始终返回 False。"""
        return False

    def to_dict(self) -> dict:
        """返回配置的字典表示。"""
        return {
            "base_url": self.base_url,
            "agent_auth_base_url": self.agent_auth_base_url,
            "agent_auth_token": "",
            "is_configured": self.is_configured,
        }

    def save(self):
        """保存配置 - 空实现，无需保存。"""
        pass

    def update(self, base_url: str = "", agent_auth_base_url: str = "", agent_auth_token: str = ""):
        """更新配置 - 空实现，不允许更新。"""
        pass

    def validate(self) -> list:
        """验证配置完整性 - 始终返回空列表。"""
        return []


# 全局配置实例（惰性初始化）
_config: VirsicalConfig = None


def get_config(env_path: str = None) -> VirsicalConfig:
    """获取全局配置实例。

    Args:
        env_path: 已废弃，保留参数兼容性

    Returns:
        VirsicalConfig 实例
    """
    global _config
    if _config is None:
        _config = VirsicalConfig()
    return _config


def reset_config():
    """重置全局配置实例缓存。"""
    global _config
    _config = None


if __name__ == "__main__":
    cfg = get_config()
    print(f"Base URL: {cfg.base_url}")
    print(f"Configured: {cfg.is_configured}")
