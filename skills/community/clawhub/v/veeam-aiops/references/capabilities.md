# veeam-aiops capabilities

27 MCP tools (19 read, 8 write), each wrapped with the bundled `@governed_tool`
harness. Typical response token estimates assume a small/medium environment.

## Overview (1 — read)

| Tool | R/W | Risk | Typical response tokens |
|------|:---:|:----:|:----------------------:|
| `overview` | R | low | ~150 |

Fan-out health summary: jobs grouped by last result, repositories at/above 85%
used, and currently-running sessions. Call this first to triage an environment.

## Diagnostics / RCA (2 — read)

| Tool | R/W | Risk | Typical response tokens |
|------|:---:|:----:|:----------------------:|
| `job_failure_rca` | R | low | ~200–600 |
| `repository_capacity_rca` | R | low | ~150 |

`job_failure_rca` scans the newest `limit` sessions (default 100, newest first by
`creationTime`; `sessionsTruncated` says older ones exist) — pass `since_hours=24`
to make the window "the last day" instead — flags every Failed/Warning run, and
categorizes the likely cause (repository full, source/guest unreachable,
credential/VSS failure, retry exhaustion) from the failing log records — each
finding cites the session result + matched error substring, worst-first.
`repository_capacity_rca` flags repositories under the free-space thresholds
(<15% warn, <10% critical), citing the measured free% and free bytes.

## Backup Jobs (7 — 2 read, 5 write)

| Tool | R/W | Risk | Undo | Typical response tokens |
|------|:---:|:----:|------|:----------------------:|
| `job_list` | R | low | — | 150–600 (depends on job count) |
| `job_get` | R | low | — | ~120 |
| `job_start` | W | medium | `job_stop` | ~50 |
| `job_stop` | W | medium | `job_start` | ~50 |
| `job_retry` | W | medium | `job_stop` | ~50 |
| `job_enable` | W | medium | `job_disable` | ~40 |
| `job_disable` | W | medium | `job_enable` | ~40 |

REST endpoints: `GET /api/v1/jobs`, `GET /api/v1/jobs/{id}`,
`POST /api/v1/jobs/{id}/{start|stop|retry|enable|disable}`. The write tools
capture the job's prior status/lastResult for context.

## Restore (2 — 1 read, 1 write)

| Tool | R/W | Risk | Undo | Typical response tokens |
|------|:---:|:----:|------|:----------------------:|
| `restore_list_points` | R | low | — | 150–800 |
| `start_vm_restore` | W | high | **none — irreversible** | ~40 |

`restore_list_points` returns the newest `limit` points (default 100, max 1000) as
`{"restorePoints", "returned", "limit", "truncated", "order"}` — an estate's restore
points are far too many to return whole. With `backup_id`, a point from another
backup coming back means the server ignored the filter, and that is refused.

REST endpoints: `GET /api/v1/restorePoints` (`orderColumn=CreationTime&orderAsc=false`,
optional `backupIdFilter`),
`GET /api/v1/restorePoints/{id}` (to name what a restore would overwrite),
`POST /api/v1/restore/vm`. `start_vm_restore` is a documented skeleton: the
exact restore endpoint and payload vary by restore type and Veeam version.

The payload carries **no target mapping**, so it is a restore-to-original — an
in-place overwrite. Two consequences worth knowing before you call it:

- `dry_run=True` resolves the opaque restore-point id to the **VM name and
  creation time** it would overwrite.
- **An unreadable restore point is refused**, by the preview and the real call
  alike: with no target mapping this is a restore-to-original with no undo, and
  a tool that cannot name the machine it is about to overwrite has not given
  anyone something to approve. `acknowledge_unresolved=True`
  (CLI `--acknowledge-unresolved`) proceeds anyway, for when the target has been
  confirmed in the Veeam console; `resolved: false` then says the target is
  unknown. Refusing errs recoverably — restore from the console — while
  proceeding errs onto a machine nobody could name.
- It **refuses** when that VM name matches the configured VBR host — **on the
  dry-run as well as the real call**, with identical behaviour. A
  preview that returns green for a call that will then be refused is a preview
  reporting the wrong outcome. Veeam's own
  guidance is to back up the VBR server itself, so its restore point sits in the
  same list as every other one with nothing marking it as special. **This check
  is a safety net, not a proof**: a VM display name is not a hostname, so a VBR
  server whose VM is named `Backup Server 01` is not caught. An unknown name is
  still never read as "it is the VBR server" — that judgement stays open — but
  the restore itself is now refused in that case by the separate unreadable-
  target guard above.

### Dry-run semantics (line-wide)

`dry_run=True` returns `{"dryRun": true, "would...": {...}}`. A dry-run **may read** —
resolving ids and evaluating guards is exactly what lets it answer "would this be
refused?" — but it **never writes** and records **no undo**. It runs through
`@governed_tool` like any other call, so it is audited and it can be refused. The CLI
`--dry-run` routes through the same governed function, so both entry points behave
identically.

## Repositories (3 — read)

| Tool | R/W | Risk | Typical response tokens |
|------|:---:|:----:|:----------------------:|
| `repository_list` | R | low | 100–400 |
| `repository_get` | R | low | ~120 |
| `repository_state` | R | low | 100–400 |

REST endpoints: `GET /api/v1/backupInfrastructure/repositories`,
`GET /api/v1/backupInfrastructure/repositories/{id}`,
`GET /api/v1/backupInfrastructure/repositories/states` (capacity / free / used,
plus a computed used%). `repository_get` merges the static record with its state
row when available.

## Backups (4 — read)

| Tool | R/W | Risk | Typical response tokens |
|------|:---:|:----:|:----------------------:|
| `backup_list` | R | low | 150–800 |
| `backup_object_list` | R | low | 150–800 |
| `backup_object_storage_usage` | R | low | 400–1500 |
| `backup_storage_ranking` | R | low | 300–2000 |

REST endpoints: `GET /api/v1/backups`, `GET /api/v1/backups/{id}/objects`.

### Backup storage footprint (`backup_object_storage_usage`, `backup_storage_ranking`)

Sums Veeam's own per-file accounting from `GET /api/v1/backups/{id}/backupFiles`:
`backupSize` (on disk after compression and deduplication) and `dataSize`
(before). Other reads: `GET /api/v1/serverInfo` (build → REST revision),
`GET /api/v1/backupObjects?nameFilter=`, `GET /api/v1/restorePoints?backupObjectIdFilter=`,
`GET /api/v1/backups/{id}`, `GET /api/v1/jobs/{id}` (retention), `GET /api/v1/backupObjects/{id}`
(ranking: owners a backup does not list). Every collection
is paged to completion — the server caps a page at 200 by default.

- **Needs VBR 12.3+.** `backupFiles` first appears in REST revision 1.2-rev0
  (VBR 12.3.0.310, per Veeam's published revision table). The size reads send
  the newest revision the server's build serves; the rest of the tool keeps its
  pinned 1.1-rev1. Older builds get a refusal that names the minimum build.
- **Works with a read-only Backup Viewer account.** `/api/v1/serverInfo` (the
  build) is Backup Administrator only from revision 1.1-rev2 on; without it the
  tools offer each revision newest-first on a one-item `GET /api/v1/backups` and
  use the first the server accepts (`apiRevision.basis: "probe"`; refused
  revisions are listed in `apiRevision.probeRefusals`).
- **Shared files are never charged to one machine.** Per-job backup chains keep
  several VMs in one file; revision 1.3-rev2 (VBR 13.1+) lists every owner, and
  such files land in `sharedStoredBytes`, outside `storedBytes`. Older revisions
  name one owner per file, so sharing is decided by the restore points the file
  itself lists (`restorePointIds`): any point that is not this machine's makes
  it shared, whatever owner it names. A file whose ownership the server states
  inconsistently (no owner and no point list, or a single other owner with only
  this machine's points) goes to `unattributedStoredBytes` — never charged, and
  visible if owner ids ever turn out not to match backup-object ids. The ranking
  reads no restore points and charges each file to its listed owner.
- **The ranking separates two kinds of uncharged file.** A file naming no owner
  at all is an ordinary per-job chain file and lands in `ownerlessStoredBytes`.
  A file naming an owner id that its own backup's object listing does not
  contain lands in `unmatchedOwnerStoredBytes` and raises a caveat — that is the
  signal that backup-file owner ids and backup-object ids are different
  namespaces on this build, which is the one assumption the Veeam spec never
  pins down. `unresolvedStoredBytes` remains the sum of both. Judge a ranking's
  fitness for chargeback on `unmatchedOwnerFiles`, never on the sum: a healthy
  estate can carry a large ownerless total.
- **A partial ranking says so.** `backupsScanned`/`backupsTotal`/
  `backupsTruncated` are in the payload and the CLI prints an explicit PARTIAL
  line, because the default `max_backups` (100) is below some estates' backup
  count and widening a scan can put a previously unseen object at rank 1.
- **Scope the scan instead of waiting for the whole estate.** A complete
  ranking of a 123-backup VBR 13.1 estate took 21 minutes with 4 s of local
  CPU — the time is the server. `backups` (ids or names; a backup is named
  after its job) and `repository` (id or name) select what is read; the
  filter is applied locally because `/backups` offers no repository filter;
  names come from both plain and scale-out repositories.
  A scope that matches nothing is an error, not an empty ranking. The payload
  carries `scoped`, `scope` and `backupsInScope`; a scoped ranking adds a
  caveat and the CLI prints SCOPED, because it ranks the selection, not the
  environment. `backupsTruncated` is measured against the scope.
- **Backups can be read in parallel** (`concurrency`, 1–8, **default 1**).
  Opt-in because it is unmeasured on a real VBR: the server is already the
  bottleneck, and parallel reads can push a slow `backupFiles` read past the
  timeout — lower it if backups time out. Results are folded in scan order, so
  the payload is identical at any concurrency; a hard error in one read returns
  at once instead of waiting out the others. Token renewal is serialised, so
  parallel reads that all meet an expired token log in once. The CLI reports
  progress on stderr, so `--json` stays parseable.
- **An owner missing from its backup's listing is looked up** once per id via
  `GET /api/v1/backupObjects/{id}` (at most 200 ids; the rest are counted in
  `ownerLookupsSkipped`; the budget goes to the ids carrying the most bytes, and
  skipped ids get their own caveat rather than the namespace one, since they
  were never checked). Found → the id is a backup-object id (typically a
  machine moved to another job or removed from this one), its bytes are
  charged to that machine and also counted in `recoveredOwnerStoredBytes`.
  404 or a failed lookup → the bytes stay in `unmatchedOwnerStoredBytes` and
  the namespace caveat stands. `unmatchedOwners` lists every id with its
  `resolution` (`otherBackup`, `sameBackup`, `resolved`, `notFound`,
  `lookupFailed`, `skipped`), largest first, at most 50 entries
  (`unmatchedOwnersTotal`, `unmatchedOwnersTruncated`). A backup the server
  lists without an id is reported in `unreadableBackups`, not silently skipped.
- **One unreadable backup does not blank the result**: it is listed in
  `unreadableBackups` (with the error) and left out of every total. An entry
  with `timedOut: true` adds a caveat naming the fix — raise the target's
  `timeout` in config.yaml (the same estate needed 300 s for `/backupFiles`
  where the default is 30 s) — since retrying at the same budget cannot help.
- **The restore-point filter is checked, not trusted.** A query for a random
  object id must come back empty (`restorePointFilter: "honoured"`); then points
  under a machine's old name are kept (`restorePointNamesSeen`). If the server
  ignores the filter — or the check itself fails — points are matched by name,
  the others are counted in `restorePointsSetAside`, and a caveat says so; if
  two same-named machines then get the same points, totals are withheld and each
  machine is marked `attributable: false`.
- **Full vs incremental** comes from each restore point's `type` and the
  `backupFileId` it lives in; the `.vbk`/`.vib`/`.vrb` extension is a fallback,
  and `kindBasis` counts which rule classified each file.
- **Missing is not zero**: files without a size are counted in `unsizedFiles`
  and left out of the sums. `approxSourceBytes` is null before revision 1.3-rev2.
- **Block cloning**: on ReFS / XFS fast-clone repositories synthetic fulls share
  blocks, so summed file sizes can exceed physical consumption — an upper bound.
- **Same name, different machines** (two vCenters) are kept apart by identity
  (`path`, then `objectId` / BIOS UUID) and a caveat is added; the ranking merges
  one machine across backups by the same identity. Where the revision exposes no
  inventory id (Hyper-V and agents before 1.3-rev2) identity falls back to name,
  with a caveat.
- **Paging checks the server**: `skip` advances by what was actually returned,
  items are de-duplicated by id, and a server that stops short of its own total
  or repeats a page is refused rather than billed partially or twice.
- `changeRate` is mean incremental `dataSize` ÷ latest full `dataSize`, per
  increment (not per day).
- No pricing: storage cost models are organisation-specific.

## Infrastructure (2 — read)

| Tool | R/W | Risk | Typical response tokens |
|------|:---:|:----:|:----------------------:|
| `managed_server_list` | R | low | 150–600 |
| `proxy_list` | R | low | 150–600 |

REST endpoints: `GET /api/v1/backupInfrastructure/managedServers`,
`GET /api/v1/backupInfrastructure/proxies`. Read-only inventory of where jobs
run and what moves the data.

## Sessions (4 — 3 read, 1 write)

| Tool | R/W | Risk | Undo | Typical response tokens |
|------|:---:|:----:|------|:----------------------:|
| `session_list` | R | low | — | 150–800 |
| `session_get` | R | low | — | ~120 |
| `session_log` | R | low | — | 150–800 |
| `session_stop` | W | medium | **none** | ~40 |

REST endpoints: `GET /api/v1/sessions`, `GET /api/v1/sessions/{id}`,
`GET /api/v1/sessions/{id}/logs`, `POST /api/v1/sessions/{id}/stop`. Sessions
are how Veeam exposes async job/restore progress — poll these instead of
re-issuing the originating operation; read `session_log` to see *why* one failed —
each record carries `title`, `description` (the error detail), `status`,
`startTime` and `updateTime`.
`session_list` returns the newest `limit` sessions (default 100, max 1000) as
`{"sessions", "returned", "limit", "truncated", "order"}`, sorted by the server
(`orderColumn=CreationTime&orderAsc=false`), so "recent" is explicit;
`since_hours` narrows it to sessions created in the last N hours.
`overview` does **not** derive "running" from that window: it queries each
unfinished state (`stateFilter`: Starting, Working, Stopping, Pausing, Resuming,
Postprocessing, WaitingTape, WaitingRepository, WaitingSlot), so a job started
days ago is still reported; a refused state lands in `stateQueryErrors`.

### List reads and paging

The VBR REST API pages its collections; Veeam's spec gives `limit` a default of
200 from revision 1.3-rev0 (the pinned 1.1-rev1 documents no default). Inventory reads (`backup_list`,
`backup_object_list`, `job_list`, `repository_list`, `repository_state`,
`managed_server_list`, `proxy_list`) page to the end; `overview` and
`repository_capacity_rca` therefore see every repository. The pager advances by
what the server actually returned, de-duplicates by id, and raises instead of
returning a partial list if the server stops short or repeats a page.
`backup_object_list` sends no paging parameters on its first request (the pinned
revision 1.1-rev1 declares none for that endpoint) and pages only if the server's
pagination block shows more.

## Undo (2 — 1 read, 1 write)

| Tool | R/W | Risk | Undo | Typical response tokens |
|------|:---:|:----:|------|:----------------------:|
| `undo_list` | R | low | — | ~100–400 |
| `undo_apply` | W | medium | **none — single-use** | ~60 |

Generic governance tools provided by the bundled harness, not the Veeam REST
API. `undo_list` lists the recorded reversible writes whose undo tokens have not
yet been applied. `undo_apply` executes a recorded inverse for one token — it is
itself governed (audited and budget-checked), single-use (a token
cannot be replayed), and supports `dry_run` to preview the inverse first.

## Harness behavior

- **Encrypted credentials**: passwords are stored in `~/.veeam-aiops/secrets.enc`
  (Fernet + scrypt), unlocked by `VEEAM_AIOPS_MASTER_PASSWORD` or a prompt —
  never plaintext on disk.
- **Audit**: all 27 tools log to `~/.veeam-aiops/audit.db`.
- **Undo store**: the five reversible job writes record an inverse descriptor
  (`_undo_id` on the result); `session_stop` and the high-risk restore record none.
- **Budget/runaway guard**: caps cumulative calls + wall-time and trips tight
  session-poll loops.
- **Risk tier**: a descriptive label on each audit row derived from `risk_level`;
  it gates nothing. `VEEAM_AUDIT_APPROVED_BY` / `VEEAM_AUDIT_RATIONALE` are
  optional annotations recorded on the audit row, never required.
- **Sanitize**: all API-returned text is truncated + control-char stripped.
