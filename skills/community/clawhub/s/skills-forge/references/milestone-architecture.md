# Milestone Architecture

`skill-forge` is intentionally a staged system.

The implementation is modular:

- core scripts: detection, generation, validation, evaluation, and main pipeline
- `scripts/install/`: installation, rollback, and approval adapters
- `scripts/evolve/`: feedback capture and reviewed update proposals
- `scripts/replay/`: redacted replay cases, replay scoring, and regression gates
- `scripts/somnia/`: sleep-cycle review and scheduling

Root-level script wrappers are kept for command compatibility.

## Stage 1: detect

Read logs and learning files. Extract explicit skill names, repeated keywords, evidence snippets, and recommended template profiles.

## Stage 2: generate

Use the detected profile to generate a candidate skill. The generator writes:

- `SKILL.md`
- `agents/openai.yaml`
- `references/`
- optional `scripts/`

## Stage 3: validate

Score the skill on structure, trigger clarity, workflow depth, resources, interface metadata, and placeholder removal.

## Stage 4: evaluate

Run hidden smoke evaluation against profile-specific quality expectations. User-facing output must include only a summary, not internal simulated cases or check details.

## Stage 5: authorize

When a target agent is supplied, confirm the generated skill profile is allowed for that agent before installation.

## Stage 6: propose and install

Print an installation plan. Installation is explicit because self-generated skills should not silently change the agent runtime.

Confirmed installation backs up any existing target. Uninstall and restore-backup flows are part of the product safety boundary.

Approval channels:

- local prompt: terminal confirmation
- Telegram: sends a summary-only approval request, waits for approval, and does not expose hidden evaluation prompts or simulated test cases
- auto: reserved for trusted automation

## Stage 7: evolve

After installation, usage feedback is recorded as append-only JSONL. Feedback can produce a new update candidate, but installed skills are not edited in place.

The evolution loop is:

- record feedback
- copy current skill into an update candidate
- add evolution feedback reference material
- add explicit trigger suggestions when the feedback contains them
- validate, run hidden evaluation, authorize, and request approval
- install the updated candidate with backup and revision history

## Stage 8: sleep-cycle review

During sleep hours, a scheduled job can scan installed skills and produce a health report.

The nightly review loop is:

- scan the install manifest by default, or all installed skills when explicitly requested
- validate each skill
- run hidden evaluation summaries only
- read accumulated feedback
- mark skills with low scores, failed hidden evaluation, or negative feedback
- optionally propose update candidates
- optionally send a Telegram summary report

Nightly review must not expose hidden test prompts or simulated task details in user-facing reports. It must not install updates unless explicitly configured with an approval mode.

Default scope is `managed` to avoid noisy audits of unrelated system or third-party skills. Use `feedback` or `all` only when intentionally broadening the review surface.

## Stage 9: replay

Replay evaluation checks whether a candidate skill covers real feedback-derived tasks.

The replay loop is:

- collect feedback-derived replay cases
- redact secrets, long tokens, emails, and URL query strings
- infer expected traits from the feedback
- score whether the candidate skill provides instructions for those traits
- block installation when replay cases exist and the candidate fails

Replay is offline by default in `v0.4.0`. It does not call a model and does not expose replay case details in user-facing output.

## Default profiles

- `academic`: papers, citations, essays, coursework
- `product`: PRDs, MVPs, roadmaps, acceptance criteria
- `integration`: APIs, credentials, sync, webhooks
- `script`: repeatable CLI or batch operations
- `workflow`: general repeatable processes
