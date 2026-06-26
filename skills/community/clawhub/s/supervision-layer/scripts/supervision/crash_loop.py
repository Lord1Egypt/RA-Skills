"""
Crash Loop Protection — P0 Security

Track subagent/worker restart count. After N restarts (default 3),
mark permanently failed. Prevents infinite restart loops burning resources.
"""

import json
import time
import logging
import os
from dataclasses import dataclass, field, asdict
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)

DEFAULT_MAX_RESTARTS = 3
DEFAULT_CRASH_WINDOW = 3600  # 1 hour — only count crashes within this window

# Default state file location — uses SUPERVISION_WORKSPACE or falls back to ~/.openclaw/workspace
DEFAULT_STATE_DIR = os.path.join(
    os.environ.get("SUPERVISION_WORKSPACE", os.path.expanduser("~/.openclaw/workspace")),
    "logs"
)
DEFAULT_STATE_FILE = "crash-loop-state.json"


@dataclass
class CrashRecord:
    """Record of a single crash event."""
    timestamp: float
    agent_id: str
    session_id: str
    task_name: Optional[str] = None
    error: Optional[str] = None


@dataclass 
class AgentCrashState:
    """Crash state for a single agent."""
    agent_id: str
    crash_count: int = 0
    crashes: List[Dict] = field(default_factory=list)  # Recent crash records
    permanently_failed: bool = False
    first_crash: Optional[float] = None
    last_crash: Optional[float] = None


class CrashLoopProtector:
    """
    Track subagent/worker restart count and prevent infinite crash loops.
    
    After N crashes within a time window, mark the agent as permanently failed.
    This prevents runaway workers from burning resources.
    
    Usage:
        protector = get_crash_loop_protector()
        
        # Before spawning a worker
        if protector.is_permanently_failed("worker-1"):
            logger.error("Worker-1 is in crash loop — skipping dispatch")
            return
        
        # After a worker crashes
        protector.record_crash(
            agent_id="worker-1",
            session_id="abc123",
            task_name="build-timeouts",
            error="Process exited with code 1"
        )
        
        # Check crash count
        state = protector.get_state("worker-1")
        print(f"Worker-1 has crashed {state.crash_count} times")
    """
    
    def __init__(
        self,
        max_restarts: int = DEFAULT_MAX_RESTARTS,
        crash_window: float = DEFAULT_CRASH_WINDOW,
        state_file: Optional[str] = None,
    ):
        self.max_restarts = max_restarts
        self.crash_window = crash_window
        self.state_file = state_file or os.path.join(DEFAULT_STATE_DIR, DEFAULT_STATE_FILE)
        self.agents: Dict[str, AgentCrashState] = {}
        self._ensure_dir()
        self._load_state()
    
    def _ensure_dir(self) -> None:
        """Ensure state directory exists."""
        state_dir = os.path.dirname(self.state_file)
        if state_dir:
            os.makedirs(state_dir, exist_ok=True)
    
    def _load_state(self) -> None:
        """Load crash state from disk."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    data = json.load(f)
                for agent_id, agent_data in data.get("agents", {}).items():
                    self.agents[agent_id] = AgentCrashState(
                        agent_id=agent_id,
                        crash_count=agent_data.get("crash_count", 0),
                        crashes=agent_data.get("crashes", []),
                        permanently_failed=agent_data.get("permanently_failed", False),
                        first_crash=agent_data.get("first_crash"),
                        last_crash=agent_data.get("last_crash"),
                    )
                logger.info(f"Loaded crash state for {len(self.agents)} agents")
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to load crash state: {e}")
                self.agents = {}
    
    def _save_state(self) -> None:
        """Save crash state to disk."""
        data = {
            "max_restarts": self.max_restarts,
            "crash_window": self.crash_window,
            "agents": {}
        }
        for agent_id, state in self.agents.items():
            data["agents"][agent_id] = {
                "crash_count": state.crash_count,
                "crashes": state.crashes[-20:],  # Keep last 20
                "permanently_failed": state.permanently_failed,
                "first_crash": state.first_crash,
                "last_crash": state.last_crash,
            }
        
        try:
            with open(self.state_file, "w") as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            logger.error(f"Failed to save crash state: {e}")
    
    def _prune_old_crashes(self, agent_id: str) -> None:
        """Remove crash records outside the time window."""
        if agent_id not in self.agents:
            return
        
        now = time.time()
        state = self.agents[agent_id]
        
        # Filter crashes within window
        recent_crashes = [
            c for c in state.crashes
            if now - c.get("timestamp", 0) < self.crash_window
        ]
        
        state.crashes = recent_crashes
        state.crash_count = len(recent_crashes)
    
    def record_crash(
        self,
        agent_id: str,
        session_id: str,
        task_name: Optional[str] = None,
        error: Optional[str] = None,
    ) -> AgentCrashState:
        """
        Record a worker crash.
        
        Args:
            agent_id: Agent/worker identifier
            session_id: Session that crashed
            task_name: Task name if available
            error: Error message
        
        Returns:
            Updated AgentCrashState
        """
        now = time.time()
        
        if agent_id not in self.agents:
            self.agents[agent_id] = AgentCrashState(agent_id=agent_id)
        
        state = self.agents[agent_id]
        
        # Add crash record
        crash_record = {
            "timestamp": now,
            "session_id": session_id,
            "task_name": task_name,
            "error": error,
        }
        state.crashes.append(crash_record)
        state.last_crash = now
        if state.first_crash is None:
            state.first_crash = now
        
        # Prune old crashes
        self._prune_old_crashes(agent_id)
        state.crash_count = len(state.crashes)
        
        # Check if crash loop threshold reached
        if state.crash_count >= self.max_restarts:
            state.permanently_failed = True
            logger.error(
                f"Agent {agent_id} has crashed {state.crash_count} times "
                f"within {self.crash_window}s — marking as permanently failed"
            )
        else:
            logger.warning(
                f"Agent {agent_id} crashed ({state.crash_count}/{self.max_restarts} "
                f"within window) — {error or 'unknown error'}"
            )
        
        self._save_state()
        return state
    
    def is_permanently_failed(self, agent_id: str) -> bool:
        """Check if an agent is in a crash loop (permanently failed)."""
        if agent_id not in self.agents:
            return False
        
        self._prune_old_crashes(agent_id)
        return self.agents[agent_id].permanently_failed
    
    def can_restart(self, agent_id: str) -> bool:
        """Check if an agent can be restarted (not in crash loop)."""
        return not self.is_permanently_failed(agent_id)
    
    def get_remaining_restarts(self, agent_id: str) -> int:
        """Get number of remaining restarts before crash loop protection kicks in."""
        if agent_id not in self.agents:
            return self.max_restarts
        
        self._prune_old_crashes(agent_id)
        state = self.agents[agent_id]
        return max(0, self.max_restarts - state.crash_count)
    
    def reset(self, agent_id: str) -> None:
        """Manually reset crash state for an agent (e.g., after fixing the issue)."""
        if agent_id in self.agents:
            self.agents[agent_id] = AgentCrashState(agent_id=agent_id)
            self._save_state()
            logger.info(f"Crash state reset for agent {agent_id}")
    
    def get_state(self, agent_id: str) -> AgentCrashState:
        """Get crash state for an agent."""
        if agent_id not in self.agents:
            return AgentCrashState(agent_id=agent_id)
        self._prune_old_crashes(agent_id)
        return self.agents[agent_id]
    
    def get_all_states(self) -> Dict[str, AgentCrashState]:
        """Get crash states for all agents."""
        for agent_id in list(self.agents.keys()):
            self._prune_old_crashes(agent_id)
        return dict(self.agents)
    
    def get_config(self) -> Dict:
        """Get current configuration."""
        return {
            "max_restarts": self.max_restarts,
            "crash_window_seconds": self.crash_window,
        }


# Global singleton
_crash_loop_protector: Optional[CrashLoopProtector] = None

def get_crash_loop_protector() -> CrashLoopProtector:
    """Get or create the global crash loop protector."""
    global _crash_loop_protector
    if _crash_loop_protector is None:
        _crash_loop_protector = CrashLoopProtector()
    return _crash_loop_protector