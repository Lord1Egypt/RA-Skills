"""
AgentScope股票诊断系统配置文件
使用 AgentScope 框架的标准模型配置
"""

import os
from dataclasses import dataclass, field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# AgentScope 相关导入（供外部模块使用）
from agentscope.model import OpenAIChatModel
from agentscope.formatter import OpenAIChatFormatter
from agentscope.memory import InMemoryMemory

# LLM API配置
LLM_API_KEY = {
    "bailian": os.getenv("ALIYUN_BAILIAN_API_KEY", "")
}

@dataclass
class Config:
    """系统配置"""
    
    # Tushare配置
    tushare_token: str = field(
        default_factory=lambda: os.getenv("TUSHARE_TOKEN", "")
    )
    
    # 阿里云百炼配置
    bailian_api_key: str = field(
        default_factory=lambda: os.getenv("ALIYUN_BAILIAN_API_KEY", "")
    )
    
    # 模型配置
    model_name: str = "qwen3.5-plus"  # 默认使用Qwen-Max
    temperature: float = 0.3
    
    # 支持的模型配置
    supported_models: dict = field(default_factory=lambda: {
        "kimi-k2.5": {
            "display_name": "Kimi",
            "model_name": "kimi-k2.5",
            "description": "月之暗面 Kimi 模型"
        },
        "qwen-max-2025-01-25": {
            "display_name": "Qwen-Max",
            "model_name": "qwen-max-2025-01-25",
            "description": "通义千问 Max 最新版本"
        },
        "qwen3.5-plus": {
            "display_name": "Qwen3.5",
            "model_name": "qwen3.5-plus",
            "description": "通义千问3.5 Plus"
        },
        "glm-5": {
            "display_name": "GLM5",
            "model_name": "glm-5",
            "description": "智谱 GLM5"
        },
        "MiniMax/MiniMax-M2.5": {
            "display_name": "Minimax",
            "model_name": "MiniMax/MiniMax-M2.5",
            "description": "Minimax M2.5"
        }
    })
    
    # 数据采集配置
    market_data_days: int = 60  # 获取近60个交易日数据
    news_days: int = 7  # 获取近7天新闻
    
    # 辩论/讨论配置
    debate_rounds: int = 2  # 研究员辩论轮数
    risk_discussion_rounds: int = 2  # 风控讨论轮数
    
    # 权重配置
    tech_weight: float = 0.25  # 技术面权重
    fund_weight: float = 0.35  # 基本面权重
    news_weight: float = 0.20  # 舆情面权重
    research_weight: float = 0.20  # 研究员共识权重
    
    def validate(self) -> bool:
        """验证配置完整性"""
        errors = []
        
        if not self.tushare_token:
            errors.append("缺少TUSHARE_TOKEN")
        
        if not self.bailian_api_key:
            errors.append("缺少ALIYUN_BAILIAN_API_KEY")
        
        if errors:
            print(f"配置验证失败: {', '.join(errors)}")
            return False
        
        return True


# 全局配置实例
config = Config()


def create_model(model_name: Optional[str] = None, stream: bool = True) -> OpenAIChatModel:
    """
    创建 AgentScope OpenAIChatModel 实例（通过百炼平台调用）
    
    Args:
        model_name: 模型名称，默认使用配置中的 model_name
        stream: 是否启用流式输出
        
    Returns:
        OpenAIChatModel 实例
    """
    actual_model_name = model_name or config.model_name
    
    # 验证模型是否支持
    if actual_model_name not in config.supported_models:
        print(f"警告: 不支持的模型 {actual_model_name}，将使用默认模型")
        actual_model_name = config.model_name
    
    return OpenAIChatModel(
        model_name=actual_model_name,
        api_key=LLM_API_KEY.get("bailian") or "",
        client_args={
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"
        },
        stream=stream,
    )


def create_formatter() -> OpenAIChatFormatter:
    """创建 AgentScope OpenAI 消息格式化器"""
    return OpenAIChatFormatter()


def create_memory() -> InMemoryMemory:
    """创建 AgentScope 内存实例"""
    return InMemoryMemory()
