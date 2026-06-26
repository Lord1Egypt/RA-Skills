# Reliability Evidence Pack (REP) Specification

## Overview

The **Reliability Evidence Pack (REP)** is a structured documentation system for capturing, validating, and auditing agent reliability artifacts. REP provides cryptographic integrity, chain-of-custody, and cross-reference validation for critical operational data.

### Why REP Matters

- **Accountability**: Every decision, handoff, and incident is documented with signatures
- **Integrity**: SHA256 content hashing ensures artifacts haven't been tampered with
- **Auditability**: Cross-reference validation verifies completeness
- **Automation**: CLI tooling enables CI/CD integration

---

## Artifact Types

### Required Types (v0.1)

| Type | Purpose | Key Fields |
|------|---------|------------|
| `decision_rejection_log` | Documents approval/rejection decisions | `decision`, `action_class`, `criteria`, `rationale` |
| `memory_reconstruction_audit` | Verifies memory recall accuracy | `claim_ref`, `consistency_score`, `audit_outcome` |
| `handoff_acceptance_packet` | Formal task transfer with SLA | `handoff_id`, `sla`, `acceptance_criteria` |
| `near_miss_reliability_trailer` | Captures near-miss incidents | `incident_id`, `potential_impact`, `containment_action` |
| `signed_divergence_violation_record` | Tracks policy/SLA violations | `severity`, `signatures`, `disposition` |

### v0.2 Types

| Type | Purpose | Key Fields |
|------|---------|------------|
| `agent_heartbeat_record` | Long-running agent health | `status`, `uptime_sec`, `tasks_active` |
| `context_snapshot` | Decision point context capture | `trigger`, `active_memory`, `decision_context` |
| `claim_file` | Production change safety docs | `change_summary`, `expected_files`, `rollback_method` |

### v0.3 Types

| Type | Purpose | Key Fields |
|------|---------|------------|
| `error_recovery_log` | Tracks error recovery attempts | `error_type`, `recovery_strategy`, `attempt_count`, `outcome`, `time_to_recovery_ms` |
| `performance_baseline` | Tracks performance metrics over time | `metric_name`, `baseline_value`, `current_value`, `trend`, `sample_size`, `measurement_window` |

### v0.4 Types

| Type | Purpose | Key Fields |
|------|---------|------------|
| `model_switch_event` | Tracks model/provider switches during agent execution | `trigger_reason`, `from_model`, `to_model`, `switch_overhead_ms`, `context_preserved`, `fallback_enabled` |

### v0.5 Types

| Type | Purpose | Key Fields |
|------|---------|------------|
| `tool_execution_failure_record` | Tracks tool execution failures and diagnostics | `tool_name`, `failure_type`, `error_message`, `retry_count`, `recovery_action`, `execution_context` |
| `session_context_loss_record` | Tracks context loss events during agent sessions | `loss_type`, `trigger_event`, `lost_state_summary`, `recovery_method`, `downtime_ms`, `preserved_data` |
| `security_policy_violation` | Tracks security-related policy violations | `violation_type`, `severity`, `policy_name`, `detection_method`, `blocked_action`, `resolution`, `threat_indicators` |

### v0.6 Types (Capability Evolution)

| Type | Purpose | Key Fields |
|------|---------|------------|
| `capability_degradation_record` | Tracks agent capability degradation over time | `metric_name`, `baseline_value`, `current_value`, `degradation_percent`, `trigger_threshold`, `detection_method`, `affected_capabilities`, `remediation_action` |
| `evolution_recommendation_accepted` | Tracks when evolver recommendations are accepted | `recommendation_id`, `target_capability`, `expected_improvement`, `acceptance_rationale`, `implementation_plan`, `success_criteria` |
| `evolution_cycle_record` | Documents each evolution cycle execution | `cycle_id`, `start_time`, `end_time`, `trigger_type`, `changes_applied`, `outcomes`, `rollback_available` |

#### capability_degradation_record

Records when agent capabilities degrade below acceptable thresholds, triggering evolution workflows.

```json
{
  "rep_version": "1.0",
  "artifact_type": "capability_degradation_record",
  "artifact_id": "cdgr-20260302-capability-001",
  "session_id": "sess-evolver-001",
  "interaction_id": "msg-capcheck-042",
  "created_at": "2026-03-02T03:15:00Z",
  "actor": { "id": "agent:capability-evolver", "role": "agent" },
  "content_hash": "sha256:a1b2c3d4e5f6...",
  "prev_hash": "sha256:previous...",
  "content": {
    "metric_name": "task_completion_rate",
    "baseline_value": 0.95,
    "current_value": 0.72,
    "degradation_percent": 24.2,
    "trigger_threshold": 0.80,
    "detection_method": "rolling_window_analysis",
    "affected_capabilities": [
      "context_retention",
      "tool_execution_accuracy",
      "response_relevance"
    ],
    "remediation_action": "trigger_evolution_cycle",
    "measurement_window": {
      "start": "2026-02-23T00:00:00Z",
      "end": "2026-03-02T00:00:00Z",
      "duration_days": 7
    },
    "sample_size": 487,
    "confidence_interval": {
      "lower": 0.68,
      "upper": 0.76,
      "confidence": 0.95
    },
    "trend_direction": "declining",
    "consecutive_degradation_cycles": 3,
    "notes": "Primary degradation in context retention metrics; tool execution remains stable"
  }
}
```

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| `metric_name` | string | Yes | Must be non-empty; should describe the capability metric | Name of the capability metric being tracked |
| `baseline_value` | number | Yes | Must be between 0 and 1 (inclusive) | Original baseline value for the metric |
| `current_value` | number | Yes | Must be between 0 and 1 (inclusive) | Current measured value of the metric |
| `degradation_percent` | number | Yes | Must be non-negative; represents percentage drop from baseline | Percentage degradation from baseline |
| `trigger_threshold` | number | Yes | Must be between 0 and 1 | Threshold that triggers this record |
| `detection_method` | string | Yes | Must be non-empty | Method used to detect degradation (e.g., rolling_window_analysis, anomaly_detection, threshold_breach) |
| `affected_capabilities` | array | Yes | Must be non-empty array of strings | List of capabilities affected by degradation |
| `remediation_action` | string | Yes | Must be non-empty | Recommended action to remediate (e.g., trigger_evolution_cycle, adjust_parameters, retrain_model) |
| `measurement_window` | object | No | If present, must contain valid ISO 8601 dates | Time window for measurements |
| `sample_size` | integer | No | Must be positive if present | Number of samples in measurement |
| `confidence_interval` | object | No | If present, lower < upper; both between 0-1 | Statistical confidence interval |
| `trend_direction` | string | No | Must be one of: declining, stable, improving | Direction of the metric trend |
| `consecutive_degradation_cycles` | integer | No | Must be non-negative if present | Number of consecutive cycles with degradation |
| `notes` | string | No | Free-form text | Additional context or notes |

#### evolution_recommendation_accepted

Records when an evolution recommendation is accepted and queued for implementation.

```json
{
  "rep_version": "1.0",
  "artifact_type": "evolution_recommendation_accepted",
  "artifact_id": "era-20260302-rec-042",
  "session_id": "sess-evolver-001",
  "interaction_id": "msg-evolver-156",
  "created_at": "2026-03-02T03:20:00Z",
  "actor": { "id": "agent:capability-evolver", "role": "agent" },
  "content_hash": "sha256:b2c3d4e5f6a7...",
  "prev_hash": "sha256:previous...",
  "content": {
    "recommendation_id": "rec-2026-03-02-capability-042",
    "target_capability": "context_retention",
    "expected_improvement": {
      "metric": "task_completion_rate",
      "baseline": 0.72,
      "target": 0.90,
      "improvement_percent": 25.0
    },
    "acceptance_rationale": "Degradation has persisted for 3 consecutive cycles; manual intervention unsuccessful; evolution protocol recommended",
    "implementation_plan": {
      "phase_1": "Collect 500+ training samples from recent successful sessions",
      "phase_2": "Fine-tune context handling parameters",
      "phase_3": "A/B test with 10% traffic",
      "phase_4": "Full rollout if metrics stabilize"
    },
    "success_criteria": {
      "task_completion_rate": { "minimum": 0.88, "window_days": 7 },
      "false_positive_rate": { "maximum": 0.05 },
      "latency_impact": { "maximum_ms": 50 }
    },
    "risk_assessment": {
      "risk_level": "medium",
      "rollback_time_minutes": 15,
      "fallback_strategy": "revert_to_previous_parameter_set",
      "mitigations": ["maintain rollback capability", "gradual rollout", "monitoring_dashboard"]
    },
    "requested_by": "agent:capability-evolver",
    "approved_by": "system:auto-approved",
    "priority": "high",
    "estimated_implementation_hours": 4
  }
}
```

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| `recommendation_id` | string | Yes | Must be non-empty; unique identifier | Unique identifier for this recommendation |
| `target_capability` | string | Yes | Must be non-empty | Capability being improved |
| `expected_improvement` | object | Yes | Must contain metric, baseline, target | Expected improvement details |
| `acceptance_rationale` | string | Yes | Must be non-empty | Reason for accepting this recommendation |
| `implementation_plan` | object | Yes | Must contain at least one phase | Phased implementation plan |
| `success_criteria` | object | Yes | Must contain measurable criteria | Criteria for determining success |
| `risk_assessment` | object | No | If present, must contain risk_level | Risk evaluation and mitigation |
| `requested_by` | string | No | If present, must be valid actor ID | Who/what requested this recommendation |
| `approved_by` | string | No | If present, must be valid actor ID | Who/what approved this recommendation |
| `priority` | string | No | Must be one of: low, medium, high, critical | Implementation priority |
| `estimated_implementation_hours` | number | No | Must be non-negative if present | Estimated hours to implement |

#### evolution_cycle_record

Documents the complete execution of an evolution cycle, including changes applied and outcomes.

```json
{
  "rep_version": "1.0",
  "artifact_type": "evolution_cycle_record",
  "artifact_id": "ecr-20260302-cycle-018",
  "session_id": "sess-evolver-001",
  "interaction_id": "msg-evolver-201",
  "created_at": "2026-03-02T03:45:00Z",
  "actor": { "id": "agent:capability-evolver", "role": "agent" },
  "content_hash": "sha256:c3d4e5f6a7b8...",
  "prev_hash": "sha256:previous...",
  "content": {
    "cycle_id": "cycle-2026-03-02-018",
    "start_time": "2026-03-02T03:30:00Z",
    "end_time": "2026-03-02T03:45:00Z",
    "duration_minutes": 15,
    "trigger_type": "automatic_degradation",
    "trigger_details": {
      "degradation_record_ref": "cdgr-20260302-capability-001",
      "consecutive_failures": 3,
      "threshold_breached": "task_completion_rate < 0.80"
    },
    "changes_applied": [
      {
        "change_type": "parameter_adjustment",
        "target": "context_window_allocation",
        "previous_value": 0.6,
        "new_value": 0.75,
        "rationale": "Increase context retention capacity"
      },
      {
        "change_type": "parameter_adjustment",
        "target": "memory_consolidation_interval",
        "previous_value": 300,
        "new_value": 180,
        "rationale": "More frequent memory consolidation"
      }
    ],
    "outcomes": {
      "status": "completed_with_warnings",
      "metrics_delta": {
        "task_completion_rate": { "before": 0.72, "after": 0.78, "delta": 0.06 },
        "latency_ms": { "before": 245, "after": 267, "delta": 22 }
      },
      "warnings": ["Latency increased beyond target threshold"],
      "errors": []
    },
    "rollback_available": true,
    "rollback_id": "rollback-20260302-018",
    "validation_results": {
      "pre_deployment_checks": "passed",
      "smoke_tests": "passed",
      "integration_tests": "passed"
    },
    "artifacts_generated": [
      "cdgr-20260302-capability-001",
      "era-20260302-rec-042"
    ],
    "agent_version_before": "christine-v2.4.1",
    "agent_version_after": "christine-v2.4.2"
  }
}
```

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| `cycle_id` | string | Yes | Must be non-empty; unique identifier | Unique identifier for this evolution cycle |
| `start_time` | string | Yes | Must be ISO 8601 format | When the cycle started |
| `end_time` | string | Yes | Must be ISO 8601 format; must be >= start_time | When the cycle ended |
| `duration_minutes` | number | Yes | Must be non-negative | Duration of the cycle in minutes |
| `trigger_type` | string | Yes | Must be non-empty | What triggered this cycle (e.g., automatic_degradation, manual_request, scheduled, threshold_breach) |
| `trigger_details` | object | No | Additional trigger context | Details about what triggered the cycle |
| `changes_applied` | array | Yes | Must be non-empty array | List of changes made during this cycle |
| `outcomes` | object | Yes | Must contain status | Results of the evolution cycle |
| `rollback_available` | boolean | Yes | Must be boolean | Whether rollback is available for this cycle |
| `rollback_id` | string | No | Required if rollback_available is true | Identifier for rollback operation |
| `validation_results` | object | No | Results of pre-deployment validation | Validation test results |
| `artifacts_generated` | array | No | Array of artifact_id references | Other artifacts created during this cycle |
| `agent_version_before` | string | No | Version string | Agent version before cycle |
| `agent_version_after` | string | No | Version string | Agent version after cycle |

---

## Envelope Schema

All REP artifacts share a common envelope:

```json
{
  "rep_version": "1.0",
  "artifact_type": "decision_rejection_log",
  "artifact_id": "dec-abc12345",
  "session_id": "sess-xyz",
  "interaction_id": "msg-789",
  "created_at": "2026-02-28T06:00:00Z",
  "actor": { "id": "agent:christine", "role": "agent" },
  "content_hash": "sha256:abc123...",
  "prev_hash": "sha256:previous..."
}
```

---

## Bundle v1.0 Schema

REP v1.0 introduces a bundled format with a `manifest.json` file that encapsulates the entire evidence pack. This format provides enhanced integrity verification and metadata management.

### manifest.json Structure

```json
{
  "bundle_version": "1.0",
  "bundle_id": "bundle-abc123",
  "created_at": "2026-03-01T12:00:00Z",
  "created_by": "agent:christine",
  "description": "Evidence pack for Q1 reliability audit",
  "integrity_policy": "strict",
  "metadata": {
    "campaign_id": "campaign-2026-q1",
    "tags": ["reliability", "audit", "q1"],
    "expires_at": "2027-03-01T00:00:00Z",
    "custom_fields": {
      "project": "openclaw",
      "owner": "platform-team"
    }
  },
  "artifacts": {
    "decision_rejection_log": { "count": 12, "file": "artifacts/decision_rejection_log.jsonl" },
    "memory_reconstruction_audit": { "count": 5, "file": "artifacts/memory_reconstruction_audit.jsonl" },
    "handoff_acceptance_packet": { "count": 3, "file": "artifacts/handoff_acceptance_packet.jsonl" },
    "near_miss_reliability_trailer": { "count": 2, "file": "artifacts/near_miss_reliability_trailer.jsonl" },
    "signed_divergence_violation_record": { "count": 1, "file": "artifacts/signed_divergence_violation_record.jsonl" },
    "agent_heartbeat_record": { "count": 48, "file": "artifacts/agent_heartbeat_record.jsonl" },
    "context_snapshot": { "count": 7, "file": "artifacts/context_snapshot.jsonl" },
    "claim_file": { "count": 2, "file": "artifacts/claim_file.jsonl" },
    "error_recovery_log": { "count": 4, "file": "artifacts/error_recovery_log.jsonl" },
    "performance_baseline": { "count": 24, "file": "artifacts/performance_baseline.jsonl" },
    "model_switch_event": { "count": 1, "file": "artifacts/model_switch_event.jsonl" },
    "tool_execution_failure_record": { "count": 3, "file": "artifacts/tool_execution_failure_record.jsonl" },
    "session_context_loss_record": { "count": 2, "file": "artifacts/session_context_loss_record.jsonl" },
    "security_policy_violation": { "count": 1, "file": "artifacts/security_policy_violation.jsonl" }
  },
  "chain": {
    "first_hash": "sha256:abc123...",
    "last_hash": "sha256:def456...",
    "total_artifacts": 115
  },
  "integrity": {
    "root_hash": "sha256:chain-root-abc123...",
    "algorithm": "sha256",
    "computed_at": "2026-03-01T12:05:00Z"
  }
}
```

### integrity_policy Options

The `integrity_policy` field controls how strictly the bundle enforces validation rules:

| Policy | Behavior |
|--------|----------|
| `none` | No integrity checks performed; manifest is informational only |
| `warn` | Integrity violations are logged as warnings but do not fail validation |
| `strict` | Integrity violations cause validation to fail; all checks must pass |

**Strict Policy Requirements:**
- All `content_hash` values must match computed SHA256 of artifact content
- All `prev_hash` chains must be continuous (no gaps)
- All cross-references must resolve to existing artifacts
- All required fields must be present per artifact type

### Metadata Fields

The `metadata` object provides extensible key-value storage for bundle-level information:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `campaign_id` | string | No | Identifier for the campaign or project this bundle belongs to |
| `tags` | array | No | Array of string tags for categorization and filtering |
| `expires_at` | ISO 8601 | No | Timestamp when the bundle should be considered stale/archived |
| `custom_fields` | object | No | User-defined key-value pairs for application-specific data |

**Reserved Metadata Keys:**
- `campaign_id`, `tags`, `expires_at` are reserved by the REP system
- Custom fields should be placed under `custom_fields` to avoid conflicts

---

## CLI Commands

### Initialize Bundle
```bash
node scripts/rep.mjs init <directory>
```

### Create Artifact
```bash
node scripts/rep.mjs create --type decision --session sess-1 --actor agent:christine
```

### Validate Bundle
```bash
node scripts/rep.mjs validate rep-bundle.jsonl --require-pack --check-chain --xref
```

### Export Bundle
```bash
node scripts/rep.mjs export <input> --output <file> [--format markdown|json|html] [--include-metadata] [--filter-type <artifact_type>]
```

**Export Options:**

| Flag | Description |
|------|-------------|
| `<input>` | Input file (JSONL or manifest.json for bundled format) |
| `--output`, `-o` | Output file path |
| `--format` | Output format: `markdown` (default), `json`, `html` |
| `--include-metadata` | Include bundle metadata in output (for bundled format) |
| `--filter-type` | Only export artifacts of specified type |

**Examples:**
```bash
# Export to Markdown with metadata
node scripts/rep.mjs export bundle/manifest.json --output review.md --include-metadata

# Export only decision artifacts to JSON
node scripts/rep.mjs export artifacts/all.jsonl --output decisions.json --format json --filter-type decision_rejection_log

# Export to HTML report
node scripts/rep.mjs export bundle/manifest.html --output report.html --format html
```

---

## Validation Options

| Flag | Purpose |
|------|---------|
| `--require-pack` | Fail if required artifact types missing |
| `--check-chain` | Validate prev_hash chain continuity |
| `--xref` | Validate cross-artifact references exist |
| `--verify-hash` | Verify content_hash matches computed SHA256 |
| `--dedup` | Check for duplicate artifact_id values |

---

## Validation Rules

### Required Fields per Artifact Type

| Artifact Type | Required Fields |
|---------------|-----------------|
| `decision_rejection_log` | `decision`, `action_class`, `criteria`, `rationale` |
| `memory_reconstruction_audit` | `claim_ref`, `consistency_score`, `audit_outcome` |
| `handoff_acceptance_packet` | `handoff_id`, `sla`, `acceptance_criteria` |
| `near_miss_reliability_trailer` | `incident_id`, `potential_impact`, `containment_action` |
| `signed_divergence_violation_record` | `severity`, `signatures`, `disposition` |
| `agent_heartbeat_record` | `status`, `uptime_sec`, `tasks_active` |
| `context_snapshot` | `trigger`, `active_memory`, `decision_context` |
| `claim_file` | `change_summary`, `expected_files`, `rollback_method` |
| `error_recovery_log` | `error_type`, `recovery_strategy`, `attempt_count`, `outcome` |
| `performance_baseline` | `metric_name`, `baseline_value`, `current_value`, `sample_size` |
| `model_switch_event` | `trigger_reason`, `from_model`, `to_model`, `switch_overhead_ms` |
| `tool_execution_failure_record` | `tool_name`, `failure_type`, `error_message` |
| `session_context_loss_record` | `loss_type`, `trigger_event`, `recovery_method` |
| `security_policy_violation` | `violation_type`, `severity`, `policy_name` |
| `capability_degradation_record` | `metric_name`, `baseline_value`, `current_value`, `degradation_percent`, `trigger_threshold`, `detection_method`, `affected_capabilities`, `remediation_action` |
| `evolution_recommendation_accepted` | `recommendation_id`, `target_capability`, `expected_improvement`, `acceptance_rationale`, `implementation_plan`, `success_criteria` |
| `evolution_cycle_record` | `cycle_id`, `start_time`, `end_time`, `duration_minutes`, `trigger_type`, `changes_applied`, `outcomes`, `rollback_available` |

### Envelope Validation Rules

1. **rep_version**: Must be a valid semver string (e.g., "0.1", "0.2", "0.3", "0.4", "0.5", "0.6")
2. **artifact_type**: Must match one of the defined artifact types
3. **artifact_id**: Must be unique within the bundle; must follow naming convention `<type-abbrev>-<uuid/timestamp>`
4. **session_id**: Must be non-empty string if provided
5. **interaction_id**: Must be non-empty string if provided
6. **created_at**: Must be ISO 8601 format
7. **actor**: Must contain `id` field; `role` must be valid (agent, user, system)
8. **content_hash**: Must start with "sha256:" prefix followed by 64 hex characters
9. **prev_hash**: Must start with "sha256:" prefix OR be empty string for first artifact
10. **created_at ordering**: Artifacts within a session must have non-decreasing timestamps (chronological order enforcement)
11. **actor consistency**: Artifacts with the same `artifact_id` prefix (e.g., `dec-*`) should have consistent `actor.role` unless explicitly transitioning responsibility

### Cross-Reference Validation Rules

- `claim_ref` in `memory_reconstruction_audit` must reference a valid `artifact_id` from another artifact
- `incident_id` in `near_miss_reliability_trailer` must be unique within the bundle
- `handoff_id` in `handoff_acceptance_packet` must be unique within the bundle
- `trigger_event` in `session_context_loss_record` may reference a preceding `artifact_id` if causally related

### Hash Chain Validation Rules

- First artifact in a session must have `prev_hash` as empty string
- Each subsequent artifact must have `prev_hash` matching the `content_hash` of the previous artifact in chronological order
- Gaps in chain must be flagged as warnings (not errors) unless `--strict-chain` is used

---

## Best Practices

### When to Use Each Artifact Type

| Artifact Type | Use Case | Frequency |
|---------------|----------|-----------|
| `decision_rejection_log` | Any approval/rejection decision that blocks or allows action | Per decision |
| `memory_reconstruction_audit` | After memory recall tasks to verify accuracy | Post-recall |
| `handoff_acceptance_packet` | When transferring tasks between agents or sessions | Per handoff |
| `near_miss_reliability_trailer` | When incidents nearly occurred but were caught | Post-incident |
| `signed_divergence_violation_record` | When policy or SLA violations are detected | Per violation |
| `agent_heartbeat_record` | Long-running agents; monitors health | Every 5-15 min |
| `context_snapshot` | Before critical decisions or model switches | On trigger |
| `claim_file` | Before production deployments or changes | Per change |
| `error_recovery_log` | After any error recovery attempt | Per error |
| `performance_baseline` | Periodic performance measurement | Hourly/daily |
| `model_switch_event` | When model/provider changes mid-execution | Per switch |
| `tool_execution_failure_record` | When tool execution fails (exec, browser, API calls) | Per failure |
| `session_context_loss_record` | When session context is lost or corrupted | Per loss event |
| `security_policy_violation` | When security policies are violated | Per violation |

### Operational Guidance

- **High-volume artifacts** (`agent_heartbeat_record`, `performance_baseline`): Use automated generation via cron jobs to ensure consistent monitoring
- **Event-driven artifacts** (`decision_rejection_log`, `near_miss_reliability_trailer`): Emit on specific triggers; avoid over-logging
- **Audit-critical artifacts** (`signed_divergence_violation_record`, `claim_file`): Always include comprehensive `rationale` and `disposition` fields
- **Cross-referenced artifacts** (`memory_reconstruction_audit`, `handoff_acceptance_packet`): Validate that referenced `artifact_id`s exist before finalizing
- **Operational reliability artifacts** (`tool_execution_failure_record`, `session_context_loss_record`, `security_policy_violation`): Use for debugging and monitoring agent health; include execution context for root cause analysis

### Bundle Organization

- Group artifacts by `session_id` for clear audit trails
- Use `--xref` validation regularly to catch broken references
- Export bundles to Markdown for human review before archival

---

## Workflows

### Manual Workflow
1. Initialize bundle: `rep.mjs init my-campaign`
2. Create artifacts as events occur
3. Periodically validate: `rep.mjs validate my-campaign --require-pack`
4. Export for review: `rep.mjs export --output report.md`

### Automated Workflow (CI/CD)
```bash
# In CI pipeline
node scripts/rep-validate.mjs artifacts.jsonl --require-pack --check-chain --xref --json > validation.json
```

---

## Integration Points

### From Subagents
Subagents can emit REP artifacts by writing JSONL to the appropriate artifact file:

```javascript
// In subagent code
const artifact = {
  rep_version: '0.5',
  artifact_type: 'tool_execution_failure_record',
  artifact_id: `tef-${Date.now()}`,
  // ... other fields
  content_hash: computeHash(artifact),
};
fs.appendFileSync('artifacts/tool_execution_failure_record.jsonl', JSON.stringify(artifact) + '\n');
```

### From Cron Jobs
Cron jobs can generate `agent_heartbeat_record` and `near_miss_reliability_trailer` artifacts for operational visibility.

### Tool Execution Failure Tracking
When a tool fails, capture:
- Tool name and parameters (sanitized)
- Failure type (timeout, permission denied, invalid input, etc.)
- Error message and stack trace
- Retry count and recovery action taken
- Execution context for debugging

### Session Context Loss Tracking
When context loss occurs, capture:
- Loss type (session restart, memory overflow, explicit clear, etc.)
- Trigger event that caused the loss
- Summary of lost state
- Recovery method used
- Downtime experienced
- Any data that was preserved

---

## File Structure

```
rep-bundle/
├── manifest.json          # Bundle metadata
└── artifacts/
    ├── decision_rejection_log.jsonl
    ├── memory_reconstruction_audit.jsonl
    ├── handoff_acceptance_packet.jsonl
    ├── near_miss_reliability_trailer.jsonl
    ├── signed_divergence_violation_record.jsonl
    ├── agent_heartbeat_record.jsonl
    ├── context_snapshot.jsonl
    ├── claim_file.jsonl
    ├── error_recovery_log.jsonl
    ├── performance_baseline.jsonl
    ├── model_switch_event.jsonl
    ├── tool_execution_failure_record.jsonl
    ├── session_context_loss_record.jsonl
    ├── security_policy_violation.jsonl
    ├── capability_degradation_record.jsonl
    ├── evolution_recommendation_accepted.jsonl
    └── evolution_cycle_record.jsonl
```

---

## Version History

- **v0.1**: Required artifact types (5)
- **v0.2**: Added agent_heartbeat_record, context_snapshot, claim_file
- **v0.3**: Added error_recovery_log, performance_baseline; added validation rules section
- **v0.4**: Added model_switch_event; added timestamp ordering and actor consistency validation rules; added Best Practices section
- **v0.5**: Added tool_execution_failure_record, session_context_loss_record, security_policy_violation; added operational reliability tracking
- **v1.0**: Added bundle format with manifest.json; added integrity_policy options; added metadata fields; added new export command

---

## Changelog

### v0.1 → v0.2
- **Added**: `agent_heartbeat_record` artifact type for long-running agent health monitoring
- **Added**: `context_snapshot` artifact type for decision point context capture
- **Added**: `claim_file` artifact type for production change safety documentation
- **Updated**: Envelope schema version to "0.2"
- **Updated**: File structure to include new artifact JSONL files

### v0.2 → v0.3
- **Added**: `error_recovery_log` artifact type for tracking error recovery attempts with fields: error_type, recovery_strategy, attempt_count, outcome, time_to_recovery_ms
- **Added**: `performance_baseline` artifact type for tracking performance metrics over time with fields: metric_name, baseline_value, current_value, trend, sample_size, measurement_window
- **Added**: Validation Rules section with:
  - Required fields per artifact type table
  - Envelope validation rules (rep_version, artifact_type, artifact_id, timestamps, hashes)
  - Cross-reference validation rules
  - Hash chain validation rules
- **Updated**: Envelope schema version to "0.3"
- **Updated**: File structure to include new artifact JSONL files

### v0.3 → v0.4
- **Added**: `model_switch_event` artifact type for tracking model/provider switches during agent execution with fields: trigger_reason, from_model, to_model, switch_overhead_ms, context_preserved, fallback_enabled
- **Added**: Two new envelope validation rules:
  - Timestamp ordering: artifacts within a session must have non-decreasing timestamps
  - Actor consistency: artifacts with same prefix should have consistent actor.role unless transitioning responsibility
- **Added**: Best Practices section with guidance on when to use each artifact type, operational recommendations, and bundle organization tips
- **Updated**: Envelope schema version to "0.4"
- **Updated**: File structure to include new artifact JSONL file
- **Updated**: Required fields table to include `model_switch_event`

### v0.4 → v0.5
- **Added**: `tool_execution_failure_record` artifact type for tracking tool execution failures with fields: tool_name, failure_type, error_message, retry_count, recovery_action, execution_context
- **Added**: `session_context_loss_record` artifact type for tracking context loss events during agent sessions with fields: loss_type, trigger_event, lost_state_summary, recovery_method, downtime_ms, preserved_data
- **Added**: `security_policy_violation` artifact type for tracking security-related policy violations with fields: violation_type, severity, policy_name, detection_method, blocked_action, resolution, threat_indicators
- **Added**: Integration Points section with guidance on tracking tool failures, session context loss, and security violations
- **Updated**: Envelope schema version to "0.5"
- **Updated**: File structure to include three new artifact JSONL files
- **Updated**: Required fields table to include new v0.5 artifact types
- **Updated**: Best Practices section with operational reliability artifact guidance

### v0.5 → v1.0
- **Added**: Bundle v1.0 format with `manifest.json` for encapsulating entire evidence packs
- **Added**: `Bundle v1.0 Schema` section documenting:
  - manifest.json structure with all fields
  - `integrity_policy` options: `none`, `warn`, `strict`
  - Metadata fields including campaign_id, tags, expires_at, custom_fields
- **Added**: New `export` command with options:
  - `--format` for output format (markdown/json/html)
  - `--include-metadata` for bundle metadata inclusion
  - `--filter-type` for artifact type filtering
- **Updated**: CLI Commands section with comprehensive export command documentation

---

*Generated: 2026-03-02*
