import asyncio
import json
import os
import logging
import redis.asyncio as redis
import redis.exceptions as redis_ex
from typing import Dict, Callable, Any, Optional, List
import yaml
from .permissions import check_permission

logger = logging.getLogger("taichi.bus")


class CentralizedBus:
    """
    Centralized Redis-based message bus.
    Each subscriber (Agent/Worker) gets its own pubsub connection.
    """

    def __init__(self, redis_url: str, permissions_config: str):
        self.redis_url = redis_url
        self.redis_client: Optional[redis.Redis] = None
        self.pubsub_connections: Dict[str, Any] = {}
        self.permissions = self._load_permissions(permissions_config)
        self.handlers: Dict[str, Callable] = {}
        self._debug = os.environ.get("TAICHI_DEBUG", "").lower() in ("1", "true", "yes")

    def _load_permissions(self, path: str) -> List[Dict]:
        with open(path) as f:
            return yaml.safe_load(f).get("rules", [])

    async def connect(self):
        self.redis_client = await redis.from_url(self.redis_url, decode_responses=True)

    async def publish(self, to: str, message: Dict[str, Any]):
        """Publish a message to a specific agent's channel."""
        msg_type = message.get("type")
        from_agent = message.get("from", "unknown")

        if not check_permission(self.permissions, from_agent, to, msg_type):
            raise PermissionError(f"{from_agent} -> {to} ({msg_type}): permission denied")

        channel = f"agent.{to}"
        if self._debug:
            logger.debug(f"[publish] {from_agent} -> {channel}: {msg_type}")
        try:
            await self.redis_client.publish(channel, json.dumps(message))
        except redis_ex.ConnectionError as e:
            logger.warning(f"[publish] Redis connection error: {e}")

    async def subscribe(self, agent_name: str, handler: Callable):
        """
        Subscribe to messages for a specific agent.
        Creates a dedicated pubsub connection per agent.
        """
        pubsub = self.redis_client.pubsub()
        await pubsub.subscribe(f"agent.{agent_name}")
        self.pubsub_connections[agent_name] = pubsub
        self.handlers[agent_name] = handler
        asyncio.create_task(self._listen(pubsub, agent_name, handler))

    async def _listen(self, pubsub, agent_name: str, handler: Callable):
        """Listen for messages on a pubsub connection."""
        try:
            async for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        data = json.loads(message["data"])
                        if self._debug:
                            logger.debug(f"[recv] {agent_name}: {data.get('type')}")
                        await handler(data)
                    except Exception as e:
                        logger.exception(f"[handler] {agent_name} error")
        except (asyncio.CancelledError, ConnectionError, redis_ex.ConnectionError):
            pass
        except Exception as e:
            logger.exception(f"[listener] {agent_name} error")
        finally:
            try:
                await pubsub.unsubscribe(f"agent.{agent_name}")
                await pubsub.aclose()
            except Exception:
                pass

    async def close(self):
        """Close all pubsub connections."""
        for pubsub in self.pubsub_connections.values():
            try:
                await pubsub.unsubscribe()
                await pubsub.aclose()
            except Exception:
                pass
        if self.redis_client:
            await self.redis_client.aclose()
