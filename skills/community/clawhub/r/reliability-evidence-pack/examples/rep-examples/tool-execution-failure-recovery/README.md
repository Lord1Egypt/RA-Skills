# Tool Execution Failure Recovery

## Overview

This REP (Recovery Execution Pattern) example demonstrates how to track, document, and recover from tool execution failures using REP artifacts. It provides a systematic approach to handling tool failures in agentic systems.

## Use Case

When an agent executes tools (read, write, exec, browser, etc.), failures can occur due to various reasons:
- Network timeouts or connectivity issues
- Permission denied errors
- Invalid inputs or parameters
- Resource constraints (memory, disk, CPU)
- External service unavailability

This example shows how to:
1. **Track** tool execution failures with structured REP artifacts
2. **Document** recovery attempts using `error_recovery_log`
3. **Chain** artifacts together for complete audit trails

## Artifacts in This Example

| Artifact | Type | Description |
|----------|------|-------------|
| manifest.json | manifest | Master document linking all artifacts |
| error_recovery_log.md | log | Detailed error and recovery attempt documentation |
| tool_execution_audit.md | audit | Complete audit trail of tool executions |
| failure_classification.md | classification | Categorized failure types and patterns |
| recovery_validation.md | validation | Post-recovery validation results |

## Running the Example

### Option 1: Generate Artifacts with example.sh

```bash
cd /home/qq1028280994/.openclaw/workspace/rep-examples/tool-execution-failure-recovery
chmod +x example.sh
./example.sh
```

This will:
- Create the directory structure
- Generate sample REP artifacts
- Output JSONL format artifacts to stdout

### Option 2: Use Pre-generated Artifacts

The `sample-artifacts.jsonl` file contains pre-generated artifacts demonstrating the pattern. You can parse and examine them:

```bash
# View all artifacts
cat sample-artifacts.jsonl

# Parse specific artifact types
grep '"type":"error_recovery_log"' sample-artifacts.jsonl
grep '"type":"tool_execution_audit"' sample-artifacts.jsonl
```

## Artifact Chaining Pattern

This example demonstrates artifact chaining for audit trails:

```
manifest.json
    ├──> error_recovery_log.md (primary recovery documentation)
    │         └──> Links to: tool_execution_audit.md
    ├──> tool_execution_audit.md (execution history)
    │         └──> Links to: failure_classification.md
    ├──> failure_classification.md (categorized failures)
    └──> recovery_validation.md (proof of recovery)
                  └──> Links back to: error_recovery_log.md
```

Each artifact references others using artifact IDs, creating a navigable audit chain.

## Key Patterns

### 1. Error Recovery Log Structure

```markdown
### Phase 1: Failure Detection
- Timestamp of failure
- Tool name and parameters (sanitized)
- Error type and message
- Impact assessment

### Phase 2: Root Cause Analysis
- Failure classification
- Contributing factors
- Related system state

### Phase 3: Recovery Strategy
- Options considered
- Selection rationale
- Execution plan

### Phase 4: Recovery Execution
- Actions taken
- Validation steps
- Success/failure status
```

### 2. Artifact References

Each artifact includes references to related artifacts:

```json
{
  "artifact_id": "artifact-002",
  "type": "error_recovery_log",
  "references": [
    {"artifact_id": "artifact-001", "relationship": "preceded_by"},
    {"artifact_id": "artifact-003", "relationship": "validated_by"}
  ]
}
```

### 3. JSONL Format

Each artifact is also available in JSONL format for programmatic consumption:

```json
{"artifact_id":"artifact-001","type":"tool_execution","timestamp":"...","data":{...}}
{"artifact_id":"artifact-002","type":"error_recovery_log","timestamp":"...","data":{...}}
```

## Integration with Agent Systems

To integrate this pattern into your agent:

1. **Wrap tool executions** in try-catch blocks
2. **On failure**, create a failure artifact immediately
3. **Attempt recovery** based on failure type
4. **Document** each recovery attempt in error_recovery_log
5. **Chain** artifacts for complete traceability

See `example.sh` for a reference implementation.

## Version

- **Version:** 1.0.0
- **Created:** 2026-03-02
- **Pattern:** REP (Recovery Execution Pattern)
