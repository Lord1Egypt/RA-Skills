"""配置管理模块"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from wiz_logging import get_logger

logger = get_logger()


class Config:
    """为知笔记 MCP 配置类"""

    def __init__(self, user_id: str, password: str, base_url: str,
                 group_name: str = None, kb_guid: str = None):
        self.user_id = user_id
        self.password = password
        self.base_url = base_url.rstrip('/')
        self.group_name = group_name or ""
        self.kb_guid = kb_guid or ""

        # as_url 和 kb_server 都使用统一的 base_url
        self.as_url = self.base_url
        self.kb_server = self.base_url

    @classmethod
    def load(cls, env_path: str = None):
        """
        加载配置
        1. 若项目根目录存在 .env，则 load_dotenv
        2. 校验 WIZ_USER_ID/WIZ_PASSWORD/WIZ_BASE_URL 必填
        3. kb_guid 若包含 "://" 视为误填，置空
        """
        # 确定项目根目录
        if env_path:
            project_root = Path(env_path).parent
        else:
            project_root = Path(__file__).parent.parent

        dotenv_path = project_root / ".env"

        if dotenv_path.exists():
            load_dotenv(dotenv_path)
            logger.info(f"已加载 .env 文件: {dotenv_path}")

        # 读取必填配置
        user_id = os.getenv("WIZ_USER_ID")
        password = os.getenv("WIZ_PASSWORD")
        base_url = os.getenv("WIZ_BASE_URL")

        # 校验必填字段
        if not user_id:
            raise ValueError("WIZ_USER_ID 是必填配置项")
        if not password:
            raise ValueError("WIZ_PASSWORD 是必填配置项")
        if not base_url:
            raise ValueError("WIZ_BASE_URL 是必填配置项")

        # 读取可选配置
        group_name = os.getenv("WIZ_GROUP_NAME")
        kb_guid = os.getenv("WIZ_KB_GUID")

        # kb_guid 若包含 "://" 视为误填，置空
        if kb_guid and "://" in kb_guid:
            logger.warning(f"WIZ_KB_GUID 包含 '://'，视为误填，将置空: {kb_guid}")
            kb_guid = ""

        return cls(user_id, password, base_url, group_name, kb_guid)


def get_config(env_path: str = None) -> Config:
    """获取配置单例"""
    global _config
    if _config is None:
        _config = Config.load(env_path)
    return _config


_config = None
