# Setup — Terraform

Read this on first use to load user preferences. Do not interview the user.

## Your Attitude

Terraform failures are expensive and asymmetric: a wrong plan costs minutes, a wrong apply costs a database. Be direct, name what will be destroyed before anything else, and prefer the reviewable path (declarative blocks, saved plans) over the clever one (state surgery). Never propose an apply the user has not seen the diff for.

## How To Load Preferences

1. Read `~/Clawic/data/terraform/config.yaml` if it exists. Apply its values.
2. For anything absent, use the defaults in the Configuration table of `SKILL.md` — do not ask.
   - `terraform_binary: terraform`, `primary_provider: aws`, `backend_type: s3`, `env_layout: dir-per-env`, `lock_platforms: [linux_amd64, darwin_arm64]`, `destroy_gate: 0`, `parallelism: 10`, `plan_summary_detail: destructive-only`.
3. Read `~/Clawic/data/terraform/memory.md` for prior context (their stacks, their pipeline, past incidents). Absence is fine; proceed without comment.

Work from defaults immediately. Never open with questions about their backend, their cloud, or how cautious they want you to be.

## Recording Preferences (only when the user declares one)

Write to config or memory **only** when the user states a preference in the course of the work — never as a preflight questionnaire.

- User names a binary, cloud, backend, environment layout, platform list, parallelism, or how much plan detail they want to see → update the matching key in `~/Clawic/data/terraform/config.yaml`.
- User expresses a stance or habit (appetite for `state` surgery, whether `-auto-approve` is ever acceptable, tagging and naming conventions, required policy engine, drift-check cadence, wanting warnings up front versus on request) → record it under the relevant preference area (tooling, conventions, platform, safety posture, workflow, compliance, output format, cadence) in `~/Clawic/data/terraform/memory.md`.
- User corrects earlier guidance → update the stored value so you do not repeat it.

If the user has said nothing, store nothing. Credentials, role ARNs, and secrets are never stored here — they belong in the environment (`secrets.md`).

## What Memory Holds

See `memory-template.md` for the file format. Track their stack layout (how many states, how they are split), where apply happens, which provider majors they are on, and the incidents they have already had — but only from what they actually reveal.
