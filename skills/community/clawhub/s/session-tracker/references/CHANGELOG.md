# session-tracker — changelog

## Changelog

### v2.4-superz → v2.5 (security hardening)

**A.I.G findings (5):**
- **T09 (Critical)**: Import-time guard rejects dangerous `SESSION_TRACKER_DIR`; `cleanup` re-checks realpath; new `--dry-run` flag.
- **T05 (High)**: `monitor.pid` records `{pid, start_time, session_id}`; `stop_monitor`/`doctor` validate process identity via `/proc/<pid>/stat` before signaling.
- **T02 (Medium ×2)**: `crash-detect`/`resume` label restored content as UNTRUSTED DATA; `init` aborts on orphan, requires `--replace`; secret-redaction rule added to skill instructions.
- **T01 (Error/High)**: MUST language replaced with "Use when:" trigger list + "Do NOT use for" exclusion criteria.

**SkillSpector findings:**
- **Lp3 (95%)**: Machine-readable `permissions:` block added to YAML frontmatter.
- **Tp4 (93%)**: Description now discloses PID-identity validation, init-aborts-on-orphan, untrusted-data labeling, dangerous-path guard, dry-run.
- Description-behavior mismatch (96%): retained v2.4 fix (`status` no longer scans by default).

**Code changes:**
- `_pid_start_time()`, `_read_monitor_pid_record()`, `_is_our_monitor()` helpers (T05).
- `_DANGEROUS_PATHS` frozenset + import-time + cleanup-time guards (T09).
- `cmd_init`: `--replace` flag; aborts on orphan unless `--replace` (T02).
- `cmd_crash_detect` / `cmd_resume`: UNTRUSTED DATA labeling (T02).
- `cmd_cleanup`: `--dry-run` flag; realpath re-check (T09).
- `cmd_monitor`: writes JSON PID record with `start_time` + `session_id` (T05).
- `stop_monitor`: PID-identity validation before signaling (T05).
- `cmd_doctor`: uses `_is_our_monitor` for liveness check (T05).
- Version bumped to 2.5.0; test suite extended from 27 to 43 assertions.

### v2.3 → v2.4-superz (production dogfooding)

See PROVENANCE.md for the full dogfooding notes. Key additions: orphan archive, journal, doctor, stats, freshness fix, ad-hoc steps, string IDs in sync, portability (`SESSION_TRACKER_DIR`).

### v2.2 → v2.3 (first audit response)

Data minimization (no baseline FS snapshot on `init`), `--auto-cleanup`, `prune`, monitor hardening (log file, minimal env, 24h cap), cleanup confirmation, permissions declaration.

## Research basis

v2.5 incorporates patterns from analogous skills and the wider agent ecosystem:

- **session-fork v2.4.18** (ClawHub): `--dry-run` for destructive ops; boundary-statement pattern.
- **self-improving agent v4.0.2** (ClawHub): "Use when:" trigger list; explicit untrusted-data labeling in restored content; secret-redaction rule.
- **Skill Vetter v1.0.0** (ClawHub): negative-permission "What this skill does NOT do" section (kept from v2.3).
- **LangGraph** (LangChain): explicit run-status enum; `pending_writes` for mid-flight tracking (noted as future enhancement).
- **systemd / K8s**: PID file with `{pid, start_time}` record (T05 fix); watchdog/liveness-probe thresholds.
- **Codex `/rewind`**: named checkpoints with selective restore (noted as future enhancement).

The snapshot + append-journal + sentinel core is the database-industry standard crash-recovery pattern (PostgreSQL WAL, ZFS, SQLite "checkpoint"). session-tracker occupies the durable-execution-layer niche for ClawHub that Diagrid/Statefold/Temporal occupy for CrewAI/LangGraph.
