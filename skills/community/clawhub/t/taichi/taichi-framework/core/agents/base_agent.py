import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

from core.communication.centralized_bus import CentralizedBus


class BaseAgent:
    """
    Base class for all agents.
    Provides message handling and sending via the CentralizedBus.
    """

    def __init__(self, name: str, bus: CentralizedBus, config: dict):
        self.name = name
        self.bus = bus
        self.config = config
        self._running = True

    async def start(self):
        """Subscribe to the bus for incoming messages."""
        await self.bus.subscribe(self.name, self.handle_message)

    async def handle_message(self, message: dict):
        """
        Handle an incoming message. Override in subclass.
        """
        raise NotImplementedError

    async def send(
        self,
        to: str,
        msg_type: str,
        payload: dict,
        correlation_id: Optional[str] = None,
        from_: Optional[str] = None,
    ):
        """Send a message to another agent via the bus."""
        msg = {
            "id": uuid.uuid4().hex,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "from": from_ or self.name,
            "to": to,
            "type": msg_type,
            "correlation_id": correlation_id,
            "payload": payload,
        }
        await self.bus.publish(to, msg)

    async def stop(self):
        self._running = False
