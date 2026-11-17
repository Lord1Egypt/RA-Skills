# CI — Plan On PR, Apply On Merge, And The Gates Between

The shape that works, in one line: **PR → fmt/validate/lint/policy → `plan -out=tfplan` → post the summary → merge → apply that exact plan file.**

## Artifact Discipline

- The plan file, the lock file, and the commit are one unit. `apply tfplan` built from a different commit is a different change wearing the reviewed change's name.
- If the pipeline cannot carry the artifact between jobs, re-plan at apply time and be honest that you are approving a summary, not a diff. Then compensate with a policy gate on the new plan.
- The plan file is a secret (`secrets.md`): it contains new values in clear. Short retention, restricted download, never pasted into a PR comment.
- **"Saved plan is stale"** means another apply landed in between. Re-plan, re-review, re-apply — there is no flag that makes the old plan safe.

## Authentication

- OIDC federation from the CI provider to a per-environment cloud role. Long-lived keys in CI secrets are exactly what OIDC exists to delete.
- Two roles, not one: the plan role needs cloud **read** plus state **read/write** (plan takes the lock and may persist a refreshed state — a truly read-only role fails on the lock); the apply role adds cloud write.
- Fork PRs must never receive the plan role. Run fmt/validate/lint on forks and gate the plan behind a maintainer label.

## Concurrency And Locking

- One concurrency group per state. Two jobs against one state means one waits, one times out, and eventually someone adds a `force-unlock` step to "fix the flakiness" — which is how a half-written state happens.
- `-lock-timeout=5m` so a queued job waits instead of failing. Set it once with `TF_CLI_ARGS_plan` / `TF_CLI_ARGS_apply`.
- Never put `force-unlock` in a pipeline. It is a human decision with preconditions (`recovery.md`).

## Non-Interactive Hygiene

```bash
export TF_IN_AUTOMATION=1     # trims "next step" hints from output
export TF_INPUT=0             # never prompt; fail instead
terraform init -input=false -lockfile=readonly
terraform plan -out=tfplan -input=false -no-color
```

`terraform fmt -check -recursive` in CI; `fmt -w` writes files and belongs in a pre-commit hook, not a pipeline.

## The Gates, Cheapest First

1. `fmt -check -recursive` — style, instant.
2. `validate` — type-correctness, needs `init`, no credentials.
3. `tflint` — provider-aware: invalid instance types, deprecated arguments, unused declarations.
4. Static security scan on the HCL — catches the obvious open-to-the-world defaults.
5. **Policy on the plan JSON** — the highest-value gate, because the plan is what actually happens after variables, defaults, and modules resolve.
6. `terraform test` for module contracts (`testing.md`).

The single most useful gate is the destroy count:

```bash
terraform show -json tfplan \
  | jq '[.resource_changes[] | select(.change.actions | index("delete"))] | length'
```

Fail the job above `destroy_gate`, and print the addresses when it fails — a number alone tells the reviewer nothing.

## Posting A Useful Plan Summary

- Post the counts, the full list of destroyed and replaced addresses, and every "forces replacement" attribute. Those are the lines humans actually review.
- Collapse the rest. A 4,000-line plan in a PR comment is read by nobody, which is the same as no review. `plan_summary_detail` sets how far to go: `destructive-only` is this shape, `full` renders every changed resource, `counts` drops to the summary line plus the destroy list.
- Include the commit SHA and the plan artifact ID so the apply can be traced back.

## Drift Detection

- Scheduled `terraform plan -detailed-exitcode`: **0 no changes · 1 error · 2 changes present.**
- Exit 2 opens an issue or pages, and never auto-applies. Auto-remediating drift is how a manual production fix gets reverted at 3am.
- Cadence: nightly for production, weekly elsewhere. Expect recurring noise from providers that normalize attributes — fix or `ignore_changes` those once (`debug.md`), or the signal dies.
- A drift job needs the plan role and its own concurrency group, or it will fight the deploy pipeline for the lock.

## Ephemeral Runners

- `.terraform` does not survive between jobs, so every run re-downloads providers. Cache the plugin directory keyed on the hash of `.terraform.lock.hcl` — the correct key, because the lock is exactly what determines the contents.
- `TF_PLUGIN_CACHE_DIR` plus that cache turns `init` from the slowest step into a no-op (`providers.md`).

## Monorepos And Promotion

- Plan only the stacks whose files changed. A changed shared module means every consuming stack plans — that fan-out is correct, not a bug to suppress.
- Promotion applies the **same code** with a different `-backend-config` and `-var-file`, in order: dev → stage → prod. A failure stops the chain.
- Never promote by copying code between directories. The directories then drift and the "same" change behaves differently per environment.

## When Auto-Apply Is Defensible

All three must hold: the applied artifact is the reviewed plan file, a policy gate fails closed on destroys above the threshold, and the pipeline is the only writer to that state. Missing any one of them, use a manual approval step that displays the destroy list.
