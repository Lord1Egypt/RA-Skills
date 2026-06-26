"""
Proxy Gateway - 统一配置管理
使用 Pydantic Settings 进行类型安全的配置管理
"""

from typing import List, Optional
from functools import lru_cache
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Proxy Gateway 配置"""
    
    # 应用信息
    APP_NAME: str = "Proxy Gateway"
    APP_VERSION: str = "0.3.0"
    APP_DESCRIPTION: str = "HTTP API forwarding service for AI agents"
    
    # 网络配置
    NETWORK: str = Field(default="testnet", description="Network: mainnet or testnet")
    CHAIN_ID: int = Field(default=80001, description="Polygon chain ID")
    RPC_URL: str = Field(default="https://rpc-mumbai.maticvigil.com")
    EXPLORER_URL: str = Field(default="https://mumbai.polygonscan.com")
    
    # 区块链配置
    USDC_CONTRACT: str = Field(default="0xe11A86849d99F524cAC3E7A0Ec1241828e332C62")
    HOSTED_WALLET: Optional[str] = Field(default=None, description="Platform hosted wallet address (required for mainnet)")
    
    # 服务配置
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    DEBUG: bool = False
    
    # 安全配置
    ADMIN_TOKEN: Optional[str] = Field(default=None, description="Admin token for testnet operations")
    CORS_ORIGINS: str = Field(default="*", description="Comma-separated CORS origins")
    
    # Redis 配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    # 功能配置
    FREE_TRIAL_ENABLED: bool = True
    FREE_TRIAL_LIMIT: int = 10
    COST_PER_REQUEST: float = 0.001
    
    # x402 配置
    X402_CHAIN: str = Field(default="base", description="Blockchain network: base, base-sepolia, polygon")
    DEVELOPER_WALLET: Optional[str] = Field(default=None, description="Developer wallet address to receive payments")
    
    # 代理配置
    CLASH_HTTP_PORT: int = 7890
    CLASH_MIXED_PORT: int = 7893
    CLASH_API_PORT: int = 9090
    
    # 数据库配置 (可选)
    DATABASE_URL: Optional[str] = Field(default=None, description="PostgreSQL database URL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    @field_validator("NETWORK")
    @classmethod
    def validate_network(cls, v: str) -> str:
        if v not in ("mainnet", "testnet"):
            raise ValueError("NETWORK must be 'mainnet' or 'testnet'")
        return v
    
    @property
    def is_testnet(self) -> bool:
        return self.NETWORK == "testnet"
    
    @property
    def is_mainnet(self) -> bool:
        return self.NETWORK == "mainnet"
    
    @property
    def cors_origins_list(self) -> List[str]:
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()
