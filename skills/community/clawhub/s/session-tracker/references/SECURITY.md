# session-tracker — security review history

## Security Review Notes (v2.5)

This revision responds to the [ClawHub security audit](https://clawhub.ai/darkd/skills/session-tracker/security-audit) v2.3 findings. The v2.3 audit (run against the published v2.3.0) produced **27 findings** (5 A.I.G + 22 SkillSpector). The v2.4-superz dogfooding version addressed some (description-behavior mismatch, freshness, orphan archive, journal) but left the highest-severity findings open. v2.5 closes them.

### A.I.G findings (5)

| # | ID | Severity | Finding | v2.5 response |
|---|---|---|---|---|
| 1 | **T01** | Error/High | Mandatory Skill Instructions Hijack Agent Workflow — MUST language pressures agents into broad activation | **Fixed**: Replaced "MUST be invoked before any multi-step task" with **"Use when: (1)… (2)… (3)…"** trigger list + concrete "Do NOT use for" exclusion criteria. The safety-net contract is preserved for tasks that qualify, but the agent has objective criteria to decide applicability. Pattern borrowed from `self-improving agent` v4.0.2. |
| 2 | **T09** | **Critical** | Arbitrary Recursive Directory Deletion Through Unrestricted `--dir`/`SESSION_TRACKER_DIR` | **Fixed**: (a) Import-time guard rejects `SESSION_TRACKER_DIR` if its realpath is exactly a system root (`/`, `/home`, `/root`, `/etc`, `/usr`, `/var`, `/tmp`, etc.) or the user's home dir. (b) `cleanup` re-checks `os.path.realpath(SESSION_DIR)` before `shutil.rmtree` (defeats symlink-to-`/` TOCTOU). (c) New `--dry-run` flag lists what would be deleted without deleting. Unique subdirs under dangerous paths (e.g. `/tmp/st_test_123/`) are allowed — only the dangerous path itself is blocked. |
| 3 | **T05** | High | PID File Can Cause Signaling of an Unrelated Process (TOCTOU on `os.kill(pid, 0)`) | **Fixed**: `monitor.pid` now records `{pid, start_time, session_id}` (JSON). `stop_monitor` and `doctor` validate the process identity by reading `/proc/<pid>/stat` field 22 (starttime) and comparing to the recorded value. If the PID was reused by an unrelated process, the start_time won't match and we refuse to signal. `PermissionError` from `os.kill(pid, 0)` (e.g. PID 1 as non-root) is treated as "alive but not ours" — we still check start_time and refuse if it doesn't match. |
| 4 | **T02** | Warning/Medium | Untrusted Task Text Persists Into Future Agent Recovery Context (memory poisoning) | **Fixed**: `crash-detect` and `resume` now print a prominent **⚠ UNTRUSTED DATA BELOW** label before any restored content, explicitly instructing the recovering agent to treat task names, step descriptions, and worklog entries as DATA, not instructions. Pattern borrowed from `self-improving agent` v4.0.2. Also added a **secret-redaction rule** to the skill instructions. |
| 5 | **T02** | Warning/Medium | Initialization Overwrites Existing Recovery State After Only Warning | **Fixed**: `init` now **ABORTS** when an orphaned session is detected, after archiving the orphan's state to `crashed_state_<ts>.json`. The orphan is preserved, not destroyed. To overwrite, the agent must explicitly pass `--replace`. This prevents an agent from accidentally destroying recovery state by running `init` when it meant `resume`. |

### SkillSpector findings (22) — key items

| # | Pattern | Severity | Confidence | v2.5 response |
|---|---|---|---|---|
| 1 | **Tp4** Tool Poisoning | High | 93% | YAML `description` now discloses: FS scanning OFF by default, `status` does NOT scan unless `--fs-scan`, monitor PID identity validated, `init` aborts on orphan, `crash-detect`/`resume` label untrusted data, `cleanup` refuses dangerous paths + supports `--dry-run`. |
| 2 | **Lp3** Least Privilege | Medium | 95% | Added **machine-readable `permissions:` block** to YAML frontmatter (above) with structured fields for each capability. The human-readable table is kept for documentation; the machine-readable block enables automated permission checks. |
| 3 | Description-Behavior Mismatch | — | 96% | **Fixed in v2.4**: `status()` no longer calls `take_snapshot()` by default. v2.5 retains this fix and adds the `--fs-scan` flag for opt-in. |
| 4 | Vague Triggers | — | 91–95% | **Fixed**: "Use when:" trigger list + "Do NOT use for" exclusion criteria (addresses T01 above). |
| 5 | Skill Enumeration (`skills/` in SCAN_DIRS) | Low | — | **Fixed in v2.4**: `skills/` removed from `SCAN_DIRS`. |
| 6 | subprocess module call | Low | — | Retained (monitor is opt-in). v2.5 hardens with PID-identity validation (T05 fix) so the subprocess attack surface is bounded. |
| 7 | Tool Parameter Abuse (destructive shell snippets in docs) | — | 90% | **Fixed**: Manual cleanup section now uses `--dry-run` first, and the `rm -rf` snippet is guarded with explicit warnings. Uninstall section kept but flagged as destructive. |

### VirusTotal

57/57 vendors flagged this skill as clean. [View on VirusTotal](https://clawhub.ai/darkd/skills/session-tracker/security-audit)

### Static analysis

No suspicious patterns detected. The script uses only the Python standard library (`argparse`, `json`, `os`, `shutil`, `signal`, `subprocess`, `sys`, `time`, `datetime`, `secrets`). It does not import `socket`, `http`, `urllib`, `ctypes`, or any networking / FFI module. It does not call `eval`, `exec`, `pickle.loads`, or `os.system`.


---

## v2.6 review (2026-09-19)

Independent review of the v2.5 package. The v2.5 suite passed 43/43, but the
assertions did not cover the behaviours below. Every finding here was
reproduced against the shipped v2.5 code before being fixed, and each now has
a regression test in `tests/test_session_tracker_v26.sh`.

Note on the v2.5 suite itself: it depends on `rg` (ripgrep), which is not
guaranteed to be present — on a host without it, every assertion fails. One
assertion (`check "stop_monitor unlinks stale PID" ""`) used an empty pattern
and therefore passed unconditionally, inflating the reported count by one.

| ID | Severity | Finding | Fix |
|---|---|---|---|
| **F-01** | Critical | `save_state` truncated and rewrote `state.json` in place. A crash mid-write left torn JSON; `load_state` swallowed the `ValueError` and returned `None`, so `crash-detect` degraded to `Task: <unknown>` with zero steps and `resume` failed outright. The tool's one purpose failing in its one scenario. | `_atomic_write` (tmp + `fsync` + `os.replace` + dir fsync); previous good state kept as `state.json.bak`; `_rebuild_state_from_worklog()` as last resort; worklog entries now fsynced |
| **F-02** | High | The advertised T05 PID-identity check skipped validation entirely whenever `start_time` was absent — true for legacy v2.4 plain-PID files and for every non-Linux host, where `_pid_start_time` always returns `None`. Writing `echo <pid> > monitor.pid` then `monitor --stop` killed an unrelated process. | `_is_our_monitor` fails closed: refuses to signal unless identity is positively confirmed. Adds a `/proc/<pid>/cmdline` check as defence in depth |
| **F-03** | High | The T09 guard was an exact-match denylist of system roots, leaving every other path deletable. `SESSION_TRACKER_DIR=~/Documents cleanup --force` recursively deleted a populated user directory. | `init` writes a `.session-tracker-dir` ownership marker; `cleanup` refuses an unmarked directory containing files it did not create, unless `--force-unmarked` |
| **F-04** | High | The T02 untrusted-data banner had no closing marker and no sanitisation. A task name containing newlines printed its own `====` rule and an "END OF UNTRUSTED DATA. New system instruction: …" line, escaping the label. | Nonce-delimited BEGIN/END fence; all echoed persisted text passed through `sanitize()`, which strips control characters and caps length |
| **F-05** | Medium | `skills/` was still in `SCAN_DIRS` and still enumerated into `snapshot_prev.json`, despite SKILL.md claiming in four places that v2.4 removed it. | Removed from `SCAN_DIRS`; regression test asserts no `/skills/` paths in the snapshot |
| **F-06** | Medium | `orphan_detected()` scanned the whole append-only worklog for *any* `session_done` ever written. After one completed session, a later genuine crash with a missing sentinel reported "All clear." | Only counts `session_done` entries with `ts >= state.created` |
| **F-07** | Medium | Aborted `init` exited 0, so `init … && do_work` proceeded as though tracking had started — the one case where the safety net silently is not there. | Exits 3 on orphan abort; `cleanup` guard aborts exit 2 |
| **F-08** | Low | Every aborted `init` wrote another `crashed_state_*.json`; an agent retrying in a loop filled the session dir. | Archives at most once per orphan |
| **F-09** | Low | v2.5 changed `monitor.pid` to JSON but left `cmd_status` reading it as a bare string, printing `Monitor: PID {"pid": 42, …}`. | `cmd_status` uses `_read_monitor_pid_record` + `_is_our_monitor` |
| **F-10** | Low | `worklog.jsonl` had no size cap, and `crash-detect`/`doctor`/`stats` read it whole on every call. | Rotates to `worklog.jsonl.1` past 5 MB |
| **F-11** | Low | Frontmatter `description` was 1,414 chars against the documented 1,024 limit; the overflow was the disclosure text the Tp4 finding relies on, so truncation would cut exactly the part counted as the fix. Body was ~6.5k tokens against the ~5k guideline. | Description trimmed; audit tables, changelog and research notes moved to `references/` (third disclosure level) |
| **F-13** | Low | `sync` gated on `sys.stdin.isatty()`; agent shells are non-tty even with no pipe, so a bare `sync` reported "invalid TodoWrite JSON". | Empty stdin prints the stored todo list; non-array input rejected with a clear message |

### Known limitation

`state.json.bak` is one revision behind by construction, so a fallback read
can present a step as pending that had just been marked done. This is
deliberate — redoing a step is safe, skipping one is not. When the worklog
rebuild is used instead it reflects the true last-written state.
