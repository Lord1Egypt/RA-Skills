"""
契约测试 — 状态机
──────────────────
验证 PipelineState 的状态转换合法性。
"""
import pytest
from contracts.state_schema import (
    PipelineState,
    PipelinePhase,
    PhaseContext,
    WALEntry,
)


class TestPipelineState:
    """PipelineState 契约测试"""

    def test_valid_transition_idle_to_pending(self):
        state = PipelineState(session_id="test")
        new_state = state.transition_to(PipelinePhase.PENDING)
        assert new_state.current_phase == PipelinePhase.PENDING

    def test_invalid_transition_idle_to_done(self):
        """IDLE → DONE 是非法转换"""
        state = PipelineState(session_id="test")
        with pytest.raises(ValueError, match="非法状态转换"):
            state.transition_to(PipelinePhase.DONE)

    def test_invalid_transition_done_to_searching(self):
        """DONE → SEARCHING 是非法转换"""
        state = PipelineState(session_id="test")
        state = state.transition_to(PipelinePhase.PENDING)
        state = state.transition_to(PipelinePhase.SEARCHING)
        state = state.transition_to(PipelinePhase.CRAWLING)
        state = state.transition_to(PipelinePhase.ANALYZING)
        state = state.transition_to(PipelinePhase.REPORTING)
        state = state.transition_to(PipelinePhase.DELIVERING)
        state = state.transition_to(PipelinePhase.DONE)

        with pytest.raises(ValueError, match="非法状态转换"):
            state.transition_to(PipelinePhase.SEARCHING)

    def test_full_pipeline_transitions(self):
        """完整管道状态转换应全部合法"""
        state = PipelineState(session_id="test")
        transitions = [
            PipelinePhase.PENDING,
            PipelinePhase.SEARCHING,
            PipelinePhase.CRAWLING,
            PipelinePhase.ANALYZING,
            PipelinePhase.REPORTING,
            PipelinePhase.DELIVERING,
            PipelinePhase.DONE,
        ]
        for phase in transitions:
            state = state.transition_to(phase)
            assert state.current_phase == phase

        # 最终回到 IDLE
        state = state.transition_to(PipelinePhase.IDLE)
        assert state.current_phase == PipelinePhase.IDLE

    def test_failed_to_retrying(self):
        state = PipelineState(session_id="test")
        state = state.transition_to(PipelinePhase.PENDING)
        state = state.transition_to(PipelinePhase.SEARCHING)
        state = state.transition_to(PipelinePhase.FAILED)
        state = state.transition_to(PipelinePhase.RETRYING)
        assert state.current_phase == PipelinePhase.RETRYING

    def test_frozen_state(self):
        """PipelineState 应该是不可变的"""
        state = PipelineState(session_id="test")
        with pytest.raises(Exception):
            state.current_phase = PipelinePhase.DONE

    def test_transition_produces_new_object(self):
        """transition_to 应返回新对象，不修改原对象"""
        state = PipelineState(session_id="test")
        new_state = state.transition_to(PipelinePhase.PENDING)
        assert state.current_phase == PipelinePhase.IDLE
        assert new_state.current_phase == PipelinePhase.PENDING
        assert state is not new_state

    def test_can_retry_under_max(self):
        state = PipelineState(session_id="test")
        state = state.transition_to(PipelinePhase.PENDING)
        state = state.transition_to(PipelinePhase.SEARCHING)
        state = state.transition_to(PipelinePhase.FAILED)
        # 第一次失败，应该可以重试
        assert state.can_retry(PipelinePhase.SEARCHING)

    def test_history_recorded(self):
        state = PipelineState(session_id="test")
        state = state.transition_to(PipelinePhase.PENDING)
        state = state.transition_to(PipelinePhase.SEARCHING)
        assert len(state.phase_history) == 2


class TestWALEntry:
    """WALEntry 契约测试"""

    def test_valid_entry(self):
        entry = WALEntry(
            session_id="test-001",
            phase="searching",
            action="search_start",
            status="prepared",
            details="Starting search for 'AI'",
        )
        assert entry.session_id == "test-001"
        assert entry.status == "prepared"

    def test_default_timestamp(self):
        entry = WALEntry(
            session_id="test",
            phase="idle",
            action="init",
            status="committed",
        )
        assert entry.timestamp > 0
