#!/usr/bin/env python3
"""
Autonomous Agent Framework - Main Module
Author: Socneo
Created with Claude Code
Version: 1.0.0

Core autonomous agent implementation with four-layer architecture.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

# Perception Layer
from scripts.event_listener import EventListener
from scripts.smart_heartbeat import SmartHeartbeat
from scripts.state_awareness import StateAwareness

# Judgment Layer
from scripts.priority_evaluator import PriorityEvaluator
from scripts.risk_decision_matrix import RiskDecisionMatrix
from scripts.uncertainty_handler import UncertaintyHandler

# Execution Layer
from scripts.task_decomposer import TaskDecomposer
from scripts.resilient_executor import ResilientExecutor
from scripts.error_recovery import ErrorRecovery
from scripts.progress_tracking import ProgressTracker

# Reflection Layer
from scripts.auto_reflection import AutoReflection
from scripts.pattern_recognizer import PatternRecognizer
from scripts.memory_system import MemorySystem
from scripts.self_correction import SelfCorrection


class AgentMode(Enum):
    """Agent operating modes."""
    FULLY_AUTONOMOUS = "fully_autonomous"
    ASSISTED = "assisted"
    MANUAL = "manual"


@dataclass
class AgentConfig:
    """Agent configuration."""
    mode: AgentMode = AgentMode.ASSISTED
    risk_threshold: float = 0.5
    confidence_threshold: float = 0.7
    max_retries: int = 3
    heartbeat_interval: int = 300


class AutonomousAgent:
    """
    Main autonomous agent class implementing four-layer architecture.

    Architecture:
    1. Perception: Monitor system state and events
    2. Judgment: Evaluate priorities and risks
    3. Execution: Execute tasks with resilience
    4. Reflection: Learn and improve from experiences
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig()

        # Initialize perception layer
        self.event_listener = EventListener()
        self.heartbeat = SmartHeartbeat(interval=self.config.heartbeat_interval)
        self.state_awareness = StateAwareness()

        # Initialize judgment layer
        self.priority_evaluator = PriorityEvaluator()
        self.risk_matrix = RiskDecisionMatrix(
            threshold=self.config.risk_threshold
        )
        self.uncertainty_handler = UncertaintyHandler(
            confidence_threshold=self.config.confidence_threshold
        )

        # Initialize execution layer
        self.task_decomposer = TaskDecomposer()
        self.executor = ResilientExecutor(max_retries=self.config.max_retries)
        self.error_recovery = ErrorRecovery()
        self.progress_tracker = ProgressTracker()

        # Initialize reflection layer
        self.auto_reflection = AutoReflection()
        self.pattern_recognizer = PatternRecognizer()
        self.memory_system = MemorySystem()
        self.self_correction = SelfCorrection()

        self.is_running = False

    def perceive(self) -> Dict[str, Any]:
        """Perception layer: Collect and analyze current state."""
        events = self.event_listener.collect_all_events()
        state = self.state_awareness.capture_system_state()
        anomalies = self.state_awareness.detect_anomalies()

        return {
            'events': events,
            'state': state,
            'anomalies': anomalies,
            'timestamp': self._get_timestamp()
        }

    def judge(self, perception_data: Dict[str, Any]) -> Dict[str, Any]:
        """Judgment layer: Evaluate and make decisions."""
        events = perception_data.get('events', [])
        state = perception_data.get('state')

        # Evaluate task priorities
        priorities = self.priority_evaluator.evaluate(
            events=events,
            state=state
        )

        # Assess risks
        risk_decisions = []
        for task in priorities:
            risk_result = self.risk_matrix.evaluate(task)
            risk_decisions.append(risk_result)

        # Handle uncertainties
        uncertain_tasks = [
            t for t in risk_decisions
            if t['confidence'] < self.config.confidence_threshold
        ]
        uncertainty_results = self.uncertainty_handler.handle(uncertain_tasks)

        return {
            'priorities': priorities,
            'risk_decisions': risk_decisions,
            'uncertainty_results': uncertainty_results,
            'recommended_actions': self._decide_actions(risk_decisions)
        }

    def execute(self, judgment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execution layer: Perform tasks with resilience."""
        actions = judgment_data.get('recommended_actions', [])

        execution_results = []
        for action in actions:
            # Decompose complex tasks
            subtasks = self.task_decomposer.decompose(action)

            # Execute with retry logic
            result = self.executor.execute(subtasks)

            # Track progress
            self.progress_tracker.update(action, result)

            execution_results.append({
                'action': action,
                'result': result,
                'success': result.get('success', False)
            })

        return {
            'executions': execution_results,
            'summary': self._summarize_executions(execution_results)
        }

    def reflect(self, execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Reflection layer: Learn and improve."""
        executions = execution_data.get('executions', [])

        # Analyze outcomes
        analysis = self.auto_reflection.analyze(executions)

        # Recognize patterns
        patterns = self.pattern_recognizer.recognize(executions)

        # Update memory
        self.memory_system.store({
            'executions': executions,
            'analysis': analysis,
            'patterns': patterns,
            'timestamp': self._get_timestamp()
        })

        # Self-correct if needed
        corrections = self.self_correction.check_and_correct(
            executions=executions,
            patterns=patterns
        )

        return {
            'analysis': analysis,
            'patterns': patterns,
            'corrections': corrections,
            'improvements': self._identify_improvements(patterns, corrections)
        }

    def run_cycle(self) -> Dict[str, Any]:
        """Execute one complete autonomous cycle."""
        # Perception
        perception = self.perceive()

        # Judgment
        judgment = self.judge(perception)

        # Execution (only in autonomous mode)
        execution = None
        if self.config.mode == AgentMode.FULLY_AUTONOMOUS:
            execution = self.execute(judgment)

        # Reflection
        reflection = self.reflect(execution or {'executions': []})

        return {
            'perception': perception,
            'judgment': judgment,
            'execution': execution,
            'reflection': reflection,
            'status': 'success'
        }

    def _decide_actions(self, risk_decisions: List[Dict]) -> List[Dict]:
        """Decide which actions to take based on risk matrix."""
        actions = []
        for decision in risk_decisions:
            if decision['action'] in ['EXECUTE', 'EXECUTE_NOTIFY']:
                actions.append(decision)
        return actions

    def _summarize_executions(self, executions: List[Dict]) -> Dict[str, Any]:
        """Summarize execution results."""
        total = len(executions)
        successful = sum(1 for e in executions if e.get('success'))
        return {
            'total': total,
            'successful': successful,
            'failed': total - successful,
            'success_rate': successful / total if total > 0 else 0
        }

    def _identify_improvements(
        self,
        patterns: List[Dict],
        corrections: List[Dict]
    ) -> List[str]:
        """Identify areas for improvement."""
        improvements = []

        for pattern in patterns:
            if pattern.get('type') == 'failure':
                improvements.append(f"Address failure pattern: {pattern.get('description')}")

        for correction in corrections:
            if correction.get('applied'):
                improvements.append(f"Applied correction: {correction.get('reason')}")

        return improvements

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()

    def start(self):
        """Start the autonomous agent."""
        self.is_running = True
        self.heartbeat.start()
        self.event_listener.start_monitoring()

    def stop(self):
        """Stop the autonomous agent."""
        self.is_running = False
        self.heartbeat.stop()
        self.event_listener.stop_monitoring()

    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        return {
            'is_running': self.is_running,
            'mode': self.config.mode.value,
            'perception': {
                'events_count': len(self.event_listener.collect_all_events()),
                'state_health': self.state_awareness.get_state_summary()
            },
            'memory': self.memory_system.get_stats()
        }


def create_agent(mode: str = 'assisted') -> AutonomousAgent:
    """Factory function to create an autonomous agent."""
    agent_mode = AgentMode.FULLY_AUTONOMOUS if mode == 'autonomous' else AgentMode.ASSISTED
    config = AgentConfig(mode=agent_mode)
    return AutonomousAgent(config)


if __name__ == "__main__":
    # Demo: Create and run autonomous agent
    print("Initializing Autonomous Agent...")

    agent = create_agent(mode='assisted')
    agent.start()

    print("Running one autonomous cycle...")
    result = agent.run_cycle()

    print(f"\nAgent Status: {result['status']}")
    print(f"Perception - Events: {len(result['perception']['events'])}")
    print(f"Judgment - Actions recommended: {len(result['judgment']['recommended_actions'])}")
    print(f"Reflection - Patterns found: {len(result['reflection']['patterns'])}")

    agent.stop()
    print("\nAgent stopped.")
