---
name: Terraform
slug: terraform
version: 1.0.4
description: >-
  Writes, debugs, and refactors Terraform — HCL and modules, plan and apply failures, state
  surgery, drift, and provider pinning. Use when writing or reviewing HCL, when terraform plan
  or apply errors out, when a plan shows a permanent diff, an unexplained destroy, or "forces
  replacement", when renaming, importing, or moving resources between modules and states, when
  a state lock is stuck or state is lost or corrupted, when for_each fails because a value is
  not known until apply, when pinning providers or surviving a major version upgrade, or when
  wiring plan-on-PR, apply-on-merge, drift detection, and policy gates. Covers OpenTofu,
  tfstate, backends, workspaces, and infrastructure-as-code review. Not for choosing which
  cloud services to build — see aws, gcp, or azure.
homepage: https://clawic.com/skills/terraform
changelog: "Display name shown correctly"
metadata:
  clawdbot:
    emoji: 🟪
    requires:
      anyBins:
      - terraform
      - tofu
    os:
    - linux
    - darwin
    - win32
    displayName: Terraform
    configPaths:
    - ~/Clawic/data/terraform/
---

User preferences and memory live in `~/Clawic/data/terraform/` (see `setup.md` on first use, `memory-template.md` for the file format). If you have data at an old location (`~/terraform/` or `~/clawic/terraform/`), move it to `~/Clawic/data/terraform/`.

## When To Use

- Writing or reviewing HCL: resource design, count vs for_each, module boundaries, variable types and validation
- Debugging plan/apply failures, permanent diffs, cycles, unknown-at-plan errors, stuck locks, drift
- Refactoring live infrastructure: renames, module extraction, imports, splitting or merging state
- Pinning providers, upgrading the CLI or a provider major version, moving between Terraform and OpenTofu
- Designing backends, environment layout, and CI plan/apply gates with policy, tests, and drift detection
- Recovering after damage: lost or corrupted state, wrong `state rm`, unintended destroy, interrupted apply
- Not for choosing which cloud resources to build (→ `aws`, `gcp`, `azure`) or configuring what runs inside them (→ `ansible`)

## Quick Reference

| Situation | Play |
|---|---|
| Renamed a resource or module in code | `moved` block (>=1.1); apply everywhere, delete the block in a later PR → `refactoring.md` |
| Cloud object exists but is not in state | `import` block (>=1.5) + `plan -generate-config-out=gen.tf`; rewrite the draft, merge at zero diff → `refactoring.md` |
| Stop managing something without destroying it | `removed` block with `destroy = false` (>=1.7); `state rm` only as one-off surgery → `refactoring.md` |
| Permanent diff on every plan | Find the writer (autoscaler, console, another pipeline, provider normalization) before reaching for `ignore_changes` → `debug.md` |
| "Invalid for_each argument" / "Invalid count argument" | Key on values known at plan time, never on resource attributes → `expressions.md` |
| A variable value is ignored, or an old value keeps winning | Precedence: `-var`/`-var-file` > `*.auto.tfvars` > `terraform.tfvars` > `TF_VAR_` > the declared default → `expressions.md` |
| "Error: Cycle: ..." | Break the mutual reference into a standalone rule/attachment resource → `debug.md` |
| "Provider produced inconsistent final plan" | Provider bug: upgrade the provider, then pin and report → `debug.md` |
| "Saved plan is stale" | State moved between plan and apply; re-plan, re-review, re-apply → `ci.md` |
| Stuck state lock | Prove the holder is dead, then `force-unlock <LOCK_ID>` → `recovery.md` |
| State lost, corrupted, or pushed wrong | Bucket object versions are the only undo; rebuild by import if there are none → `recovery.md` |
| "Inconsistent dependency lock file" or a checksum error on install | The lock lacks that provider or that platform → `providers.md` |
| Two regions, two accounts, one config | Provider `alias` + explicit `providers` map into modules → `providers.md` |
| Plan takes minutes | `-refresh=false` while iterating, then split state by blast radius → `performance.md` |
| Throttling or "Rate exceeded" during apply | Lower `-parallelism` (default 10) → `performance.md` |
| Moving to a remote backend or between backends | Pull a backup, then `init -migrate-state` → `state.md` |
| Secret landed in state, a plan file, or a log | Rotate first; state is plaintext and old versions keep it → `secrets.md` |
| Provider major upgrade (v4 → v5) | Upgrade guide, one canary stack, explained diff per environment → `upgrades.md` |
| Module design, versioning, or nesting question | Exact pins for third-party, `~>` for internal, two levels max → `modules.md` |
| Resource must never be destroyed, must rotate with another, or keeps diffing on one attribute | `lifecycle` meta-arguments and what each one costs → `lifecycle.md` |
| A `destroy` fails or a teardown leaves debris | Deletion protection, retained objects, reverse-order dependencies → `lifecycle.md` |
| Wiring plan-on-PR and apply-on-merge | OIDC role, saved plan artifact, one concurrency group per state → `ci.md` |
| Need tests or policy gates | `.tftest.hcl` (>=1.6), plan-JSON assertions, policy engine → `testing.md` |
| Need the exact command under pressure | → `commands.md` |
| Anything else | Smallest possible change; `plan -out=tfplan`; read the destroy count and every "forces replacement" line before applying |

Depth on demand: `debug.md` plan/apply symptom→cause chains · `state.md` backends, locking, layout · `refactoring.md` moved/import/removed · `modules.md` design and versioning · `expressions.md` HCL loops, types, functions · `lifecycle.md` replacement, protection, ignored drift · `providers.md` pinning, lock file, aliases · `secrets.md` sensitive values and state exposure · `ci.md` pipelines, OIDC, drift detection · `testing.md` validate, `terraform test`, policy · `upgrades.md` CLI and provider majors, OpenTofu · `performance.md` slow plans and big states · `recovery.md` after the damage · `commands.md` incident toolkit.

## Core Rules

1. **The saved plan is the contract.** `terraform plan -out=tfplan` → review → `terraform apply tfplan`. A bare `apply` re-plans against a world that may have changed since you read the diff: you approve one change and execute another.
2. **Back up before state surgery.** `terraform state pull > backup-$(date +%s).tfstate`; restore with `terraform state push`. One wrong `state rm` orphans a live resource that keeps running and billing with nothing tracking it.
3. **Read the destroy count from the resource lines, not the summary.** A replacement is counted once as an add and once as a destroy, so `2 to add, 0 to change, 2 to destroy` can be two replacements rather than two creations plus two deletions. Machine gate: `terraform show -json tfplan | jq '[.resource_changes[] | select(.change.actions | index("delete"))] | length'` — compare against `destroy_gate`.
4. **Pin everything.** Providers via `required_providers` plus a committed `.terraform.lock.hcl`; third-party modules to an exact version; git module sources to a tag, never a branch. Unpinned means CI breaks on someone else's release day.
5. **Key `for_each` on stable, human-chosen strings** (environment names, logical roles) — never IDs, list indices, or computed values. Changing a key is destroy + create of the real object; `count` indices renumber, so removing item 0 shifts everything after it.
6. **Refactor declaratively.** `moved`, `import`, and `removed` blocks put the change in the PR diff and replay in every environment. `state mv`/`state rm` are out-of-band: unreviewable, unreplayable, invisible to the next reader.
7. **Nothing sensitive is safe in state.** `sensitive = true` masks CLI output; the value sits in plaintext in the state file, the saved plan, and `TF_LOG` output. Encrypt the backend, restrict who can read state, and prefer ephemeral values (>=1.10) and write-only arguments (>=1.11).
8. **Drift is a question, not an error.** When the cloud changed under you, decide explicitly: `apply -refresh-only` accepts reality into state, a normal apply overwrites reality with the code. Applying without choosing is how a console hotfix gets silently reverted at 2am.

## Plan Triage

Read the symbols before the summary:

| Marker | Means | Reaction |
|---|---|---|
| `+` | create | Expected count matches the change you made? |
| `~` | update in place | Safe class; still check the attribute is the one you edited |
| `-/+` | destroy then create | Downtime and a new ID; find the `# forces replacement` line |
| `+/-` | create then destroy | `create_before_destroy` is on; unique names will collide |
| `-` | destroy | Needs an explanation you could give in an incident review |
| `(known after apply)` | value unresolved at plan | Anything keyed on it will fail `for_each`; anything printed from it is unverifiable now |
| `Note: Objects have changed outside of Terraform` | drift detected during refresh | Rule 8 — decide before you apply |

- `terraform show tfplan` re-renders a saved plan; `terraform show -json tfplan` is the machine-readable form every gate should read (`ci.md`).
- `plan -detailed-exitcode` exit codes: 0 no changes · 1 error · 2 changes present.
- "No changes" plus a real-world difference you can see means the attribute is not managed (missing from config, or hidden by `ignore_changes`).

## Count vs for_each

- `count` is positional. Reserve it for identical replicas and the enable flag: `count = var.enabled ? 1 : 0`, referenced as `one(aws_x.y[*].id)`.
- `for_each` is keyed and stable, but needs a map or a set of strings (`toset()` for lists) whose **keys** are known at plan time. Values may be unknown; keys may not. Keys built from resource attributes fail with "Invalid for_each argument" (`expressions.md`).
- Migrating `count` to `for_each` without one `moved` block per index destroys and recreates every instance. Get the index→key mapping from `terraform state list`, not from memory (worked example in `refactoring.md`).
- Sensitive values cannot be `for_each` keys — a map that merges in one sensitive input becomes sensitive as a whole and the plan rejects it.

## Version Floors

`required_version` in the root module turns "my colleague gets a parse error" into a clear message. Floors for the syntax this skill recommends:

| Feature | Floor |
|---|---|
| `moved` blocks | terraform >=1.1 |
| `precondition` / `postcondition`, `replace_triggered_by` | terraform >=1.2 |
| `optional()` object attributes with defaults | terraform >=1.3 |
| `terraform_data` (replaces `null_resource`) | terraform >=1.4 |
| `import` blocks, `check` blocks, `plan -generate-config-out` | terraform >=1.5 |
| `terraform test` with `.tftest.hcl` | terraform >=1.6 |
| `removed` blocks, `for_each` in `import`, `mock_provider` | terraform >=1.7 |
| Provider-defined functions | terraform >=1.8 |
| Ephemeral values and resources, S3 backend `use_lockfile` | terraform >=1.10 |
| Write-only arguments | terraform >=1.11 |

OpenTofu forked at the 1.6 line: floors above 1.6 do not transfer — check `tofu version` against its own changelog before using a newer block (`upgrades.md`).

## Output Gates

Before emitting HCL or proposing an apply:

- Plan saved to a file, and the thing applied is that file?
- Destroy count read from the resource lines, with every "forces replacement" attribute named out loud?
- Every `for_each` keyed on a plan-time-known string?
- Providers pinned and `.terraform.lock.hcl` covering every platform in `lock_platforms`?
- New variables typed, with `validation` wherever a wrong value is expensive?
- No secret in a committed `.tfvars`, a variable default, or an unmasked output?
- If this is a refactor: does the plan read `0 to add, 0 to change, 0 to destroy`?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/terraform/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| terraform_binary | terraform \| tofu | terraform | Command name in every example; `tofu` switches version-floor checks to the OpenTofu changelog and enables its native state-encryption guidance |
| primary_provider | aws \| gcp \| azure \| other | aws | Which provider's examples, auth model, and backend appear first in explanations |
| backend_type | s3 \| gcs \| azurerm \| tfc \| local | s3 | Locking mechanism, versioning advice, and CI credential wiring |
| env_layout | dir-per-env \| workspace-per-env \| single-state | dir-per-env | Refactoring and CI examples; `workspace-per-env` turns on the workspace-safety warnings instead of suppressing them |
| lock_platforms | list | linux_amd64, darwin_arm64 | Platforms passed to `terraform providers lock` and checked in the Output Gates |
| destroy_gate | number (>=0) | 0 | Destroy count above which the agent stops, names every destroyed address, and asks before proposing an apply |
| parallelism | number (1-50) | 10 | Value used in generated plan/apply commands; lower it when the provider throttles |
| plan_summary_detail | full \| destructive-only \| counts | destructive-only | How much plan output gets surfaced (chat and the PR comment in `ci.md`): `full` renders every changed resource, `destructive-only` posts counts plus every destroyed, replaced, and "forces replacement" line and collapses the rest, `counts` posts the summary line and the destroy list only |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied:

- **Tooling**: wrappers (Terragrunt, Terramate), pre-commit hooks, plan-summary tooling — affects which pipeline shape gets proposed
- **Conventions**: resource and module naming, tagging standard, file split (main/variables/outputs vs per-domain) — affects every generated block
- **Platform**: clouds, regions, and accounts in play, and the cross-account role-assumption pattern — affects provider aliases and backend keys
- **Safety posture**: appetite for `state` surgery vs declarative blocks, whether `-auto-approve` is ever acceptable — affects which refactoring path is offered first
- **Workflow**: where apply happens (laptop, CI, managed platform), review gates, who holds production credentials — affects the CI examples
- **Compliance**: mandatory policy engine, required tags, encryption and public-access rules — affects the testing and gate recommendations
- **Output format**: plan-summary verbosity beyond `plan_summary_detail`, HCL-vs-explanation ratio in answers, proactive warnings versus on-demand — affects how every plan and review is reported
- **Cadence**: drift-detection schedule and provider-upgrade rhythm — affects what gets scheduled versus run on demand

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| CLI workspaces for dev/prod separation | Same backend, same credentials; the active workspace is invisible CLI state — applying in the wrong one looks identical to the right one | Directory per environment with separate backends and separate cloud roles (`state.md`) |
| Routine `-target` applies | Leaves the graph partially applied; the next full plan is a surprise diff nobody scoped | Emergencies only, always followed by a clean full plan |
| Interpolation in the `backend` block | Backends cannot read variables or locals — the block is evaluated before anything else exists | Partial config: omit the keys and pass `-backend-config=env/prod.tfbackend` |
| Provisioners for configuration | Not idempotent, untracked in state; a failed provisioner taints the whole resource | `user_data`/cloud-init, config management, or `terraform_data` (>=1.4) |
| Hand-editing state JSON | Serial and lineage mismatch corrupts the backend copy — or worse, the push succeeds | `state mv`/`rm`/`push` on a pulled backup (Core Rules 2) |
| `ignore_changes = all` | Freezes the entire resource forever; future config edits become silent no-ops | Ignore the one attribute, with a comment saying who writes it (`lifecycle.md`) |
| Treating plan success as apply safety | Plan validates config against state, not against the cloud: quotas, IAM, name collisions, and eventual consistency all surface at apply | Apply early in a sandbox account; keep changes small so failures are attributable |
| `apply -auto-approve` outside CI | Removes the only human checkpoint between a typo and deleted production | Auto-approve only in a pipeline applying a reviewed saved plan |
| Committing `terraform.tfstate` or `.terraform/` | Ships every secret in state to git history and leaves everyone on a different copy | Gitignore both; commit `.terraform.lock.hcl` |
| Module source pinned to a branch (`?ref=main`) | The build changes under you with no diff in your repo | Tag refs (`?ref=v1.2.3`) or registry versions |
| `depends_on` sprinkled to fix ordering | Hides a missing attribute reference and, at module level, defers every data source inside to apply time | Reference the attribute you actually need; pass explicit values between modules |

## Where Experts Disagree

- **Vanilla Terraform vs wrapper tooling (Terragrunt and friends)**: the frontier is duplication — one team with a handful of stacks loses more to wrapper complexity than it saves; once environments × stacks means maintaining dozens of near-identical backend and provider blocks, DRY tooling earns its cost.
- **Exact module pins vs `~>` constraints**: exact pins for third-party registry modules (supply-chain surface); pessimistic minor constraints acceptable for internal modules gated by your own CI.
- **One shared state vs many micro-states**: the frontier is change coupling — resources that always ship together belong in one state; every cross-state reference costs a data-source hop and an ordering problem between pipelines.
- **Terraform vs OpenTofu**: the frontier is licensing exposure and feature need, not ideology — OpenTofu is a drop-in for most existing code and adds state encryption; teams already on a managed HashiCorp platform, or depending on features that landed after the fork, pay a migration cost for nothing. Decide once, per organization (`upgrades.md`).

## Related Skills

More Clawic skills, get them at https://clawic.com/skills/terraform (install if the user confirms):

- **[aws](https://clawic.com/skills/aws)** — provider-specific resource and service guidance
- **[devops](https://clawic.com/skills/devops)** — pipeline and delivery design around plan/apply gates
- **[github-actions](https://clawic.com/skills/github-actions)** — wiring plan-on-PR / apply-on-merge workflows
- **[ansible](https://clawic.com/skills/ansible)** — configuring what lives inside the instances Terraform creates
- **[k8s](https://clawic.com/skills/k8s)** — workloads on the clusters Terraform provisions

## Feedback

- If useful, star it: https://clawic.com/skills/terraform
- Latest version: https://clawic.com/skills/terraform

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/terraform.
