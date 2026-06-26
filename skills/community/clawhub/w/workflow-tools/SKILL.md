---
name: workflow-tools
version: 1.5.0
description: Work smarter with loop detection, parallel decisions, and file size analysis
author: Live Neon <hello@liveneon.ai>
homepage: https://github.com/live-neon/skills/tree/main/agentic/workflow-tools
repository: leegitw/workflow-tools
license: MIT
tags: [agentic, workflow, automation, orchestration, parallel, decision-making, loops, task-management]
layer: extensions
status: active
alias: wt
metadata:
  openclaw:
    requires:
      config:
        - .openclaw/workflow-tools.yaml
        - .claude/workflow-tools.yaml
      workspace:
        - output/loops/
        - output/parallel-decisions/
        - output/mce-analysis/
        - output/subworkflows/
---

# workflow-tools (工具)

Unified skill for workflow utilities including open loop detection, parallel/serial
decision framework, MCE file analysis, and subworkflow spawning. Consolidates 4 skills.

**Trigger**: 明示呼出 (explicit invocation)

**Source skills**: loop-closer, parallel-decision, MCE (minimal-context-engineering), subworkflow-spawner

**Removed**: pbd-strength-classifier (redundant with `/fm classify`)

## Installation

```bash
openclaw install leegitw/workflow-tools
```

**Dependencies**:
- `leegitw/failure-memory` (for loop context)
- `leegitw/constraint-engine` (for enforcement context)

```bash
# Install with dependencies
openclaw install leegitw/context-verifier
openclaw install leegitw/failure-memory
openclaw install leegitw/constraint-engine
openclaw install leegitw/workflow-tools
```

**Standalone usage**: Loop detection, parallel decisions, and MCE analysis work independently.
Full integration provides constraint-aware workflow recommendations.

**Data handling**: This skill operates within your agent's trust boundary. When triggered,
it uses your agent's configured model for workflow analysis and decision support. No external APIs
or third-party services are called. Results are written to `output/` subdirectories in your workspace.

**⚠️ File access**: This skill reads user-specified directories and files for analysis:
- `/wt loops [path]` scans the specified directory (default: current working directory)
- `/wt mce <file>` reads the specified file for size analysis
The metadata declares only config and output paths. See Security Considerations for details.

## What This Solves

Workflows accumulate friction — loops that never close, decisions about parallel vs serial execution, files that grow too large. This skill provides utilities for common workflow problems:

1. **Loop detection** — find DEFERRED, PLACEHOLDER, and TODO markers before marking work complete
2. **Parallel decisions** — 5-factor framework for when to parallelize vs serialize
3. **MCE analysis** — identify files exceeding size thresholds, suggest splits

**The insight**: Small tools that do one thing well. Don't overthink the workflow — detect, decide, analyze, move on.

## Usage

```
/wt <sub-command> [arguments]
```

## Sub-Commands

| Command | CJK | Logic | Trigger |
|---------|-----|-------|---------|
| `/wt loops` | 循環 | scan(DEFERRED∨PLACEHOLDER∨TODO)→openloop[] | Explicit |
| `/wt parallel` | 並列 | 5因子→serial∨parallel | Explicit |
| `/wt mce` | 極限 | file.lines>200→split_suggestions[] | Explicit |
| `/wt subworkflow` | 副流 | task→spawn(clawhub.skill) | Explicit |

## Arguments

### /wt loops

| Argument | Required | Description |
|----------|----------|-------------|
| path | No | Directory to scan (default: current) |
| --pattern | No | Custom patterns to detect (comma-separated) |
| --exclude | No | Paths to exclude (comma-separated) |

### /wt parallel

| Argument | Required | Description |
|----------|----------|-------------|
| task | Yes | Description of task to evaluate |
| --factors | No | Specific factors to evaluate (default: all 5) |

### /wt mce

| Argument | Required | Description |
|----------|----------|-------------|
| file | Yes | File to analyze |
| --threshold | No | Line threshold (default: 200) |
| --suggest | No | Generate split suggestions |

### /wt subworkflow

| Argument | Required | Description |
|----------|----------|-------------|
| task | Yes | Task description |
| --skill | No | Specific ClawHub skill to use |
| --background | No | Run in background |

## Configuration

Configuration is loaded from (in order of precedence):
1. `.openclaw/workflow-tools.yaml` (OpenClaw standard)
2. `.claude/workflow-tools.yaml` (Claude Code compatibility)
3. Defaults (built-in)

```yaml
# .openclaw/workflow-tools.yaml
loops:
  patterns:                  # Patterns to detect as open loops
    - "TODO:"
    - "FIXME:"
    - "HACK:"
    - "XXX:"
    - "DEFERRED:"
    - "PLACEHOLDER:"
  exclude:                   # Paths to exclude from scanning
    - "vendor/"
    - "node_modules/"
mce:
  threshold: 200             # Line threshold for MCE compliance
  warning_threshold: 300     # Line threshold for warning
parallel:
  default_factors: 5         # Number of factors to evaluate
```

## Core Logic

### Open Loop Detection

Scans for unclosed work items:

| Pattern | Type | Example |
|---------|------|---------|
| `DEFERRED:` | Postponed work | `// DEFERRED: handle edge case` |
| `PLACEHOLDER:` | Temporary code | `// PLACEHOLDER: implement auth` |
| `TODO:` | Task marker | `// TODO: add error handling` |
| `FIXME:` | Bug marker | `// FIXME: race condition` |
| `HACK:` | Technical debt | `// HACK: workaround for bug` |
| `XXX:` | Attention needed | `// XXX: review this logic` |

### Parallel vs Serial Decision Framework

Five factors determine parallel suitability:

| Factor | Question | Parallel If | Serial If |
|--------|----------|-------------|-----------|
| **Team** | Can different people work on parts? | Independent parts | Shared expertise needed |
| **Coupling** | How connected are the tasks? | Loose coupling | Tight coupling |
| **Interface** | Are boundaries clear? | Well-defined | Fluid/evolving |
| **Pattern** | Is approach consistent? | Divergent exploration | Convergent refinement |
| **Integration** | How complex is merging? | Simple merge | Complex coordination |

Decision matrix:

| Factors favoring parallel | Recommendation |
|---------------------------|----------------|
| 5/5 | Strongly parallel |
| 4/5 | Parallel with coordination checkpoints |
| 3/5 | Consider case-by-case |
| 2/5 | Serial with parallel sub-tasks |
| 0-1/5 | Serial |

### MCE (Minimal Context Engineering)

File size thresholds for context efficiency:

| Lines | Status | Action |
|-------|--------|--------|
| ≤200 | ✓ MCE compliant | No action needed |
| 201-300 | ⚠ Approaching limit | Consider refactoring |
| >300 | ✗ Exceeds MCE | Split recommended |

Split suggestions based on:
- Function/method boundaries
- Logical groupings
- Import dependencies
- Test coverage boundaries

### Subworkflow Spawning

Delegate tasks to specialized ClawHub skills:

```
Task → Skill Selection → Spawn → Monitor → Collect Results
```

Available skill categories:
- `research-*`: Investigation and analysis
- `generate-*`: Content generation
- `validate-*`: Verification and testing
- `transform-*`: Data transformation

### Example: Deployment Workflow Analysis

```
/wt parallel "Deploy new payment service to production"
[PARALLEL VS SERIAL ANALYSIS]
Task: "Deploy new payment service to production"

Factor Analysis:
1. Team: ✗ Serial - Single SRE team handles deploys
2. Coupling: ✗ Serial - Payment depends on auth service
3. Interface: ✓ Parallel - Clear API contracts defined
4. Pattern: ✗ Serial - Requires sequential rollout (canary → staging → prod)
5. Integration: ✗ Serial - Payment gateway integration must be verified

Score: 1/5 factors favor parallel
Recommendation: SERIAL deployment
Rationale: High-risk service requiring careful sequential verification.
```

### Example: Infrastructure Loop Detection

```
/wt loops infra/ --pattern "MANUAL:,HARDCODED:"
[OPEN LOOPS DETECTED]
Scanned: ./infra
Files checked: 23

Infrastructure Issues (5):
  infra/terraform/main.tf:45  HARDCODED: AWS region
  infra/k8s/deployment.yaml:78  MANUAL: replica count
  infra/docker/Dockerfile:12  TODO: multi-stage build
  infra/scripts/deploy.sh:34  FIXME: rollback not implemented
  infra/helm/values.yaml:56  PLACEHOLDER: production secrets

Summary: 2 high, 2 medium, 1 low priority
Action: Address HARDCODED and FIXME before next release.
```

## Output

### /wt loops output

```
[OPEN LOOPS DETECTED]
Scanned: ./src
Files checked: 47

Open loops found (12):

High Priority (FIXME, XXX):
  src/auth/handler.go:45  FIXME: race condition in token refresh
  src/api/client.go:123   XXX: review error handling

Medium Priority (TODO):
  src/handlers/user.go:78  TODO: add input validation
  src/db/queries.go:234    TODO: optimize query
  src/utils/hash.go:12     TODO: add caching

Low Priority (DEFERRED, PLACEHOLDER):
  src/config/loader.go:89  DEFERRED: support YAML config
  src/templates/email.go:34 PLACEHOLDER: email templates
  ...

Summary: 2 high, 5 medium, 5 low priority loops
Action: Address high priority loops before release.
```

### /wt parallel output

```
[PARALLEL VS SERIAL ANALYSIS]
Task: "Implement authentication and authorization"

Factor Analysis:

1. Team (独立性):
   ✓ Parallel - Auth and authz can be assigned separately

2. Coupling (結合度):
   ✗ Serial - Authz depends on auth tokens

3. Interface (境界):
   ✓ Parallel - Clear token interface between them

4. Pattern (手法):
   ✓ Parallel - Both follow established patterns

5. Integration (統合):
   ✗ Serial - Token format must match exactly

Score: 3/5 factors favor parallel

Recommendation: SERIAL with parallel sub-tasks
Rationale: Core dependency between auth and authz, but sub-components
           within each can be developed in parallel.

Suggested approach:
1. Define token interface (serial, required first)
2. Implement auth + authz (parallel, once interface stable)
3. Integration testing (serial, final step)
```

### /wt mce output

```
[MCE ANALYSIS]
File: src/handlers/user.go
Lines: 347

Status: ✗ EXCEEDS MCE THRESHOLD (200 lines)

Complexity Analysis:
  Functions: 12
  Avg function length: 29 lines
  Max function length: 67 lines (HandleUserUpdate)
  Import groups: 4

Split Suggestions:

1. Extract CRUD handlers (lines 45-180):
   → src/handlers/user_crud.go (~135 lines)
   - CreateUser, GetUser, UpdateUser, DeleteUser

2. Extract validation (lines 181-250):
   → src/handlers/user_validation.go (~70 lines)
   - ValidateUserInput, ValidateEmail, ValidatePassword

3. Keep orchestration (remaining):
   → src/handlers/user.go (~142 lines)
   - Handler setup, middleware, routing

After split: 3 files, all ≤200 lines ✓
```

### /wt subworkflow output

```
[SUBWORKFLOW SPAWNED]
Task: "Research competitor authentication implementations"
Skill: research-web-analysis
Status: Running in background

Job ID: SW-20260215-001
Monitor: /wt subworkflow --status SW-20260215-001

Expected completion: ~5 minutes
Results will be written to: output/subworkflows/SW-20260215-001/
```

## Integration

- **Layer**: Extensions
- **Depends on**: failure-memory (for loop context), constraint-engine (for enforcement context)
- **Used by**: governance (for loop detection), review-orchestrator (for parallel decisions)

## Failure Modes

| Condition | Behavior |
|-----------|----------|
| Invalid sub-command | List available sub-commands |
| File not found | Error: "File not found: {path}" |
| No patterns found | Info: "No open loops detected" |
| Skill not available | Error: "Skill not found: {skill}" |

## Next Steps

After invoking this skill:

| Condition | Action |
|-----------|--------|
| Loops found | Prioritize and address high-priority loops |
| Parallel recommended | Create parallel work streams |
| MCE exceeded | Apply split suggestions |
| Subworkflow complete | Review and integrate results |

## Workspace Files

This skill reads/writes:

```
output/
├── loops/
│   └── scan-YYYY-MM-DD.md    # Loop scan results
├── parallel-decisions/
│   └── task-YYYY-MM-DD.md    # Decision records
├── mce-analysis/
│   └── file-YYYY-MM-DD.md    # MCE analysis results
└── subworkflows/
    └── SW-YYYYMMDD-XXX/      # Subworkflow outputs
        ├── status.json
        └── results.md
```

## Security Considerations

**What this skill accesses:**
- Configuration files in `.openclaw/workflow-tools.yaml` and `.claude/workflow-tools.yaml`
- **User-specified directories** via `/wt loops [path]` — scans for patterns (read-only)
- **User-specified files** via `/wt mce <file>` — reads for size analysis (read-only)
- Its own output directories (write):
  - `output/loops/` — loop scan results
  - `output/parallel-decisions/` — decision records
  - `output/mce-analysis/` — file analysis results
  - `output/subworkflows/` — subworkflow outputs

**⚠️ IMPORTANT**: The metadata declares only config and output paths. However, `/wt loops` and
`/wt mce` read **arbitrary user-specified paths** beyond the declared metadata. This is by
design — analysis requires reading the files/directories you want to analyze.

**What this skill does NOT access:**
- System environment variables
- Network resources or external APIs

**What this skill does NOT do:**
- Send data to external services
- Execute arbitrary code
- Modify source files (analysis is read-only)

**⚠️ Path scanning (`/wt loops`):**
The `/wt loops` command accepts an arbitrary directory path argument. It will recursively
scan the specified directory for loop patterns (TODO, FIXME, etc.). This is a read-only
operation but can scan any directory you have filesystem access to. The skill does NOT
restrict which paths can be scanned — use caution with sensitive directories. Consider
using `--exclude` to skip sensitive paths.

**Subworkflow spawning (`/wt subworkflow`):**
The `/wt subworkflow` command spawns other ClawHub skills installed in your environment.
- **Scope**: Can invoke any skill installed via `openclaw install`
- **Permissions**: Spawned skills execute with their own declared permissions (not elevated)
- **Categories**: Typically `research-*`, `generate-*`, `validate-*`, `transform-*` skills
- **Risk**: The effective permission footprint is the union of this skill plus any spawned skills

Review your installed skills (`openclaw list`) to understand the combined permission scope
when using subworkflow spawning.

**Provenance note:**
This skill is developed by Live Neon (https://github.com/live-neon/skills) and published
to ClawHub under the `leegitw` account. Both refer to the same maintainer.

## Acceptance Criteria

- [ ] `/wt loops` detects all standard loop patterns
- [ ] `/wt loops` categorizes by priority (high/medium/low)
- [ ] `/wt parallel` evaluates all 5 factors
- [ ] `/wt parallel` provides clear recommendation with rationale
- [ ] `/wt mce` identifies files exceeding threshold
- [ ] `/wt mce --suggest` generates actionable split suggestions
- [ ] `/wt subworkflow` spawns ClawHub skills correctly
- [ ] `/wt subworkflow` supports background execution
- [ ] Results written to workspace files

---

*Consolidated from 4 skills as part of agentic skills consolidation (2026-02-15).*
