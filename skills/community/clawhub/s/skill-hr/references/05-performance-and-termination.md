# Performance, probation, and termination

## KPIs (lightweight)

Tracked in `registry.json` per skill:

- `tasks_total` — completed assignments (success + fail + partial counted once each completion).
- `tasks_success` — P05 `outcome: success`.
- `tasks_fail` — P05 `outcome: fail` with `root_cause_class` in `skill_limit` or `wrong_match` (configurable).

**Partial** outcomes: increment `tasks_total`; do not increment `tasks_success` unless user accepts partial as success (document in incident).

## Probation rules

- New external hires default to `on_probation`.
- Promote to `active` after **1** documented success on a non-trivial criterion (or **2** if org is risk-averse—state in registry `notes`).
- If **two consecutive** failures with `wrong_match` or `skill_limit`, set `terminated` unless user overrides.

## Termination (pool removal)

**Always**:

1. Set `status: terminated` in registry.
2. Write P06 report and link incidents.
3. Exclude from P02 permanently unless user rehires (manual status change + rationale in `notes`).

**Physical uninstall** (optional):

- Only with **explicit user confirmation** and a path audit.
- Never delete skills outside the user's skills directories (e.g. system or shared plugins).

## Retrain vs terminate

- **`environment`** failures: prefer fix + retry; do not terminate the skill.
- **`user_spec`** failures: prefer clarification and P03 revision; do not terminate unless repeated scope mismatch after documented warnings.
- **`wrong_match`**: terminate quickly after `max_trials_per_task_per_skill` exhausted.

## Trial limits

`matching.max_trials_per_task_per_skill` (default **2**) counts P03 iterations for **same skill_id** on **same incident thread**. After exceeded → `escalate` or recruit replacement.

## Frozen state

Use `frozen` for:

- Pending security review
- License uncertainty
- User asked to pause a skill without deleting history

Frozen skills are skipped in P02 like terminated, but are visible for audit.
