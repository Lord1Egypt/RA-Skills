# Custom Metrics — Self-Smarter-Everyday

## Overview

This guide covers defining, collecting, tracking, and acting on custom improvement metrics within the self-smarter-everyday framework. While the skill ships with a set of default metrics covering response quality, token efficiency, error rate, and memory utilization, real-world deployments benefit enormously from domain-specific metrics that capture the aspects of performance that actually matter for the agent's role. This guide walks through the complete lifecycle of a custom metric: from definition and data collection through baseline establishment, trend analysis, alerting, visualization, and reporting. By the end, you will be able to create metrics that give you genuine insight into your agent's improvement trajectory and trigger actionable responses when performance deviates from expectations.

## Metric Definition Format

Custom metrics are defined in the configuration file under the `audit.custom_metrics` array. Each metric follows a structured definition format that specifies the metric's identity, data source, calculation logic, target range, and role in the composite score. Understanding each field is essential for creating metrics that produce meaningful and actionable data.

The metric definition consists of these fields. The `name` field is a unique identifier using snake_case convention. The `description` field is a human-readable explanation of what the metric measures and why it matters. The `source` field identifies where the raw data comes from — this can be a log file path, a database table, an API endpoint, or a computed value derived from other metrics. The `filter` field is an optional expression that selects a subset of the source data. The `formula` field defines how the raw data is transformed into a metric value. The `unit` field specifies the measurement unit for display purposes. The `target_range` field defines the acceptable range as a two-element array of minimum and maximum values. The `weight` field determines how much this metric contributes to the composite improvement score. The `aggregation` field specifies how multiple data points are combined: `mean`, `median`, `percentile`, `sum`, `count`, `min`, or `max`. The `sampling` field controls how often the metric is evaluated: `per_interaction`, `hourly`, `daily`, or `per_nightly_run`.

Here is a complete example of a custom metric definition for measuring task completion quality. This metric examines all tasks completed during the day, scores each on a scale from zero to one based on whether the task output matched the expected format and content requirements, and reports the average quality score.

```json
{
  "name": "task_completion_quality",
  "description": "Average quality score of completed tasks based on output validation against expected format and content requirements. Higher is better, target is above 0.85.",
  "source": "task_log",
  "source_path": "~/self-smarter-everyday/logs/task-completions.jsonl",
  "filter": "status == 'completed' AND validation_run == true",
  "formula": "mean(quality_scores)",
  "unit": "score_0_to_1",
  "target_range": [0.85, 1.0],
  "weight": 0.25,
  "aggregation": "mean",
  "sampling": "daily",
  "data_type": "float",
  "precision": 3
}
```

## Data Collection

Metrics are only as good as the data that feeds them. The self-smarter-everyday skill provides several mechanisms for collecting the raw data that custom metrics depend on. Understanding these mechanisms helps you design metrics that are reliably fed by the available data infrastructure.

The primary data collection mechanism is the interaction logger. Every agent interaction can be logged to a JSONL file with a structured schema that includes timestamps, input/output content, metadata about the task type, and outcome indicators. To enable interaction logging, add the following to your agent configuration:

```json
{
  "data_collection": {
    "interaction_log": {
      "enabled": true,
      "path": "~/self-smarter-everyday/logs/interactions.jsonl",
      "fields": [
        "timestamp",
        "task_type",
        "input_summary",
        "output_summary",
        "tokens_used",
        "duration_seconds",
        "error_occurred",
        "quality_score",
        "user_feedback"
      ],
      "rotation": {
        "max_file_size_mb": 100,
        "retain_files": 30,
        "compress_old": true
      }
    },
    "memory_access_log": {
      "enabled": true,
      "path": "~/self-smarter-everyday/logs/memory-access.jsonl",
      "fields": ["timestamp", "tier", "access_type", "entry_id", "relevance_score"]
    },
    "error_log": {
      "enabled": true,
      "path": "~/self-smarter-everyday/logs/errors.jsonl",
      "fields": ["timestamp", "error_type", "error_message", "task_context", "recovery_action"]
    }
  }
}
```

For metrics that require data from external systems, the skill supports data ingestion hooks. These hooks run before the nightly routine and pull data from external sources into local files that the metric formulas can reference. Supported hook types include HTTP fetch for REST APIs, file copy for shared network drives, database query for SQL databases, and command execution for CLI tools.

```json
{
  "data_collection": {
    "ingestion_hooks": [
      {
        "name": "pull_customer_feedback",
        "type": "http_fetch",
        "url": "https://api.example.com/feedback/today",
        "headers": {"Authorization": "Bearer YOUR_API_TOKEN"},
        "output_path": "~/self-smarter-everyday/data/customer-feedback.json",
        "schedule": "pre_nightly"
      },
      {
        "name": "pull_task_metrics",
        "type": "database_query",
        "connection": "postgresql://readonly:YOUR_PASSWORD@db.example.com:5432/analytics",
        "query": "SELECT task_id, quality_score, completion_time FROM tasks WHERE completed_at >= CURRENT_DATE",
        "output_path": "~/self-smarter-everyday/data/task-metrics.json",
        "schedule": "pre_nightly"
      }
    ]
  }
}
```

## Baseline Establishment

Before a metric can be used for improvement tracking, a baseline must be established. The baseline represents the agent's normal performance level before any self-improvement interventions take effect. Without a baseline, it is impossible to determine whether a metric change represents improvement or degradation.

The skill automatically establishes baselines during the first seven days of operation. During this period, metrics are collected but not used for improvement decisions. Instead, they are stored as baseline data. After seven days, the system computes baseline statistics including the mean, standard deviation, and percentile distribution for each metric. These baselines are persisted in `~/self-smarter-everyday/data/baselines.json`.

You can also manually establish baselines if you have historical data. Create a baseline file with the following structure:

```json
{
  "metric_name": "task_completion_quality",
  "baseline_period": {"start": "2026-07-01", "end": "2026-07-31"},
  "statistics": {
    "mean": 0.78,
    "std_dev": 0.08,
    "p25": 0.72,
    "p50": 0.79,
    "p75": 0.84,
    "min": 0.55,
    "max": 0.95,
    "sample_count": 450
  },
  "established_at": "2026-08-01T02:00:00Z",
  "method": "historical_data"
}
```

## Trend Analysis

Once baselines are established, the nightly routine tracks trends by comparing current metric values against the baseline and against historical values. The trend analysis system identifies several patterns: sustained improvement where the metric consistently moves toward the target range, sustained degradation where the metric consistently moves away from the target range, oscillation where the metric bounces around without clear direction, and step change where the metric suddenly shifts to a new level and stabilizes there.

Trend data is stored in `~/self-smarter-everyday/data/trends/` with one file per metric. Each file contains a time series of daily values along with computed trend indicators. The trend analysis feeds directly into the improvement planning phase — metrics showing sustained degradation trigger high-priority improvement actions, while metrics showing sustained improvement are noted as strengths to be maintained.

## Alerting Thresholds

Alerts fire when metrics deviate significantly from expected ranges. The alerting system supports multiple severity levels and notification channels. Alerts are configured per-metric in the custom metric definition or globally in the alerting configuration.

```json
{
  "alerting": {
    "rules": [
      {
        "metric": "task_completion_quality",
        "conditions": [
          {"severity": "info", "condition": "value < target_range[0] * 1.1", "message": "Quality approaching lower bound"},
          {"severity": "warning", "condition": "value < target_range[0]", "message": "Quality below target minimum"},
          {"severity": "critical", "condition": "value < baseline_mean - 2 * baseline_std_dev", "message": "Quality significantly below baseline"}
        ],
        "cooldown_hours": 24,
        "channels": ["file_log", "webhook"]
      }
    ],
    "channels": {
      "file_log": {
        "path": "~/self-smarter-everyday/logs/alerts.jsonl"
      },
      "webhook": {
        "url": "https://your-monitoring.example.com/alerts",
        "headers": {"Authorization": "Bearer YOUR_WEBHOOK_TOKEN"},
        "template": "alert_payload.json"
      }
    }
  }
}
```

## Visualization Examples

The skill generates visualization data in formats compatible with common charting tools. For markdown-based reports, ASCII trend charts are generated inline. For integration with Grafana or similar tools, the Prometheus export provides time-series data ready for graphing.

An example ASCII trend chart included in the nightly report looks like this:

```
Task Completion Quality — Last 14 Days
Target: [0.85 ─────────────────── 1.00]

Aug 10 ████████████████████░░░░░ 0.82 ↓
Aug 09 ███████████████████░░░░░░ 0.79 ↓
Aug 08 ██████████████████░░░░░░░ 0.76 ↓
Aug 07 █████████████████░░░░░░░░ 0.74 ↓
Aug 06 ████████████████░░░░░░░░░ 0.71 ↓
Aug 05 █████████████████████░░░░ 0.84 ─
Aug 04 ██████████████████████░░░ 0.87 ✓
Aug 03 ███████████████████████░░ 0.89 ✓
Aug 02 ████████████████████████░ 0.91 ✓
Aug 01 ████████████████████████░ 0.90 ✓
Jul 31 █████████████████████████ 0.93 ✓
Jul 30 ████████████████████████░ 0.91 ✓
Jul 29 ███████████████████████░░ 0.88 ✓
Jul 28 ██████████████████████░░░ 0.86 ✓

Legend: ✓ within target  ─ near boundary  ↓ below target
```

## Reporting Templates

Custom metrics are included in the nightly improvement report in a dedicated section. You can customize the report template to highlight the metrics that matter most for your deployment. The report template uses Jinja2 syntax and has access to all metric values, trend data, alert status, and baseline comparisons.

```markdown
## Custom Metrics Dashboard

| Metric | Current | Target | Trend | Status |
|--------|---------|--------|-------|--------|
{% for metric in custom_metrics %}
| {{ metric.name }} | {{ metric.current_value }} | {{ metric.target_range }} | {{ metric.trend_arrow }} | {{ metric.status_emoji }} |
{% endfor %}

### Metric Highlights

{% for metric in custom_metrics if metric.status == 'critical' %}
**⚠️ {{ metric.name }}**: {{ metric.current_value }} (target: {{ metric.target_range }})
- Delta from baseline: {{ metric.baseline_delta }}
- Days below target: {{ metric.days_below_target }}
- Suggested action: {{ metric.suggested_action }}
{% endfor %}
```

This template generates a compact dashboard showing all custom metrics at a glance, followed by detailed callouts for any metrics in critical status. The suggested action field is populated by the improvement planning phase based on the nature and severity of the metric deviation.

## Best Practices

When designing custom metrics, follow these principles. First, start with fewer metrics and add more only when you have a clear action plan for each one. A metric without an associated action is just noise. Second, ensure every metric has a clear target range — metrics without targets cannot trigger meaningful alerts. Third, validate your metrics during the baseline period by checking that they produce stable, sensible values before relying on them for improvement decisions. Fourth, review metric relevance monthly — remove metrics that consistently stay within target and are not driving improvements. Fifth, correlate custom metrics with the composite score to ensure they are contributing meaningfully to the overall improvement trajectory. If a custom metric never influences the improvement plan, consider whether it deserves its weight in the composite calculation.
