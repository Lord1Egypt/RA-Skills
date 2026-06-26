"""
spirit/proactive_delivery.py — Proactive Memory Delivery & Spirit Pulse

The butler proactively pushes relevant memories to Agents
when it detects they might need them for their current task.
Also implements the Spirit Pulse notification system for
real-time proactive notifications (knowledge gaps, contradictions, etc.).
"""

from __future__ import annotations

import collections
import logging
import time
import uuid
from dataclasses import dataclass
from typing import Any, Callable

logger = logging.getLogger(__name__)


@dataclass
class DeliverySuggestion:
    """A suggested memory delivery to an Agent."""
    agent_id: str
    memory_id: str
    reason: str
    relevance_score: float = 0.0
    delivered: bool = False


class ProactiveDelivery:
    """Proactively deliver memories to Agents based on context.

    The butler monitors Agent activity and suggests relevant memories
    that the Agent might not know about.

    Also implements the Spirit Pulse notification system:
    - Subscribers (e.g. WebSocket connections) receive real-time notifications
    - Recent pulses are stored in a bounded deque for polling
    - Health checks generate proactive notifications

    NOTE: This is NOT a background push system. The check_and_deliver()
    method must be called periodically (e.g., by Spirit's daily check
    or by an external scheduler) to deliver proactive messages.
    """

    def __init__(self, memory=None, store=None, agent_manager=None, spirit=None):
        self.memory = memory
        self.store = store
        self.agent_manager = agent_manager
        self.spirit = spirit
        self._delivery_log: dict[str, float] = {}  # agent_id -> last_delivery_time
        self._min_delivery_interval: float = 300.0  # 5 minutes between deliveries

        # Spirit Pulse infrastructure
        self._subscribers: list[Callable] = []  # callback functions for pulse notifications
        self._pulse_queue: collections.deque = collections.deque(maxlen=100)  # recent pulses

    # ── Spirit Pulse API ─────────────────────────────────────

    def subscribe(self, callback: Callable) -> None:
        """Register a callback for pulse notifications.

        Args:
            callback: A callable that accepts a single dict argument (the pulse).
        """
        self._subscribers.append(callback)

    def unsubscribe(self, callback: Callable) -> None:
        """Remove a previously registered callback."""
        try:
            self._subscribers.remove(callback)
        except ValueError:
            pass

    def deliver(self, notification: dict) -> dict:
        """Deliver a proactive notification to all subscribers.

        Args:
            notification: Dict with keys: type, title, message, action (optional).

        Returns:
            The pulse dict that was delivered (with id and timestamp added).
        """
        pulse = {
            "id": str(uuid.uuid4()),
            "type": notification.get("type", "info"),
            "title": notification.get("title", ""),
            "message": notification.get("message", ""),
            "timestamp": time.time(),
            "action": notification.get("action"),
        }
        self._pulse_queue.append(pulse)

        # Notify all subscribers
        dead = []
        for callback in self._subscribers:
            try:
                callback(pulse)
            except Exception:
                dead.append(callback)
        for cb in dead:
            try:
                self._subscribers.remove(cb)
            except ValueError:
                pass

        logger.info("Spirit Pulse: [%s] %s", pulse["type"], pulse["title"])
        return pulse

    def get_recent_pulses(self, limit: int = 10) -> list[dict]:
        """Get recent pulse notifications.

        Args:
            limit: Maximum number of pulses to return.

        Returns:
            List of pulse dicts, most recent last.
        """
        items = list(self._pulse_queue)
        return items[-limit:] if items else []

    def check_and_deliver(self) -> list[dict]:
        """Run health checks and deliver proactive notifications.

        Checks for:
        1. Knowledge gaps (via motivation engine)
        2. Memory contradictions (via self-healing)
        3. Stale memories (via decay analysis)
        4. PII risks (via privacy guard)
        5. Health issues (via Spirit health checker)

        Returns:
            List of pulse dicts that were delivered.
        """
        notifications = []

        # 1. Check for knowledge gaps
        try:
            motivation = getattr(self.memory, 'motivation', None)
            if motivation is not None and hasattr(motivation, 'detect_knowledge_gaps'):
                gaps = motivation.detect_knowledge_gaps()
                if gaps:
                    top_gaps = gaps[:3] if isinstance(gaps, list) else [gaps]
                    for gap in top_gaps:
                        notifications.append({
                            "type": "knowledge_gap",
                            "title": "Knowledge Gap Detected",
                            "message": str(gap)[:200] if gap else "",
                        })
        except Exception as e:
            logger.debug("Knowledge gap check failed: %s", e)

        # 2. Check for memory contradictions
        try:
            if self.memory is not None and hasattr(self.memory, 'self_healing'):
                heal_result = self.memory.self_healing.check_contradictions()
                contradictions = heal_result.get("contradictions", []) if isinstance(heal_result, dict) else []
                if contradictions:
                    for c in contradictions[:2]:
                        notifications.append({
                            "type": "contradiction",
                            "title": "Memory Contradiction Found",
                            "message": str(c)[:200],
                        })
        except Exception as e:
            logger.debug("Contradiction check failed: %s", e)

        # 3. Check for stale memories
        try:
            if self.memory is not None and hasattr(self.memory, 'decay'):
                decay_result = self.memory.decay.analyze_all()
                needs_action = decay_result.get("needs_action", []) if isinstance(decay_result, dict) else []
                if needs_action:
                    count = len(needs_action)
                    notifications.append({
                        "type": "stale_memory",
                        "title": f"{count} Stale Memories Need Attention",
                        "message": f"{count} memories have decayed below threshold and may need refresh or archival.",
                    })
        except Exception as e:
            logger.debug("Stale memory check failed: %s", e)

        # 4. Check for PII risks
        try:
            if self.store is not None and hasattr(self.store, 'query'):
                recent = self.store.query(limit=10)
                for mem in recent:
                    if isinstance(mem, dict) and mem.get("pii_detected"):
                        notifications.append({
                            "type": "pii_risk",
                            "title": "PII Risk in Memory",
                            "message": f"Memory {mem.get('memory_id', '?')} contains PII data.",
                        })
                        break  # Only notify once per check
        except Exception as e:
            logger.debug("PII risk check failed: %s", e)

        # 5. Check Spirit health
        try:
            if self.spirit is not None and hasattr(self.spirit, 'health'):
                report = self.spirit.health.check()
                if report and hasattr(report, 'issues') and report.issues:
                    worst = report.issues[0]
                    notifications.append({
                        "type": "health_alert",
                        "title": f"Health Alert: {worst.category}",
                        "message": worst.description if hasattr(worst, 'description') else str(worst),
                    })
        except Exception as e:
            logger.debug("Spirit health check failed: %s", e)

        # Deliver all notifications
        delivered = []
        for n in notifications:
            pulse = self.deliver(n)
            delivered.append(pulse)

        return delivered

    # ── Legacy Agent delivery API ────────────────────────────

    def check_and_suggest(self, agent_id: str,
                          current_task: str | None = None) -> list[DeliverySuggestion]:
        """Check if there are memories to proactively deliver to an Agent.

        Args:
            agent_id: The target Agent
            current_task: Optional description of the Agent's current task

        Returns:
            List of DeliverySuggestions
        """
        suggestions = []

        # Rate limit: don't deliver too frequently
        last_delivery = self._delivery_log.get(agent_id, 0)
        if time.time() - last_delivery < self._min_delivery_interval:
            return suggestions

        if not current_task or not self.memory:
            return suggestions

        try:
            # Search for relevant memories
            results = self.memory.recall(query=current_task, top_k=5)
            if not results:
                return suggestions

            # Convert results to suggestions
            if isinstance(results, dict):
                for mid, mem in results.items():
                    if isinstance(mem, dict):
                        suggestions.append(DeliverySuggestion(
                            agent_id=agent_id,
                            memory_id=mid,
                            reason=f"Relevant to task: {current_task[:50]}",
                            relevance_score=0.7,
                        ))
            elif isinstance(results, list):
                for mem in results[:5]:
                    if isinstance(mem, dict):
                        suggestions.append(DeliverySuggestion(
                            agent_id=agent_id,
                            memory_id=mem.get("id", ""),
                            reason=f"Relevant to task: {current_task[:50]}",
                            relevance_score=0.7,
                        ))

        except Exception as e:
            logger.warning("Proactive delivery check failed: %s", e)

        return suggestions

    def deliver_suggestion(self, suggestion: DeliverySuggestion) -> bool:
        """Deliver a memory suggestion to an Agent.

        In a real implementation, this would push to the Agent's
        message queue or callback. For now, it logs the delivery
        and notifies Spirit Pulse subscribers.
        """
        suggestion.delivered = True
        self._delivery_log[suggestion.agent_id] = time.time()

        # Also deliver as a Spirit Pulse notification
        self.deliver({
            "type": "proactive_delivery",
            "title": "Proactive Memory Delivery",
            "message": f"Memory {suggestion.memory_id} → Agent {suggestion.agent_id}: {suggestion.reason}",
        })

        logger.info("Proactive delivery: memory %s → agent %s (%s)",
                    suggestion.memory_id, suggestion.agent_id, suggestion.reason)
        return True

    def get_recent_deliveries(self, agent_id: str | None = None) -> list[dict]:
        """Get recent delivery history."""
        if agent_id:
            ts = self._delivery_log.get(agent_id, 0)
            return [{"agent_id": agent_id, "last_delivery": ts}] if ts else []
        return [{"agent_id": aid, "last_delivery": ts}
                for aid, ts in self._delivery_log.items()]
