"""Tests for sal.contract — TaskContract, TaskResult, AgentCallable."""

import pytest

from sal.contract import AgentCallable, TaskContract, TaskResult, TaskStatus


class TestTaskContract:
    def test_default_id(self):
        """should generate a SAL- prefixed task ID."""
        c = TaskContract(objective="test objective")
        assert c.task_id.startswith("SAL-")
        assert len(c.task_id) == 12  # SAL- + 8 hex chars

    def test_to_prompt_contains_objective(self):
        """should include objective in prompt."""
        c = TaskContract(
            objective="Increase LR",
            acceptance_criteria=["Code runs", "Metric improves"],
        )
        prompt = c.to_prompt()
        assert "Increase LR" in prompt
        assert "Code runs" in prompt
        assert "OUTPUT FORMAT (MANDATORY)" in prompt


class TestTaskResult:
    def test_parse_success_json(self):
        """should parse valid JSON block from agent output."""
        raw = '''Some text
```json
{"task_id": "SAL-abc123", "status": "success", "files_created": ["train.py"], "evidence": "tests pass"}
```
'''
        result = TaskResult.from_agent_output(raw, "SAL-abc123")
        assert result.parse_success is True
        assert result.status == TaskStatus.SUCCESS
        assert result.files_created == ["train.py"]

    def test_parse_blocked(self):
        """should parse blocked status correctly."""
        raw = '''```json
{"task_id": "SAL-x", "status": "blocked", "what_failed": "missing dep", "what_i_need": "numpy"}
```'''
        result = TaskResult.from_agent_output(raw, "SAL-x")
        assert result.status == TaskStatus.BLOCKED
        assert result.what_failed == "missing dep"

    def test_parse_no_json(self):
        """should report NO_JSON_OUTPUT when no JSON found."""
        result = TaskResult.from_agent_output("just plain text", "SAL-x")
        assert result.parse_success is False
        assert "NO_JSON_OUTPUT" in result.what_failed

    def test_parse_invalid_json(self):
        """should report INVALID_JSON for malformed JSON."""
        raw = '```json\n{not valid json}\n```'
        result = TaskResult.from_agent_output(raw, "SAL-x")
        assert "INVALID_JSON" in result.what_failed

    def test_parse_raw_json_without_backticks(self):
        """should find JSON even without markdown backticks."""
        raw = 'some output {"task_id": "x", "status": "success", "evidence": "ok"}'
        result = TaskResult.from_agent_output(raw, "x")
        assert result.parse_success is True


class TestAgentCallable:
    def test_function_is_agent_callable(self):
        """should accept any function matching the protocol."""
        def my_agent(prompt: str) -> str:
            return "output"

        assert isinstance(my_agent, AgentCallable)

    def test_class_is_agent_callable(self):
        """should accept class with __call__."""
        class MyAgent:
            def __call__(self, prompt: str) -> str:
                return "output"

        agent = MyAgent()
        assert isinstance(agent, AgentCallable)
