# Work graph compiler

Compile reviewed Linear/Jira exports and agent-run assignments into a generic,
read-only operations graph:

```bash
node scripts/work-graph.js < reviewed-input.json > work-graph.json
```

The CLI reads at most 4 MiB from stdin and writes only JSON on success. It does not
read credentials, contact trackers, install files, or modify tracker state. Review
the output before atomically placing it at `state/command-center/work-graph.json`
in an intended workspace. Command Center's operations map consumes this format;
existing project-snapshot collection is independent and does not supply these tasks.

See `tests/fixtures/work-graph/input.json` for a fully synthetic example.

## Input

`schemaVersion: 1`, `profile`, `agentId`, `observedAt`, `sources`, and optional `runs`.
Each source has a unique organization/account-scoped `id`, `provider`, `observedAt`,
`complete`, and `issues`. Declare incomplete exports explicitly. Optional `statusMap`
maps native status IDs to `planned|doing|review|done|canceled|unknown`.

- Linear: `projects` with `id/name/status`; issues with `id/identifier/title/state`,
  optional `parent.id`, `project.id`, and `labels.nodes[].name`.
- Jira: issues with `id/key/fields`; fields include `summary/status/issuetype.id`,
  optional `parent.id`, `labels`, and `issuelinks`. `epicTypeIds` must explicitly name
  the native issue type IDs treated as outcomes. Optional `blocksTypeIds` identifies
  directional blocking links; outward means current issue blocks outward issue.
  Do not guess custom relationship types from translated display names.
- Run: `id/sourceId/agentId/sessionKey/title/state/observedAt`; optional `taskId`,
  `role`, and `brief`. Agent IDs must be runtime/account-scoped when collecting a
  fleet; identical supplied IDs intentionally identify one agent across sources.

Native status category maps provide conservative defaults. Unmapped statuses stay
unknown; configuring a review status does not silently classify every in-progress
status as review. Jira legacy epic custom fields must be normalized into `parent`
by the exporting adapter; this compiler does not discover instance-specific fields.

## Evidence and inference

Explicit provider relationships, `role:*` / `topic:*` labels, and run bindings
produce observed edges. Supported roles: frontend, backend, infra, qa, architecture,
copywriting, legal. An explicit run role describes that assignment, not a permanent
agent capability.

Two deterministic proposal rules help when tracking is incomplete:

1. A task title containing a role cue can suggest roles when no explicit role label
   exists. For example “database migration” suggests backend.
2. An exact issue identifier mentioned in an unbound run brief can suggest a task/run
   link inside the same source scope. Mentions are not assignment proof.

These are explainable heuristics, not semantic embeddings or an LLM classifier.
Proposals retain `basis: inferred` and evidence; they do not change tracker status,
accept assignments, or run work. Brief contents are not copied into the graph.
Explicit links always remain distinguishable from suggestions. Missing references
produce warnings; no replacement entities or fake progress are manufactured.

## Output and boundaries

Output contains `sources`, `nodes`, `edges`, `warnings` plus the scope/version/time
fields. Nodes: outcome, task, run, agent, role, topic. Edges: contains, works-on,
runs, role, topic, blocks. Identity includes source + kind + native ID. Parent cycles
and duplicate identities fail closed. Capacity: eight sources, 500 issues and 100
projects per source, 500 runs, 2,000 output nodes, and 5,000 edges.

Tracker Done is not verified acceptance. No weighted progress, ETA, schedule
variance, token rates, automatic reassignment, live subscription, or inference
acceptance workflow is provided. Source freshness is evaluated by the viewer;
source timestamps are not refreshed by compilation. Public examples must remain
synthetic; local exports may contain private names and descriptions.
