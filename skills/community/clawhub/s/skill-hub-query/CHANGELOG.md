# Changelog

All notable changes to this skill are documented here.

### v1.4.0 (2026-09-16)

Three portability fixes + team management, ported from the internal fork
(v2.3.0 – v2.3.2). All were field-tested failures, not theoretical ones.

- **Added: `team.sh` — team member management.** search / my / info / list
  (full pagination) / member / add / remove. Optional Hub capability; the
  contract (including the fake-200 envelope and the `current=` pagination
  quirk) is documented in `references/api.md` §5, with a
  `SKILL_HUB_DISABLE_TEAM=1` kill switch for Hubs without it. Field-tested
  pitfalls are baked in as guardrails:
  - `add` returns 200 success for **non-existent emails too**, writing a
    dangling record (`handle == email`, no avatar) — every add is re-verified
    against the member list, and dangling records are flagged with a cleanup
    hint.
  - `add` is idempotent-success for existing members — inputs are
    de-duplicated first and the existing role reported, never silently changed.
  - `remove` silently 200s unknown emails — re-verified after the call.
  - Writes show the target team + roster and wait for confirmation; `--yes`
    must be user-authorized.
- **Fixed: BSD/GNU `mktemp` incompatibility (P0 on macOS).** The old
  `mktemp ... || mktemp -t name` fallback chains break on both families:
  GNU rejects `-t` without X's ("too few X's in template"), and `--suffix`
  (never used here, but the reason the internal fork had this bug) is
  GNU-only. All temp file/dir creation now goes through one `shq_mktemp`
  helper in `_lib.sh` that uses the only universally supported form: an
  explicit template ending in `XXXXXX`, with a prefix whitelist guarding
  against `/` or leading `-` injection. Direct `mktemp` calls are banned
  from all scripts.
- **Fixed: C-locale crashes in `_zip_safe.py` (doctor self-check false
  alarm on macOS).** Environments without `LANG` (launchd, cron, bare ssh)
  get **ascii** for both stdio *and* `sys.getfilesystemencoding()` on Python
  3.7–3.10, because macOS offers no `C.UTF-8` for PEP 538 coercion to find.
  Two distinct crash points: printing non-ASCII entry names, and
  `Path.resolve()` on paths containing them (the filesystem encoding is
  independent of stdio — reconfiguring streams alone is *not* enough; that
  was the first, insufficient attempt). Fix: when the filesystem encoding is
  not UTF-8, set `PYTHONUTF8=1` and `exec` ourselves with the same argv,
  letting interpreter-level UTF-8 mode take over every encoding uniformly;
  `doctor.sh`'s test-ZIP construction also gets a `PYTHONUTF8=1` prefix.
- **Fixed: mid-extract write failures left half-installed directories.**
  `_zip_safe.py` now tracks written files and cleans them up on
  `OSError` (disk full, permission) before returning 1, so a partial
  extraction is never mistaken for a complete version.

### v1.3.0 (2026-08-23)

Adds a stale-cache warning to `query.sh`. Same theme as v1.2.0: a failure that
reports success and only bites later.

- **Added: `query.sh` warns when the local cache is old.** List queries read the
  local cache by design — that is what makes them fast. The problem is that a
  stale `latestVersion` is **indistinguishable from a fresh one**: same shape,
  same field, no staleness marker anywhere in the output. Observed failure: a
  cache untouched for 67 days reported an old release as "latest", which nearly
  caused a publish against the wrong version baseline. A single `sync.sh` fixed
  the data instantly — the data path was never broken, the *silence* was.
  - Thresholds: **>7 days** prints a notice, **>30 days** prints a loud warning
    that also points at `query.sh versions <slug>` (live API, never cached).
  - **Warn only, never block.** Offline operation stays intentional, so a stale
    cache is still usable — you just get told.
  - All warning output goes to **stderr**, so `query.sh ... | jq` pipelines are
    unaffected.
  - Applies to the cache-backed providers only. `skillhub_cn` returns before the
    cache is ever consulted (it queries live), so the warning is correctly absent
    there.

- **Note for anyone extending this: do not mix the two timestamps in
  `skill-cache-meta.json`.** The first implementation computed cache age from
  `max(lastFullSync, lastIncrementalSync)`, which is wrong and **silently
  defeats the whole feature**:
  - `lastFullSync` is a **local wall-clock** stamp — "a sync actually ran".
  - `lastIncrementalSync` is the **server-side max `updatedAt`** — the
    incremental cursor, i.e. "when the newest skill on the hub last changed".
    It is deliberately *not* wall-clock (see `sync.sh`), because using local
    time there would drop records on the next incremental sync under clock skew.

  Taking `max()` of the two makes the computed age collapse to ~0 whenever the
  hub has recent activity — so "local cache 67 days stale + hub updated
  yesterday" produced **no warning at all**, exactly the case the warning exists
  for. Age is now derived from `lastFullSync` only, falling back to the cache
  file's `mtime` when it is absent or `0` (i.e. only incremental syncs have run);
  `mtime` is also a local clock, so it is semantically safe.

  Worth stating plainly: the first round of tests passed while this bug was live,
  because every test case set both fields to the same value — the inputs could
  not express the bug. Verified now with the two fields deliberately diverged.

### v1.2.0 (2026-08-22)

Install-reliability release. All three issues below were **silent failures** —
the install reported success and the damage only surfaced later, usually pointing
the blame at the wrong component.

- **Fixed: non-ASCII filenames were mangled on extraction.** Info-ZIP `unzip`
  6.00 ignores the ZIP spec's UTF-8 filename flag (general purpose bit 11) and
  decodes names with the local codepage, so an entry such as
  `references/<non-ascii>.json` landed on disk as mojibake. Any script in the
  installed skill that opened the file by its real name then died with
  `FileNotFoundError` — looking like a bug in the *installed* skill rather than
  in the installer. `unzip -O UTF-8` only exists in the Windows build, so there
  is no flag-level workaround: listing and extraction now go through the new
  `scripts/_zip_safe.py` (Python `zipfile`), which keeps the same
  absolute-path / traversal checks plus a per-entry `resolve()` check before
  writing.
  - Handles **both** archive flavours: names flagged UTF-8, and names written as
    raw UTF-8 bytes *without* the flag (which a naive `zipfile` reader decodes as
    CP437 and mangles in the opposite direction). Unflagged entries are
    round-tripped and retried as UTF-8.
  - Entries are written individually with the corrected name (not via
    `extractall`, which would reuse the mangled one), preserving the executable
    bit recorded in the archive.
- **Fixed: version resolution trusted a stale cache (risk of data loss).** The
  old order was "cache first, API as fallback". The cached
  `.latestVersion.version` is a `sync.sh` snapshot that is not invalidated when
  the Hub publishes afterwards, and was observed reading `1.3.0` while the real
  latest was `2.2.2` — so omitting a version silently installed an **older**
  release *and* replaced the whole directory of the newer copy the user already
  had. Order is now "version-history API first, cache only as fallback", and a
  fallback prints an explicit warning plus recovery instructions.
- **Added: version-consistency check before the directory is replaced.** A Hub's
  download endpoint was observed serving `v1.3.0` when `v2.2.2` was requested,
  while the script still printed success and recorded the *requested* version.
  The package's own declared version is now compared **before** anything is
  replaced (i.e. while the existing install is still intact); a mismatch warns
  and the ledger records the actual version. Recognises both the frontmatter
  `version:` and the open-source body `- **Version**:` conventions.
- **Fixed: temp-file leak window.** The `trap` was registered several lines after
  `mktemp`, so a download or `stat` failure in between left the ZIP behind. The
  trap is now registered first (with `${var:-}` guards for `set -u`).
- **Improved: API failures are no longer swallowed.** The version-history call's
  stderr used to be discarded, leaving users with "falling back to cache" and no
  idea whether the cause was an expired token or a dead network. The real reason
  is now captured and shown in both the fallback warning and the final error.
- **Improved: `doctor.sh` now actually tests ZIP filename handling.** Checking
  that `python3` exists proves nothing; doctor now builds an archive containing a
  non-ASCII filename and verifies `_zip_safe.py list` returns it byte-for-byte,
  and reports a blocking issue when it does not. `unzip` is no longer a listed
  dependency; `python3` is. Temp dirs created by diagnostics are cleaned up on
  every exit path.
- **Docs**: new "Requirements" table (explaining why `python3` replaces `unzip`),
  five new rows in the error reference, and two new known limitations covering the
  stale-cache field and the download-endpoint version mismatch.

### v1.1.5 (2026-07-28)
- Maintenance release (version bump only). Reviewed against clawhub SkillSpector findings; the flagged `xargs -r rm` is confirmed a false positive — it only prunes this skill's own edit-backup snapshots under a controlled `EDIT_BACKUP_DIR` (retention rotation), so no code change was needed.

### v1.1.4 (2026-07-17)
- Docs: move changelog out of SKILL.md into this standalone CHANGELOG.md (open-source convention)
- **v1.0.1** (2026-06-22): UGLIC patch — all 3 ERR + 4 WARN + 2 INFO fixed.
  - **L1 (ERR)** Fix `require_hub_url` exit-in-cmdsub trap: `endpoint="$(require_hub_url)"` silently dropped the exit because `exit` only kills the subshell. Refactored to `require_hub_url || exit $?; endpoint="$(load_endpoint)"` (api_get / api_download / edit.sh). Adds an explicit doc-comment so callers don't regress.
  - **L2 (ERR)** All curl calls now set `--max-time`: 30s for JSON API (api_get / _edit_lib `PUT`/`GET`) and 120s for ZIP downloads (overridable via `SKILL_HUB_DOWNLOAD_TIMEOUT`). Previously a hung Hub would hang the entire skill indefinitely.
  - **L3 (WARN)** `sync.sh` now validates the first-page response is non-empty JSON before computing `total / pages`, instead of silently reporting "Hub has 0 skill(s)" on failure.
  - **U1 (ERR)** Auto-fixed by L1: misleading legacy-fallback notice no longer appears before the real "no Hub URL" error in sync.sh.
  - **U2 (WARN)** `edit.sh` now calls `require_hub_url` before printing any step output (previously: empty `[edit] Hub URL :` and `[1/5] fetching...` were printed before the actual error).
  - **U3 (INFO)** `load_auth_scheme` now auto-appends a trailing space if non-empty and missing one (so `SKILL_HUB_AUTH_SCHEME="Bearer"` works, not just `"Bearer "`); explicit empty (X-API-Key style) still keeps no space.
  - **I1 (WARN)** Documented previously-undocumented env vars: `SKILL_HUB_BACKUP_RETENTION` (edit.sh backups) and the new `SKILL_HUB_DOWNLOAD_TIMEOUT`.
  - **C1 (WARN)** `sync.sh` and `doctor.sh` now register `trap` EXIT handlers that prune their `mktemp` temp files on any exit path (success / error / Ctrl-C). install.sh already had one.
- **v1.0.0** (2026-06-22): Initial open-source release of `skill-hub-query`.
  Generalized fork of an internal Hub query tool:
  - `SKILL_HUB_URL` / `SKILL_HUB_AUTH_HEADER` / `SKILL_HUB_API_PREFIX` / `SKILL_HUB_LEGACY_API_PREFIX` env-driven configuration (no baked-in default; see Hub compatibility note)
  - XDG-compliant cache and credentials directories
  - Owner pre-check via `git config user.email` (no internal-network-specific paths)
  - `edit.sh` made truly optional via `SKILL_HUB_DISABLE_EDIT=1` for Hubs without `/edit` endpoint
  - Full five-stage safety flow for metadata edits (GET -> diff -> backup -> PUT -> dual-channel verify -> rollback)
  - English-first, no organization-specific identifiers
