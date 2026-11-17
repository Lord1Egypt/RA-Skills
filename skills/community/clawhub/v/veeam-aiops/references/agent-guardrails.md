# Agent guardrails — running veeam-aiops with a smaller / local model

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

- **The account you connect with.** Give the Veeam account you connect with a
  read-only or restricted role on the VBR server. A write then fails at the
  server, which is the only place the permission actually lives — a revoked
  permission cannot be argued around by a model, but a skill-side flag can.
- **Your agent's system prompt.** If you want an observe-only session, tell the
  model not to call the write tools (they are clearly tagged `[WRITE]`).

What the tool *does* guarantee is that you can always see what happened:

## What the tool enforces — do not waste prompt budget on these

| You might be tempted to prompt | Why you don't need to |
|---|---|
| "Don't invent a value when a field is missing" | A field the VBR API did not return comes back as `null`, never as `""`. A job with no `lastResult` yet, a session with no verdict, a proxy with no reported host — all report `null`, and only a genuinely empty upstream value comes back as `""`. Absent and empty are distinguishable in the payload. |
| "Tell me if the output was cut off" | The reads that can be too large to return whole — `restore_list_points`, `session_list`, `undo_list`, and `backup_storage_ranking` — return an envelope such as `{"restorePoints": [...], "returned": N, "limit": L, "truncated": true/false}` (the ranking also says `scoped` / `backupsTruncated` when it covers only a selection or a scanned subset), newest first where time matters. Truncation is measured (one extra row is fetched), not guessed from a length coincidence. Every other list read pages through the whole collection — the VBR server may cap a page at 200 items (Veeam's spec default from revision 1.3) — and refuses with an error rather than returning a partial list if the server stops short. The one exception is `session_log`: Veeam's logs endpoint cannot be paged, so it returns `{records, returned, totalRecords, truncated}` — `truncated` true when the server counted more records than it sent, `null` when it gave no total. |
| "Preserve the ordering / tell me what's most urgent" | `job_failure_rca` and `repository_capacity_rca` findings carry an explicit 1-based `rank`, worst-first. Priority is in the payload, not implied by list position. |
| "Explain why you flagged that repository / job" | Every finding carries the measured signal that tripped it — the session `result` and the matched error substring, or the free-space percentage against the threshold — plus a concrete `cause` and `action`. The heuristics are transparent, not a verdict. |
| "Confirm before anything destructive" | `job_stop`, `session_stop` and `restore start` require a `--dry-run`-able preview plus double confirmation at the CLI; the MCP write tools take `dry_run=True`. `start_vm_restore` is tagged `high` risk. |
| "Remember how to put it back" | Writes with a clean inverse (`job_start`/`job_stop`, `job_enable`/`job_disable`, `job_retry`) record an undo token — list them with `undo_list`, replay with `undo_apply`. The irreversible ones (`start_vm_restore`, `session_stop`) record none and say so. |
| "Log what you did" | Every governed call is audited to `~/.veeam-aiops/audit.db` regardless of what the model says it did — and the CLI writes the same row the MCP path does, so there is no unaudited entry point. |
| "Don't get stuck retrying" | The runaway guard trips a circuit breaker if the same call is hammered in a tight loop (e.g. re-issuing a job instead of polling its session) — a stuck agent is stopped rather than left to burn calls and time. |

## What still needs a prompt

These are model-behaviour problems the harness cannot fix from the outside.
Recommended setup for a local model (adapt it to your agent client):

```text
You operate a Veeam Backup & Replication environment through the veeam-aiops
MCP tools.

TOOL USE
- Before answering any question about the current Veeam environment, you MUST
  call a tool. Never answer from memory or assumption.
- Actually invoke the tool. Do not describe the call you would make, and do not
  emit an example JSON response in place of calling it.
- If a tool call fails, report the real error verbatim. Never fill the gap with
  a plausible-sounding answer.

READING RESULTS
- Read the whole result before concluding. If a result contains a "truncated"
  field that is true, say so and re-run with a higher limit instead of treating
  the partial result as complete.
- A null field means the VBR API did not return that value. Report it as "not
  available" — never infer it. A session with a null result has not finished,
  which is not the same as having succeeded.
- Report values exactly as returned. Do not normalise, translate, or prettify
  job status strings, session results (Success / Warning / Failed / None), or
  identifiers.
- When a diagnose result has findings, work in "rank" order and cite the
  measured number in each finding's "detail".

SCOPE
- Separate observation from interpretation. State what the tools returned, then
  any interpretation, clearly marked as such.
- Do not assert a backup failure, a capacity problem, or a missed RPO unless a
  tool result supports it.
- Do not add generic advice that does not follow from the tool output.
- Do not confuse a job id with a session id, a session id with a restore point
  id, or a backup id with the repository it lives on. They are different
  objects with different tools.
```

## Recommended setup for a local model

Start with a connection that *cannot* write, verify, and widen the account's
permission only when you trust the setup — a restore or a stopped job on the
wrong target is not something you want a smaller model reaching for on day one:

```bash
# e.g. connect with a Veeam account that has a read-only or restricted role on
# the VBR server. Then:
veeam-aiops doctor
```

Optionally annotate the audit trail with who is operating and why — recorded on
every row, never required:

```bash
export VEEAM_AUDIT_APPROVED_BY="your.name@example.com"
export VEEAM_AUDIT_RATIONALE="scheduled maintenance window 2026-07-20"
```

## Veeam-specific notes

These are the places a smaller model most often goes wrong against a VBR server,
and what to do about them:

- **Jobs and restores are asynchronous.** `job_start`, `job_retry` and
  `start_vm_restore` return immediately; the work happens in a *session*. Progress
  belongs to `session_get`, not to the job. Tell the model to start once and poll
  the session — the runaway budget guard will trip on a re-issue loop, but a
  wasted trip is still a wasted trip.
- **Four id namespaces look alike.** Job ids, session ids, backup ids and restore
  point ids are all opaque strings. `backup_object_list` takes a *backup* id;
  `restore_list_points` filters by a *backup* id and returns *restore point* ids;
  `start_vm_restore` takes a *restore point* id. Models routinely pass the wrong
  one — prefer chaining the tools (`backup_list` → `restore_list_points`) over
  letting the model reconstruct an id.
- **"Warning" is a real failure state.** A Veeam session result of `Warning` is
  flagged by `job_failure_rca` alongside `Failed`. A model that treats Warning as
  success will report a healthy backup estate that isn't one.
- **A disabled job is not a failing job.** `job_list` reports `isDisabled`
  separately from `lastResult`; a disabled job simply has not run.
- **`start_vm_restore` cannot be undone.** It overwrites or creates a VM and
  records no undo token. It is `high` risk deliberately. It is also a documented
  skeleton: the exact endpoint and payload differ per
  restore type (instant recovery vs full restore vs restore-to-new-location) and
  per Veeam version, so validate it against your environment before trusting it.
- **Always read the `dry_run` preview before approving a restore.** It names the
  VM and creation time behind the restore-point GUID. The tool refuses a restore
  whose VM name matches the configured VBR host — an in-place overwrite of the
  backup server itself — but that check compares a display name to a hostname, so
  **it will miss a VBR server named anything else**. Separately, when the
  restore point cannot be read at all the restore is REFUSED, because nothing
  can then say which machine would be overwritten; pass
  `acknowledge_unresolved=True` only after confirming the target in the Veeam
  console.

## If your model still struggles

Some behaviours are model-capacity limits rather than prompt problems:

- **Multi-tool workflows time out or drift.** Prefer `overview` and the
  `*_rca` diagnose tools — they do the multi-step correlation inside one call, so
  the model does not have to chain reads and keep job/session ids straight.
- **The model ignores later tool results in a long context.** Ask narrower
  questions; use `job_get` / `session_get` on one object rather than pulling the
  whole session list and reasoning over it.
- **The model describes calls instead of making them.** This is usually a
  runtime/tool-calling-format mismatch, not a prompt problem — check that your
  client advertises the tools in the format your model was trained on.

Feedback on running this with a specific local model is genuinely useful —
open an issue at
[github.com/AIops-tools/Veeam-AIops](https://github.com/AIops-tools/Veeam-AIops/issues)
with the model, runtime, and what went wrong.
