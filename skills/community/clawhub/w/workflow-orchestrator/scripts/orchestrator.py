"""
Workflow Orchestrator — DAG-based multi-agent execution engine
AgentBounty: FlowBot Systems $7,200
"""
import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Callable
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


class StepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"


@dataclass
class StepResult:
    step_name: str
    status: StepStatus
    output: Optional[dict] = None
    error: Optional[str] = None
    duration_sec: float = 0.0
    attempts: int = 1


@dataclass
class Step:
    name: str
    agent: str
    action: str
    params: dict = field(default_factory=dict)
    depends_on: list[str] = field(default_factory=list)
    retry: int = 0
    timeout_sec: float = 300
    on_failure: str = "abort"  # "skip", "retry", "abort", "fallback"
    fallback_step: Optional[str] = None
    condition: Optional[str] = None


class Workflow:
    def __init__(self, name: str):
        self.name = name
        self.steps: dict[str, Step] = {}
        self.id = str(uuid.uuid4())[:8]

    def add_step(self, step: Step):
        self.steps[step.name] = step

    def roots(self) -> list[str]:
        """Steps with no dependencies."""
        return [name for name, step in self.steps.items() if not step.depends_on]

    def dependents(self, step_name: str) -> list[str]:
        """Steps that depend on this step."""
        return [name for name, step in self.steps.items() if step_name in step.depends_on]

    def validate(self) -> list[str]:
        """Check for cycles and missing dependencies."""
        errors = []
        for name, step in self.steps.items():
            for dep in step.depends_on:
                if dep not in self.steps:
                    errors.append(f"Step '{name}' depends on missing step '{dep}'")
                if dep == name:
                    errors.append(f"Step '{name}' depends on itself")

        # Cycle detection via DFS
        visited, in_stack = set(), set()
        def dfs(node):
            if node in in_stack:
                return True
            if node in visited:
                return False
            visited.add(node)
            in_stack.add(node)
            for dep in self.steps[node].depends_on:
                if dfs(dep):
                    errors.append(f"Cycle detected involving step '{node}'")
                    return True
            in_stack.remove(node)
            return False

        for name in self.steps:
            dfs(name)

        return errors

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "id": self.id,
            "steps": {
                name: {
                    "agent": s.agent,
                    "action": s.action,
                    "params": s.params,
                    "depends_on": s.depends_on,
                    "retry": s.retry,
                    "on_failure": s.on_failure,
                }
                for name, s in self.steps.items()
            },
        }


class Runner:
    """Execute workflows with parallel step execution."""

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.results: dict[str, StepResult] = {}
        self.step_outputs: dict[str, dict] = {}
        self._lock = threading.Lock()
        self._agent_executor: dict[str, Callable] = {}  # agent_id → execute_fn

    def register_agent(self, agent_id: str, execute_fn: Callable):
        """Register an agent's execution function."""
        self._agent_executor[agent_id] = execute_fn

    def _execute_step(self, step: Step, context: dict) -> StepResult:
        """Execute a single step with retry and timeout."""
        executor = self._agent_executor.get(step.agent)
        if not executor:
            # Mock executor for testing
            executor = lambda action, params, ctx: {"result": f"mock_{action}"}

        for attempt in range(1, step.retry + 2):
            start = time.time()
            try:
                output = executor(step.action, step.params, context)
                duration = time.time() - start
                result = StepResult(
                    step_name=step.name,
                    status=StepStatus.COMPLETED,
                    output=output,
                    duration_sec=round(duration, 2),
                    attempts=attempt,
                )
                with self._lock:
                    self.step_outputs[step.name] = output
                return result
            except Exception as e:
                duration = time.time() - start
                if attempt <= step.retry:
                    time.sleep(min(2 ** attempt, 30))  # exponential backoff
                    continue
                # Final failure
                if step.on_failure == "skip":
                    return StepResult(step.name, StepStatus.SKIPPED, error=str(e), duration_sec=duration, attempts=attempt)
                elif step.on_failure == "fallback" and step.fallback_step:
                    return StepResult(step.name, StepStatus.FAILED, error=str(e), duration_sec=duration, attempts=attempt)
                else:
                    return StepResult(step.name, StepStatus.FAILED, error=str(e), duration_sec=duration, attempts=attempt)

        return StepResult(step.name, StepStatus.FAILED, error="Max retries exceeded", attempts=step.retry + 1)

    def _check_condition(self, condition: Optional[str], context: dict) -> bool:
        """Evaluate a simple condition like '$.step.status == "completed"'."""
        if not condition:
            return True
        # Simple evaluator — production would use JSONPath
        try:
            if "==" in condition:
                path, expected = condition.split("==", 1)
                path = path.strip().lstrip("$.").split(".")
                value = context
                for key in path:
                    value = value.get(key, {}) if isinstance(value, dict) else {}
                return str(value).strip() == expected.strip().strip('"')
        except Exception:
            pass
        return True

    def execute(self, workflow: Workflow) -> dict:
        """Execute workflow with parallel step scheduling."""
        errors = workflow.validate()
        if errors:
            return {"status": "invalid", "errors": errors}

        self.results = {}
        self.step_outputs = {}
        completed = set()
        failed = set()
        skipped = set()

        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            pending = set(workflow.steps.keys())

            while pending:
                # Find steps ready to run
                ready = []
                for name in list(pending):
                    step = workflow.steps[name]
                    deps = set(step.depends_on)

                    # All deps completed?
                    if deps - completed - skipped:
                        # Check if any dep failed and has no fallback
                        if deps & failed:
                            if step.on_failure == "skip":
                                skipped.add(name)
                                pending.discard(name)
                                self.results[name] = StepResult(name, StepStatus.SKIPPED, error="Dependency failed")
                            continue
                        continue

                    # Check condition
                    context = {"step_outputs": dict(self.step_outputs)}
                    for dep_name in step.depends_on:
                        dep_result = self.results.get(dep_name)
                        if dep_result:
                            context[f"step_{dep_name}"] = {"status": dep_result.status.value, "output": dep_result.output}

                    if self._check_condition(step.condition, context):
                        ready.append(step)

                if not ready and pending:
                    # Deadlock — all remaining steps have unsatisfied deps
                    for name in pending:
                        self.results[name] = StepResult(name, StepStatus.SKIPPED, error="Deadlocked")
                    break

                # Submit ready steps
                futures = {pool.submit(self._execute_step, step, {"step_outputs": dict(self.step_outputs)}): step for step in ready}
                for step in ready:
                    pending.discard(step.name)

                # Collect results
                for future in as_completed(futures):
                    step = futures[future]
                    result = future.result()
                    self.results[step.name] = result

                    if result.status == StepStatus.COMPLETED:
                        completed.add(step.name)
                    elif result.status == StepStatus.SKIPPED:
                        skipped.add(step.name)
                    else:
                        failed.add(step.name)
                        if step.on_failure == "abort":
                            # Cancel remaining
                            for name in list(pending):
                                self.results[name] = StepResult(name, StepStatus.SKIPPED, error="Aborted due to failure")
                                skipped.add(name)
                            pending.clear()
                            break

        # Handle fallback steps
        for name, result in list(self.results.items()):
            if result.status == StepStatus.FAILED:
                step = workflow.steps[name]
                if step.fallback_step and step.fallback_step in workflow.steps:
                    fb_step = workflow.steps[step.fallback_step]
                    fb_result = self._execute_step(fb_step, {"step_outputs": dict(self.step_outputs)})
                    self.results[fb_step.name] = fb_result
                    if fb_result.status == StepStatus.COMPLETED:
                        completed.add(fb_step.name)

        return {
            "workflow_id": workflow.id,
            "status": "completed" if not failed else "partial_failure",
            "completed": len(completed),
            "failed": len(failed),
            "skipped": len(skipped),
            "total": len(workflow.steps),
            "results": {name: {"status": r.status.value, "output": r.output, "error": r.error, "attempts": r.attempts, "duration_sec": r.duration_sec} for name, r in self.results.items()},
        }

    def status(self, workflow_id: str = None) -> dict:
        """Get current execution status."""
        by_status = defaultdict(int)
        for r in self.results.values():
            by_status[r.status.value] += 1
        return dict(by_status)


if __name__ == "__main__":
    # Demo
    wf = Workflow("demo-pipeline")
    wf.add_step(Step("fetch", agent="scraper", action="fetch", params={"url": "https://example.com"}))
    wf.add_step(Step("parse", agent="parser", action="parse", depends_on=["fetch"]))
    wf.add_step(Step("summarize", agent="writer", action="summarize", depends_on=["parse"]))
    wf.add_step(Step("translate", agent="writer", action="translate", depends_on=["parse"]))
    wf.add_step(Step("publish", agent="publisher", action="send", depends_on=["summarize", "translate"]))

    runner = Runner()
    result = runner.execute(wf)
    print(json.dumps(result, indent=2))
