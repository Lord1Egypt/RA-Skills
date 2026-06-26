"""
配置加载器 - 从 config.yaml 读取，支持环境变量覆盖
"""

import os
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class WeComConfig:
    bot_id: str = ""
    bot_secret: str = ""
    ws_url: str = "wss://openws.work.weixin.qq.com"
    ping_interval: int = 30
    reconnect_max: int = 10


@dataclass
class AgentConfig:
    endpoint: str = "http://localhost:3000/chat"
    timeout: int = 30
    retry: int = 3


@dataclass
class ConnectorConfig:
    host: str = "127.0.0.1"
    port: int = 9527
    log_level: str = "INFO"
    log_file: str = ""


@dataclass
class P2PConfig:
    enabled: bool = False
    signaling_server: str = ""
    pair_code: str = ""


@dataclass
class Config:
    wecom: WeComConfig = field(default_factory=WeComConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)
    connector: ConnectorConfig = field(default_factory=ConnectorConfig)
    p2p: P2PConfig = field(default_factory=P2PConfig)


def load_config(path: Optional[str] = None) -> Config:
    """加载配置，优先级：环境变量 > config.yaml > 默认值"""
    if path is None:
        path = Path(__file__).parent / "config.yaml"

    data = {}
    if Path(path).exists():
        with open(path) as f:
            data = yaml.safe_load(f) or {}

    config = Config()

    # WeCom
    w = data.get("wecom", {})
    config.wecom.bot_id = os.getenv("WECOM_BOT_ID", w.get("bot_id", ""))
    config.wecom.bot_secret = os.getenv("WECOM_BOT_SECRET", w.get("bot_secret", ""))
    config.wecom.ws_url = os.getenv("WECOM_WS_URL", w.get("ws_url", "wss://openws.work.weixin.qq.com"))
    config.wecom.ping_interval = int(os.getenv("WECOM_PING_INTERVAL", w.get("ping_interval", 30)))
    config.wecom.reconnect_max = int(os.getenv("WECOM_RECONNECT_MAX", w.get("reconnect_max", 10)))

    # Agent
    a = data.get("agent", {})
    config.agent.endpoint = os.getenv("AGENT_ENDPOINT", a.get("endpoint", "http://localhost:3000/chat"))
    config.agent.timeout = int(os.getenv("AGENT_TIMEOUT", a.get("timeout", 30)))
    config.agent.retry = int(os.getenv("AGENT_RETRY", a.get("retry", 3)))

    # Connector
    c = data.get("connector", {})
    config.connector.host = os.getenv("CONNECTOR_HOST", c.get("host", "127.0.0.1"))
    config.connector.port = int(os.getenv("CONNECTOR_PORT", c.get("port", 9527)))
    config.connector.log_level = os.getenv("CONNECTOR_LOG_LEVEL", c.get("log_level", "INFO"))
    config.connector.log_file = os.getenv("CONNECTOR_LOG_FILE", c.get("log_file", ""))

    # P2P
    p = data.get("p2p", {})
    config.p2p.enabled = os.getenv("P2P_ENABLED", str(p.get("enabled", False))).lower() == "true"
    config.p2p.signaling_server = os.getenv("P2P_SIGNALING", p.get("signaling_server", ""))
    config.p2p.pair_code = os.getenv("P2P_PAIR_CODE", p.get("pair_code", ""))

    return config


def validate_config(config: Config) -> list[str]:
    """验证配置，返回错误列表。空列表 = 配置正确"""
    errors = []
    if not config.wecom.bot_id:
        errors.append("wecom.bot_id 未配置")
    if not config.wecom.bot_secret:
        errors.append("wecom.bot_secret 未配置")
    if not config.agent.endpoint:
        errors.append("agent.endpoint 未配置")
    return errors
