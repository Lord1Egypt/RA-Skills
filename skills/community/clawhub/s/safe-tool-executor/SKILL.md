---
name: safe-tool-executor
description: |
  Safe Tool Executor — Enforces least-privilege execution with tier-based access control.
  Use when: (1) executing tools with destructive potential, (2) validating tool safety before execution,
  (3) requiring human approval for dangerous operations, (4) preventing unsafe file deletions.
triggers:
  - "tool safety"
  - "tool execution"
  - "dangerous command"
  - "destructive action"
  - "human approval"
  - "least privilege"
author: "Axioma Cluster"
date: "2026-05-17"
version: 1.0.0
tags:
  - tool-safety
  - execution-control
  - security
  - least-privilege
  - approval-workflow
status: "active"
---

# Safe Tool Executor

Enforces safe tool execution with tier-based access control and human approval for dangerous operations.

## Problem: Unsafe Tool Use

```
SYMPTOMS:
├── Over-privileged tools
├── Destructive action undetected
├── Deletion of important data
└── Insufficient watchdog severity
```

## Solutions Implemented

### 1. Least Privilege Principle

```python
class SafeToolExecutor:
    tool_tiers = {
        'READ_ONLY': ['ls', 'cat', 'head', 'tail', 'grep'],
        'WRITE': ['write', 'edit', 'mkdir', 'touch'],
        'DELETE': ['rm', 'rmdir', 'unlink']
    }
    
    required_approval = ['DELETE', 'DROP', 'TRUNCATE', 'FORMAT']
```

### 2. Approval Workflow

```python
def execute_dangerous_tool(action, tool, args):
    if tool in required_approval:
        request_human_approval(f"DANGER: {tool} {args}")
        wait_for_approval(timeout=60)
        if not approved:
            return {'status': 'BLOCKED', 'reason': 'No approval'}
    return execute_tool(tool, args)
```

### 3. Tier Separation

```python
def validate_tool_access(tool, operation):
    # READ_ONLY tools cannot write
    if operation == 'WRITE' and tool in tool_tiers['READ_ONLY']:
        return False
    # DELETE tools require approval by default
    if tool in tool_tiers['DELETE']:
        return require_approval(tool)
    return True
```

## Watchdogs

| Watchdog | Role | Threshold |
|----------|------|------------|
| **VLS** | Logical validation | >0.700 = BLOCK |
| **ABS** | Architecture | Any delete = APPROVAL |
| **STC** | Tension | >0.600 = WARNING |

## Usage

```python
from safe_tool_executor import SafeToolExecutor

executor = SafeToolExecutor()

# READ_ONLY tool - OK directly
result = executor.execute('cat', '/etc/passwd')

# WRITE tool - Warning
result = executor.execute('write', '/project/config.py')

# DELETE tool - BLOCKED without approval
result = executor.execute('rm', '/important/file.txt')
# → BLOCKED: requires human approval
```

## Dangerous Patterns (Blocked)

| Pattern | Action |
|---------|--------|
| `rm -rf /*` | BLOCK + ALERT |
| `DROP TABLE` | APPROVAL REQUIRED |
| `TRUNCATE` | APPROVAL REQUIRED |
| `DELETE /system` | APPROVAL + LOG |
| `format` | COMPLETE BLOCK |

## Prerequisites

| Condition | Requirement | Check Command |
|-----------|-------------|---------------|
| Python | >= 3.8 | `python3 --version` |
| VLS Watchdog | Active | `curl -s http://localhost:6333/collections/vls_watchdog` |
| ABS Watchdog | Active | `curl -s http://localhost:6333/collections/abs_watchdog` |
| Qdrant | Running | `curl -s http://localhost:6333/collections` |

## Files

```
safe-tool-executor/
├── SKILL.md
├── scripts/
│   ├── safe_tool_executor.py
│   ├── main.py
│   └── utils.py
├── data/
├── models/
└── tests/
```