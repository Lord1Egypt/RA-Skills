# COMMON_READONLY.md

This document defines shared conventions for read-only Flink skills.
Reference this file for skills that inspect, query, diagnose, or generate examples
without changing remote Flink resources or local critical configuration.

## Scope

Typical read-only skills include:

- project listing / project detail
- catalog metadata inspection
- monitoring / logs / events / metrics queries
- diagnosis / root cause analysis
- SQL/template/example generation
- syntax validation that does not publish or start jobs

## Read-Only Rules (MUST)

- Never perform state-changing actions in a read-only workflow.
- Never call `jobs stop`, `jobs restart`, `jobs rescale`, `drafts publish`, or delete operations.
- Never assume a read-only request implies permission to fix or restart anything.
- If the user moves from inspection to change, stop and switch to a mutation skill flow.

## Query Strategy

### Scope First

- Resolve `project_name`, `job_id`, or `draft_id` before querying deep details.
- If the target object is ambiguous, ask the user to choose.

### Narrow Queries

- Prefer small, targeted queries over large dumps.
- For logs, reduce time range and line count first.
- For events, use recent entries first.
- For metrics, prefer the metric directly related to the user's question.

## Recommended Read Flow

1. Confirm scope: project / job / draft.
2. Pick the minimal query that answers the question.
3. Expand only if the first query is insufficient.
4. Summarize evidence before suggesting the next step.

## Escalation To Mutation

If the user asks to actually change anything, hand off to a mutation-capable skill.
Examples:

- "Stop this job" -> mutation
- "Publish this draft" -> mutation
- "Rescale to 8" -> mutation
- "Delete this savepoint" -> mutation

## Output Contract

When responding from a read-only workflow, include:

- Scope: `project_name`, `job_name/draft_name`, `job_id/draft_id`
- Query performed: what was inspected
- Evidence: key log/event/metric/schema findings
- Suggested next step: continue reading, validate, or switch to mutation flow

