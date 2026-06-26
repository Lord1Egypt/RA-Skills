# Entry Examples

Concrete examples of well-formatted analytics entries with all fields.

## Learning: Data Quality (NULL Values After Migration)

```markdown
## [LRN-20250415-001] data_quality

**Logged**: 2025-04-15T10:30:00Z
**Priority**: high
**Status**: pending
**Area**: ingestion

### Summary
NULL values in user_id column after source system migration from Oracle to PostgreSQL

### Details
Source system migration changed the user table's primary key generation strategy. The Oracle
sequence-based IDs were replaced with PostgreSQL UUIDs, but the ETL pipeline's NOT NULL
validation was applied after a type-cast step that silently converted empty strings to NULLs.
The old Oracle export never produced empty strings for user_id, so the pipeline had no guard
against this scenario. 14,000 rows (2.3% of daily load) arrived with NULL user_id over 3 days
before the freshness monitor caught the downstream impact.

### SQL Example

**Before (no guard):**
\`\`\`sql
INSERT INTO warehouse.dim_users (user_id, name, email)
SELECT
    CAST(src.user_id AS VARCHAR(64)),
    src.name,
    src.email
FROM staging.users_raw src
\`\`\`

**After (with validation):**
\`\`\`sql
INSERT INTO warehouse.dim_users (user_id, name, email)
SELECT
    CAST(src.user_id AS VARCHAR(64)),
    src.name,
    src.email
FROM staging.users_raw src
WHERE src.user_id IS NOT NULL
    AND TRIM(src.user_id) <> ''
\`\`\`

### Suggested Action
Add NOT NULL and non-empty validation at ingestion layer before any transformations.
Add a dbt test `not_null` on user_id in the staging model. Set up NULL rate alerting
with threshold >0.1% for key identifier columns.

### Metadata
- Source: etl_failure
- Pipeline: Airflow DAG `ingest_users_daily`
- Warehouse: Snowflake
- Related Tables: staging.users_raw, warehouse.dim_users
- Tags: null, migration, oracle, postgresql, data-quality, ingestion
- Pattern-Key: data_quality.null_after_migration

---
```

## Learning: Definition Mismatch (Active User)

```markdown
## [LRN-20250416-001] definition_mismatch

**Logged**: 2025-04-16T09:00:00Z
**Priority**: high
**Status**: pending
**Area**: governance

### Summary
Marketing defines "active user" as any login within 30 days; Product uses 7-day window

### Details
Executive dashboard showed 420K "active users" (Marketing's number) while the Product
team reported 185K to the board. The discrepancy caused a board-level escalation. Root
cause: two independent dbt models (`mart_marketing.active_users` and `mart_product.active_users`)
use different lookback windows without documenting the distinction. Marketing counts
any user who logged in within 30 days. Product counts users with at least one
feature-interaction event within 7 days. Neither model's documentation specified the
window, and both were labeled "Active Users" in Looker.

### SQL Example

**Marketing definition:**
\`\`\`sql
SELECT COUNT(DISTINCT user_id) AS active_users
FROM events.logins
WHERE login_at >= CURRENT_DATE - INTERVAL '30 days'
\`\`\`

**Product definition:**
\`\`\`sql
SELECT COUNT(DISTINCT user_id) AS active_users
FROM events.feature_interactions
WHERE event_at >= CURRENT_DATE - INTERVAL '7 days'
\`\`\`

### Suggested Action
1. Create a canonical metric definition in the data dictionary: `active_users_30d` and `active_users_7d`
2. Rename Looker explores to include the window: "Active Users (30-day)" vs "Active Users (7-day)"
3. Add a `metric_definition` YAML file in dbt with owner, definition, grain, and refresh cadence
4. Require metric name approval through governance review before dashboard deployment

### Metadata
- Source: definition_conflict
- Teams: Marketing, Product
- Warehouse: Snowflake
- Related Tables: mart_marketing.active_users, mart_product.active_users
- Tags: metric-definition, active-user, governance, looker, dbt
- Pattern-Key: definition_mismatch.active_user_window

---
```

## Learning: Metric Drift (Revenue Calculation)

```markdown
## [LRN-20250417-001] metric_drift

**Logged**: 2025-04-17T14:00:00Z
**Priority**: critical
**Status**: resolved
**Area**: modeling

### Summary
Revenue metric silently changed when new product line added without updating calculation logic

### Details
The company launched a "Professional Services" product line in Q1. Revenue from services
was recorded in a new `billing.services_invoices` table, but the master revenue model
(`mart_finance.total_revenue`) only aggregated from `billing.subscriptions` and
`billing.one_time_purchases`. For 6 weeks, executive dashboards under-reported revenue
by ~$2.1M/month. The discrepancy was only caught when Finance reconciled against
the general ledger for quarterly close.

### SQL Example

**Before (incomplete):**
\`\`\`sql
SELECT
    DATE_TRUNC('month', invoice_date) AS month,
    SUM(amount) AS total_revenue
FROM (
    SELECT invoice_date, amount FROM billing.subscriptions
    UNION ALL
    SELECT invoice_date, amount FROM billing.one_time_purchases
) combined
GROUP BY 1
\`\`\`

**After (complete with lineage):**
\`\`\`sql
SELECT
    DATE_TRUNC('month', invoice_date) AS month,
    SUM(amount) AS total_revenue,
    SUM(CASE WHEN source = 'subscription' THEN amount END) AS subscription_revenue,
    SUM(CASE WHEN source = 'one_time' THEN amount END) AS one_time_revenue,
    SUM(CASE WHEN source = 'services' THEN amount END) AS services_revenue
FROM (
    SELECT invoice_date, amount, 'subscription' AS source FROM billing.subscriptions
    UNION ALL
    SELECT invoice_date, amount, 'one_time' AS source FROM billing.one_time_purchases
    UNION ALL
    SELECT invoice_date, amount, 'services' AS source FROM billing.services_invoices
) combined
GROUP BY 1
\`\`\`

### Suggested Action
1. Add a reconciliation test: `total_revenue` in warehouse must match GL total ±0.5%
2. Create a "revenue source registry" that must be updated when new billing tables are added
3. Add dbt source freshness checks on all billing tables
4. Alert when a new table appears in the billing schema that isn't referenced by revenue model

### Metadata
- Source: reconciliation_failure
- Pipeline: dbt model `mart_finance.total_revenue`
- Warehouse: BigQuery
- Related Tables: billing.subscriptions, billing.one_time_purchases, billing.services_invoices
- Tags: revenue, metric-drift, completeness, finance, reconciliation
- Pattern-Key: metric_drift.revenue_source_missing
- Impact: $2.1M/month under-reported for 6 weeks

### Resolution
- **Resolved**: 2025-04-17T18:00:00Z
- **Commit/PR**: #312
- **Notes**: Added services table to revenue model, created reconciliation test against GL

---
```

## Data Issue: Pipeline Failure (DST Partition)

```markdown
## [DAT-20250413-001] pipeline_failure

**Logged**: 2025-04-13T06:30:00Z
**Priority**: high
**Status**: resolved
**Area**: ingestion

### Summary
Airflow DAG fails on date partition after DST change — partition key generates duplicate for spring-forward hour

### Error Output
\`\`\`
[2025-03-09T07:00:00+00:00] ERROR - Task ingest_events failed
sqlalchemy.exc.IntegrityError: duplicate key value violates unique constraint
  "events_partition_pkey"
DETAIL: Key (partition_date, hour)=(2025-03-09, 2) already exists.
\`\`\`

### Root Cause
The ingestion pipeline partitions events by local hour. During the spring-forward DST
transition (US/Eastern), the hour 2:00 AM doesn't exist. The pipeline's fallback logic
assigned events from 3:00 AM to hour=2, colliding with pre-existing partition from the
previous run that also defaulted missing hours to hour=2. The partition key constraint
rejected the duplicate.

### Fix
\`\`\`python
from datetime import datetime
import pytz

def get_partition_hour(event_time: datetime, tz: str = "US/Eastern") -> int:
    local_tz = pytz.timezone(tz)
    local_time = event_time.astimezone(local_tz)
    return local_time.hour

# Use UTC-based partitioning instead of local time
def get_partition_key(event_time: datetime) -> str:
    utc_time = event_time.astimezone(pytz.UTC)
    return utc_time.strftime("%Y-%m-%d-%H")
\`\`\`

### Prevention
- Partition by UTC hour, never local time
- Add DST transition test cases to pipeline test suite
- Run integration tests on known DST transition dates (March second Sunday, November first Sunday)
- Add Airflow alert for partition key constraint violations

### Context
- Trigger: etl_failure
- Pipeline: Airflow DAG `ingest_events_hourly`
- Warehouse: PostgreSQL (staging) → Snowflake (warehouse)
- Input: Events from 2025-03-09 02:00-03:00 US/Eastern

### Metadata
- Reproducible: yes (every DST transition)
- Related Tables: staging.events_partitioned
- See Also: DAT-20241103-002 (fall-back DST issue, same root cause)

### Resolution
- **Resolved**: 2025-04-13T10:00:00Z
- **Commit/PR**: #289
- **Notes**: Switched all partitioning to UTC. Added DST transition test fixtures.

---
```

## Data Issue: Visualization Misleads (Y-Axis)

```markdown
## [DAT-20250418-001] visualization_mislead

**Logged**: 2025-04-18T11:00:00Z
**Priority**: medium
**Status**: pending
**Area**: visualization

### Summary
Y-axis starting at non-zero makes 2% revenue change appear as 50% change in executive dashboard

### Error Output
\`\`\`
No error — visual issue identified during dashboard review.
Revenue chart Y-axis range: $9.8M to $10.2M
Actual change: $10.0M → $10.2M (2% increase)
Visual impression: bar nearly doubles in height (appears ~50% increase)
\`\`\`

### Root Cause
Looker auto-scales the Y-axis to fit data range. With revenue values between $9.8M
and $10.2M, the axis starts at $9.8M instead of $0. The compressed scale exaggerates
small percentage changes. The CEO cited this chart in an all-hands as evidence of
"dramatic revenue growth" — the actual growth was 2%.

### Fix
\`\`\`yaml
# Looker LookML view
view: revenue_chart {
  measure: total_revenue {
    type: sum
    sql: ${amount} ;;
    value_format: "$#,##0.0,,\"M\""
  }
  # Force Y-axis to start at zero for absolute value charts
  # Use a separate % change chart for growth visualization
}
\`\`\`

### Prevention
- Dashboard standard: absolute value charts must start Y-axis at zero
- Percentage change charts should be used for growth metrics
- Add a "chart review" step to dashboard deployment checklist
- Annotate charts with actual percentage change when auto-scaling is necessary

### Context
- Trigger: dashboard_review
- Tool: Looker
- Dashboard: Executive KPI Dashboard
- Metric: Monthly Recurring Revenue

### Metadata
- Reproducible: yes
- Related Dashboards: Executive KPI Dashboard, Board Report
- Tags: visualization, y-axis, misleading, looker, revenue

---
```

## Feature Request: Automated Schema Drift Detection

```markdown
## [FEAT-20250415-001] schema_drift_detection

**Logged**: 2025-04-15T15:00:00Z
**Priority**: high
**Status**: pending
**Area**: ingestion

### Requested Capability
Automated detection of schema changes in source systems before they break downstream
pipelines. Should compare current source schema against last known schema and alert
on additions, removals, type changes, and constraint modifications.

### User Context
Three pipeline failures in the past month were caused by upstream schema changes
that were not communicated to the data team. A source system added a NOT NULL column,
another renamed a column, and a third changed a VARCHAR(50) to VARCHAR(255) which
broke a downstream CAST operation. Each incident required 2-4 hours of investigation.

### Complexity Estimate
medium

### Suggested Implementation
1. Nightly job queries `INFORMATION_SCHEMA.COLUMNS` for all monitored source tables
2. Compare against a stored snapshot in `metadata.schema_snapshots`
3. Generate diff report: new columns, dropped columns, type changes, constraint changes
4. Post to Slack #data-alerts with change summary
5. Optionally block pipeline execution if breaking changes detected

\`\`\`python
def detect_schema_drift(source_table: str, warehouse_conn) -> list[SchemaChange]:
    current_schema = fetch_current_schema(source_table, warehouse_conn)
    stored_schema = load_schema_snapshot(source_table)
    return compare_schemas(current_schema, stored_schema)
\`\`\`

### Metadata
- Frequency: recurring (3 incidents in 30 days)
- Related Features: dbt source freshness, Airflow schema validation operator

---
```

## Learning: Promoted to Data Dictionary

```markdown
## [LRN-20250410-003] definition_mismatch

**Logged**: 2025-04-10T11:00:00Z
**Priority**: high
**Status**: promoted
**Promoted**: data dictionary (DATA_DICTIONARY.md, metric: churn_rate)
**Area**: governance

### Summary
Three teams had different churn definitions — standardized to a single canonical definition

### Details
Customer Success defined churn as "no login in 90 days." Finance defined it as
"subscription cancelled." Product defined it as "no feature usage in 30 days."
Board reporting used Finance's definition, but the churn dashboard used Customer
Success's definition, leading to a 4x discrepancy (2% vs 8%).

Standardized to: "A customer is churned when their subscription status transitions
to 'cancelled' or 'expired' in the billing system. Voluntary and involuntary churn
are tracked separately."

### Suggested Action
Added to data dictionary with owner (Finance), definition, grain (customer-month),
refresh cadence (daily), and approved aliases.

### Metadata
- Source: definition_conflict
- Teams: Customer Success, Finance, Product
- Related Tables: mart_finance.churn_monthly, mart_cs.user_activity
- Tags: churn, metric-definition, governance, data-dictionary
- Pattern-Key: definition_mismatch.churn_rate
- Recurrence-Count: 5
- First-Seen: 2025-02-15
- Last-Seen: 2025-04-10

---
```

## Learning: Promoted to Skill (Data Freshness Monitoring)

```markdown
## [LRN-20250412-001] freshness_issue

**Logged**: 2025-04-12T15:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/data-freshness-monitoring
**Area**: ingestion

### Summary
Systematic checklist for monitoring data freshness across pipeline stages

### Details
Developed a repeatable freshness monitoring workflow after 5 separate SLA breaches
in 2 months. The pattern is always the same: a source system delays data delivery,
no alert fires because freshness checks only exist at the final reporting layer,
and stakeholders discover stale data in dashboards hours later. By adding freshness
checks at ingestion, transformation, and reporting layers, breaches are caught within
15 minutes instead of hours.

### Suggested Action
Follow the freshness monitoring checklist:
1. Check source system data availability (row count > 0 for today's partition)
2. Validate ingestion timestamp is within SLA window
3. Confirm transformation models completed (dbt run status)
4. Verify reporting layer freshness (dashboard last-refresh timestamp)
5. Alert on any layer exceeding its SLA threshold

### Metadata
- Source: freshness_breach
- Pipeline: Multiple DAGs
- Warehouse: Snowflake
- Tags: freshness, sla, monitoring, pipeline, checklist
- See Also: LRN-20250320-001, DAT-20250401-003, DAT-20250408-001

---
```
