from __future__ import annotations

import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict, DotEnvSettingsSource


class Settings(BaseSettings):
    """小笨羊高考Skill配置"""
    
    model_config = SettingsConfigDict(
        env_prefix="XBY_GAOKAO_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # API配置
    base_url: str = "https://mcp.xiaobenyang.com"
    mcp_id: str = "1820705335657482"
    api_key: str = ""
    
    # 超时和重试配置
    timeout_seconds: float = 30.0
    max_retries: int = 2
    
    # 数据配置
    default_year: int = 2025

    def model_post_init(self, __context):
        # 强制从 .env 文件读取 XBY_APIKEY
        env_path = Path(".env")
        if env_path.exists():
            content = env_path.read_text(encoding="utf-8")
            for line in content.splitlines():
                if line.startswith("XBY_APIKEY="):
                    self.api_key = line.split("=", 1)[1].strip()
                    break
        # 如果环境变量有值，覆盖 .env 的值
        env_val = os.getenv("XBY_APIKEY", "")
        if env_val:
            self.api_key = env_val


def save_api_key_to_env(api_key: str) -> bool:
    """将API key保存到.env文件"""
    try:
        env_path = Path(".env")
        lines = []
        if env_path.exists():
            lines = env_path.read_text(encoding="utf-8").splitlines()
        found = False
        new_lines = []
        for line in lines:
            if line.startswith("XBY_APIKEY="):
                new_lines.append(f"XBY_APIKEY={api_key}")
                found = True
            else:
                new_lines.append(line)
        if not found:
            new_lines.append(f"XBY_APIKEY={api_key}")
        env_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        os.environ["XBY_APIKEY"] = api_key
        return True
    except Exception as e:
        print(f"保存API key失败: {e}")
        return False


def set_api_key(api_key: str) -> bool:
    """设置API key并持久化到.env"""
    if not api_key or not api_key.strip():
        return False
    api_key = api_key.strip()
    if not save_api_key_to_env(api_key):
        return False
    # 更新全局 settings 实例
    settings.api_key = api_key
    return True


def get_api_key() -> str:
    """获取当前API key"""
    # 优先从 settings 实例获取（已读取 .env）
    if settings.api_key:
        return settings.api_key
    # 备选：从环境变量读取
    return os.getenv("XBY_APIKEY", "")


# 全局settings实例
settings = Settings()
