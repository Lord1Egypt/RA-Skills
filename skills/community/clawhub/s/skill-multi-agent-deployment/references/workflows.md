# Workflow DAG Templates for Multi-Agent Deployment

Workflow DAG (Directed Acyclic Graph) templates for chaining multiple agents
into pipeline execution patterns. Use these templates to define multi-step
workflows where each agent's output feeds the next stage.

---

## DAG Template Specification

Workflows are defined as JSON files with a DAG structure:

```json
{
  "workflow": {
    "id": "workflow-name",
    "version": "1.0",
    "description": "Short description"
  },
  "stages": [
    {
      "id": "stage-1",
      "agent": "agent-type",
      "input": "shared_memory_key",
      "output": "shared_memory_key",
      "depends_on": [],
      "config": {
        "timeout_s": 300,
        "retry": 2
      }
    }
  ]
}
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `workflow.id` | string | Unique workflow identifier |
| `stages[].id` | string | Unique stage identifier |
| `stages[].agent` | string | Agent type to execute this stage |
| `stages[].input` | string | Shared memory key to read input from |
| `stages[].output` | string | Shared memory key to write output to |
| `stages[].depends_on` | string[] | Stage IDs that must complete first |
| `stages[].config.timeout_s` | int | Max execution time in seconds |
| `stages[].config.retry` | int | Number of retries on failure |

---

## Template 1: Content Creation Pipeline

Research → Writer → Editor → Publisher (linear pipeline).

**Use case:** Blog posts, documentation, marketing copy.

```json
{
  "workflow": {
    "id": "content-creation",
    "version": "1.0",
    "description": "End-to-end content creation pipeline"
  },
  "stages": [
    {
      "id": "research",
      "agent": "research",
      "input": "coordinator:topic",
      "output": "research:findings",
      "depends_on": [],
      "config": { "timeout_s": 300, "retry": 1 }
    },
    {
      "id": "draft",
      "agent": "builder",
      "input": "research:findings",
      "output": "builder:draft",
      "depends_on": ["research"],
      "config": { "timeout_s": 600, "retry": 2 }
    },
    {
      "id": "review",
      "agent": "auditor",
      "input": "builder:draft",
      "output": "auditor:review",
      "depends_on": ["draft"],
      "config": { "timeout_s": 300, "retry": 1 }
    },
    {
      "id": "publish",
      "agent": "coordinator",
      "input": "auditor:review",
      "output": "coordinator:published",
      "depends_on": ["review"],
      "config": { "timeout_s": 120, "retry": 0 }
    }
  ]
}
```

### Execution Flow

```
[coordinator:topic] → Research ──→ [research:findings]
     ↓                                    ↓
[research:findings] → Builder  ──→ [builder:draft]
     ↓                                    ↓
[builder:draft]    → Auditor  ──→ [auditor:review]
     ↓                                    ↓
[auditor:review]   → Coordinator → [coordinator:published]
```

---

## Template 2: Development Sprint

Planner → Coder → Tester → Deployer → Auditor (linear + parallel audit gate).

**Use case:** Code generation, feature development, bug fixes.

```json
{
  "workflow": {
    "id": "dev-sprint",
    "version": "1.0",
    "description": "Feature development sprint with audit gate"
  },
  "stages": [
    {
      "id": "plan",
      "agent": "coordinator",
      "input": "user:feature_request",
      "output": "coordinator:sprint_plan",
      "depends_on": [],
      "config": { "timeout_s": 180, "retry": 1 }
    },
    {
      "id": "code",
      "agent": "builder",
      "input": "coordinator:sprint_plan",
      "output": "builder:artifacts",
      "depends_on": ["plan"],
      "config": { "timeout_s": 900, "retry": 2 }
    },
    {
      "id": "audit",
      "agent": "auditor",
      "input": "builder:artifacts",
      "output": "auditor:audit_report",
      "depends_on": ["code"],
      "config": { "timeout_s": 300, "retry": 1 }
    },
    {
      "id": "fix_issues",
      "agent": "builder",
      "input": "auditor:audit_report",
      "output": "builder:fixed_artifacts",
      "depends_on": ["audit"],
      "config": { "timeout_s": 600, "retry": 0 }
    },
    {
      "id": "deploy",
      "agent": "coordinator",
      "input": "builder:fixed_artifacts",
      "output": "coordinator:deployed",
      "depends_on": ["fix_issues"],
      "config": { "timeout_s": 300, "retry": 0 }
    }
  ]
}
```

### Execution Flow (with audit feedback loop)

```
user:feature_request → Coordinator → [sprint_plan]
                           ↓
[sprint_plan] → Builder → [artifacts]
                           ↓
[artifacts] → Auditor → [audit_report]
                           ↓
[audit_report] → Builder → [fixed_artifacts] (feedback loop if issues found)
                           ↓
[fixed_artifacts] → Coordinator → [deployed]
```

---

## Template 3: Customer Support Team

Coordinator → [Support, Inventory, Analytics, Order] (fan-out + fan-in).

**Use case:** E-commerce support, multi-channel query resolution.

```json
{
  "workflow": {
    "id": "customer-support",
    "version": "1.0",
    "description": "Multi-agent customer support resolution"
  },
  "stages": [
    {
      "id": "triage",
      "agent": "coordinator",
      "input": "user:ticket",
      "output": "coordinator:triaged",
      "depends_on": [],
      "config": { "timeout_s": 60, "retry": 1 }
    },
    {
      "id": "inventory_check",
      "agent": "research",
      "input": "coordinator:triaged",
      "output": "research:inventory",
      "depends_on": ["triage"],
      "config": { "timeout_s": 120, "retry": 2 }
    },
    {
      "id": "order_lookup",
      "agent": "personal",
      "input": "coordinator:triaged",
      "output": "personal:order_info",
      "depends_on": ["triage"],
      "config": { "timeout_s": 120, "retry": 2 }
    },
    {
      "id": "resolution",
      "agent": "builder",
      "input": ["research:inventory", "personal:order_info"],
      "output": "builder:resolution",
      "depends_on": ["inventory_check", "order_lookup"],
      "config": { "timeout_s": 180, "retry": 1 }
    }
  ]
}
```

### Execution Flow (fan-out)

```
user:ticket → Coordinator
                ├──→ Research → [inventory]
                └──→ Personal → [order_info]
                                ↓
         [inventory] + [order_info] → Builder → [resolution]
```

---

## Template 4: Data Processing Pipeline

Extract → Transform → Load → Validate (ETL pipeline).

**Use case:** Data ingestion, batch processing, reporting.

```json
{
  "workflow": {
    "id": "data-pipeline",
    "version": "1.0",
    "description": "ETL data processing pipeline"
  },
  "stages": [
    {
      "id": "extract",
      "agent": "research",
      "input": "coordinator:datasource",
      "output": "research:raw_data",
      "depends_on": [],
      "config": { "timeout_s": 600, "retry": 3 }
    },
    {
      "id": "transform",
      "agent": "builder",
      "input": "research:raw_data",
      "output": "builder:transformed_data",
      "depends_on": ["extract"],
      "config": { "timeout_s": 600, "retry": 2 }
    },
    {
      "id": "load",
      "agent": "personal",
      "input": "builder:transformed_data",
      "output": "personal:loaded",
      "depends_on": ["transform"],
      "config": { "timeout_s": 300, "retry": 1 }
    },
    {
      "id": "validate",
      "agent": "auditor",
      "input": "personal:loaded",
      "output": "auditor:validation_report",
      "depends_on": ["load"],
      "config": { "timeout_s": 180, "retry": 1 }
    }
  ]
}
```

### Execution Flow

```
datasource → Research → [raw_data]
                           ↓
[raw_data] → Builder → [transformed_data]
                           ↓
[transformed_data] → Personal → [loaded]
                           ↓
[loaded] → Auditor → [validation_report]
```

---

## Template 5: Personal Productivity Workflow

Coordinator → [Research, Builder, Personal] (parallel tasks, merged results).

**Use case:** Daily briefing, meeting prep, research tasks.

```json
{
  "workflow": {
    "id": "daily-briefing",
    "version": "1.0",
    "description": "Personal daily briefing generation"
  },
  "stages": [
    {
      "id": "gather_news",
      "agent": "research",
      "input": "coordinator:briefing_request",
      "output": "research:news_summary",
      "depends_on": [],
      "config": { "timeout_s": 120, "retry": 1 }
    },
    {
      "id": "check_schedule",
      "agent": "personal",
      "input": "coordinator:briefing_request",
      "output": "personal:schedule",
      "depends_on": [],
      "config": { "timeout_s": 60, "retry": 1 }
    },
    {
      "id": "compose_briefing",
      "agent": "builder",
      "input": ["research:news_summary", "personal:schedule"],
      "output": "builder:briefing",
      "depends_on": ["gather_news", "check_schedule"],
      "config": { "timeout_s": 180, "retry": 1 }
    }
  ]
}
```

---

## Running Workflows

### Basic Execution via Shared Memory

Trigger stages by writing to the appropriate shared memory keys:

```bash
# Step 1: Seed the workflow input
python scripts/memory_sync.py \
  --write 'coordinator:topic:{"topic":"OpenClaw multi-agent scaling"}' \
  --schema task_assignment

# Step 2: Research agent picks up input, writes findings
python scripts/memory_sync.py --read research:findings

# Step 3: Check if all outputs are populated
python scripts/memory_sync.py --stats
```

### Workflow Execution Script

Save a workflow DAG as `workflow.json` and use this pattern:

```bash
#!/bin/bash
# execute_workflow.sh — Run a DAG workflow
set -e

WORKFLOW_FILE="${1:-workflow.json}"

# Validate workflow file
if [ ! -f "$WORKFLOW_FILE" ]; then
  echo "Workflow file not found: $WORKFLOW_FILE"
  exit 1
fi

echo "Running workflow: $(python3 -c "import json; print(json.load(open('$WORKFLOW_FILE'))['workflow']['id'])")"

# For each stage (topologically sorted — stages are already ordered in the DAG)
python3 -c "
import json, subprocess, sys

with open('$WORKFLOW_FILE') as f:
    wf = json.load(f)

stages = wf['stages']
results = {}

for i, stage in enumerate(stages):
    sid = stage['id']
    agent = stage['agent']
    print(f'[{i+1}/{len(stages)}] Stage: {sid} ({agent})')

    # Check dependencies
    deps = stage.get('depends_on', [])
    for d in deps:
        if d not in results:
            print(f'  Dependency not met: {d}')
            sys.exit(1)

    # Read inputs
    inputs = stage.get('input', [])
    if isinstance(inputs, str):
        inputs = [inputs]

    for inp in inputs:
        agent_key = inp.split(':', 1)
        if len(agent_key) == 2:
            agent_id, key = agent_key
            result = subprocess.run(
                ['python3', 'scripts/memory_sync.py', '--read', f'{agent_id}:{key}'],
                capture_output=True, text=True, cwd='.'
            )
            print(f'  Input {inp}: {\"found\" if result.returncode == 0 else \"not found\"}')

    # Simulate stage execution (in production, this triggers the agent)
    print(f'  Stage {sid} ready for execution')
    results[sid] = True

print()
print('Workflow DAG validation PASSED')
print(f'Stages: {len(stages)}, Dependencies: all met')
"
```

### Workflow Status Tracking

After execution, check which stages completed:

```bash
python scripts/memory_sync.py --stats
# Look for output keys matching your workflow stages
```

---

## Best Practices

### 1. Topological Ordering
Define stages in dependency order — siblings can run in parallel.

### 2. Input/Output Keys
- Use `agent_type:stage_id` naming for clarity
- Prefix workflow outputs: `workflow_name:stage_id:output`
- Keep keys consistent between stages

### 3. Error Handling
- Always set `config.timeout_s` — prevents hung agents
- Set `config.retry` for unreliable stages
- Use auditor stages as quality gates before deployment

### 4. Shared Memory Keyspace
- Workflow inputs: `coordinator:workflow_name:input_key`
- Stage outputs: `agent_type:workflow_name:output_key`
- Use `--schema` validation for structured stage outputs

### 5. Testing
Test each stage individually before wiring up the full pipeline:
```bash
# Test stage 1
python scripts/memory_sync.py --write 'coordinator:topic:{\"topic\":\"test\"}'
python scripts/memory_sync.py --read research:findings

# Validate stage 1 output
python scripts/memory_sync.py --write 'auditor:test:{\"verdict\":\"pass\"}' --schema audit_report
```
