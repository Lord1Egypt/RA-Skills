"""
Per-Call Audit Logging — P0 Security

Structured JSON events for every tool call.
Writes to JSONL file, queryable via API.
Foundation for observability, replay, and debugging.
"""

import json
import time
import uuid
import logging
import os
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)

# Default audit log location — uses SUPERVISION_WORKSPACE or falls back to ~/.openclaw/workspace
DEFAULT_AUDIT_DIR = os.path.join(
    os.environ.get("SUPERVISION_WORKSPACE", os.path.expanduser("~/.openclaw/workspace")),
    "logs"
)
DEFAULT_AUDIT_FILE = "tool-audit.jsonl"


@dataclass
class AuditEntry:
    """Structured audit entry for a single tool call."""
    timestamp: float
    request_id: str
    session_id: str
    agent_id: str
    tool: str
    phase: str  # "pre", "execute", "post", "timeout", "circuit_open", "error"
    outcome: str  # "success", "failure", "timeout", "circuit_open", "error", "blocked"
    duration_ms: float = 0.0
    tokens_used: int = 0
    estimated_cost_usd: float = 0.0
    error: Optional[str] = None
    args_summary: Optional[str] = None  # Truncated args for audit (no PII)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_json(self) -> str:
        return json.dumps(asdict(self), default=str)


class AuditLogger:
    """
    Per-call audit logger. Writes structured JSONL events.
    
    Usage:
        audit = get_audit_logger()
        entry = audit.log(
            tool="web_search",
            agent_id="worker-1",
            session_id="abc123",
            outcome="success",
            duration_ms=450,
            phase="execute"
        )
    """
    
    def __init__(
        self,
        audit_file: Optional[str] = None,
        max_args_length: int = 100,
        rotate_size_mb: float = 50.0,
    ):
        self.audit_file = audit_file or os.path.join(DEFAULT_AUDIT_DIR, DEFAULT_AUDIT_FILE)
        self.max_args_length = max_args_length
        self.rotate_size_mb = rotate_size_mb
        self._ensure_dir()
    
    def _ensure_dir(self) -> None:
        """Ensure audit log directory exists."""
        audit_dir = os.path.dirname(self.audit_file)
        if audit_dir:
            os.makedirs(audit_dir, exist_ok=True)
    
    def _truncate_args(self, args: Any) -> Optional[str]:
        """Truncate args for audit log, stripping PII-prone values."""
        if args is None:
            return None
        s = str(args)
        if len(s) > self.max_args_length:
            return s[:self.max_args_length] + "..."
        return s
    
    def _should_rotate(self) -> bool:
        """Check if audit log needs rotation."""
        if not os.path.exists(self.audit_file):
            return False
        size_mb = os.path.getsize(self.audit_file) / (1024 * 1024)
        return size_mb >= self.rotate_size_mb
    
    def _rotate(self) -> None:
        """Rotate audit log file."""
        import shutil
        backup = self.audit_file + ".1"
        if os.path.exists(backup):
            os.remove(backup)
        if os.path.exists(self.audit_file):
            shutil.move(self.audit_file, backup)
        logger.info(f"Rotated audit log to {backup}")
    
    def log(
        self,
        tool: str,
        agent_id: str,
        session_id: str,
        outcome: str,
        phase: str = "execute",
        duration_ms: float = 0.0,
        tokens_used: int = 0,
        estimated_cost_usd: float = 0.0,
        error: Optional[str] = None,
        args: Any = None,
        metadata: Optional[Dict] = None,
    ) -> AuditEntry:
        """
        Log a tool call audit entry.
        
        Args:
            tool: Tool name (e.g., "web_search", "exec")
            agent_id: Agent/worker that made the call
            session_id: Session identifier
            outcome: One of "success", "failure", "timeout", "circuit_open", "error", "blocked"
            phase: Phase of execution ("pre", "execute", "post", etc.)
            duration_ms: Duration in milliseconds
            tokens_used: Token count if applicable
            estimated_cost_usd: Estimated cost in USD
            error: Error message if applicable
            args: Tool arguments (will be truncated, no PII)
            metadata: Additional metadata dict
        
        Returns:
            AuditEntry that was logged
        """
        entry = AuditEntry(
            timestamp=time.time(),
            request_id=str(uuid.uuid4()),
            session_id=session_id,
            agent_id=agent_id,
            tool=tool,
            phase=phase,
            outcome=outcome,
            duration_ms=round(duration_ms, 2),
            tokens_used=tokens_used,
            estimated_cost_usd=round(estimated_cost_usd, 6),
            error=error,
            args_summary=self._truncate_args(args),
            metadata=metadata or {},
        )
        
        try:
            if self._should_rotate():
                self._rotate()
            
            with open(self.audit_file, "a") as f:
                f.write(entry.to_json() + "\n")
        except IOError as e:
            logger.error(f"Failed to write audit log: {e}")
        
        return entry
    
    def query(
        self,
        tool: Optional[str] = None,
        agent_id: Optional[str] = None,
        session_id: Optional[str] = None,
        outcome: Optional[str] = None,
        since: Optional[float] = None,
        limit: int = 100,
    ) -> List[AuditEntry]:
        """
        Query audit log entries.
        
        Args:
            tool: Filter by tool name
            agent_id: Filter by agent
            session_id: Filter by session
            outcome: Filter by outcome
            since: Filter by timestamp (Unix epoch)
            limit: Max entries to return
        
        Returns:
            List of matching AuditEntry objects
        """
        entries = []
        
        if not os.path.exists(self.audit_file):
            return entries
        
        try:
            with open(self.audit_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        entry = AuditEntry(
                            timestamp=data.get("timestamp", 0),
                            request_id=data.get("request_id", ""),
                            session_id=data.get("session_id", ""),
                            agent_id=data.get("agent_id", ""),
                            tool=data.get("tool", ""),
                            phase=data.get("phase", ""),
                            outcome=data.get("outcome", ""),
                            duration_ms=data.get("duration_ms", 0),
                            tokens_used=data.get("tokens_used", 0),
                            estimated_cost_usd=data.get("estimated_cost_usd", 0),
                            error=data.get("error"),
                            args_summary=data.get("args_summary"),
                            metadata=data.get("metadata", {}),
                        )
                        
                        # Apply filters
                        if tool and entry.tool != tool:
                            continue
                        if agent_id and entry.agent_id != agent_id:
                            continue
                        if session_id and entry.session_id != session_id:
                            continue
                        if outcome and entry.outcome != outcome:
                            continue
                        if since and entry.timestamp < since:
                            continue
                        
                        entries.append(entry)
                        
                        if len(entries) >= limit:
                            break
                    except json.JSONDecodeError:
                        continue
        except IOError:
            pass
        
        return entries
    
    def get_stats(self, since: Optional[float] = None) -> Dict[str, Dict]:
        """
        Get aggregate statistics from audit log.
        
        Returns:
            Dict mapping tool names to their call statistics
        """
        stats: Dict[str, Dict] = {}
        
        entries = self.query(since=since, limit=10000)
        
        for entry in entries:
            tool = entry.tool
            if tool not in stats:
                stats[tool] = {
                    "calls": 0,
                    "successes": 0,
                    "failures": 0,
                    "timeouts": 0,
                    "circuit_opens": 0,
                    "blocked": 0,
                    "total_duration_ms": 0.0,
                    "total_tokens": 0,
                    "total_cost_usd": 0.0,
                }
            
            s = stats[tool]
            s["calls"] += 1
            s["total_duration_ms"] += entry.duration_ms
            s["total_tokens"] += entry.tokens_used
            s["total_cost_usd"] += entry.estimated_cost_usd
            
            if entry.outcome == "success":
                s["successes"] += 1
            elif entry.outcome == "failure":
                s["failures"] += 1
            elif entry.outcome == "timeout":
                s["timeouts"] += 1
            elif entry.outcome == "circuit_open":
                s["circuit_opens"] += 1
            elif entry.outcome == "blocked":
                s["blocked"] += 1
        
        # Compute averages
        for tool, s in stats.items():
            if s["calls"] > 0:
                s["avg_duration_ms"] = round(s["total_duration_ms"] / s["calls"], 1)
                s["success_rate"] = round(s["successes"] / s["calls"], 3)
            else:
                s["avg_duration_ms"] = 0
                s["success_rate"] = 0
        
        return stats


# Global singleton
_audit_logger: Optional[AuditLogger] = None

def get_audit_logger() -> AuditLogger:
    """Get or create the global audit logger."""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger