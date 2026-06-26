#!/bin/bash
# Analytics Self-Improvement Error Detector Hook
# Triggers on PostToolUse for Bash to detect pipeline errors, data quality issues, and query failures
# Reads CLAUDE_TOOL_OUTPUT environment variable

set -e

OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

ERROR_PATTERNS=(
    "ETL"
    "pipeline"
    "DAG"
    "freshness"
    "stale"
    "NULL"
    "schema"
    "mismatch"
    "anomaly"
    "outlier"
    "duplicate"
    "missing data"
    "timeout"
    "partition"
    "lineage"
    "ERROR"
    "FAILED"
    "error:"
    "Error:"
    "failed"
    "Traceback"
    "sqlalchemy"
    "OperationalError"
    "ProgrammingError"
    "IntegrityError"
    "DataError"
    "constraint"
    "violation"
    "deadlock"
    "query timeout"
    "out of memory"
    "skew"
    "data drift"
    "row count"
    "zero rows"
    "empty result"
    "type mismatch"
    "cast failed"
    "invalid date"
    "overflow"
    "truncated"
    "dbt"
    "Airflow"
    "Dagster"
    "Fivetran"
    "stitch"
    "WARN"
    "SLA"
    "breach"
)

contains_error=false
for pattern in "${ERROR_PATTERNS[@]}"; do
    if [[ "$OUTPUT" == *"$pattern"* ]]; then
        contains_error=true
        break
    fi
done

if [ "$contains_error" = true ]; then
    cat << 'EOF'
<analytics-error-detected>
A data/analytics error was detected in command output. Consider logging to .learnings/ if:
- Pipeline failure required investigation → DATA_ISSUES.md [DAT-YYYYMMDD-XXX]
- Query error revealed a data model issue → DATA_ISSUES.md with schema_drift trigger
- Data quality problem with non-trivial root cause → DATA_ISSUES.md with data_quality trigger
- Metric anomaly or unexpected values → LEARNINGS.md with metric_drift category
- Freshness SLA breach detected → DATA_ISSUES.md with freshness_issue trigger
- Conflicting definitions discovered → LEARNINGS.md with definition_mismatch category

Include SQL snippets, affected tables/columns, pipeline name, and area tag.
</analytics-error-detected>
EOF
fi
