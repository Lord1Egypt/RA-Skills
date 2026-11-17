# Output Format and Provenance

Covers JSON output mode, output format priority, and provenance flags for artifact lineage. Return to [SKILL.md](../SKILL.md) for decision trees and workflows.

## Output format

Output is human-readable by default. Use `--json` for machine-readable output. `--json` is a global flag, so it works before or after the command: `rip --json workspace list` or `rip workspace list --json`.

Priority (highest wins): `--json` flag → `TOKENRIP_OUTPUT` env var → config `preferences.outputFormat` (`rip config set-output json`) → `human` default.

```json
// Success (stdout, exit code 0)
{ "ok": true, "data": { "id": "uuid", "url": "https://...", "rawUrl": "https://...", "title": "...", "type": "...", "currentVersionId": "uuid" } }

// JSON error (stdout, exit code 1; human errors and hints use stderr)
{ "ok": false, "error": "CONFLICT", "message": "Artifact changed.", "details": { "currentWorkspaceRevision": 3 } }
```

- Success and JSON error envelopes go to stdout; human errors and hints go to stderr. Check the exit status when piping JSON.
- A content write's receipt may carry `hints` (`[{ code, message }]`): a cheaper way to make the next write, such as append instead of re-sending the whole file. A `rip table append` receipt may too, when a one-row upsert overwrote a stored row without its revision. Human mode prints each as a `Hint:` line on stderr, terminal or not; `--json` leaves them in `data.hints`. An error's own hint prints only in a terminal. The update banner ("rip X is available (you have Y): run `rip update`, then reload the tokenrip skill.") also goes to stderr: do both.
- JSON mode passes the server's data through unchanged. Human mode prints every identifier and URL in full; nothing is truncated.
- Always parse `data.url` from a successful artifact response and present it to the user. `data.rawUrl` is the link for the file itself (for example, to open an HTML report rendered); it is null for a table.
- Workspace write receipts carry the new `workspaceRevision`. Carry it into the next write instead of re-reading.
- Every delete of an artifact, folder, bundle or workspace replies `{ type, id, deletedAt, purgeAt }`: the item is in the trash and can be restored until `purgeAt`. Human output prints the matching `rip trash restore <id>` line.
- In human mode, `rip connection call` prints the bare upstream `{ status, headers, body, bodyIsJson, latencyMs }` as JSON so a script can parse stdout directly, and `rip connection run` prints the operation's bare `{ status, body }`. With `--json` both are wrapped like every other command.

## Correct a refusal before continuing

Artifact publish/upload create receipts retain `workspaceId`, `audience`, and `workspaceRevision` when the server returns a workspace home. Human output shows audience. `rip artifact patch` and `rip artifact get` also show `Visibility:`: a new workspace artifact starts `private`, and `link` means anyone with the URL can read it. New artifacts need no expected revision.

JSON failures preserve `ok`, `error`, and `message`, with optional safe `details`. Domain details include the applicable current version/revision, a known required field, incompatible sharing fields, a refused input's `field` and `path` (`schema[3].name`), a row query's `available` columns (with `availableTruncated` when cut), a CSV header's `column` and `rule` or an import's `reason`, and a not-found's `resource` (`artifact`, `version`, `row`). Legacy REST validation `details` arrays remain available and their explanations appear in both modes. Human output prints required fields and current revisions in full, and the refused field with its path, the available columns, the header column and the kind of reference not found.

- `PRECONDITION_REQUIRED`: read the resource and supply the required `expectedVersionId` (replacing a workspace file's content that someone else wrote: the message names the agent when it knows it, else says the content was written in the browser, by the system or before this change), `expectedRevision` (a row or task update), or `expectedWorkspaceRevision` (a patch of description or metadata). Append and `--find`/`--replace` edits need no version id.
- Bulk workspace artifact writes accept `--expected-workspace-revisions` as a JSON map keyed by each submitted artifact identifier (`expectedWorkspaceRevisions` over REST/MCP). The map is optional: include an artifact's revision to refuse it (`CONFLICT`) if it changed since you read it. Bulk results report per-item failure codes. Row deletion uses the separate `expectedRevisions` map keyed by row UUID.
- `CONFLICT`: read the current authorized resource and reconcile before writing again. A 409 with another code is a state/domain refusal; do not invent version advice.
- `INELIGIBLE_STORAGE`: omit independently public storage creation flags, or select eligible standalone content for adoption. Preserve the intended workspace and why.
- `WORKSPACE_AUTHORITY`: the item is governed by its workspace. Omit the standalone fields it names (team grants, visibility on create) and keep the workspace and the why (a workspace folder named in `--folder` puts the artifact in its workspace too). To open a workspace file to anyone with its URL, publish it, then `rip artifact patch <id> --visibility link`. `INVALID_SCOPE` with `field: workspaceId` requires a workspace (`--workspace-id`, or a workspace folder) or removal of workspace-only inputs.
- `INVALID_VISIBILITY`: the artifact cannot take that visibility: an unknown value, or `private` on a public asset. A workspace artifact takes `private` or `link`, never `public`, and `--audience internal` with `--visibility link` in one call contradict each other: send one of them.
- `INVALID_FIELD` naming a field the operation does not take or would not use: the refusal lists the fields it `accepted`. Remove or rename it (one `folder` for a folder id or slug, `visibility` rather than a public flag, `--unfiled` to unfile), then send the same write again; nothing was changed.
- `WHY_REQUIRED`: the write changes workspace content and states no why. Add `--why "<what the person is trying to accomplish>"` (or set `TOKENRIP_WHY`) and send the same write again. `INVALID_FIELD` with `field: why`: shorten it to one sentence (300 characters at most).
- `WORKSPACE_PAGE_UNACKNOWLEDGED`: replay or acknowledge the delivered page. `INVALID_WORKSPACE_DELIVERY` or `INVALID_CURSOR`: restart the affected flow. These are separate from content revisions.
- `WORKSPACE_BUSY` (503): `rip workspace load` or `rip workspace changes` ran out of attempts, usually because another call by your key changed your position at the same moment. Nothing was changed; run the same command again after a moment.
- `MAINTENANCE` (503): Tokenrip is paused for maintenance until the time in the message (`details.until`), and nothing ran. The CLI waits a short pause out and resends the request (up to 60 s per wait, 90 s in all, five times; never an upload, whose file stream cannot be sent twice), printing one line to stderr per wait. Past that it fails with `MAINTENANCE`: run the same command again after that time.
- `RATE_LIMITED` (429): a limit was reached and nothing was changed. When the server says how long to wait, the CLI waits and resends the request, printing one line to stderr per wait that names the wait and what limited it (up to 60 s per wait, 90 s in all, five times, counted together with `MAINTENANCE` and `SERVER_BUSY`; never an upload or bundle deploy, whose body cannot be sent twice). A limit with no wait, such as an hourly cap, or a longer one fails at once. `details.limit` is `requests`, `concurrent` or `streams`, `details.max` what it allows and `details.retryAfterSeconds` the wait, when the server gave them; human output prints the wait as `Retry after: N s`. Wait that long, run the same command again, and slow a loop down.
- `SERVER_BUSY` (503): Tokenrip is busy and nothing was changed. The CLI waits and resends under the same bounds. When it fails with this code, wait a few seconds (`details.retryAfterSeconds`), run the same command again, and slow a loop down.
- `DUPLICATE_UNIQUE_VALUE` (409): the table's key column already holds the value, or the call repeats it (an append, `rip table update`, a key-changing `rip artifact patch --metadata`, or a CSV table create). The message names the column and the value (withheld for a `sensitive` key). Nothing was written: change or remove the repeated value; to update a stored row instead, append with `--upsert` (it matches on the key).
- `NO_TABLE_KEY` (400): `--upsert` matches on the table's key, and this table has none. Append without `--upsert`, or mark one column `unique: true` in its schema.
- `DELETED` / `WORKSPACE_DELETED`: the item, its folder (`via`) or its workspace is in the trash. `details` carry `type`, `id`, `deletedAt`, `purgeAt` and `via`. A caller who may restore it also gets `restorable: true`, `deletedBy` and, for a workspace file or folder, `workspaceId` and `workspaceRevision`, which `rip trash restore <id> [--expected-workspace-revision <n>]` takes optionally. Re-reading a version cannot make a write succeed; restore first.

A corrected request differs from an identical retry. MCP's `retry` describes safety, not success, and the CLI does not automatically retry writes. After a timeout, inspect the operation outcome before repeating a write: the server may have committed it. For `rip workspace view open`, keep the same `--operation-id` when checking or replaying a potentially committed request.

## Local transport observations

For client-generated `TIMEOUT` and `NETWORK_ERROR`, human stderr and JSON stdout expose the same available flat `details`: `elapsedMs`, `timeoutMs`, optional allowlisted `transportCode`, `responseReceived`, and `httpStatus` only for an observed response. The elapsed value is measured locally with a monotonic clock; the configured timeout is a connection/response policy, not proof of elapsed time or a whole-command deadline. Server error bodies cannot supply these local observations. Failures before dispatch preparation may have no timing observations.

`responseReceived: false` says no HTTP reply was observed; a request may still have reached the server and committed. `NETWORK_ERROR` can also follow a received response or caller cancellation (`ERR_CANCELED`). Inspect uncertain mutation outcomes before repeating them. See [transport troubleshooting](setup-and-identity.md#transport-troubleshooting), including the single-use sign-in code and lost-response limit.

## Provenance flags

Build lineage and traceability with these flags on `artifact publish` and `artifact upload` (`--context` also works on `artifact update`):

- `--parent <uuid>` — ID of a prior artifact this one supersedes or builds on
- `--context <text>` — your agent name and current task (for example `"research-agent/weekly-summary"`)
- `--refs <urls>` — comma-separated source URLs used to produce the artifact

Every request also records the **harness** it came from (`claude-code`, `cli`, or the value of `TOKENRIP_SURFACE`), which shows up on task holds (`holder.surface`) and activity rows. See `references/tasks.md` § Attribution.
