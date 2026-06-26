"""Task contracts and result schemas.

Standalone reimplementation inspired by governed-agents contract pattern.
Defines the agent_callable Protocol (🔴 Dr. Neuron finding).
"""

import json
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol, runtime_checkable


class TaskStatus(Enum):
    SUCCESS = "success"
    BLOCKED = "blocked"
    FAILED = "failed"


@runtime_checkable
class AgentCallable(Protocol):
    """Protocol for agent implementations.

    Any callable matching this signature can be used as the agent
    in the evolve loop. This resolves the agent_callable interface
    blocker (🔴 Dr. Neuron).

    Examples:
        # Simple function
        def my_agent(prompt: str) -> str:
            return subprocess.run(["codex", "--task", prompt], capture_output=True).stdout

        # Class-based
        class CodexAgent:
            def __call__(self, prompt: str) -> str:
                return codex_cli(prompt)
    """

    def __call__(self, prompt: str) -> str:
        """Execute a task prompt and return raw agent output.

        Args:
            prompt: The full task prompt including contract, context,
                    and instructions.

        Returns:
            Raw text output from the agent, expected to contain a
            JSON result block.
        """
        ...


@dataclass
class TaskContract:
    """What the agent MUST deliver — defined BEFORE work begins."""

    task_id: str = field(default_factory=lambda: f"SAL-{uuid.uuid4().hex[:8]}")
    objective: str = ""
    acceptance_criteria: list[str] = field(default_factory=list)
    required_files: list[str] = field(default_factory=list)
    run_tests: str | None = None
    check_syntax: bool = True
    constraints: list[str] = field(default_factory=list)
    timeout_seconds: int = 120

    def to_prompt(self) -> str:
        """Format contract as a binding instruction prompt for the agent."""
        criteria = "\n".join(f"  - {c}" for c in self.acceptance_criteria)
        constraints = "\n".join(f"  - {c}" for c in self.constraints)
        files = "\n".join(f"  - {f}" for f in self.required_files)

        return f"""## TASK CONTRACT (BINDING)

**Task ID:** {self.task_id}
**Objective:** {self.objective}

**Acceptance Criteria:**
{criteria}

**Constraints:**
{constraints}

**Required Output Files:**
{files}

**Timeout:** {self.timeout_seconds}s

---

## OUTPUT FORMAT (MANDATORY)

You MUST end your work with a JSON block in this EXACT format:

If you SUCCEEDED:
```json
{{
  "task_id": "{self.task_id}",
  "status": "success",
  "files_created": ["list", "of", "files"],
  "evidence": "Brief proof that acceptance criteria are met"
}}
```

If you are BLOCKED or FAILED:
```json
{{
  "task_id": "{self.task_id}",
  "status": "blocked",
  "what_failed": "What exactly went wrong",
  "what_i_need": "Specific resource or clarification needed"
}}
```

CRITICAL: An HONEST blocker report is valued MORE than a fake success.
"""


@dataclass
class TaskResult:
    """Parsed result from an agent's output."""

    task_id: str = ""
    status: TaskStatus = TaskStatus.FAILED
    files_created: list[str] = field(default_factory=list)
    evidence: str = ""
    what_failed: str = ""
    what_i_need: str = ""
    raw_output: str = ""
    parse_success: bool = False
    verification_passed: bool = False

    @classmethod
    def from_agent_output(cls, raw: str, task_id: str) -> "TaskResult":
        """Parse the JSON block from agent output."""
        result = cls(task_id=task_id, raw_output=raw)

        json_str = None
        if "```json" in raw:
            parts = raw.split("```json")
            if len(parts) > 1:
                json_str = parts[-1].split("```")[0].strip()
        elif "{" in raw and "}" in raw:
            start = raw.rfind("{")
            end = raw.rfind("}") + 1
            json_str = raw[start:end]

        if not json_str:
            result.what_failed = "NO_JSON_OUTPUT: Agent did not produce required JSON"
            return result

        try:
            data = json.loads(json_str)
            result.parse_success = True
            result.status = TaskStatus(data.get("status", "failed"))
            result.files_created = data.get("files_created", [])
            result.evidence = data.get("evidence", "")
            result.what_failed = data.get("what_failed", "")
            result.what_i_need = data.get("what_i_need", "")
        except (json.JSONDecodeError, ValueError) as e:
            result.what_failed = f"INVALID_JSON: {e}"

        return result
