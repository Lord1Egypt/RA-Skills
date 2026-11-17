# Scope and task acceptance

## Classify the requested outcome

Read the original request and generated `task_contract.json` before dispatch. Explicit complete-project goals and affirmative bounded work are distinct. Negation applies to its object, not every later cue: neither/nor, not-only/but-also, double negatives and unrelated “without deploying” context must not silently expand or narrow scope.

For example, “Complete the project-level objective, not just the first bounded milestone” remains a project; “Without deploying anything implement a bounded milestone for the project-level objective” remains scoped work. Verify Chinese and English affirmative/negative controls and generated contracts in disposable queues after changes. The inference is not a complete natural-language parser; correct a mismatched contract before executing it.

## Inspect effective reviews and gates

- Read checkpoint reviews, task gates and `final_judgement.json` together. Checkpoint sequence and creation time establish chronology; filename numbering and regenerated review timestamps do not. Missing or conflicting ordering must not erase a live blocker.
- For a task with at most one planned checkpoint, an accepted terminal task review can remain terminal despite a later project `needs_human_acceptance` snapshot only when chronology is established and that later review is independently accepted with no materializable deferred gates. Preserve blocked, revise and unordered reviews unless explicit validated revision coverage closes status-only phases as described below. Different explicit milestone identities never supersede each other by chronology. Multiple planned milestones still require their effective reviews.
- A task terminal result is not project completion or deployment authorization. Inspect the original completion contract and project backlog independently.
- Reconcile a consumed gate only through the recorded same-task successor link, `revises_checkpoint_id`. A satisfied gate records the successor, not proof that the successor passed acceptance. Check the effective review and final queue state separately.
- Effective human/authority blockers and uncertain external outcomes remain `needs_human_input`, including after ordinary worker failure; do not turn them into development revisions or automatic retries. Resolved historical blockers do not permanently veto continuation.

## Evidence boundaries

Inspect artifacts rather than dispatcher exit status. A checkpoint accepted by the worker is not the outer queue's final judgement; `ready_to_apply` is not applied. For multiple PRs, test each exact candidate and a correctly constructed combined tree separately. Local tests, exact-HEAD remote CI, package installation and live-instance acceptance are distinct claims.

## Explicit status-only phase closure

An accepted final checkpoint may close unordered `in_progress` phases through `revision_coverage`: each entry binds `checkpoint_id`, `checkpoint_sha256` (exact historical bytes), concrete `resolution`, and nonempty verification strings present in the final checkpoint. Require unique same-task, same-planned-milestone records, and reject reversed known clocks. Keep historical files unchanged. `revises_checkpoint_id` alone is lineage, not this coverage proof.

Coverage cannot close real defects, missing evidence, corruption, duplicate identities, human blockers, deferred gates, or a phase that itself declares coverage. Invalid coverage remains a failure regardless of chronological ordering. Inspect actual verification artifacts; references are cooperative claims.

## Continuation and invalid history

Progress is newly accepted durable milestone identity, not renamed plans, extra files or repeated accepted snapshots. Preserve explicit and inferred project plans. Malformed/non-object checkpoints may receive a bounded repairing dispatch, but unknown pre-dispatch history persists as `invalid_checkpoint_baseline`, blocks automatic acceptance, and requires explicit revision from validated history. Gate reconciliation leaves gates unchanged while any checkpoint is invalid. Filesystem errors are not JSON corruption.
