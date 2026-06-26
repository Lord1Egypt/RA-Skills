"""
Tests for Supervision Layer — P0 Security

Tests all four P0 components:
1. Tool Call Timeouts
2. Circuit Breakers
3. Per-Call Audit Logging
4. Crash Loop Protection
5. Integrated SupervisedCall

Run: python -m pytest test_supervision.py -v
"""

import asyncio
import json
import os
import tempfile
import time
import pytest

# Import modules
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from supervision.timeout import TimeoutWrapper, TimeoutResult, DEFAULT_TIMEOUTS
from supervision.circuit_breaker import CircuitBreaker, CircuitState
from supervision.audit import AuditLogger, AuditEntry
from supervision.crash_loop import CrashLoopProtector, AgentCrashState
from supervision import SupervisedCall


# ============================================================
# 1. Timeout Tests
# ============================================================

class TestTimeoutWrapper:
    """Tests for tool call timeout wrapper."""
    
    @pytest.mark.asyncio
    async def test_successful_call(self):
        """Successful call completes within timeout."""
        wrapper = TimeoutWrapper()
        
        async def quick_fn(x):
            return f"result: {x}"
        
        result = await wrapper.call("test_tool", quick_fn, x="hello")
        assert result.succeeded is True
        assert result.output == "result: hello"
        assert result.timed_out is False
        assert result.duration_ms > 0
    
    @pytest.mark.asyncio
    async def test_timeout_occurs(self):
        """Call that exceeds timeout returns timed_out result."""
        wrapper = TimeoutWrapper(custom_timeouts={"slow_tool": 0.1})
        
        async def slow_fn():
            await asyncio.sleep(5)  # Way beyond timeout
        
        result = await wrapper.call("slow_tool", slow_fn)
        assert result.succeeded is False
        assert result.timed_out is True
        assert "Timeout" in result.error
    
    @pytest.mark.asyncio
    async def test_custom_timeout_override(self):
        """Per-call timeout override works."""
        wrapper = TimeoutWrapper()
        
        async def medium_fn():
            await asyncio.sleep(0.15)
            return "done"
        
        # Should succeed with 1s timeout
        result = await wrapper.call("medium_tool", medium_fn, timeout=1.0)
        assert result.succeeded is True
        
        # Should timeout with 0.05s timeout
        result2 = await wrapper.call("medium_tool", medium_fn, timeout=0.05)
        assert result2.succeeded is False
        assert result2.timed_out is True
    
    @pytest.mark.asyncio
    async def test_exception_handling(self):
        """Call that raises an exception returns error result."""
        wrapper = TimeoutWrapper()
        
        async def error_fn():
            raise ValueError("test error")
        
        result = await wrapper.call("error_tool", error_fn)
        assert result.succeeded is False
        assert result.timed_out is False
        assert "test error" in result.error
    
    @pytest.mark.asyncio
    async def test_default_timeouts_exist(self):
        """Default timeouts are set for common tools."""
        assert "exec" in DEFAULT_TIMEOUTS
        assert "web_fetch" in DEFAULT_TIMEOUTS
        assert DEFAULT_TIMEOUTS["exec"] > 0
    
    @pytest.mark.asyncio
    async def test_stats_tracking(self):
        """Stats are tracked for timeout monitoring."""
        wrapper = TimeoutWrapper()
        
        async def fn():
            return "ok"
        
        await wrapper.call("stat_tool", fn)
        await wrapper.call("stat_tool", fn)
        
        stats = wrapper.get_stats()
        assert "stat_tool" in stats
        assert stats["stat_tool"]["calls"] == 2
    
    @pytest.mark.asyncio
    async def test_set_timeout(self):
        """set_timeout overrides work."""
        wrapper = TimeoutWrapper()
        wrapper.set_timeout("custom_tool", 99.0)
        assert wrapper.get_timeout("custom_tool") == 99.0
    
    @pytest.mark.asyncio
    async def test_invalid_timeout(self):
        """Negative timeout raises ValueError."""
        wrapper = TimeoutWrapper()
        with pytest.raises(ValueError):
            wrapper.set_timeout("bad_tool", -1.0)


# ============================================================
# 2. Circuit Breaker Tests
# ============================================================

class TestCircuitBreaker:
    """Tests for per-tool circuit breaker."""
    
    @pytest.mark.asyncio
    async def test_starts_closed(self):
        """New circuit starts in CLOSED state."""
        cb = CircuitBreaker()
        circuit = cb._get_circuit("test_tool")
        assert circuit.state == CircuitState.CLOSED
    
    @pytest.mark.asyncio
    async def test_closed_allows_calls(self):
        """CLOSED state allows calls."""
        cb = CircuitBreaker()
        assert await cb.can_call("test_tool") is True
    
    @pytest.mark.asyncio
    async def test_opens_after_threshold(self):
        """Circuit opens after N consecutive failures."""
        cb = CircuitBreaker(failure_threshold=3)
        
        for i in range(3):
            await cb.record_failure("test_tool")
        
        state = cb._get_circuit("test_tool")
        assert state.state == CircuitState.OPEN
        assert await cb.can_call("test_tool") is False
    
    @pytest.mark.asyncio
    async def test_half_open_after_timeout(self):
        """Circuit transitions to HALF_OPEN after reset_after."""
        cb = CircuitBreaker(failure_threshold=2, reset_after=0.1)
        
        # Open the circuit
        await cb.record_failure("test_tool")
        await cb.record_failure("test_tool")
        assert cb._get_circuit("test_tool").state == CircuitState.OPEN
        
        # Wait for reset_after
        await asyncio.sleep(0.15)
        
        # Should transition to HALF_OPEN
        assert await cb.can_call("test_tool") is True
        assert cb._get_circuit("test_tool").state == CircuitState.HALF_OPEN
    
    @pytest.mark.asyncio
    async def test_half_open_to_closed_on_success(self):
        """HALF_OPEN transitions to CLOSED on success."""
        cb = CircuitBreaker(failure_threshold=2, reset_after=0.1)
        
        # Open the circuit
        await cb.record_failure("test_tool")
        await cb.record_failure("test_tool")
        
        # Wait for half-open
        await asyncio.sleep(0.15)
        await cb.can_call("test_tool")
        
        # Record success
        await cb.record_success("test_tool")
        assert cb._get_circuit("test_tool").state == CircuitState.CLOSED
    
    @pytest.mark.asyncio
    async def test_half_open_to_open_on_failure(self):
        """HALF_OPEN transitions back to OPEN on failure."""
        cb = CircuitBreaker(failure_threshold=2, reset_after=0.1)
        
        # Open the circuit
        await cb.record_failure("test_tool")
        await cb.record_failure("test_tool")
        
        # Wait for half-open
        await asyncio.sleep(0.15)
        await cb.can_call("test_tool")
        
        # Record failure
        await cb.record_failure("test_tool")
        assert cb._get_circuit("test_tool").state == CircuitState.OPEN
    
    @pytest.mark.asyncio
    async def test_manual_reset(self):
        """Manual reset closes an open circuit."""
        cb = CircuitBreaker(failure_threshold=2)
        
        await cb.record_failure("test_tool")
        await cb.record_failure("test_tool")
        assert cb._get_circuit("test_tool").state == CircuitState.OPEN
        
        await cb.reset("test_tool")
        assert cb._get_circuit("test_tool").state == CircuitState.CLOSED
    
    @pytest.mark.asyncio
    async def test_per_tool_isolation(self):
        """Different tools have independent circuits."""
        cb = CircuitBreaker(failure_threshold=2)
        
        await cb.record_failure("tool_a")
        await cb.record_failure("tool_a")
        
        # tool_a is open
        assert cb._get_circuit("tool_a").state == CircuitState.OPEN
        # tool_b is still closed
        assert cb._get_circuit("tool_b").state == CircuitState.CLOSED
    
    @pytest.mark.asyncio
    async def test_status_report(self):
        """get_status returns proper state information."""
        cb = CircuitBreaker(failure_threshold=3)
        await cb.record_failure("test_tool")
        
        status = cb.get_status()
        assert "test_tool" in status
        assert status["test_tool"]["consecutive_failures"] == 1


# ============================================================
# 3. Audit Logger Tests
# ============================================================

class TestAuditLogger:
    """Tests for per-call audit logging."""
    
    def test_log_entry(self):
        """Log entry is written to JSONL file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            audit_file = f.name
        
        try:
            audit = AuditLogger(audit_file=audit_file)
            entry = audit.log(
                tool="web_search",
                agent_id="mario",
                session_id="test-session-1",
                outcome="success",
                duration_ms=450.5,
                tokens_used=1500,
                estimated_cost_usd=0.003,
            )
            
            assert entry.tool == "web_search"
            assert entry.agent_id == "mario"
            assert entry.outcome == "success"
            assert entry.duration_ms == 450.5
            
            # Verify written to file
            with open(audit_file) as f:
                lines = f.readlines()
                assert len(lines) == 1
                data = json.loads(lines[0])
                assert data["tool"] == "web_search"
                assert data["outcome"] == "success"
        finally:
            os.unlink(audit_file)
    
    def test_query_by_tool(self):
        """Query filters by tool name."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            audit_file = f.name
        
        try:
            audit = AuditLogger(audit_file=audit_file)
            audit.log(tool="exec", agent_id="mario", session_id="s1", outcome="success")
            audit.log(tool="web_search", agent_id="lilo", session_id="s2", outcome="success")
            audit.log(tool="exec", agent_id="mario", session_id="s3", outcome="failure")
            
            results = audit.query(tool="exec")
            assert len(results) == 2
            assert all(r.tool == "exec" for r in results)
        finally:
            os.unlink(audit_file)
    
    def test_query_by_outcome(self):
        """Query filters by outcome."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            audit_file = f.name
        
        try:
            audit = AuditLogger(audit_file=audit_file)
            audit.log(tool="exec", agent_id="mario", session_id="s1", outcome="success")
            audit.log(tool="exec", agent_id="mario", session_id="s2", outcome="failure")
            audit.log(tool="exec", agent_id="mario", session_id="s3", outcome="success")
            
            results = audit.query(outcome="failure")
            assert len(results) == 1
            assert results[0].outcome == "failure"
        finally:
            os.unlink(audit_file)
    
    def test_stats_aggregation(self):
        """Stats are properly aggregated."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            audit_file = f.name
        
        try:
            audit = AuditLogger(audit_file=audit_file)
            audit.log(tool="exec", agent_id="mario", session_id="s1", outcome="success", duration_ms=100)
            audit.log(tool="exec", agent_id="mario", session_id="s2", outcome="failure", duration_ms=200)
            audit.log(tool="exec", agent_id="mario", session_id="s3", outcome="success", duration_ms=150)
            
            stats = audit.get_stats()
            assert "exec" in stats
            assert stats["exec"]["calls"] == 3
            assert stats["exec"]["successes"] == 2
            assert stats["exec"]["failures"] == 1
        finally:
            os.unlink(audit_file)
    
    def test_args_truncation(self):
        """Args are truncated to max length."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            audit_file = f.name
        
        try:
            audit = AuditLogger(audit_file=audit_file, max_args_length=20)
            entry = audit.log(
                tool="exec",
                agent_id="mario",
                session_id="s1",
                outcome="success",
                args="a" * 500,
            )
            assert len(entry.args_summary) <= 23  # 20 + "..."
        finally:
            os.unlink(audit_file)


# ============================================================
# 4. Crash Loop Protection Tests
# ============================================================

class TestCrashLoopProtector:
    """Tests for crash loop protection."""
    
    def test_initial_state(self):
        """New agent has no crash history."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            state_file = f.name
        
        try:
            protector = CrashLoopProtector(state_file=state_file)
            assert protector.can_restart("mario") is True
            assert protector.is_permanently_failed("mario") is False
            assert protector.get_remaining_restarts("mario") == 3  # default max_restarts
        finally:
            os.unlink(state_file)
    
    def test_record_crash(self):
        """Recording crashes increments count."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            state_file = f.name
        
        try:
            protector = CrashLoopProtector(state_file=state_file)
            state = protector.record_crash("mario", "session-1", "build-timeouts", "exit code 1")
            
            assert state.crash_count == 1
            assert state.permanently_failed is False
            assert protector.get_remaining_restarts("mario") == 2
        finally:
            os.unlink(state_file)
    
    def test_crash_loop_detected(self):
        """After max_restarts, agent is marked permanently failed."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            state_file = f.name
        
        try:
            protector = CrashLoopProtector(max_restarts=3, state_file=state_file)
            
            protector.record_crash("mario", "s1", error="crash 1")
            assert protector.can_restart("mario") is True
            
            protector.record_crash("mario", "s2", error="crash 2")
            assert protector.can_restart("mario") is True
            
            protector.record_crash("mario", "s3", error="crash 3")
            assert protector.is_permanently_failed("mario") is True
            assert protector.can_restart("mario") is False
            assert protector.get_remaining_restarts("mario") == 0
        finally:
            os.unlink(state_file)
    
    def test_manual_reset(self):
        """Manual reset clears crash state."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            state_file = f.name
        
        try:
            protector = CrashLoopProtector(max_restarts=2, state_file=state_file)
            protector.record_crash("mario", "s1", error="crash 1")
            protector.record_crash("mario", "s2", error="crash 2")
            assert protector.is_permanently_failed("mario") is True
            
            protector.reset("mario")
            assert protector.can_restart("mario") is True
            assert protector.get_remaining_restarts("mario") == 2
        finally:
            os.unlink(state_file)
    
    def test_state_persists(self):
        """Crash state persists to disk."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            state_file = f.name
        
        try:
            # Write state
            protector1 = CrashLoopProtector(max_restarts=3, state_file=state_file)
            protector1.record_crash("mario", "s1", error="crash")
            
            # Load from disk
            protector2 = CrashLoopProtector(max_restarts=3, state_file=state_file)
            assert protector2.get_state("mario").crash_count == 1
        finally:
            os.unlink(state_file)
    
    def test_per_agent_isolation(self):
        """Different agents have independent crash counts."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            state_file = f.name
        
        try:
            protector = CrashLoopProtector(max_restarts=2, state_file=state_file)
            protector.record_crash("mario", "s1", error="crash")
            protector.record_crash("mario", "s2", error="crash")
            
            # Mario is failed
            assert protector.is_permanently_failed("mario") is True
            # Lilo is fine
            assert protector.can_restart("lilo") is True
            assert protector.get_remaining_restarts("lilo") == 2
        finally:
            os.unlink(state_file)


# ============================================================
# 5. Integrated SupervisedCall Tests
# ============================================================

class TestSupervisedCall:
    """Tests for integrated supervision."""
    
    @pytest.mark.asyncio
    async def test_successful_call(self):
        """Successful call goes through all supervision layers."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            audit_file = f.name
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            crash_file = f.name
        
        try:
            supervisor = SupervisedCall()
            supervisor.audit = AuditLogger(audit_file=audit_file)
            supervisor.crash = CrashLoopProtector(state_file=crash_file)
            
            async def good_fn():
                return "hello"
            
            result = await supervisor.execute(
                tool="test_tool", fn=good_fn,
                agent_id="mario", session_id="test-1"
            )
            
            assert result["success"] is True
            assert result["output"] == "hello"
            assert result["timed_out"] is False
            assert result["duration_ms"] > 0
        finally:
            os.unlink(audit_file)
            os.unlink(crash_file)
    
    @pytest.mark.asyncio
    async def test_crash_loop_blocks(self):
        """Agent in crash loop is blocked."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            audit_file = f.name
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            crash_file = f.name
        
        try:
            supervisor = SupervisedCall()
            supervisor.audit = AuditLogger(audit_file=audit_file)
            supervisor.crash = CrashLoopProtector(max_restarts=2, state_file=crash_file)
            
            # Crash mario twice
            supervisor.crash.record_crash("mario", "s1", error="crash 1")
            supervisor.crash.record_crash("mario", "s2", error="crash 2")
            
            async def fn():
                return "should not run"
            
            result = await supervisor.execute(
                tool="test_tool", fn=fn,
                agent_id="mario", session_id="test-blocked"
            )
            
            assert result["success"] is False
            assert "crash loop" in result["error"]
        finally:
            os.unlink(audit_file)
            os.unlink(crash_file)
    
    @pytest.mark.asyncio
    async def test_circuit_open_blocks(self):
        """Open circuit breaker blocks calls."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            audit_file = f.name
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            crash_file = f.name
        
        try:
            supervisor = SupervisedCall()
            supervisor.audit = AuditLogger(audit_file=audit_file)
            supervisor.crash = CrashLoopProtector(state_file=crash_file)
            supervisor.circuit = CircuitBreaker(failure_threshold=2)
            
            # Open circuit for test_tool
            await supervisor.circuit.record_failure("test_tool")
            await supervisor.circuit.record_failure("test_tool")
            
            async def fn():
                return "should not run"
            
            result = await supervisor.execute(
                tool="test_tool", fn=fn,
                agent_id="mario", session_id="test-circuit"
            )
            
            assert result["success"] is False
            assert result["circuit_open"] is True
        finally:
            os.unlink(audit_file)
            os.unlink(crash_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])