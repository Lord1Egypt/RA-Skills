# Slow query lookup API reference

## Scope

This reference is only for the simplified slow-query lookup skill.

The goal is to return report-style slow SQL information with minimal branching and no cause analysis.

## Allowed read-only actions

Use only these PostgreSQL OpenAPI actions:

- `DescribeSlowQueryList`
- `DescribeSlowQueryAnalysis`

## Fixed query workflow

1. Confirm region, instance ID, and time window.
2. Normalize the region.
3. Pull the slow query list.
4. Pull the slow query analysis summary when aggregated ranking is needed.
5. Return the result in a fixed output format.

## Basic fields to display

When available, the skill should show fields such as:

- SQL text or normalized SQL
- database name
- user name
- client address
- duration
- execution count
- total cost time
- start time
- session ID or process ID

## Output schema

### 1. Query scope
- Region
- Instance ID
- Time window
- Optional filters
- Sort basis

### 2. Slow SQL basic list
For each record or aggregated item include:
- SQL text or normalized SQL
- key numeric fields returned by the API
- available identity fields
- missing fields if the API does not return them

## Guardrails

- Do not output ranked causes.
- Do not output root-cause conclusions.
- Do not output tuning suggestions.
- Do not expand into unrelated evidence collection.
- If the API only returns summary-level data, say the result is summary only.
