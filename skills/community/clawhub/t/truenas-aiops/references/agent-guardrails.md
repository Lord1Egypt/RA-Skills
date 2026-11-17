# Agent guardrails — running truenas-aiops with a smaller / local model

If you drive these tools with a local model (Llama, Qwen, Mistral … via Goose,
Ollama, LM Studio, or any OpenAI-compatible runtime), you will get noticeably
better results with a short system prompt. This page gives you one, and — more
importantly — tells you which guardrails you **no longer need to write**, because
the tool now enforces them itself.

The distinction matters. A guardrail in a prompt is a request. A guardrail in the
harness is a guarantee. Anything below that we could move into the harness, we did.

## Authorization is not this tool's job — decide it where it belongs

Whether a write should happen is your decision, or the account's. The tool does
not gate it — there is no read-only switch and no approval prompt to configure.
The two right places to control read vs write:

- **The account you connect with.** Scope the TrueNAS API key to a
  limited-privilege account (the key inherits its user's permissions). A write
  then fails at the appliance, which is the only place the permission actually
  lives — a revoked permission cannot be argued around by a model, but a
  skill-side flag can.
- **Your agent's system prompt.** If you want an observe-only session, tell the
  model not to call the write tools (they are clearly tagged `[WRITE]`).

What the tool *does* guarantee is that you can always see what happened:

## What the tool enforces — do not waste prompt budget on these

| You might be tempted to prompt | Why you don't need to |
|---|---|
| "Don't invent a value when a field is missing" | A field the TrueNAS middleware did not return comes back as `null`, never as `""`. Absent and empty are distinguishable in the payload — a disk with no `serial`, a dataset with no `mountpoint`, a replication task with no `state` all report `null`. |
| "Tell me if the output was cut off" | `snapshot_list` returns `{"snapshots": [...], "returned": N, "limit": L, "truncated": true/false}` and `undo_list` the same shape under `undos`. Truncation is measured, not guessed from a length coincidence. This matters most for snapshots: a periodic snapshot task retaining hourly/daily/weekly across a few datasets produces thousands of rows. |
| "Preserve the ordering / tell me what's most urgent" | `pool_health_rca` and `alert_and_capacity_rca` findings carry an explicit 1-based `rank`, worst-first. Priority is in the payload, not implied by list position. |
| "Confirm before anything destructive" | `snapshot delete` and `service restart` at the CLI require a `--dry-run`-able preview plus double confirmation. `snapshot_delete` captures the BEFORE state for the audit record. |
| "Log what you did" | Every governed call is audited to `~/.truenas-aiops/audit.db` regardless of what the model says it did — and the CLI writes the same row the MCP path does, so there is no unaudited entry point. `snapshot_create` additionally records a replayable inverse undo token. |
| "Don't get stuck retrying" | The runaway guard trips a circuit breaker if the same call is hammered in a tight loop — a stuck agent is stopped rather than left to burn calls and time. |
| "Don't paraphrase the pool status" | Pool `status` and `healthy` are passed through verbatim from ZFS — the ops layer never normalises `HEALTHY` / `DEGRADED` / `FAULTED` / `OFFLINE`. Only the model can break that; see the prompt below. |

## What still needs a prompt

These are model-behaviour problems the harness cannot fix from the outside.
Recommended setup for a local model (adapt it to your agent client):

```text
You operate a TrueNAS SCALE storage appliance through the truenas-aiops MCP tools.

TOOL USE
- Before answering any question about the current TrueNAS appliance, you MUST
  call a tool. Never answer from memory or assumption.
- Actually invoke the tool. Do not describe the call you would make, and do not
  emit an example JSON response in place of calling it.
- If a tool call fails, report the real error verbatim. Never fill the gap with
  a plausible-sounding answer.

READING RESULTS
- Read the whole result before concluding. If a result contains a "truncated"
  field that is true, say so and re-run with a higher limit instead of treating
  the partial result as complete.
- A null field means the middleware did not return that value. Report it as
  "not available" — never infer it.
- Report ZFS status strings exactly as returned: HEALTHY, DEGRADED, FAULTED,
  OFFLINE, UNAVAIL, REMOVED. Do not paraphrase "DEGRADED" as "having issues",
  and do not translate or prettify alert levels or IDs.
- When an RCA result has findings, work in "rank" order and cite the measured
  number in each finding's "detail" (used-percent, error counters, alert level).

IDENTIFIERS
- A pool name ("tank") is not a dataset path ("tank/data/vm") and neither is a
  snapshot id ("tank/data@auto-2026-07-18"). A snapshot id is always
  <dataset>@<snapshot-name>. Do not construct one by guessing; take it from
  snapshot_list.
- A disk device name ("sda") is not a disk serial and is not stable across
  reboots or controller changes. Quote both when identifying a disk.
- Service names are the TrueNAS middleware names ("smb", "nfs", "ssh"), not
  systemd unit names.

SCOPE
- Separate observation from interpretation. State what the tools returned, then
  any interpretation, clearly marked as such.
- Do not assert a capacity, redundancy, or performance problem unless a tool
  result supports it.
- Do not add generic advice that does not follow from the tool output.
```

## Recommended setup for a local model

Start with a connection that *cannot* write, verify, and widen the account's
permission only when you trust the setup — snapshot deletion is irreversible and
takes any dependent clones with it:

```bash
# e.g. connect with an API key for a limited-privilege TrueNAS account that
# lacks write access. Then:
truenas-aiops doctor
```

Optionally annotate the audit trail with who is operating and why — recorded on
every row, never required:

```bash
export TRUENAS_AUDIT_APPROVED_BY="your.name@example.com"
export TRUENAS_AUDIT_RATIONALE="scheduled maintenance window 2026-07-20"
```

## TrueNAS-specific notes worth knowing

- **A dataset path is not a pool name.** `tank` is a pool; `tank/data/vm` is a
  dataset inside it. `pool_get`/`pool_status` take a pool id; `dataset_get`
  takes the full dataset path. Passing one where the other is expected returns a
  404 from the middleware, not a helpful error.
- **Snapshot deletion is irreversible and destroys dependent clones.** ZFS
  clones are backed by their origin snapshot; deleting
  `tank/data@auto-2026-07-18` takes any clone promoted from it with it. That is
  why `snapshot_delete` is `high` risk, declares no undo, and only captures the
  BEFORE state for the audit record. There is no "restore from the recycle bin".
- **Report pool status verbatim.** `HEALTHY` and `DEGRADED` are ZFS states with
  precise meanings — `DEGRADED` means redundancy is lost but the pool is still
  serving I/O, which is a very different operational posture from `FAULTED`.
  Paraphrasing loses the distinction an operator acts on.
- **A scrub is not a repair.** `pool_scrub_start` kicks an integrity check; it
  will surface checksum errors and repair what redundancy allows, but it does
  not replace a failing disk. It is also long-running — poll `scrub_status`,
  never re-issue.
- **`healthy: false` with status `ONLINE` is real.** ZFS reports it after recent
  errors or an incomplete resilver. `pool_health_rca` flags it as a warning
  rather than swallowing it.
- **Capacity thresholds are about ZFS, not disk space etiquette.** ZFS is
  copy-on-write; above roughly 80% it slows and above 90% it fragments sharply.
  The RCA thresholds (`CAP_WARN_PCT` 80, `CAP_CRIT_PCT` 90) exist for that
  reason and are cited in every capacity finding.
- **Dataset usage is measured against a quota when one is set**, otherwise
  against `used + available` headroom. The finding text says which.

## If your model still struggles

Some behaviours are model-capacity limits rather than prompt problems:

- **Multi-tool workflows time out or drift.** Prefer `overview` and the two RCA
  tools (`pool_health_rca`, `alert_and_capacity_rca`) — they do the multi-step
  correlation inside one call, so the model does not have to chain reads and
  keep pool/dataset ids straight.
- **The model ignores later tool results in a long context.** Ask narrower
  questions; filter `snapshot_list` to one dataset and use `limit` deliberately
  rather than pulling every snapshot on the appliance.
- **The model describes calls instead of making them.** This is usually a
  runtime/tool-calling-format mismatch, not a prompt problem — check that your
  client advertises the tools in the format your model was trained on.

Feedback on running this with a specific local model is genuinely useful —
open an issue at
[github.com/AIops-tools/TrueNAS-AIops](https://github.com/AIops-tools/TrueNAS-AIops/issues)
with the model, runtime, and what went wrong.
