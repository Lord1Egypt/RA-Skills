# Inspection monitor API reference

## Scope

This reference is only for the simplified PostgreSQL inspection skill.

The goal is to collect a small set of monitor facts and return a stable inspection result with minimal branching.

## Preferred monitor actions

Use the Tencent Cloud monitor API actions below:

- `DescribeProductList`: confirm the monitor product when needed
- `DescribeBaseMetrics`: discover which PostgreSQL metrics are supported
- `GetMonitorData`: fetch monitor data for the target metric
- `DescribeStatisticData`: fetch monitor data with dimension filtering when needed

## Fixed inspection workflow

1. Confirm region, instance ID, and optional time window.
2. Normalize the region.
3. Use `DescribeBaseMetrics` first to confirm which PostgreSQL metrics are available.
4. Pull only the fixed inspection metrics that are actually supported.
5. Return results in a stable output format without expanding the workflow.

## Recommended metric set

The skill should prefer the following basic metrics when they are available:

- CPU usage
- memory usage
- storage usage or remaining storage
- connection count
- disk I/O related metric
- replication delay

If a metric is not supported by the monitor API for the current target, return `unsupported` instead of guessing.

## Output schema

### 1. Executive summary
- overall inspection status: `normal` / `attention` / `abnormal` / `manual review needed`
- 2-4 key findings written as short operations-report bullets
- summary counts when useful, such as how many metrics are `available`, `unsupported`, or `no-data`

### 2. Inspection target
- Region
- Instance ID
- Time window
- monitor actions used

### 3. Health snapshot
For each major metric area include a short line with:
- metric area or metric name
- latest value or summarized value
- unit if available
- observation label: `normal` / `attention` / `abnormal` / `manual review needed`
- short fact-only note

### 4. Metric details
For each metric include:
- metric name
- latest value or summarized value
- unit if available
- data status: `available` / `unsupported` / `no-data`
- optional note if the API returns partial data only

### 5. Risk and manual review items
Only include items that are directly supported by metric status or returned values, such as:
- metrics in `attention` or `abnormal`
- unsupported critical metrics
- `no-data` areas that limit confidence

### 6. Data notes
- unsupported metrics list
- no-data metrics list
- whether the result is a point-in-time view or a summarized window view

If a metric cannot be safely judged, use `manual review needed`.

## Guardrails

- Do not use PostgreSQL management actions in this skill.
- Do not output remediation actions.
- Do not correlate metrics into root-cause conclusions.
- Do not fabricate thresholds, values, or unavailable metrics.
