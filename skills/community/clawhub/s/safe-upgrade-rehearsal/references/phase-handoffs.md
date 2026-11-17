# Safe-update phase handoffs

Package compatibility, state migration, activation, and post-activation
recovery are separate claims. They share a candidate root but never inherit
authority from one another.

The machine-readable contracts are the four
`schemas/openclaw.safe_update.*_handoff.v1.schema.json` files. Every document
is read-only, hash-bound, non-authoritative, and unable to grant operator
approval. A handoff records what the next owner may inspect; it is not a
command or permission to mutate a runtime.

## Phase ownership

| Phase | Producer | Consumer | Claim | Stop condition |
| --- | --- | --- | --- | --- |
| `preflight_compatible` | safe-update rehearsal | migration rehearsal or operator planning | The exact candidate reached `ready_for_operator_plan`. | Any required gate is missing, the candidate root changes, or live E2E is represented as anything except `not_run`. |
| `migration_restore_rehearsal` | disposable migration harness | operator planning | A digest-bound snapshot was migrated and restored in a disposable environment. | Snapshot, migration, restore, or `state-migration-rehearsal` evidence is missing or bound to another candidate. |
| `activation_boundary` | operator-plan preparation | operator | The point of no return, rollback boundary, recovery rule, and E2E plan are explicit. | Approval is not separately granted; rollback boundary is unknown; `rollback-evidence` is missing; or either rollback and forward recovery is unbound. |
| `forward_reconcile` | activation recorder | separately approved operations capability | Post-activation evidence identifies a bounded recovery or containment action. | Operational approval is absent, activation receipt is unbound, E2E is missing, or neither rollback nor containment is defined. |

## Stable gate consumption

`required_gate_ids` may contain only gate IDs owned by the deterministic
conservative policy. This contract consumes their names and evidence digests;
it does not reinterpret what satisfies them.

State-affecting updates require `state-migration-rehearsal`. An activation
handoff with an unknown rollback boundary is `blocked`, includes
`rollback-evidence` in `required_gate_ids`, and keeps
`rollback_evidence_digest` null. An operator may accept residual risk outside
this skill, but that acceptance does not rewrite the handoff as machine green.

## Phase transitions

1. Preflight may produce `ready_for_operator_plan`; it does not prove migration,
   activation, channel behavior, state continuity, or rollback.
2. Migration/restore rehearsal consumes the same `candidate_root` and emits
   disposable evidence. It cannot activate the candidate.
3. Activation planning records an external approval requirement and keeps live
   E2E `not_run`. The safe-update skill stops here.
4. After a separately controlled activation, an operational capability may
   create a forward-reconcile handoff. That capability owns its approval,
   rollback, and containment semantics.

Changing `candidate_root` or `source_status_digest` invalidates downstream
handoffs. No phase document contains an executable update, deploy, restart,
repair, or live-write operation.
