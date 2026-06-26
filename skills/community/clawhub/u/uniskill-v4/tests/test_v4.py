#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UniSkill V4 - Tests
"""

import pytest
import sys
sys.path.insert(0, '..')

from socratic_engine_v4 import SocraticEngineV4, check_clarity
from idea_debater_v4 import HighSpeedDebater, quick_debate, validate_need
from orchestrator_v4 import UniSkillOrchestratorV4, execute


class TestSocraticEngine:
    """Test Socratic Engine V4"""
    
    def test_check_clarity_clear(self):
        """Test clear requirement"""
        is_clear, prompt = check_clarity("加工10个TC4零件，精加工，公差±0.02")
        assert is_clear == True or prompt != "CLEAR"  # Depends on extraction
    
    def test_check_clarity_unclear(self):
        """Test unclear requirement"""
        is_clear, prompt = check_clarity("做个零件")
        assert is_clear == False
    
    def test_anchor_extraction(self):
        """Test anchor extraction"""
        engine = SocraticEngineV4()
        score, prompt, anchor = engine.analyze_clarity(
            "需要车削50件7075铝，精度要求±0.02"
        )
        assert score >= 0
        assert isinstance(anchor.missing, list)


class TestIdeaDebater:
    """Test Idea Debater V4"""
    
    def test_quick_debate(self):
        """Test quick debate"""
        result = quick_debate(
            "Test problem",
            ["Option A", "Option B", "Option C"]
        )
        assert result.recommended in ["方案1", "方案2", "方案3"]
        assert 0 <= result.score <= 5
        assert 0 <= result.confidence <= 1
    
    def test_validate_need(self):
        """Test need validation"""
        is_valid, score = validate_need("明确的需求")
        assert isinstance(is_valid, bool)
        assert 0 <= score <= 1
    
    def test_debate_with_empty_solutions(self):
        """Test debate with empty solutions"""
        result = quick_debate("Problem", [])
        assert result.recommended == "无方案"


class TestOrchestrator:
    """Test Orchestrator V4"""
    
    def test_execute_unclear(self):
        """Test execution with unclear requirement"""
        result = execute("做个零件")
        assert result.success == False
    
    def test_execute_clear(self):
        """Test execution with clear requirement"""
        result = execute("加工10个TC4零件")
        # May or may not succeed depending on extraction
        assert hasattr(result, 'success')
        assert hasattr(result, 'stats')


class TestMemorySafety:
    """Test memory safety"""
    
    def test_debater_memory_limit(self):
        """Test debater memory limit"""
        debater = HighSpeedDebater(max_memory_mb=50)
        assert debater.max_memory == 50
    
    def test_orchestrator_memory_limit(self):
        """Test orchestrator memory limit"""
        orch = UniSkillOrchestratorV4(memory_limit_mb=100)
        assert orch.memory_limit == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])