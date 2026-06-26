---
name: taskflow
description: |
  TaskFlow 3.0 - Agent-Native 项目化任务调度系统。
  
  AGENT INSTRUCTIONS:
  1. Read PROJECT.yaml from project directory
  2. Parse meta/content/target/constraints/workflow
  3. Execute workflow.step_by_step sequentially
  4. Record execution to memory/executions.json
  
  PATH RULES:
  - All paths in PROJECT.yaml are relative to project root
  - Resolve to absolute paths at execution time
  - Workspace root: determined at runtime
  - Project path: {workspace}/projects/{project_id}/
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      python: ["pyyaml"]
    install:
      - id: pyyaml
        kind: pip
        package: pyyaml
        bins: []
---

# TaskFlow 3.0 - Agent Execution Guide

## Quick Start

```bash
# Install skill
clawhub install taskflow

# Run a project
taskflow run <project-id>

# Run all due projects
taskflow run-projects

# List all projects
taskflow list

# Edit project config
taskflow edit <project-id>
```

## When to Use

When you receive a task to execute a project or when scheduler triggers project execution.

## Execution Steps

### Step 1: Locate Project

```bash
# Determine workspace (current working directory or env)
WORKSPACE="${OPENCLAW_WORKSPACE:-$(pwd)}"
PROJECT_ID="{project_id_from_task}"  # Extract from task

# Build paths
PROJECT_PATH="${WORKSPACE}/projects/${PROJECT_ID}"
CONFIG_FILE="${PROJECT_PATH}/PROJECT.yaml"

# Verify existence
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: PROJECT.yaml not found at $CONFIG_FILE"
    exit 1
fi
```

### Step 2: Parse Configuration

Read and parse PROJECT.yaml:

```yaml
# Required fields you MUST extract:
meta.id              # Project identifier
meta.enabled         # Skip if false
content.source       # Where to get content from
content.creation     # How to create/modify content
target.platform      # Where to deliver
target.manual_ref    # Platform operation manual
constraints.*        # Execution constraints
workflow.step_by_step # Steps to execute (CRITICAL)
```

### Step 3: Check Constraints

Before execution, verify:

```bash
# Check daily limits
TODAY_COUNT=$(grep "$(date +%Y-%m-%d)" "${PROJECT_PATH}/memory/post/history.md" | wc -l)
DAILY_MAX=$(jq -r '.constraints.daily_max' "$CONFIG_FILE")

if [ "$TODAY_COUNT" -ge "$DAILY_MAX" ]; then
    echo "Daily limit reached ($TODAY_COUNT/$DAILY_MAX), skipping"
    exit 0
fi

# Check interval
LAST_TIME=$(tail -1 "${PROJECT_PATH}/memory/post/history.md" | grep -oE '[0-9]{2}:[0-9]{2}')
INTERVAL=$(jq -r '.constraints.interval_min_minutes' "$CONFIG_FILE")
# Calculate time difference, skip if < interval

# Check best_times (optional)
CURRENT_HOUR=$(date +%H)
BEST_TIMES=$(jq -r '.constraints.best_times[]' "$CONFIG_FILE")
```

### Step 4: Execute Workflow

Read `workflow.step_by_step` array and execute each step in order:

```bash
# Extract workflow steps
STEPS=$(jq -r '.workflow.step_by_step[]' "$CONFIG_FILE")

# Execute each step
for step in $STEPS; do
    echo "Executing: $step"
    
    # Step format: "N. [TYPE] Action description"
    # TYPE and action are defined in PROJECT.yaml workflow
    # Common patterns (examples only, actual types vary by project):
    #   [读取] - Read file for context/deduplication
    #   [生成] - Generate/create content  
    #   [处理] - Process/transform content
    #   [发布] - Deliver to target
    #   [记录] - Update records
    #   [压缩] - Compress content
    #   [归档] - Archive content
    
    # Extract any file paths mentioned in step
    REF_FILE=$(echo "$step" | grep -oE '\S+\.md' | head -1)
    if [ -n "$REF_FILE" ]; then
        RESOLVED_PATH="${PROJECT_PATH}/${REF_FILE}"
    fi
    
    # Execute step based on content.source, content.creation, target settings
    # Implementation varies by project type
done
```

### Step 5: Record Execution

After completion, update executions.json:

```json
{
  "timestamp": "$(date -Iseconds)",
  "project_id": "${PROJECT_ID}",
  "action": "publish",
  "status": "success|failed|skipped",
  "reason": "if skipped or failed",
  "metadata": {
    "constraints_checked": true,
    "steps_executed": N
  }
}
```

## Path Resolution Rules

When resolving paths from PROJECT.yaml:

| Pattern | Resolution | Example |
|---------|------------|---------|
| `path/file.md` | `${PROJECT_PATH}/path/file.md` | Relative to project |
| `/abs/path` | `/abs/path` | Absolute path |
| `~/$HOME/path` | `~/$HOME/path` | User home |

**Always resolve relative paths to absolute at execution time.**

## Configuration Schema

PROJECT.yaml structure you MUST handle:

```yaml
meta:
  id: string              # Project ID (matches directory name)
  name: string            # Human-readable name
  version: string         # Config version
  enabled: boolean        # Skip if false
  manual_ref: string      # Path to platform manual (relative to workspace)

description: string       # Human-readable description

content:                  # Content configuration
  source:
    type: string          # memory | intel | project | rss | etc.
    path: string          # Source path (relative)
    # ... type-specific fields
  creation:
    mode: string          # original | adapt | republish | translate
    # ... mode-specific fields
  dedup:
    strategy: string      # How to check duplicates
    reference: string     # File to check against (relative path)

target:                   # Delivery target
  platform: string        # Platform identifier
  name: string            # Display name
  url: string             # Platform URL

constraints:              # Execution constraints
  daily_min: number       # Minimum daily executions
  daily_max: number       # Maximum daily executions
  interval_min_minutes: number  # Minimum interval between executions
  best_times: [string]    # Preferred time windows
  word_count:             # Content size limits
    min: number
    max: number

workflow:                 # Execution workflow (CRITICAL)
  step_by_step: [string] # Ordered list of steps to execute

memory_structure:         # Project memory organization
  # Reference only - describes file layout
```

## Error Handling

| Error | Action |
|-------|--------|
| PROJECT.yaml not found | Log error, exit |
| meta.enabled = false | Log skip reason, exit 0 |
| Constraint violation | Log skip reason, exit 0 |
| Step execution fails | Record failure, attempt rollback if needed |
| Manual reference missing | Use default platform behavior |

## Multi-Project Coordination

When handling multiple projects:

1. Read all enabled PROJECT.yaml files
2. Check constraints for each
3. Prioritize by: last_execution_time, priority, daily progress
4. Execute ONE project at a time (no parallel execution)
5. Respect global interval constraints

## Recording to Global Log

After any execution (success, skip, or failure), append to global log:

```bash
LOG_FILE="${WORKSPACE}/memory/taskflow-log.md"

echo "
### $(date '+%H:%M')
- **项目**: ${PROJECT_ID}
- **状态**: ${STATUS}
- **原因**: ${REASON}
- **详情**: ${PROJECT_PATH}/memory/executions.json
" >> "$LOG_FILE"
```

## CLI Commands

When user asks about TaskFlow status:

```bash
# Check all projects status
ls -1 "${WORKSPACE}/projects/" | while read proj; do
    [ -f "${WORKSPACE}/projects/$proj/PROJECT.yaml" ] && echo "$proj"
done

# Read specific project config
cat "${WORKSPACE}/projects/{project_id}/PROJECT.yaml"

# Check project history
cat "${WORKSPACE}/projects/{project_id}/memory/post/history.md"
```

---

*Agent Guide: Read PROJECT.yaml → Parse → Check constraints → Execute workflow → Record*
