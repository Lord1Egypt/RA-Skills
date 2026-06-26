# Specialization: Data Pipeline / Data Platform

Apply this guidance for ETL, ELT, data warehouse, data lake, streaming, and analytics platform designs.

## Phase 3 — Data Pipeline Architecture Patterns

| Pattern | When to choose |
|---------|---------------|
| Batch ETL | Latency tolerance hours/days; large volume; simple transforms |
| Streaming (Lambda) | Real-time + batch coexist; complex state management |
| Streaming-only (Kappa) | All processing as streams; late data handled by reprocessing |
| ELT (load first, transform in warehouse) | Cloud DW available; raw data preservation needed |
| Medallion (Bronze/Silver/Gold) | Data lake; incremental quality improvement; multiple consumer types |

## Phase 5 — Critical Flows for Data Pipelines

1. **Ingestion flow**: source → extract → validate → land (raw)
2. **Transform flow**: raw → clean → enrich → aggregate
3. **Serving flow**: aggregated data → query engine → consumer (BI, API, ML)
4. **Backfill / reprocessing flow**: historical data re-ingestion on schema/logic change
5. **Data quality check flow**: record → validation rules → quarantine or pass

## Phase 6 — Storage Layers

| Layer | Purpose | Technology options |
|-------|---------|-------------------|
| Landing (raw) | Exact copy of source, immutable | Object storage (S3/MinIO), file system |
| Staging | Cleaned, typed, deduplicated | Parquet on object storage |
| Curated | Business-ready aggregates | Data warehouse (PostgreSQL, ClickHouse, BigQuery) |
| Serving | Low-latency query | Columnar DB, materialized views, Redis cache |
| Metadata | Lineage, schema, quality stats | Relational DB (PostgreSQL) |

## Phase 7 — Data Pipeline Decision Points

| Decision | Key question | Options |
|----------|-------------|---------|
| Batch vs stream | What is the acceptable latency? | minutes → micro-batch; seconds → streaming |
| Orchestration | How many pipelines? Complex dependencies? | Cron → Airflow → Prefect/Dagster |
| Transform engine | Data volume? Team language? | SQL (dbt) vs Python (Spark/Pandas) vs Beam |
| Messaging | Throughput and durability? | Redis Streams → RabbitMQ → Kafka |
| Schema management | Schema evolution needed? | None → JSON Schema → Avro/Protobuf |

## Phase 8 — Data Pipeline Interface Design

Define these contracts explicitly:

- **Source connectors**: protocol, auth, extraction mode (full / incremental / CDC), rate limits
- **Schema registry**: where schemas are defined, how consumers discover them
- **Data quality contract**: which fields are required, valid ranges, uniqueness constraints
- **SLA contract**: ingestion frequency, max latency, freshness guarantee

## Phase 9 — Deployment Patterns

| Pattern | Scale | Notes |
|---------|-------|-------|
| Single server + cron | Small, < 10 pipelines | Simple, low ops overhead |
| Docker Compose + Airflow | Medium, < 100 pipelines | Managed scheduling |
| Kubernetes + Helm | Large, 100+ pipelines, multi-tenant | Complex ops, full isolation |
| Cloud-managed (Glue, Dataflow) | Cloud-first | Reduces ops, higher cost |

## Phase 10 — Data Pipeline NFR

- **Idempotency**: every pipeline run must be safe to re-run without duplicating data
- **Exactly-once semantics**: define per pipeline whether at-least-once or exactly-once is required
- **Data retention**: define per layer — raw data kept longer than curated
- **Lineage tracking**: every output table must know its source tables and transform version
- **Alerting on data quality**: failed quality checks must trigger alerts, not silently pass bad data
- **Backpressure**: streaming pipelines must handle source bursts without data loss
