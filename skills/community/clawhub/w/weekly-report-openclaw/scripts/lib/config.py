"""Configuration management for weekly report skill."""

import os
from pathlib import Path
from typing import Literal, Optional, List

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SystemConfig(BaseModel):
    """System configuration."""

    base_url: str = Field(default="http://120.210.237.117:7006/hap", description="Base URL of the weekly report system")
    account_id: str = Field(default="a0aadd3f-2d30-4dcd-b901-8cf689c59dc3", description="Account ID for API requests")


class ApiConfig(BaseModel):
    """API configuration."""

    worksheet_id: str = Field(default="64b4912b881be8545d91a689", description="Worksheet ID for data fetching")
    app_id: str = Field(default="355690a6-f48c-4373-8a55-465bee680f30", description="Application ID")
    view_id: str = Field(default="64b4912cda6eba1005393603", description="View ID")
    report_page_url: str = Field(default="/worksheet/{worksheet_id}", description="Report page URL template")


class LoginConfig(BaseModel):
    """Login configuration."""

    headless: bool = Field(default=False, description="Run browser in headless mode")
    timeout: int = Field(default=300, description="Login timeout in seconds")
    login_url: str = Field(default="/login", description="Login page path")


class LLMConfig(BaseModel):
    """LLM configuration."""

    provider: Literal["deepseek", "openai"] = Field(default="deepseek", description="LLM provider")
    model: str = Field(default="deepseek-chat", description="Model name")
    base_url: str = Field(default="https://api.deepseek.com/v1", description="API base URL")
    max_tokens: int = Field(default=4000, description="Maximum tokens in response")
    temperature: float = Field(default=0.7, description="Temperature for generation")


class DefaultsConfig(BaseModel):
    """Default values configuration."""

    team: str = Field(default="科创研发组", description="Default team name")
    template_path: str = Field(default="template.docx", description="Template file path")
    output_dir: str = Field(default="output", description="Output directory")
    team_members: List[str] = Field(
        default=["杨浩然", "张勇", "李楠", "赵超", "陶荣鑫", "殷晨晨", "朱达贤"],
        description="List of team members to include in reports"
    )


class Settings(BaseSettings):
    """Main settings class."""

    model_config = SettingsConfigDict(
        env_prefix="WEEKLY_REPORT_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Environment variables
    username: Optional[str] = Field(default=None, description="Login username")
    password: Optional[str] = Field(default=None, description="Login password")

    # API keys
    deepseek_api_key: Optional[str] = Field(
        default=None,
        alias="DEEPSEEK_API_KEY",
        description="DeepSeek API key"
    )
    openai_api_key: Optional[str] = Field(
        default=None,
        alias="OPENAI_API_KEY",
        description="OpenAI API key"
    )

    # Configuration sections
    system: SystemConfig = Field(default_factory=SystemConfig)
    api: ApiConfig = Field(default_factory=ApiConfig)
    login: LoginConfig = Field(default_factory=LoginConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    defaults: DefaultsConfig = Field(default_factory=DefaultsConfig)

    @classmethod
    def from_yaml(cls, config_path: str | Path = None) -> "Settings":
        """Load settings from YAML file and merge with environment variables."""
        if config_path is None:
            # Try default locations
            candidates = [
                Path.cwd() / "config" / "settings.yaml",
                Path(__file__).parent.parent.parent / "config" / "settings.yaml",
                Path.cwd() / "settings.yaml",
            ]
            for candidate in candidates:
                if candidate.exists():
                    config_path = candidate
                    break

        if config_path is None or not Path(config_path).exists():
            return cls()

        with open(config_path, encoding="utf-8") as f:
            config_data = yaml.safe_load(f) or {}

        return cls(**config_data)

    def get_api_key(self) -> str:
        """Get the appropriate API key based on provider."""
        # First try environment variable directly
        if self.llm.provider == "deepseek":
            key = self.deepseek_api_key or os.environ.get("DEEPSEEK_API_KEY")
            if not key:
                raise ValueError("DEEPSEEK_API_KEY is not set in environment variables")
            return key
        elif self.llm.provider == "openai":
            key = self.openai_api_key or os.environ.get("OPENAI_API_KEY")
            if not key:
                raise ValueError("OPENAI_API_KEY is not set in environment variables")
            return key
        else:
            raise ValueError(f"Unknown LLM provider: {self.llm.provider}")

    def get_template_path(self) -> Path:
        """Get the absolute path to the template file."""
        template_path = Path(self.defaults.template_path)
        if not template_path.is_absolute():
            # Try multiple locations
            if template_path.exists():
                return template_path.resolve()
            # Try assets directory
            assets_path = Path(__file__).parent.parent / "assets" / self.defaults.template_path
            if assets_path.exists():
                return assets_path
            # Try current directory
            cwd_path = Path.cwd() / self.defaults.template_path
            if cwd_path.exists():
                return cwd_path
        return template_path

    def get_output_dir(self) -> Path:
        """Get the output directory path, creating it if necessary."""
        output_dir = Path(self.defaults.output_dir)
        if not output_dir.is_absolute():
            output_dir = Path.cwd() / self.defaults.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir
