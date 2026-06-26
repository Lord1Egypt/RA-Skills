# Changelog

All notable changes to the Reliability Evidence Pack (REP) specification are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-02

### Added

#### New Artifact Types (v0.6)

- **`capability_degradation_record`**: Tracks agent capability degradation over time
  - Fields: `metric_name`, `baseline_value`, `current_value`, `degradation_percent`, `trigger_threshold`, `detection_method`, `affected_capabilities`, `remediation_action`
  - Optional fields: `measurement_window`, `sample_size`, `confidence_interval`, `trend_direction`, `consecutive_degradation_cycles`, `notes`
  - Use case: Documents when agent capabilities degrade below acceptable thresholds, triggering evolution workflows

- **`evolution_recommendation_accepted`**: Tracks when evolver recommendations are accepted
  - Fields: `recommendation_id`, `target_capability`, `expected_improvement`, `acceptance_rationale`, `implementation_plan`, `success_criteria`
  - Optional fields: `risk_assessment`, `requested_by`, `approved_by`, `priority`, `estimated_implementation_hours`
  - Use case: Records when an evolution recommendation is accepted and queued for implementation

- **`evolution_cycle_record`**: Documents each evolution cycle execution
  - Fields: `cycle_id`, `start_time`, `end_time`, `duration_minutes`, `trigger_type`, `changes_applied`, `outcomes`, `rollback_available`
  - Optional fields: `trigger_details`, `rollback_id`, `validation_results`, `artifacts_generated`, `agent_version_before`, `agent_version_after`
  - Use case: Provides complete audit trail of evolution cycle execution including changes applied and outcomes

#### Bundle Format (v1.0)

- **manifest.json**: New bundled format that encapsulates the entire evidence pack
  - `bundle_version`: Version identifier for the bundle format
  - `bundle_id`: Unique identifier for the bundle
  - `created_at`, `created_by`: Bundle creation metadata
  - `description`: Human-readable description
  - `artifacts`: Object mapping artifact types to file paths and counts
  - `chain`: First and last hash references with total artifact count
  - `integrity`: Root hash, algorithm, and computation timestamp

- **`integrity_policy`**: Controls validation strictness
  - `none`: No integrity checks; manifest is informational only
  - `warn`: Violations logged as warnings; validation passes
  - `strict`: All integrity violations cause validation failure

- **Metadata fields**: Extensible key-value storage
  - `campaign_id`: Campaign or project identifier
  - `tags`: Array of string tags for categorization
  - `expires_at`: Timestamp when bundle becomes stale/archived
  - `custom_fields`: User-defined key-value pairs

#### CLI Commands

- **`export` command**: New command for exporting bundles
  - `--format`: Output format (`markdown`, `json`, `html`)
  - `--include-metadata`: Include bundle metadata in output
  - `--filter-type`: Export only artifacts of specified type
  - `-o/--output`: Output file path

### Changed

#### Hash Format

- **Content hash**: All artifacts now include `content_hash` (SHA256) for integrity verification
- **Hash chain**: `prev_hash` field links artifacts chronologically
  - First artifact in a session: `prev_hash` is empty string
  - Subsequent artifacts: `prev_hash` must match previous artifact's `content_hash`
  - Gaps in chain flagged as warnings (unless `--strict-chain` is used)

#### Validation Rules

- **Timestamp ordering**: Artifacts within a session must have non-decreasing timestamps
- **Actor consistency**: Artifacts with same prefix should have consistent `actor.role` unless explicitly transitioning responsibility
- **Cross-reference validation**: 
  - `claim_ref` in `memory_reconstruction_audit` must reference valid `artifact_id`
  - `incident_id` and `handoff_id` must be unique within bundle
  - `trigger_event` in `session_context_loss_record` may reference preceding `artifact_id`

#### Envelope Schema

- **rep_version**: Now accepts "1.0" in addition to "0.x" versions
- **artifact_type**: Expanded to include 3 new v0.6 types

### Updated File Structure

```
rep-bundle/
├── manifest.json              # NEW: Bundle metadata (v1.0)
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
    ├── capability_degradation_record.jsonl    # NEW (v0.6)
    ├── evolution_recommendation_accepted.jsonl # NEW (v0.6)
    └── evolution_cycle_record.jsonl            # NEW (v0.6)
```

### Migration Notes

1. **Bundle format**: Existing JSONL artifacts can be wrapped in a manifest.json to create a v1.0 bundle
2. **Hash chain**: When migrating existing artifacts, ensure `prev_hash` is set correctly or leave empty for first artifact
3. **New artifact types**: Add the three new artifact files to existing bundles to support capability evolution tracking

---

## [0.5.0] - 2025-??-??

### Added

- **`tool_execution_failure_record`**: Tracks tool execution failures and diagnostics
  - Fields: `tool_name`, `failure_type`, `error_message`, `retry_count`, `recovery_action`, `execution_context`

- **`session_context_loss_record`**: Tracks context loss events during agent sessions
  - Fields: `loss_type`, `trigger_event`, `lost_state_summary`, `recovery_method`, `downtime_ms`, `preserved_data`

- **`security_policy_violation`**: Tracks security-related policy violations
  - Fields: `violation_type`, `severity`, `policy_name`, `detection_method`, `blocked_action`, `resolution`, `threat_indicators`

- **Integration Points section**: Guidance on tracking tool failures, session context loss, and security violations

---

## [0.4.0] - 2025-??-??

### Added

- **`model_switch_event`**: Tracks model/provider switches during agent execution
  - Fields: `trigger_reason`, `from_model`, `to_model`, `switch_overhead_ms`, `context_preserved`, `fallback_enabled`

- **New validation rules**:
  - Timestamp ordering: artifacts within a session must have non-decreasing timestamps
  - Actor consistency: artifacts with same prefix should have consistent `actor.role`

- **Best Practices section**: Guidance on when to use each artifact type

---

## [0.3.0] - 2025-??-??

### Added

- **`error_recovery_log`**: Tracks error recovery attempts
  - Fields: `error_type`, `recovery_strategy`, `attempt_count`, `outcome`, `time_to_recovery_ms`

- **`performance_baseline`**: Tracks performance metrics over time
  - Fields: `metric_name`, `baseline_value`, `current_value`, `trend`, `sample_size`, `measurement_window`

- **Validation Rules section**:
  - Required fields per artifact type
  - Envelope validation rules
  - Cross-reference validation rules
  - Hash chain validation rules

---

## [0.2.0] - 2025-??-??

### Added

- **`agent_heartbeat_record`**: Long-running agent health monitoring
  - Fields: `status`, `uptime_sec`, `tasks_active`

- **`context_snapshot`**: Decision point context capture
  - Fields: `trigger`, `active_memory`, `decision_context`

- **`claim_file`**: Production change safety documentation
  - Fields: `change_summary`, `expected_files`, `rollback_method`

---

## [0.1.0] - 2025-??-??

### Added

- **Initial artifact types**:
  - `decision_rejection_log`: Documents approval/rejection decisions
  - `memory_reconstruction_audit`: Verifies memory recall accuracy
  - `handoff_acceptance_packet`: Formal task transfer with SLA
  - `near_miss_reliability_trailer`: Captures near-miss incidents
  - `signed_divergence_violation_record`: Tracks policy/SLA violations

- **Envelope schema**: Common structure for all artifacts
  - `rep_version`, `artifact_type`, `artifact_id`
  - `session_id`, `interaction_id`, `created_at`
  - `actor`, `content_hash`, `prev_hash`

- **CLI Commands**: `init`, `create`, `validate`

---

[Unreleased]: https://github.com/openclaw/rep/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/openclaw/rep/releases/tag/v1.0.0
[0.5.0]: https://github.com/openclaw/rep/releases/tag/v0.5.0
[0.4.0]: https://github.com/openclaw/rep/releases/tag/v0.4.0
[0.3.0]: https://github.com/openclaw/rep/releases/tag/v0.3.0
[0.2.0]: https://github.com/openclaw/rep/releases/tag/v0.2.0
[0.1.0]: https://github.com/openclaw/rep/releases/tag/v0.1.0
