"""
配置管理 - 支持多账号
"""

import os
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel
from pydantic_settings import BaseSettings


def is_openclaw_env() -> bool:
    """检测是否在 openclaw 环境中运行"""
    openclaw_dir = Path.home() / ".openclaw"
    return openclaw_dir.exists() and openclaw_dir.is_dir()


def load_openclaw_env() -> dict[str, str]:
    """从 ~/.openclaw/.env 加载环境变量"""
    env_file = Path.home() / ".openclaw" / ".env"
    env_vars = {}
    if env_file.exists():
        with open(env_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if "=" in line:
                        key, value = line.split("=", 1)
                        env_vars[key.strip()] = value.strip()
    return env_vars


class WeChatAccount(BaseModel):
    """微信公众号账号配置"""
    name: str = "默认账号"
    app_id: str = ""
    app_secret: str = ""


class WeChatMultiConfig(BaseModel):
    """微信公众号多账号配置"""
    accounts: dict[str, WeChatAccount] = {}
    default_account: str = ""


class AIConfig(BaseModel):
    """AI 配置"""
    provider: str = "openai"
    api_key: str = ""
    base_url: str = ""
    model: str = ""


class Settings(BaseSettings):
    """应用配置"""

    # 配置文件路径
    config_dir: Path = Path.home() / ".wechat-publish-pro"

    # 平台配置（多账号）
    wechat: WeChatMultiConfig = WeChatMultiConfig()

    # AI 配置
    ai: AIConfig = AIConfig()

    class Config:
        env_prefix = "WECHAT_PUBLISHER_"
        env_nested_delimiter = "_"

    def get_config_file(self) -> Path:
        """获取配置文件路径"""
        return self.config_dir / "config.yaml"

    def load(self) -> None:
        """从文件和环境变量加载配置"""
        # 如果在 openclaw 环境中，先加载 ~/.openclaw/.env
        openclaw_env = {}
        if is_openclaw_env():
            openclaw_env = load_openclaw_env()

        # 先从配置文件加载
        config_file = self.get_config_file()
        if config_file.exists():
            with open(config_file, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                if "accounts" in data:
                    self.wechat.accounts = {
                        k: WeChatAccount(**v) for k, v in data["accounts"].items()
                    }
                if "default_account" in data:
                    self.wechat.default_account = data["default_account"]
                if "ai" in data:
                    self.ai = AIConfig(**data["ai"])

        # 环境变量覆盖（单个账号模式，用于兼容旧配置）
        wechat_app_id = openclaw_env.get("WECHAT_APP_ID") or os.environ.get("WECHAT_APP_ID")
        wechat_app_secret = openclaw_env.get("WECHAT_APP_SECRET") or os.environ.get("WECHAT_APP_SECRET")
        
        if wechat_app_id and wechat_app_secret:
            # 如果环境变量有配置，但配置文件没有账号，则添加到 default 账号
            if not self.wechat.accounts:
                self.wechat.accounts["default"] = WeChatAccount(
                    name="默认账号",
                    app_id=wechat_app_id,
                    app_secret=wechat_app_secret
                )
                self.wechat.default_account = "default"

        # AI 配置
        ai_provider = openclaw_env.get("AI_PROVIDER") or os.environ.get("AI_PROVIDER")
        if ai_provider is not None:
            self.ai.provider = ai_provider

        ai_api_key = openclaw_env.get("AI_API_KEY") or os.environ.get("AI_API_KEY")
        if ai_api_key is not None:
            self.ai.api_key = ai_api_key

        ai_base_url = openclaw_env.get("AI_BASE_URL") or os.environ.get("AI_BASE_URL")
        if ai_base_url is not None:
            self.ai.base_url = ai_base_url

        ai_model = openclaw_env.get("AI_MODEL") or os.environ.get("AI_MODEL")
        if ai_model is not None:
            self.ai.model = ai_model

    def save(self) -> None:
        """保存配置到文件"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        config_file = self.get_config_file()

        data = {
            "accounts": {k: v.model_dump() for k, v in self.wechat.accounts.items()},
            "default_account": self.wechat.default_account,
            "ai": self.ai.model_dump(),
        }

        with open(config_file, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

    def get_account_names(self) -> list[str]:
        """获取所有账号名称"""
        return list(self.wechat.accounts.keys())

    def get_default_account(self) -> Optional[str]:
        """获取默认账号"""
        if self.wechat.default_account and self.wechat.default_account in self.wechat.accounts:
            return self.wechat.default_account
        if self.wechat.accounts:
            return list(self.wechat.accounts.keys())[0]
        return None

    def get_account(self, key: str) -> Optional[WeChatAccount]:
        """获取指定账号"""
        return self.wechat.accounts.get(key)

    def is_wechat_configured(self) -> bool:
        """检查是否已配置至少一个账号"""
        return any(
            acc.app_id and acc.app_secret 
            for acc in self.wechat.accounts.values()
        )

    def is_ai_configured(self) -> bool:
        return bool(self.ai.api_key)

    def add_account(self, key: str, name: str, app_id: str, app_secret: str) -> None:
        """添加账号"""
        self.wechat.accounts[key] = WeChatAccount(
            name=name,
            app_id=app_id,
            app_secret=app_secret
        )
        if not self.wechat.default_account:
            self.wechat.default_account = key

    def remove_account(self, key: str) -> None:
        """删除账号"""
        if key in self.wechat.accounts:
            del self.wechat.accounts[key]
            if self.wechat.default_account == key:
                self.wechat.default_account = list(self.wechat.accounts.keys())[0] if self.wechat.accounts else ""

    def set_default_account(self, key: str) -> None:
        """设置默认账号"""
        if key in self.wechat.accounts:
            self.wechat.default_account = key


# 全局配置实例
settings = Settings()
