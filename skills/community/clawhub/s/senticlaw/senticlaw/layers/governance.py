"""Layer 4 — Runtime Governance."""
import time, hashlib
from collections import defaultdict, deque
from ..models import LayerResult, RiskLevel


class GovernanceEngine:
    def __init__(self, config):
        self._minute:  dict[str, deque] = defaultdict(deque)
        self._hour:    dict[str, deque] = defaultdict(deque)
        self._history: dict[str, deque] = defaultdict(deque)
        self.cfg = config

    def check(self, text: str, sender_id: str, session_id: str) -> LayerResult:
        now = time.time()

        # Volume limits
        while self._minute[sender_id] and self._minute[sender_id][0] < now - 60:
            self._minute[sender_id].popleft()
        while self._hour[sender_id] and self._hour[sender_id][0] < now - 3600:
            self._hour[sender_id].popleft()

        if len(self._minute[sender_id]) >= self.cfg.max_messages_per_minute:
            return LayerResult(layer="governance", passed=False, risk_level=RiskLevel.MEDIUM,
                               block_message=f"Rate limit: max {self.cfg.max_messages_per_minute} messages/minute")
        if len(self._hour[sender_id]) >= self.cfg.max_messages_per_hour:
            return LayerResult(layer="governance", passed=False, risk_level=RiskLevel.MEDIUM,
                               block_message=f"Rate limit: max {self.cfg.max_messages_per_hour} messages/hour")

        self._minute[sender_id].append(now)
        self._hour[sender_id].append(now)

        # Loop detection
        hist = self._history[session_id]
        fp = hashlib.md5(" ".join(text.lower().split())[:200].encode()).hexdigest()
        while hist and hist[0][0] < now - self.cfg.loop_window_seconds:
            hist.popleft()
        count = sum(1 for _, h in hist if h == fp)
        hist.append((now, fp))

        if count >= self.cfg.loop_threshold - 1:
            return LayerResult(layer="governance", passed=False, risk_level=RiskLevel.MEDIUM,
                               block_message=f"Loop detected: same message sent {count+1} times",
                               details={"loop_count": count + 1})

        return LayerResult(layer="governance", passed=True, risk_level=RiskLevel.SAFE)
