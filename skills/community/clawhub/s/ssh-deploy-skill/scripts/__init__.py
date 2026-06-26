"""SSH Deploy Skill - 通用 SSH 远程部署工具"""

__version__ = "1.0.0"
__author__ = "OpenClaw"

from .inventory import Inventory, Server
from .deploy import SSHDeployer, DeployResult
from .templates import get_template, list_available_templates, get_mirror_config

__all__ = [
    "Inventory",
    "Server",
    "SSHDeployer",
    "DeployResult",
    "get_template",
    "list_available_templates",
    "get_mirror_config",
]
