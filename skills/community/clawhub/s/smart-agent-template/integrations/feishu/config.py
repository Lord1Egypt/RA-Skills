"""
飞书 Bot 配置管理
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class FeishuConfig:
    """飞书 Bot 配置"""
    app_id: str
    app_secret: str
    verification_token: str
    encrypt_key: Optional[str] = None
    port: int = 8080


@dataclass
class AIConfig:
    """AI 引擎配置"""
    engine: str  # openai, claude, deepseek, ollama
    api_key: Optional[str] = None
    model: str = "gpt-4"
    base_url: Optional[str] = None


class Config:
    """配置管理器"""
    
    def __init__(self):
        self.feishu = FeishuConfig(
            app_id=os.getenv('FEISHU_APP_ID', ''),
            app_secret=os.getenv('FEISHU_APP_SECRET', ''),
            verification_token=os.getenv('FEISHU_VERIFICATION_TOKEN', ''),
            encrypt_key=os.getenv('FEISHU_ENCRYPT_KEY'),
            port=int(os.getenv('FEISHU_PORT', '8080'))
        )
        
        self.ai = AIConfig(
            engine=os.getenv('AI_ENGINE', 'openai'),
            api_key=os.getenv(f"{os.getenv('AI_ENGINE', 'openai').upper()}_API_KEY"),
            model=os.getenv(f"{os.getenv('AI_ENGINE', 'openai').upper()}_MODEL", 'gpt-4'),
            base_url=os.getenv(f"{os.getenv('AI_ENGINE', 'openai').upper()}_BASE_URL")
        )
    
    def validate(self) -> bool:
        """验证配置"""
        if not self.feishu.app_id:
            raise ValueError("FEISHU_APP_ID is required")
        
        if not self.feishu.app_secret:
            raise ValueError("FEISHU_APP_SECRET is required")
        
        # VERIFICATION_TOKEN 可选（留空时跳过验证，仅用于测试）
        # if not self.feishu.verification_token:
        #     raise ValueError("FEISHU_VERIFICATION_TOKEN is required")
        
        if self.ai.engine not in ['openai', 'claude', 'deepseek', 'ollama']:
            raise ValueError(f"Unsupported AI engine: {self.ai.engine}")
        
        return True


# 全局配置实例
config = Config()
