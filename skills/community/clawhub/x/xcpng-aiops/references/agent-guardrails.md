# Agent guardrails — running xcpng-aiops with a smaller / local model

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

- **The Xen Orchestra account whose token you connect with.** Give that XO user
  a read-only ACL, or scope its personal token down. A write then fails at Xen
  Orchestra, which is the only place the permission actually lives — a revoked
  permission cannot be argued around by a model, but a skill-side flag can.
- **Your agent's system prompt.** If you want an observe-only session, tell the
  model not to call the write tools (they are clearly tagged `[WRITE]`).

What the tool *does* guarantee is that you can always see what happened:

## What the tool enforces — do not waste prompt budget on these

| You might be tempted to prompt | Why you don't need to |
|---|---|
| "Don't invent a value when a field is missing" | A field Xen Orchestra did not return comes back as `null`, never as `""`. A VM with no `name_label`, a task with no `properties.name`, an SR with no `content_type` — all report `null`. Absent and empty are distinguishable in the payload. |
| "Tell me if the output was cut off" | Every listing returns `{"vms": [...], "returned": N, "limit": L, "truncated": true/false}` (same shape with `srs`, `vdis`, `snapshots`, `tasks`, `jobs`, `logs`, `undos`). Truncation is **measured** — the full collection length client-side, or one over-fetched record for `backup_log_list` — never guessed from the row count matching the limit. The RCA tools report `inputTruncated` when the listing they correlated over was itself capped. |
| "Preserve the ordering / tell me what's most urgent" | RCA findings carry an explicit `severity` (`high`/`medium`/`low`) and are already sorted worst-first, each with the measured number in `evidence` and a concrete `action`. Priority is in the payload, not implied by list position. |
| "Confirm before anything destructive" | Destructive operations (`snapshot_delete`, `snapshot_revert`, `vm_stop`/`reboot`/`migrate`) require a `dry_run` preview + double confirmation at the CLI. Reversible writes capture the prior state so the undo token can restore it. |
| "Never stop the Xen Orchestra VM itself" | **Only if the operator declared it.** Set `xo_self_vm_uuid` on the target and `vm_stop` refuses exactly that uuid on both the MCP and CLI paths. Undeclared, nothing is refused — XO exposes no self endpoint and its token carries no claims, so the tool cannot work this out and fails open rather than guess. Keep a prompt line for this if you cannot declare the uuid. |
| "Log what you did" | Every governed call is audited to `~/.xcpng-aiops/audit.db` regardless of what the model says it did — and the CLI writes the same row the MCP path does, so there is no unaudited entry point. |
| "Don't get stuck retrying" | The runaway guard trips a circuit breaker if the same call is hammered in a tight loop — a stuck agent is stopped rather than left to burn calls and time. |

## What still needs a prompt

These are model-behaviour problems the harness cannot fix from the outside.
Recommended setup for a local model (adapt it to your agent client):

```text
You operate an XCP-ng environment through the xcpng-aiops MCP tools. They talk
to Xen Orchestra's REST API; there is no direct per-host XAPI access.

TOOL USE
- Before answering any question about the current XCP-ng environment, you MUST
  call a tool. Never answer from memory or assumption.
- Actually invoke the tool. Do not describe the call you would make, and do not
  emit an example JSON response in place of calling it.
- Start broad triage with "overview" — it fans out over pools, hosts, VMs, SRs
  and recent backup runs in one call.
- If a tool call fails, report the real error verbatim. Never fill the gap with
  a plausible-sounding answer.

READING RESULTS
- Listings come back as an envelope, not a bare list: read the items under
  "vms" / "srs" / "vdis" / "snapshots" / "tasks" / "jobs" / "logs".
- If "truncated" is true, say so and re-run with a higher limit instead of
  treating the partial result as complete. If an RCA reports "inputTruncated",
  its conclusion covers only a subset — state that.
- A null field means Xen Orchestra did not return that value. Report it as "not
  available" — never infer it.
- Report values exactly as returned. Do not normalise, translate, or prettify
  power states, SR types, statuses, or uuids.
- When an RCA result has findings, work in the order given (worst first) and
  cite the measured number in each finding's "evidence".

IDENTIFIERS
- Every object is addressed by its XO uuid: a VM uuid (vm_list), a host uuid
  (host_list), a pool uuid (pool_list), an SR uuid (sr_list), a VDI uuid
  (vdi_list), a snapshot uuid (snapshot_list). They are NOT interchangeable —
  do not pass a host uuid where a VM uuid is expected.
- A name_label is a label, not an identifier: it is not unique and must never
  be used in place of a uuid. Resolve the name to a uuid with a list tool first.
- An XO task id (task_list) identifies an async job, not the object it acted on.

SCOPE
- Separate observation from interpretation. State what the tools returned, then
  any interpretation, clearly marked as such.
- Do not assert a capacity, performance, or availability problem unless a tool
  result supports it.
- Do not add generic advice that does not follow from the tool output.
```

## Recommended setup for a local model

Start with a connection that *cannot* write, verify, and widen the account's
permission only when you trust the setup — snapshot delete/revert are
irreversible, and stopping the wrong VM can be the one XO itself runs on:

```bash
# Give the Xen Orchestra account a read-only ACL, or scope its personal token
# down, so writes fail at XO rather than depending on a skill-side flag. Then:
xcpng-aiops doctor
```

Optionally annotate the audit trail with who is operating and why — recorded on
every row, never required:

```bash
export XCPNG_AUDIT_APPROVED_BY="your.name@example.com"
export XCPNG_AUDIT_RATIONALE="scheduled maintenance window 2026-07-20"
```

## If your model still struggles

Some behaviours are model-capacity limits rather than prompt problems:

- **Multi-tool workflows time out or drift.** Prefer `overview` and the four RCA
  tools (`vm_health_rca`, `sr_usage_rca`, `backup_failure_rca`,
  `pool_patch_ha_posture`) — they do the multi-step correlation inside one call,
  so the model does not have to chain reads and keep uuids straight.
- **The model ignores later tool results in a long context.** Ask narrower
  questions and use `limit` (plus the `pool` / `sr` / `power_state` / `status`
  filters) deliberately rather than pulling whole inventories. `vdi_list` in
  particular is the longest listing in a real fleet.
- **The model describes calls instead of making them.** This is usually a
  runtime/tool-calling-format mismatch, not a prompt problem — check that your
  client advertises the tools in the format your model was trained on.

Feedback on running this with a specific local model is genuinely useful —
open an issue at
[github.com/AIops-tools/XCPng-AIops](https://github.com/AIops-tools/XCPng-AIops/issues)
with the model, runtime, and what went wrong.
