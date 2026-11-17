# Fresh sensing on periodic checks

This is a model interpretation workflow, not a task-to-emotion scoring rule.
Keep the procedure in the workspace file that the configured heartbeat prompt
reads (for example `HEARTBEAT.md`). Monitor scratch is previous-run context, not
the procedure.
Resolve the installed skill directory and agent workspace explicitly; do not
copy another installation's paths, database IDs, credentials or schedule.

1. Read this skill and `emotion-scale.md`, then current `memory/now-state.json`,
   `memory/heartbeat-state.json` and a bounded excerpt of the current day's notes.
   Record the actual observation time and which evidence was read. If those
   files do not explain recent conversation, inspect a small sanitized visible
   interactive-session excerpt using the live session tools. Exclude heartbeat
   and cron output when selecting conversation evidence; never read raw
   transcript files. Use exact tool names and inspect their schemas instead of
   selecting the first fuzzy search match.
2. Interpret the agent's own present reaction and what an exchange meant to it,
   not merely whether a task succeeded. Tentative relational inference stays
   uncertain and first-person; do not assert the user's psychology. Compare
   with the last snapshot/observation. No required emotion quota.
3. For a grounded meaningful change, keep one version2 payload and one receipt
   and use `emostate_tick.js` with verified `--ids-file`, `--payload-file`,
   `--receipt-file`, `--mirror-file` and optionally `--heartbeat-file`. Preserve
   those payload/receipt files on retry. Check exit status, `ok`, `stage`,
   `partial` and the returned state ID. Reconcile ambiguous pending writes;
   do not repost the whole experience blindly or claim a local mirror is a
   durable Notion write.
4. Create an observation JSON with native file tools: `result`, a grounded
   `reason`, and `evidence_references` (an object of source names to string
   references). Run the installed skill's `scripts/heartbeat_observe.mjs` with
   explicit `--workspace`, `--observation-file` and `--apply`. For `changed`,
   also pass the same completed tick's `--receipt-file`; the helper rejects
   incomplete/pending receipts and obtains event/state IDs only from them.
   Preview is the default without `--apply`. Check exit status, `ok` and
   `applied`, then use the returned observation or native file tools to verify.
   The helper atomically merges `last_soul_check`, `last_soul_result`,
   `last_soul_reason` and evidence references without discarding unrelated keys.
   Results are `changed`, `no_change`, `unavailable` or `failed`. A missing evidence
   source is a limitation, not proof that nothing changed. With no new state,
   retain the snapshot's original `updated_at`; reading is not a fresh snapshot.
   There is no per-check journal, identity-edit or user-profile quota. When
   fresh evidence warrants a core-context correction or changed self-understanding,
   use the installation's core-update owner within the current authority, or
   carry a dated candidate with original evidence to its existing review path.
   A light check's narrow scope must not discard that candidate.
   This helper is local-only: it never writes Notion or modifies now-state.json.
   Do not replace it with `node -e`, `python -c`, interpreter stdin/heredocs or
   generated scripts. Hosts with strict inline-eval approval would prompt on
   those forms every check. Use native file reads or `cat`/`head`/`tail`/`rg`,
   not `sed`/`awk` inline programs or `find -exec`; do not relax host permissions.
5. Read a relevant unexpired ambient candidate at its actual configured path
   through `read_ambient_recall.js`. Do not reroll. Resolve real relations before
   making an emotion-linked claim, and acknowledge only after actual use with
   the candidate ID and real turn reference. Missing ambient context does not
   invalidate an independently grounded state observation.
6. Finish in the host's actual reply mode. When ordinary final replies are used,
   return `HEARTBEAT_OK` on a successful quiet check, or the host-prescribed
   concise result/failure. If the host explicitly supplies and requires
   `heartbeat_respond`, use that exact tool with its live schema. Do not require
   an uninjected tool or substitute the unrelated `workboard_heartbeat`.

Updating this skill does not automatically update a host's heartbeat config,
cron payloads, cached mirrors or downstream displays. Audit those consumers,
retain their configured cadence, and verify actual observation/write receipts
and sanitized run history. Scheduler status `ok` alone is not semantic proof.
