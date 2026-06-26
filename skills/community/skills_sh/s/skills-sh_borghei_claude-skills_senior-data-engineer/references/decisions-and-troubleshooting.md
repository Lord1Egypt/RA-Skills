# Architecture Decisions, Anti-Patterns & Troubleshooting

Read this when choosing batch vs streaming or warehouse vs lakehouse, avoiding common pipeline mistakes, or diagnosing pipeline failures.

## Architecture Decision Framework

| Question | Batch | Streaming |
|----------|-------|-----------|
| Latency requirement | Hours to days | Seconds to minutes |
| Processing complexity | Complex transforms, ML | Simple aggregations |
| Cost sensitivity | More cost-effective | Higher infra cost |
| Error handling | Easy reprocessing | Requires careful DLQ design |

**Decision tree:**
```
Real-time insight needed?
  Yes -> Exactly-once needed?
    Yes -> Kafka + Flink/Spark Structured Streaming
    No  -> Kafka + consumer groups
  No  -> Daily volume > 1TB?
    Yes -> Spark/Databricks
    No  -> dbt + warehouse compute
```

| Feature | Warehouse (Snowflake/BigQuery) | Lakehouse (Delta/Iceberg) |
|---------|-------------------------------|---------------------------|
| Best for | BI, SQL analytics | ML, unstructured data |
| Storage cost | Higher (proprietary) | Lower (open formats) |
| Flexibility | Schema-on-write | Schema-on-read |

## Anti-Patterns

1. **Full table reload on every run** -- use incremental loads with watermark columns.
2. **No dead letter queue** -- failed records silently dropped. Always route failures to a DLQ.
3. **Timezone mismatch** -- normalize all timestamps to UTC at extraction.
4. **Missing freshness checks** -- add `dbt source freshness` before transforms start.
5. **Skipping schema drift detection** -- use `mergeSchema` option or data contracts to catch new columns.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Pipeline silently produces zero rows | Timezone mismatch on watermark column | Normalize to UTC; add row-count assertion |
| Spark shuffle 10x slower than expected | Data skew on join key | Salt the key or broadcast the smaller table |
| Airflow shows "no tasks to run" | Circular dependency or import error | `airflow dags list-import-errors`; fix import |
| dbt succeeds but dashboards stale | Source freshness not checked | Add `dbt source freshness` as prerequisite task |
| Kafka consumer lag grows unbounded | Throughput < producer rate | Increase partitions, scale consumers, batch `max.poll.records` |
| Quality validator false-positive anomalies | Z-score threshold too tight | Raise threshold or switch to IQR mode |
