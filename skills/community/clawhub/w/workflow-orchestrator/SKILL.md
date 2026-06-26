---
name: workflow-orchestrator
description: Visual workflow builder for orchestrating multi-agent systems with branching, parallel execution, error handling, and retry logic. Use when building agent pipelines, DAG-based task orchestration, multi-agent coordination, or complex automation workflows. Covers step definition, conditional branching, fan-out/fan-in, failure recovery, and live monitoring.
---

# Workflow Orchestrator

Build and run multi-agent workflows with DAG execution, branching, and error handling.

## Quick Start

```python
from orchestrator import Workflow, Step, Branch, Runner

wf = Workflow("data-pipeline")
wf.add_step(Step("fetch", agent="scraper", action="fetch_url", params={"url": "https://example.com"}))
wf.add_step(Step("extract", agent="parser", action="extract_text", depends_on=["fetch"]))
wf.add_step(Step("summarize", agent="writer", action="summarize", depends_on=["extract"]))
wf.add_step(Step("translate", agent="writer", action="translate", depends_on=["extract"]))
wf.add_step(Step("publish", agent="publisher", action="send", depends_on=["summarize", "translate"]))

runner = Runner()
result = runner.execute(wf)
```

## DAG Execution Model

```
fetch → extract → summarize → publish
                 → translate ↗
```

Steps run in parallel when their dependencies are met. The `publish` step waits for both `summarize` and `translate`.

## Step Definition

```python
Step(
    name="unique_step_name",
    agent="agent_id",          # Which agent executes this
    action="tool_name",        # What action to perform
    params={},                 # Input parameters
    depends_on=[],             # Wait for these steps first
    retry=3,                   # Max retries on failure
    timeout_sec=300,           # Step timeout
    on_failure="skip",         # "skip", "retry", "abort", "fallback"
    fallback_step="plan_b",    # Run this step on failure
    condition="$.fetch.status == 200",  # Conditional execution
)
```

## Features

- **Parallel execution**: Steps with satisfied dependencies run concurrently
- **Conditional branching**: JSONPath conditions determine which branches execute
- **Retry with backoff**: Configurable retry count and exponential backoff
- **Timeout handling**: Steps that exceed timeout are killed and handled per `on_failure`
- **Fallback steps**: Alternative steps run when the primary fails
- **Live status**: Query workflow state at any point during execution
- **Error propagation**: Configure whether failures bubble up or are contained

## Monitoring

```python
status = runner.status(workflow_id)
# {"running": 2, "completed": 3, "failed": 0, "pending": 1}
```
