# REP Adoption Workflow: Capability Evolver Integration

This example demonstrates how the Reliability Engineering Protocol (REP) tracks and monitors the reliability of the capability-evolver system.

## Overview

REP provides a structured approach to monitoring evolver reliability by:

1. **Detecting capability degradation** - Identifying when evolver capabilities degrade below acceptable thresholds
2. **Tracking evolution recommendations** - Recording when recommendations are accepted and their outcomes
3. **Logging evolution cycles** - Maintaining a complete audit trail of evolution cycles

## v0.6 Artifact Types

### 1. Capability Degradation Record
Tracks when and how capabilities degrade over time.

```json
{
  "artifact_type": "capability_degradation_record",
  "version": "0.6",
  "capability_id": "evolver.balanced.loop",
  "degradation_metrics": {
    "success_rate": 0.72,
    "threshold": 0.85,
    "consecutive_failures": 5,
    "latency_p95_ms": 2500
  },
  "detected_at": "2026-03-02T02:15:00Z",
  "severity": "warning"
}
```

### 2. Evolution Recommendation Accepted
Records when an evolution recommendation is accepted and the reasoning.

```json
{
  "artifact_type": "evolution_recommendation_accepted",
  "version": "0.6",
  "recommendation_id": "evolve-2026-0302-001",
  "triggered_by": "capability_degradation_record",
  "trigger_id": "deg-evolver-balanced-0302",
  "accepted_at": "2026-03-02T02:20:00Z",
  "evolution_strategy": "parameter_adjustment",
  "target_parameters": {
    "mutation_rate": 0.15,
    "crossover_rate": 0.7,
    "population_size": 50
  }
}
```

### 3. Evolution Cycle Record
Complete log of an evolution cycle execution.

```json
{
  "artifact_type": "evolution_cycle_record",
  "version": "0.6",
  "cycle_id": "cycle-2026-0302-001",
  "started_at": "2026-03-02T02:25:00Z",
  "completed_at": "2026-03-02T02:45:00Z",
  "recommendation_id": "evolve-2026-0302-001",
  "evolution_type": "parameter_adjustment",
  "outcomes": {
    "success": true,
    "success_rate_improvement": 0.18,
    "final_success_rate": 0.90,
    "iterations": 12
  }
}
```

## Example Files

| File | Description |
|------|-------------|
| `degradation_records.jsonl` | Example degradation detection events |
| `recommendations_accepted.jsonl` | Example accepted evolution recommendations |
| `evolution_cycles.jsonl` | Example evolution cycle executions |
| `manifest.json` | Bundle metadata and file listing |

## Usage

1. **Monitor degradation** - Process `degradation_records.jsonl` to detect reliability issues
2. **Track recommendations** - Use `recommendations_accepted.jsonl` to audit decision-making
3. **Audit cycles** - Review `evolution_cycles.jsonl` for complete evolution history

## Integration Points

REP integrates with the capability-evolver via:

- **Degradation Detection**: Evolver reports capability metrics → REP creates degradation records
- **Recommendation Tracking**: REP publishes recommendations → System accepts → REP **Cycle Logging**: logs acceptance
- Evolver executes cycles → REP captures outcomes for audit

## Reliability Metrics

The following metrics are tracked:

- **Success Rate**: Percentage of successful evolutions
- **Latency P95**: 95th percentile evolution time
- **Consecutive Failures**: Failures in sequence before intervention
- **Recovery Time**: Time from degradation detection to resolution
