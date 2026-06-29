# Node System Audit Summary

Use this when deciding whether the 6-layer / 14-node architecture is enough.

## Verdict

Keep the 14 core nodes. Do not add a 15th ordinary node yet.

Upgrade the system to:

```text
6 rebased layers + 14 core nodes + 4 cross-cutting rails + 2 optional compound nodes
```

## Recommended Layers

| Layer | Nodes |
|---|---|
| Signal & Intent | Intake |
| Context, Memory & Workspace | Context / Memory |
| Evidence & Data | Radar, Evidence Normalize, Data Modeling |
| Orchestration & Learning | Planning, Routing, Learning |
| Execution & Assurance | Action, Test, Score, Check |
| Delivery & Evolution | Handoff, Sediment |

## Required Rails

| Rail | Why |
|---|---|
| Observe / Trace | Needed for debugging, evals, monitoring, and learning loops. |
| Policy / Permission | Needed for safe tools, workspace isolation, approvals, and rollback. |
| Artifact Registry | Needed for durable outputs, schemas, versions, and source refs. |
| Human / Team | Needed for reviewers, approvals, escalations, and handoffs. |

## Optional Compound Nodes

| Compound | Compose From |
|---|---|
| Deploy / Publish | Action + Check + Handoff |
| Monitor / Ops | Trace + Test + Score + Check + Sediment |

## Main Design Rule

When a new framework concept appears, do not immediately add a new node. First decide:

```text
Is it a core node, a cross-cutting rail, or a compound pattern?
```
