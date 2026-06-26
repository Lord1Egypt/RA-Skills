import logging
import os
from typing import Union
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


def setup_logging(level: Union[str, int, None] = None) -> None:
    """初始化项目日志配置

    Args:
        level: 日志级别，支持 "DEBUG"/"INFO"/"WARNING"/"ERROR" 或 logging 常量。
               默认从环境变量 LOG_LEVEL 读取，未设置时默认 INFO。
    """
    if level is None:
        level = os.getenv("LOG_LEVEL", "INFO")
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-5s [%(name)s] %(message)s",
        datefmt="%H:%M:%S",
    )


@dataclass
class SkillConfig:
    llm_base_url: str = field(default_factory=lambda: os.getenv("LLM_BASE_URL", "https://api.deepseek.com/v1"))
    llm_api_key: str = field(default_factory=lambda: os.getenv("LLM_API_KEY", ""))
    llm_model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", "deepseek-chat"))

    serpapi_key: str = field(default_factory=lambda: os.getenv("SERPAPI_KEY", ""))
    tavily_key: str = field(default_factory=lambda: os.getenv("TAVILY_KEY", ""))
    brave_key: str = field(default_factory=lambda: os.getenv("BRAVE_KEY", ""))
    bocha_key: str = field(default_factory=lambda: os.getenv("BOCHA_KEY", ""))

    mx_apikey: str = field(default_factory=lambda: os.getenv("MX_APIKEY", ""))

    bias_threshold: float = field(default_factory=lambda: float(os.getenv("BIAS_THRESHOLD", "5.0")))
    news_max_age_days: int = field(default_factory=lambda: int(os.getenv("NEWS_MAX_AGE_DAYS", "3")))
    enable_chip: bool = field(default_factory=lambda: os.getenv("ENABLE_CHIP", "true").lower() == "true")

    @property
    def has_search_engine(self) -> bool:
        return bool(self.serpapi_key or self.tavily_key or self.brave_key or self.bocha_key)

    def validate(self) -> list[str]:
        errors = []
        if not self.llm_api_key:
            errors.append("LLM_API_KEY 未配置")
        if not self.llm_base_url:
            errors.append("LLM_BASE_URL 未配置")
        if not self.llm_model:
            errors.append("LLM_MODEL 未配置")
        return errors
