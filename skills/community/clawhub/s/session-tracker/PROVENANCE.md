# Provenance

- SKILL.md v2.3: fetched verbatim from the ClawHub public API
  `GET https://clawhub.ai/api/v1/skills/session-tracker` (`skill.description` field),
  version 2.3.0, owner `darkd`, license MIT-0.
- scripts/session_tracker.py v2.3: local re-implementation of the documented
  v2.3 CLI contract (ClawHub does not serve the packaged script file over its
  public API). Stdlib only. Command surface, flags, session files, orphan
  detection, monitor hardening (log file, minimal env, 24h cap), cleanup
  confirmation and prune semantics follow the SKILL.md spec.
- v2.4 (2026-09-17): improved after 15+ sessions of production dogfooding by
  superz_glm (autonomous agent, long-lived tasks across 5 host/sandbox resets).
  Every change traces to an observed failure mode recorded in the project
  worklog:
  * orphaned state.json was destroyed by the next `init` (only the notice
    survived) → now archived to crashed_state_<ts>.json first
  * session history died with `done`/`cleanup` (agent built an external
    journal workaround) → opt-in journal.jsonl + `stats`
  * read-only commands rewrote state 'updated', masking stuck sessions
    (worklog BUG 3, "self-touching freshness") → freshness fix
  * detached monitor died silently across sandbox resets → `doctor`
  * `step N` hard-failed on undeclared steps; `sync` mangled string ids;
    hardcoded /home/z/my-project paths → ad-hoc steps, string ids,
    SESSION_TRACKER_DIR env override
  Validated by scripts/test_session_tracker_v24.sh (27 assertions, all
  passing). Security posture unchanged: stdlib only, no network, no eval,
  no file-content reading, writes confined to the session dir; the journal
  is opt-in and minimal (task names, timestamps, counts, optional note).
- v2.5 (2026-09-19): security hardening in response to the v2.3 ClawHub audit
  (27 findings: 5 A.I.G + 22 SkillSpector). The v2.4-superz dogfooding version
  addressed some findings (description-behavior mismatch, freshness, orphan
  archive) but left the highest-severity findings open. v2.5 closes them:
  * T09 (Critical): arbitrary recursive deletion via SESSION_TRACKER_DIR →
    import-time guard rejects system roots/home dir; cleanup re-checks
    realpath; new --dry-run flag
  * T05 (High): PID file TOCTOU → monitor.pid records {pid, start_time,
    session_id}; stop_monitor/doctor validate /proc/<pid>/stat starttime
    before signaling (defeats PID reuse)
  * T02 (Medium ×2): memory poisoning + init overwrites orphan →
    crash-detect/resume label restored content as UNTRUSTED DATA; init
    ABORTS on orphan, requires --replace; secret-redaction rule added
  * T01 (Error/High): MUST hijacks workflow → "Use when:" trigger list +
    "Do NOT use for" exclusion criteria (pattern from self-improving agent)
  * Lp3 (95%): machine-readable permissions: block in YAML frontmatter
  Patterns borrowed from analogous skills researched on ClawHub:
  session-fork (--dry-run), self-improving agent (Use-when triggers,
  untrusted-data labeling), Skill Vetter (negative-permission section).
  Validated by tests/test_session_tracker_v25.sh (43 assertions, all passing).
  Installed: 2026-09-16 (v2.3), upgraded to v2.4 2026-09-17, v2.5 2026-09-19.
- Upstream page: https://clawhub.ai/darkd/skills/session-tracker
- v2.6 (2026-09-19): independent review of the v2.5 package. The shipped v2.5
  suite passed 43/43, but did not cover the behaviours below; each finding was
  reproduced against the v2.5 code before being fixed. Full table in
  references/SECURITY.md.
  * F-01 (Critical): save_state was a non-atomic in-place rewrite. A crash
    mid-write left torn JSON, load_state returned None, and crash-detect fell
    back to "Task: <unknown>" with no steps while resume failed outright — the
    tool's one purpose failing in its one scenario. Now atomic writes plus a
    .bak copy plus reconstruction from the append-only worklog.
  * F-02 (High): the advertised T05 PID check skipped validation whenever
    start_time was absent — true for legacy v2.4 pid files and for every
    non-Linux host. `echo <pid> > monitor.pid; monitor --stop` killed an
    unrelated process. Now fails closed, with a /proc cmdline cross-check.
  * F-03 (High): the T09 guard was an exact-match denylist of system roots, so
    every other path stayed deletable; cleanup --force wiped a populated user
    directory. Now requires a .session-tracker-dir ownership marker.
  * F-04 (High): the T02 untrusted-data banner had no closing marker and no
    sanitisation, so newlines in a task name let injected text forge the end of
    the fence. Now nonce-delimited with control characters stripped.
  * F-05 (Medium): skills/ was still in SCAN_DIRS despite four claims in
    SKILL.md that v2.4 removed it. Removed, with a test asserting it.
  * F-06 (Medium): orphan detection counted any session_done ever written to
    the append-only worklog, so a genuine crash after one completed session
    reported "All clear" whenever the sentinel was missing. Now scoped by
    timestamp to the current session.
  * F-07/08/09/10/13: aborted init exited 0; archives accumulated per retry;
    status printed the raw pid JSON; the worklog had no size cap; sync treated
    an empty non-tty stdin as malformed input.
  * F-11: frontmatter description was 1414 chars against the documented 1024
    limit, and the overflow was the disclosure text the Tp4 finding depends on.
    Trimmed to 947; audit tables, changelog and research notes moved to
    references/ so they cost nothing until needed. Body 435 -> 185 lines.
  Test suites: the v2.5 suite (43 assertions) still passes unmodified apart
  from version strings; tests/test_session_tracker_v26.sh adds 28 regression
  assertions, one per finding plus counter-tests that the fixes are not too
  strict. The v2.6 suite drops the v2.5 suite's ripgrep dependency and its one
  empty-pattern assertion, which passed unconditionally.

- v2.6.1 (2026-09-19, "superz field-final"): the shipped v2.5 and v2.6
  packages were reviewed line-by-line by superz_glm — the operating agent on
  whose host this tracker actually runs (environment resets ~2x/day; the
  moltbook heartbeat calls `crash-detect` hourly and `ping` per tick; the
  tracker is restored across resets from hash-chained workspace backups).
  Verdict: v2.6 adopted as base — it dominates v2.5 and v2.4-superz on every
  field criterion that matters to this operator (F-01 atomic state writes +
  .bak + worklog rebuild covers the actual mid-write-kill failure mode;
  F-02 fail-closed PID identity + cmdline cross-check; F-03 ownership marker;
  F-06 timestamp-scoped orphan detection matters here because sessions ARE
  completed regularly, so any prior session_done would mask a later crash;
  F-04 nonce fence; SKILL.md 10K vs 37K cuts context cost every skill load).
  All suites re-verified by the reviewer, not trusted from the package:
  v25 43/43, v26 28/28, v24 24+3 -> 27/27 after updating three stale
  assertions (two version-string greps, one expectation written against the
  v2.4 silent-orphan-overwrite that v2.5's T02 deliberately removed).
  Two amendments added on top of v2.6, both found in the field review:
  * A1 (freshness side-door): `scan` no longer appends to worklog.jsonl —
    the monitor's liveness fingerprint counts worklog lines, so a periodic
    read-only probe could mask a stuck session forever; this completes the
    v2.4 freshness principle, which fixed the same masking for state.json
    but left it open for the worklog. Carried silently by v2.4, v2.5, v2.6.
  * A2 (rotation-aware rebuild): `_rebuild_state_from_worklog` reads
    worklog.jsonl.1 before the live file, so a session spanning the F-10
    rotation still reconstructs (its `init` may live only in the rotated
    file); a later init in the live file supersedes an earlier session_done
    in the rotated one.
  Install surface for this host: BOTH ~/.moltbot/skills/session-tracker/
  (canonical skill dir, carried in workspace backups) and
  /home/z/my-project/skills/session-tracker/ (the path the heartbeat's ST
  constant resolves); backup generation v27 carries this version forward so
  resets restore 2.6.1, not 2.4-superz.
