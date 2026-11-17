# Workflow Orchestration Skill - API Reference

## Core Classes

### WorkflowOrchestrator

Main orchestrator class for managing workflows.

#### Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `start_workflow(workflow_name, initial_context)` | Start a workflow instance | workflow_name: str, initial_context: Dict | WorkflowInstance |
| `advance_phase(instance_id, gate_passed)` | Advance to next phase | instance_id: str, gate_passed: bool (default True) | PhaseResult |
| `handle_exception(instance_id, exception_type, severity)` | Handle exception | instance_id: str, exception_type: ExceptionType, severity: SeverityLevel | ExceptionResult |
| `get_workflow_status(instance_id)` | Get instance status | instance_id: str | WorkflowInstance |
| `route_task(metadata)` | Route task to workflow | metadata: TaskMetadata | str (workflow_name) |
| `register_workflow(workflow_config)` | Register custom workflow | workflow_config: WorkflowConfig | None |
| `save_instance(instance_id)` | Save instance to dict | instance_id: str | Dict |
| `load_instance(data)` | Load instance from dict | data: Dict | WorkflowInstance |
| `list_workflows()` | List all workflows | None | List[str] |

### WorkflowInstance

Workflow execution instance.

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | str | Instance ID |
| `workflow_name` | str | Workflow name |
| `current_phase` | str | Current phase |
| `status` | WorkflowStatus | Instance status |
| `context` | Dict | Context data |
| `artifacts` | Dict | Artifacts |
| `history` | List[PhaseResult] | Phase history |

### PhaseResult

Phase execution result.

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `phase_id` | str | Phase ID |
| `gate_passed` | bool | Gate passed status |
| `artifacts` | Dict | Artifacts |
| `message` | str | Execution message |
| `success` | bool | Execution success |

## Data Models

### WorkflowConfig

Workflow configuration.

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | str | Workflow name |
| `description` | str | Workflow description |
| `phases` | List[PhaseConfig] | Phase configurations |
| `transitions` | List[TransitionRule] | Transition rules |

### PhaseConfig

Phase configuration.

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | str | Phase ID |
| `gate` | str | Gate name |
| `agent` | str | Agent name (optional) |
| `required_artifacts` | List[str] | Required artifacts |

### TaskMetadata

Task metadata for routing.

| Attribute | Type | Description |
|-----------|------|-------------|
| `change_type` | ChangeType | Change type |
| `change_size` | SizeLevel | Change size |
| `risk_level` | RiskLevel | Risk level |
| `cross_module` | bool | Cross-module flag |
| `user_keywords` | List[str] | User keywords |

## Enums

### WorkflowStatus

| Value | Description |
|-------|-------------|
| PENDING | Workflow not started |
| RUNNING | Workflow running |
| PAUSED | Workflow paused |
| COMPLETED | Workflow completed |
| FAILED | Workflow failed |
| ROLLED_BACK | Workflow rolled back |

### ChangeType

| Values |
|--------|
| FEATURE, BUGFIX, HOTFIX, REFACTOR, DOCS, TEST, CONFIG, PROMPT, BUILD, CI, PERF, SECURITY, MIGRATION, RESEARCH, CLEANUP, CHORE |

### SizeLevel

| Value | Description |
|-------|-------------|
| XS | Extra small |
| S | Small |
| M | Medium |
| L | Large |
| XL | Extra large |

### RiskLevel

| Value | Description |
|-------|-------------|
| LOW | Low risk |
| MEDIUM | Medium risk |
| HIGH | High risk |
| CRITICAL | Critical risk |

### ExceptionType

| Value | Description |
|-------|-------------|
| REQUIREMENT_CHANGE | Requirement changes |
| TECHNICAL_DEBT | Technical debt |
| QUALITY_GATE_FAILURE | Quality gate failure |
| PRODUCTION_ISSUE | Production issue |
| PERFORMANCE_REGRESSION | Performance regression |

### SeverityLevel

| Value | Description |
|-------|-------------|
| MINOR | Minor severity |
| MAJOR | Major severity |
| CRITICAL | Critical severity |

## Exception Handling

### ExceptionResult

| Attribute | Type | Description |
|-----------|------|-------------|
| `exception_type` | ExceptionType | Exception type |
| `severity` | SeverityLevel | Severity level |
| `handled` | bool | Handled status |
| `action_taken` | str | Action taken |
| `rollback_triggered` | bool | Rollback triggered |

### RollbackResult

| Attribute | Type | Description |
|-----------|------|-------------|
| `rollback_type` | str | Rollback type |
| `success` | bool | Rollback success |
| `rollback_to_phase` | str | Target phase |
| `message` | str | Rollback message |