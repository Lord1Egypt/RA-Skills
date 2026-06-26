"""
Supervision Layer — P0 Security Package

All-in-one supervision for tool execution.
Wraps every tool call with timeouts, circuit breakers, audit logging,
and crash loop protection.

Usage:
    from supervision import get_supervisor
    result = await get_supervisor().execute("web_fetch", fn, agent_id="worker", session_id="s1")
"""

from .timeout import TimeoutWrapper, TimeoutResult, get_timeout_wrapper, DEFAULT_TIMEOUTS
from .circuit_breaker import CircuitBreaker, CircuitState, get_circuit_breaker
from .audit import AuditLogger, AuditEntry, get_audit_logger
from .crash_loop import CrashLoopProtector, AgentCrashState, get_crash_loop_protector

import asyncio
import time
import logging
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger(__name__)


class SupervisedCall:
    """
    A single supervised tool call that goes through all protection layers:
    1. Crash loop check — is the agent allowed to restart?
    2. Circuit breaker — is the tool healthy enough to call?
    3. Audit log (pre) — record the attempt
    4. Timeout — wrap the call in a timeout
    5. Circuit breaker (post) — record success or failure
    6. Audit log (post) — record the result
    """
    
    def __init__(
        self,
        audit_file: Optional[str] = None,
        crash_state_file: Optional[str] = None,
        failure_threshold: int = 5,
        reset_after: float = 60.0,
        max_restarts: int = 3,
        crash_window: float = 3600.0,
        custom_timeouts: Optional[Dict[str, float]] = None,
    ):
        self.timeout = TimeoutWrapper(custom_timeouts=custom_timeouts)
        self.circuit = CircuitBreaker(failure_threshold=failure_threshold, reset_after=reset_after)
        self.audit = AuditLogger(audit_file=audit_file)
        self.crash = CrashLoopProtector(max_restarts=max_restarts, crash_window=crash_window, state_file=crash_state_file)
    
    async def execute(
        self,
        tool: str,
        fn: Callable,
        agent_id: str,
        session_id: str,
        task_name: Optional[str] = None,
        timeout_override: Optional[float] = None,
        args_summary: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute a tool call with full supervision.
        
        Returns a dict with:
            success: bool
            output: Any (if successful)
            error: str (if failed)
            timed_out: bool
            circuit_open: bool
            duration_ms: float
            audit_id: str (request_id from audit log)
        """
        # 1. Crash loop check
        if not self.crash.can_restart(agent_id):
            error_msg = f"Agent {agent_id} is in crash loop — skipping dispatch"
            logger.error(error_msg)
            self.audit.log(
                tool=tool, agent_id=agent_id, session_id=session_id,
                outcome="blocked", phase="pre", error=error_msg,
                args=args_summary, metadata={"reason": "crash_loop"}
            )
            return {
                "success": False, "error": error_msg,
                "circuit_open": False, "timed_out": False,
                "duration_ms": 0, "audit_id": ""
            }
        
        # 2. Circuit breaker check
        if not await self.circuit.can_call(tool):
            error_msg = f"Circuit breaker OPEN for {tool} — call rejected"
            logger.warning(error_msg)
            await self.circuit.record_rejection(tool)
            self.audit.log(
                tool=tool, agent_id=agent_id, session_id=session_id,
                outcome="circuit_open", phase="pre", error=error_msg,
                args=args_summary, metadata={"reason": "circuit_breaker"}
            )
            return {
                "success": False, "error": error_msg,
                "circuit_open": True, "timed_out": False,
                "duration_ms": 0, "audit_id": ""
            }
        
        # 3. Audit log (pre)
        pre_entry = self.audit.log(
            tool=tool, agent_id=agent_id, session_id=session_id,
            outcome="attempt", phase="pre", args=args_summary,
            metadata={"task_name": task_name} if task_name else {}
        )
        
        # 4. Execute with timeout
        result = await self.timeout.call(
            tool, fn, timeout=timeout_override, **kwargs
        )
        
        # 5. Circuit breaker (post)
        if result.succeeded:
            await self.circuit.record_success(tool)
        elif result.timed_out:
            await self.circuit.record_failure(tool)
        else:
            await self.circuit.record_failure(tool)
        
        # 6. Audit log (post)
        outcome = "success" if result.succeeded else (
            "timeout" if result.timed_out else "failure"
        )
        self.audit.log(
            tool=tool, agent_id=agent_id, session_id=session_id,
            outcome=outcome, phase="post",
            duration_ms=result.duration_ms,
            error=result.error, args=args_summary,
        )
        
        # Record crash if failed
        if not result.succeeded:
            self.crash.record_crash(
                agent_id=agent_id, session_id=session_id,
                task_name=task_name, error=result.error
            )
        
        return {
            "success": result.succeeded,
            "output": result.output,
            "error": result.error,
            "timed_out": result.timed_out,
            "circuit_open": False,
            "duration_ms": result.duration_ms,
            "audit_id": pre_entry.request_id,
        }
    
    def get_all_status(self) -> Dict[str, Dict]:
        """Get combined status from all supervision layers."""
        return {
            "timeouts": self.timeout.get_stats(),
            "circuits": self.circuit.get_status(),
            "crash_loops": {
                agent_id: {
                    "crash_count": state.crash_count,
                    "permanently_failed": state.permanently_failed,
                    "remaining_restarts": self.crash.get_remaining_restarts(agent_id),
                    "last_crash": state.last_crash,
                }
                for agent_id, state in self.crash.get_all_states().items()
            },
            "audit_stats": self.audit.get_stats(),
        }


# Global singleton
_supervisor: Optional[SupervisedCall] = None

def get_supervisor(**kwargs) -> SupervisedCall:
    """Get or create the global supervised call handler."""
    global _supervisor
    if _supervisor is None:
        _supervisor = SupervisedCall(**kwargs)
    return _supervisor


__all__ = [
    "TimeoutWrapper", "TimeoutResult", "get_timeout_wrapper", "DEFAULT_TIMEOUTS",
    "CircuitBreaker", "CircuitState", "get_circuit_breaker",
    "AuditLogger", "AuditEntry", "get_audit_logger",
    "CrashLoopProtector", "AgentCrashState", "get_crash_loop_protector",
    "SupervisedCall", "get_supervisor",
]