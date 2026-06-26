import asyncio
import json
import logging
from typing import Dict, Callable, Any, Optional

import redis.asyncio as redis

logger = logging.getLogger("taichi.distbus")


class DistributedBus:
    """
    Worker-to-Worker and Worker-to-Orchestrator communication via Redis Pub/Sub.
    Each worker has its own pubsub connection for receiving messages.
    """

    def __init__(self, redis_url: str, worker_id: str):
        self.redis_url = redis_url
        self.worker_id = worker_id
        self.redis_client: Optional[redis.Redis] = None
        self.pubsub: Optional[redis.client.PubSub] = None
        self.handlers: Dict[str, Callable] = {}
        self._running = True

    async def connect(self):
        self.redis_client = await redis.from_url(self.redis_url, decode_responses=True)
        self.pubsub = self.redis_client.pubsub()
        # Subscribe to own channel + broadcast channel
        await self.pubsub.subscribe(f"worker.{self.worker_id}", "worker.broadcast")
        asyncio.create_task(self._listen())

    async def send_to(self, target_worker_id: str, msg_type: str, payload: Any, correlation_id: str = None):
        """Send a direct message to another worker."""
        import uuid
        msg = {
            "from": self.worker_id,
            "to": target_worker_id,
            "type": msg_type,
            "payload": payload,
            "correlation_id": correlation_id or uuid.uuid4().hex,
        }
        await self.redis_client.publish(f"worker.{target_worker_id}", json.dumps(msg))

    async def broadcast(self, msg_type: str, payload: Any, correlation_id: str = None):
        """Broadcast a message to all workers."""
        import uuid
        msg = {
            "from": self.worker_id,
            "to": "*",
            "type": msg_type,
            "payload": payload,
            "correlation_id": correlation_id or uuid.uuid4().hex,
        }
        await self.redis_client.publish("worker.broadcast", json.dumps(msg))

    async def register_handler(self, msg_type: str, handler: Callable):
        self.handlers[msg_type] = handler

    async def _listen(self):
        """Listen for incoming messages."""
        try:
            async for message in self.pubsub.listen():
                if message["type"] == "message":
                    try:
                        data = json.loads(message["data"])
                        handler = self.handlers.get(data.get("type"))
                        if handler:
                            await handler(data)
                    except Exception as e:
                        logger.exception(f"Handler error for {self.worker_id}: {e}")
        except (asyncio.CancelledError, ConnectionError):
            pass
        except Exception as e:
            logger.error(f"Listener error for {self.worker_id}: {e}")
        finally:
            try:
                await self.pubsub.unsubscribe()
                await self.pubsub.aclose()
            except Exception:
                pass

    async def close(self):
        self._running = False
        if self.pubsub:
            try:
                await self.pubsub.unsubscribe()
                await self.pubsub.aclose()
            except Exception:
                pass
        if self.redis_client:
            await self.redis_client.aclose()
