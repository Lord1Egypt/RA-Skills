"""
Swarm Coordinator - 智进化小队协调器
轻量级Pub/Sub协调器，基于Redis或内存队列
"""

__version__ = "1.1.0"
__author__ = "智进化小队"
__description__ = "多Agent协同工作流协调器"

# Keep protocol imports lightweight. Optional integrations such as Redis Pub/Sub
# should not break schema/protocol validation tests when their dependencies are
# not installed.
from .swarm_protocol import SwarmProtocol

try:  # optional: requires redis
    from .pubsub import PubSubCoordinator
except ModuleNotFoundError:  # pragma: no cover - environment dependent
    PubSubCoordinator = None

try:
    from .token_budget import TokenBudgetManager
except ModuleNotFoundError:  # pragma: no cover
    TokenBudgetManager = None

try:
    from .agent_manager import AgentManager
except ModuleNotFoundError:  # pragma: no cover
    AgentManager = None

try:
    from .negotiation import NegotiationProtocol
except (ModuleNotFoundError, SyntaxError):  # pragma: no cover
    NegotiationProtocol = None

__all__ = [
    "PubSubCoordinator",
    "TokenBudgetManager",
    "SwarmProtocol",
    "AgentManager",
    "NegotiationProtocol",
]