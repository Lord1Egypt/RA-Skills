---
name: uplo-data-analytics
description: AI-powered data analytics knowledge management. Search data pipeline documentation, dashboard specifications, data governance policies, and reporting standards with structured extraction.
---

# UPLO Data Analytics — Metadata That Remembers

Data teams have a documentation problem that compounds over time. The warehouse has 3,000 tables but only 200 have descriptions. The Looker instance has dashboards built by people who left two years ago. The data governance policy exists but nobody can find the version that was actually approved. UPLO Data Analytics turns this scattered tribal knowledge into a searchable, structured corpus: pipeline documentation, schema definitions, data quality rules, dashboard specs, and governance policies all in one place.

## Session Start

```
get_identity_context
```

This establishes your analytics role (data engineer, analyst, governance lead, etc.) and surfaces which data domains you have access to. Some datasets are restricted due to PII governance or competitive sensitivity.

Check current directives — the data team often has active mandates around migration timelines, deprecation notices, or data quality SLA targets:

```
get_directives
```

## When to Use

- A stakeholder asks what a specific metric means and you need to find the canonical definition, including the SQL logic, source tables, and business rules
- You are building a new pipeline and want to know if similar data already exists in the warehouse to avoid duplication
- Investigating a data quality incident and need to trace the lineage from source system through transformations to the impacted dashboard
- Preparing for a data governance review and need to compile documentation on data classification, retention policies, and access controls
- A new analyst joins and needs to understand the warehouse schema naming conventions, dbt project structure, and how to request access
- Evaluating whether a proposed schema change will break downstream dependencies by searching for references to the affected table
- Looking for the data dictionary entry for a column that has an ambiguous name like `status_cd` or `type_flag`

## Example Workflows

### Metric Definition Dispute

The finance team and product team report different DAU (Daily Active Users) numbers. The analytics lead needs to find and reconcile the definitions.

```
search_with_context query="daily active users DAU metric definition SQL logic business rules"
```

Search for the specific dashboard implementations:

```
search_knowledge query="product analytics dashboard DAU calculation Looker explore"
```

```
search_knowledge query="finance reporting DAU user count methodology monthly report"
```

If the definitions genuinely differ and need reconciliation:

```
propose_update target_table="entries" target_id="<metric-definition-entry-id>" changes='{"data":{"note":"DAU definitions diverge between product (event-based) and finance (login-based); needs governance review"}}' rationale="Metric inconsistency discovered between product and finance DAU reporting"
```

### Data Lineage Investigation

A dashboard is showing NULL values that were not there last week. The data engineer needs to trace the problem.

```
search_with_context query="customer_orders table pipeline transformations source systems dependencies"
```

```
search_knowledge query="customer_orders ETL job schedule dbt model upstream sources"
```

Check if there is a known data quality incident:

```
search_knowledge query="data quality incident customer data source system outage recent"
```

```
log_conversation summary="Traced NULL values in orders dashboard to upstream source system schema change; customer_orders dbt model needs migration" topics='["data-quality","lineage","pipeline-break"]' tools_used='["search_with_context","search_knowledge"]'
```

## Key Tools for Data Analytics

**search_with_context** — Data questions are inherently about relationships: tables connect to pipelines, pipelines connect to source systems, dashboards depend on models. Graph traversal follows these connections. Example: `search_with_context query="revenue_summary table lineage source transformations consumers"`

**search_knowledge** — Direct lookup for specific technical artifacts: a dbt model definition, a data dictionary entry, a governance policy version. Example: `search_knowledge query="dbt model dim_customers grain deduplication logic"`

**flag_outdated** — Data documentation rots faster than most content types. Table descriptions written during initial warehouse build may reference deprecated source systems. Schema diagrams from before a migration may show phantom tables. Flag aggressively.

**report_knowledge_gap** — Undocumented tables and undefined metrics are the norm in most warehouses. When you encounter a table with no data dictionary entry or a metric with no canonical definition, report the gap. The governance team uses these signals to prioritize documentation sprints.

**propose_update** — When you discover that a data dictionary entry is wrong (e.g., a column description says "customer creation date" but it actually stores "first order date"), propose the correction.

## Tips

- Technical identifiers are your best search terms. Use exact table names (`dim_customers`), column names (`order_status_cd`), dbt model names, and Looker explore names. The extraction engine indexes these precisely.
- When investigating data quality issues, start with `search_with_context` to get the lineage graph, then use `search_knowledge` for specific transformation logic. Working backwards from the symptom to the source is more efficient than searching forward.
- Data governance policies often exist in multiple versions (draft, approved, superseded). Include "approved" or "current" in your query to filter toward the authoritative version.
- The most valuable documentation to contribute back is metric definitions with SQL. When you resolve a metric dispute, log the session and propose an update with the canonical SQL so the next person does not have to repeat the investigation.
