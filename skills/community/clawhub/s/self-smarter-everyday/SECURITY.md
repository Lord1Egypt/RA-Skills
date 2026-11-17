# Security Policy

This document defines the security policy for the **self-smarter-everyday** skill, including what the skill can and cannot access, how data is handled, credential isolation, audit trails, vulnerability reporting, and the threat model.

---

## 🔒 Scope

This security policy applies to:
- All scripts in `scripts/` (`nightly_routine.py`, `self_audit.py`, `memory_compact.py`, `prompt_evolve.py`, `setup.sh`)
- All templates in `templates/`
- The state directory (`~/self-smarter/state/`)
- The log directory (`~/self-smarter/logs/`)
- The cron job configuration

This policy does **not** cover:
- The host operating system security
- OpenClaw Gateway security (see OpenClaw documentation)
- Network-level security (firewalls, SSH hardening)
- Other skills or plugins installed in the workspace

---

## ✅ What This Skill CAN Access

### File System
- **Read/Write:** `~/self-smarter/` directory and all subdirectories (state, logs, memory, reflections, prompts).
- **Read:** `~/.openclaw/workspace/skills/self-smarter-everyday/` (its own skill directory).
- **Read:** System metrics via `/proc/` (memory usage, CPU load) for audit purposes.
- **Read/Write:** Crontab (to manage its own cron job entry).

### System Resources
- **CPU:** Brief bursts during nightly routine execution (~30 seconds total).
- **Memory:** <50 MB during normal operation (state files are small).
- **Disk:** <100 MB total for state, logs, and archives.
- **Network:** None. All scripts operate entirely offline. No external API calls, no network requests.

### Process Execution
- **Python3 interpreter:** For running scripts.
- **Crontab:** For scheduling the nightly routine.
- **Standard I/O:** For logging and status output.

### Data
- **Self-generated data:** Reflection entries, audit reports, memory entries, prompt variants, improvement plans.
- **System metrics:** CPU load, memory usage, disk usage (read-only, for audit purposes).
- **Log data:** Its own log files from previous runs.

---

## ❌ What This Skill CANNOT Access

### Credentials and Secrets
- **NO access to:** API keys, passwords, tokens, SSH keys, OAuth credentials, or any other secrets.
- **NO storage of:** Credentials in any form (plaintext, encrypted, hashed, base64).
- **NO transmission of:** Credentials to any destination (file, network, log output).
- The skill has no need for external service authentication. It operates entirely on local data.

### User Data
- **NO access to:** User messages, chat history, conversation transcripts, or personal data.
- **NO access to:** Email content, contacts, calendar entries, or other personal information.
- **NO access to:** Files outside the `~/self-smarter/` directory (except its own skill directory for reading templates).
- The skill does not process, store, or transmit any user-provided content.

### External Services
- **NO network access:** Scripts do not make HTTP requests, DNS lookups, or any network calls.
- **NO API integration:** No calls to OpenAI, Anthropic, Google, or any other external API.
- **NO package installation:** Scripts do not install system packages or Python dependencies.

### System Modification
- **NO modification of:** System configuration files (`/etc/`, system crontabs, service configs).
- **NO modification of:** Other skills, plugins, or workspace files.
- **NO execution of:** Arbitrary shell commands from state files or templates (no injection vectors).
- **NO privilege escalation:** Scripts run with user-level permissions only. No `sudo`, no `setuid`.

---

## 📦 Data Handling

### Data Classification

| Data Type | Classification | Storage | Retention |
|-----------|---------------|---------|-----------|
| Reflection entries | Internal operational | `~/self-smarter/state/reflections/` | Indefinite (managed by compaction) |
| Audit reports | Internal operational | `~/self-smarter/state/audit_latest.json` | Overwritten each run |
| Memory entries | Internal operational | `~/self-smarter/state/memory/` | Indefinite (managed by tier lifecycle) |
| Prompt variants | Internal operational | `~/self-smarter/state/prompts/` | Indefinite (capped at MAX_VARIANTS) |
| Log files | Internal operational | `~/self-smarter/logs/` | 30 days (manual cleanup) |
| Routine state | Internal operational | `~/self-smarter/state/routine_state.json` | Overwritten each run |

### Data Principles
1. **Local-only:** All data stays on the local filesystem. No data is transmitted externally.
2. **Self-generated:** The skill only processes data it generated itself. No user data, no external data.
3. **Non-sensitive:** No credentials, no personal information, no secrets of any kind.
4. **Bounded:** State directory has natural size limits (tier compaction, variant cap, log rotation).
5. **Transparent:** All data is stored in human-readable JSON format. No binary or encrypted files.

### Data Lifecycle
```
Creation → Active Use → Tier Decay → Archive → Manual Deletion
   │            │            │           │            │
   ▼            ▼            ▼           ▼            ▼
 Script      Reflection   Compaction   >30 days    Operator
 generates   and audit    moves        auto-moves  manually
 data        use it       tiers        to archive  cleans up
```

### Data Integrity
- Scripts validate JSON before processing (try/except around `json.load`).
- Malformed files are skipped, not crashed on.
- State writes use atomic patterns (write to temp file, then rename) where possible.
- Log files are append-only during a run, preventing partial writes.

---

## 🔑 Credential Isolation

### Design Principle
The skill is designed to require **zero credentials**. This is a deliberate security decision:

1. **No API keys needed** — All processing is local. No LLM API calls, no external services.
2. **No authentication needed** — No network endpoints to authenticate against.
3. **No secrets in config** — Configuration files contain only paths, thresholds, and schedules.
4. **No secrets in logs** — Log output contains only operational metrics, never credentials.

### Verification
To verify the skill doesn't access credentials:
```bash
# Search for credential-related patterns in scripts
grep -rn "password\|api_key\|token\|secret\|credential\|auth" scripts/

# Search for network-related patterns
grep -rn "http\|https\|urllib\|requests\|socket\|curl\|wget" scripts/

# Both should return zero matches
```

### If Credentials Are Needed in the Future
Should future versions require external access (e.g., for cloud-based metric storage):
1. Credentials must be stored in environment variables, never in files.
2. Credentials must never appear in log output (use masking).
3. Credentials must never be written to state files.
4. Network access must be documented in this security policy.
5. A separate security review must be conducted before enabling.

---

## 📋 Audit Trail

### What Is Logged
The nightly routine logs the following to `~/self-smarter/logs/`:
- Start and end timestamps of each run.
- Phase execution status (completed, failed, skipped, timeout).
- Error messages with stack traces.
- Metric values collected during audit.
- Memory compaction transitions (promotions, demotions, merges).
- Prompt evolution results (generation, fitness scores, mutations).

### What Is NOT Logged
- User messages or conversation content.
- Credential values (there are none, but this is a guarantee).
- File contents (only file paths and sizes are logged).
- System environment variables.

### Log Retention
- Log files are created per-run: `nightly_YYYYMMDD_HHMMSS.log`.
- No automatic rotation is implemented (rely on OS-level log rotation or manual cleanup).
- Recommended: delete logs older than 30 days via cron:
  ```bash
  find ~/self-smarter/logs/ -name "nightly_*.log" -mtime +30 -delete
  ```

### Audit Verification
To verify the audit trail is complete:
```bash
# Count log files vs expected runs
ls ~/self-smarter/logs/nightly_*.log | wc -l

# Check for errors in recent logs
grep -l "ERROR" ~/self-smarter/logs/nightly_*.log | tail -5

# Verify state file matches log history
python3 -c "import json; print(json.load(open('$HOME/self-smarter/state/routine_state.json'))['run_count'])"
```

---

## 🚨 Vulnerability Reporting

### Reporting Process
If you discover a security vulnerability in this skill:

1. **Do not open a public issue** — This could expose the vulnerability before it's fixed.
2. **Contact privately** — Report via encrypted channel or private message to the maintainer.
3. **Include details:**
   - Description of the vulnerability.
   - Steps to reproduce.
   - Potential impact assessment.
   - Suggested fix (if you have one).
4. **Allow time for fix** — Give the maintainer reasonable time (7-14 days) to address the issue before public disclosure.

### Response Commitments
- Acknowledge receipt within 48 hours.
- Provide initial assessment within 7 days.
- Release fix within 14 days of confirmed vulnerability.
- Publish security advisory after fix is deployed.

### Scope of Vulnerabilities
Valid security concerns include:
- Path traversal vulnerabilities (scripts accessing files outside intended directories).
- Injection vulnerabilities (state file content being executed as code).
- Information disclosure (logs containing sensitive data).
- Denial of service (resource exhaustion from malformed state files).
- Privilege escalation (scripts gaining more access than intended).

---

## 🛡️ Security Best Practices

### For Operators
1. **Run with minimal permissions** — The skill doesn't need root or sudo. Run as the regular user.
2. **Monitor disk usage** — Set up alerts if `~/self-smarter/` exceeds 200 MB.
3. **Review logs periodically** — Check for unexpected errors or patterns.
4. **Validate state files** — Periodically inspect JSON files for unexpected content.
5. **Keep scripts updated** — Use the latest version to benefit from security fixes.
6. **Backup state directory** — Include `~/self-smarter/` in regular backups.

### For Contributors
1. **Never add network calls** — The offline-first design is a security feature.
2. **Never add credential handling** — The zero-credential design is deliberate.
3. **Validate all inputs** — State files could be malformed. Handle errors gracefully.
4. **Avoid shell injection** — Never pass state file content to `os.system()` or `subprocess` with `shell=True`.
5. **Use allowlists** — When processing file paths, validate against expected patterns.
6. **Minimize file permissions** — State files should be `600` (owner read/write only).

### For the System
1. **No eval/exec** — Scripts never evaluate content from state files as code.
2. **Path validation** — All file paths are validated against the expected base directory.
3. **JSON-only state** — State files are strictly JSON. No YAML, no pickle, no exec-able formats.
4. **Bounded loops** — All iteration over state entries has maximum limits.
5. **Timeout enforcement** — Subprocess calls have timeout parameters to prevent hangs.

---

## 🎯 Threat Model

### Threats Considered

| Threat | Likelihood | Impact | Mitigation |
|--------|-----------|--------|------------|
| Malformed state file causes crash | Medium | Low | Try/except around all JSON parsing |
| Path traversal via state file content | Low | High | Path validation against base directory |
| Log injection via state file content | Low | Medium | Structured logging with format strings |
| Disk exhaustion from unbounded growth | Low | Medium | Tier compaction, variant cap, log rotation |
| Cron job hijacking | Very Low | High | Script path is hardcoded, not configurable via state |
| Symlink attack on state files | Very Low | High | Scripts don't follow symlinks outside base dir |
| Race condition (concurrent runs) | Low | Low | State file locking (future improvement) |
| Supply chain (Python stdlib) | Very Low | Critical | No external dependencies; stdlib is trusted |

### Threats NOT Considered (Out of Scope)
- Physical access to the server (handled by OS-level security).
- Root-level compromise of the host (if root is compromised, all bets are off).
- Network-based attacks (the skill has no network surface).
- Side-channel attacks (not relevant for a non-cryptographic system).

### Attack Surface
The attack surface is intentionally minimal:
- **Input vectors:** State files (JSON), log files (text), cron schedule.
- **No network surface:** No listening ports, no HTTP endpoints, no API calls.
- **No user input:** The skill doesn't process user-provided data directly.
- **No external dependencies:** Only Python standard library is used.

### Risk Assessment
**Overall risk level: LOW**

The skill operates in a highly constrained environment:
- Reads only its own state files.
- Writes only to its own directories.
- Makes no network calls.
- Requires no credentials.
- Processes no user data.
- Has no external dependencies.

The primary risk is data loss (state files corrupted or deleted), which is mitigated by the backup strategy and the non-critical nature of the data (the skill can be re-initialized from scratch).

---

## 📝 Security Changelog

| Date | Change | Severity |
|------|--------|----------|
| 2026-08-10 | Initial security policy created for v1.0.0 | — |

---

*This security policy is reviewed and updated with each major version release. For questions or concerns, follow the vulnerability reporting process above.*
