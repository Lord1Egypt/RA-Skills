---
name: openclaw-health-monitor
version: 1.6.0
description: Cross-platform diagnostics for OpenClaw gateways. Checks gateway health, event loop degradation, WhatsApp connectivity, service state, stuck background subagents, prewarm blocking, and generates diagnostic bundles for bug reports. See SECURITY.md for privacy disclosures. Use when: (1) Gateway feels slow or unresponsive, (2) CLI health checks take unusually long, (3) WhatsApp is not receiving messages, (4) Agent responses are delayed, (5) After OpenClaw version upgrades, (6) Routine system health check.
license: MIT
compatibility: openclaw
metadata:
  openclaw:
    emoji: "🩺"
  tags: [diagnostics, monitoring, health, cross-platform, windows, linux, macos]
---

# OpenClaw Health Monitor — Cross-Platform Diagnostic Skill

Cross-platform diagnostics for OpenClaw gateways. Covers the most common performance problems discovered through real-world debugging on Windows 11 native, WSL2, Linux, and macOS environments.

See **[SECURITY.md](https://github.com/jordan-thirkle/openclaw-winhealth/blob/main/SECURITY.md)** for data collection and privacy disclosures. External alerts are off by default in v1.4.0+.

## Quick Health Check

Run a comprehensive health snapshot:

```bash
openclaw health --verbose --json
openclaw channels status --probe
openclaw status --all
```

Key metrics to watch:
- **Event loop delay**: p99 should be < 100ms. Values > 5000ms indicate degradation
- **Event loop utilization**: Should be < 0.1. Values near 1.0 indicate saturation
- **WhatsApp status**: Should say "linked, running, connected, healthy"
- **Channel auth age**: Should be recent (< 30 minutes)
- **Session store entries**: Growing without bound can cause startup slowness

### 1. Gateway Service Health

Check if the gateway process is running:

```bash
# Cross-platform (bash/zsh):
ps aux | grep openclaw | grep -v grep

# Windows PowerShell:
# Get-Process -Name "node" | Where-Object { $_.CommandLine -like "*openclaw*" }
```

Verify the gateway is listening on its health port:

```bash
# Cross-platform (bash/zsh):
curl -s --max-time 5 http://127.0.0.1:18789/health

# Windows PowerShell:
# Invoke-RestMethod -Uri "http://127.0.0.1:18789/health" -TimeoutSec 5
```

Platform-specific service management commands below.

## Platform-Specific Diagnostics

### Linux (systemd)

```bash
# Service status
systemctl --user status openclaw-gateway

# Journal logs
journalctl --user -u openclaw-gateway -n 50

# Process health
ps aux | grep openclaw | grep -v grep
```

### macOS (launchd)

```bash
# Service status
launchctl list | grep openclaw

# Disk usage
du -sh ~/.openclaw

# Process health
ps aux | grep openclaw | grep -v grep
```

### Windows (Scheduled Task)

```bash
Get-ScheduledTask -TaskName "OpenClaw Gateway" | Format-List State, LastRunTime, LastTaskResult
```

**Healthy**: State=Ready, LastTaskResult=0
**Degraded**: State=Running but gateway unresponsive → stuck restart, kill node processes and restart
**Failed**: LastTaskResult non-zero → check gateway log for errors

### 2. Event Loop Degradation

The most common performance regression appears in 2026.5.x:

```bash
# Cross-platform (bash/zsh):
openclaw health --json | grep -E "eventLoop|p99|delayMax"

# Windows PowerShell:
# openclaw health --json | Select-String "eventLoop|p99|delayMax"
```

```bash
# Cross-platform (bash/zsh):
grep -E "provider auth state pre-warmed|eventLoopMax" "$TMPDIR"/openclaw/*.log ~/.openclaw/logs/*.log 2>/dev/null

# Windows PowerShell:
# Select-String "provider auth state pre-warmed|eventLoopMax" "$env:TEMP\openclaw\openclaw-*.log"
```

Symptoms: CLI health taking 20+ seconds, "degraded" event loop, `startup model warmup timed out` in logs.

### 3. CLI Tool vs HTTP Gateway Performance Delta

A key diagnostic finding: the CLI health command can be 20-30x slower than the HTTP health endpoint on Windows:

```bash
# CLI health (slow on Windows)
openclaw health --timeout 20000
```

```bash
# Cross-platform (bash/zsh):
curl -s -H "Authorization: Bearer $OPENCLAW_GATEWAY_TOKEN" --max-time 10 "http://127.0.0.1:18789/health"

# Windows PowerShell:
# $token = $env:OPENCLAW_GATEWAY_TOKEN
# Invoke-RestMethod -Uri "http://127.0.0.1:18789/health" -Headers @{"Authorization"="Bearer $token"} -TimeoutSec 10
```

If CLI is slow but HTTP is fast (< 500ms): gateway is healthy, CLI tool has Windows WebSocket auth overhead.

### 4. Stuck Background Subagents

Background subagents can block gateway restart for 5+ minutes:

```bash
# Cross-platform (bash/zsh):
grep -E "restart.*deferred.*background task.*active" "$TMPDIR"/openclaw/*.log ~/.openclaw/logs/*.log 2>/dev/null

# Windows PowerShell:
# Select-String "restart.*deferred.*background task.*active" "$env:TEMP\openclaw\openclaw-*.log"
```

If found: kill node processes and restart gateway. The stuck subagents will not recover.

### 5. WhatsApp Reconnection Storm

```bash
# Cross-platform (bash/zsh):
grep -E "WebSocket.*closed.*408|Retry.*\/12|timed out waiting for.*WhatsApp" "$TMPDIR"/openclaw/*.log ~/.openclaw/logs/*.log 2>/dev/null

# Windows PowerShell:
# Select-String "WebSocket.*closed.*408|Retry.*\/12|timed out waiting for.*WhatsApp" "$env:TEMP\openclaw\openclaw-*.log"
```

### 6. Memory-LanceDB Integration

If memory-lancedb is installed but not configured:
- The memory slot defaults to memory-lancedb which needs embedding config
- Without embeddings, it disables itself with `disabled until configured`
- Fix: revert slot to `memory-core` or configure embeddings

```bash
# Cross-platform (bash/zsh):
openclaw plugins list | grep "memory"

# Windows PowerShell:
# openclaw plugins list | Select-String "memory"
```

### 7. Provider Auth Prewarm Blocking

2026.5.22 introduced provider auth prewarming that can block for 30-79s:

```bash
# Cross-platform (bash/zsh):
grep -E "provider auth state pre-warmed|startup model warmup timed out" "$TMPDIR"/openclaw/*.log ~/.openclaw/logs/*.log 2>/dev/null

# Windows PowerShell:
# Select-String "provider auth state pre-warmed|startup model warmup timed out" "$env:USERPROFILE\AppData\Local\Temp\openclaw\openclaw-*.log"
```

Fix: Set `OPENCLAW_SKIP_PROVIDER_AUTH_PREWARM=1` in gateway.cmd or environment variables.
Fix (future): Add `{ "gateway": { "providerAuthPrewarm": { "enabled": false } } }` to config (pending PR merge).

## Diagnostic Bundle Generation

**WARNING:** This tool collects data that may contain sensitive information. The `winhealth_diagnostics` tool gathers:
- Gateway health snapshots (event loop, memory, channel status)
- Diagnostic export archives (stability bundle, sanitized logs, config shape)
- Log tail extraction (when `include_logs` is enabled — defaults to disabled)

Diagnostic bundles may contain system metadata, log-derived details, file paths, identifiers, and configuration structure even after OpenClaw's built-in sanitation. **Review the contents before sharing.** Only share diagnostic bundles with trusted recipients for troubleshooting purposes. See [SECURITY.md](https://github.com/jordan-thirkle/openclaw-winhealth/blob/main/SECURITY.md#diagnostic-bundles).

For bug reports or sharing diagnostics:

```bash
openclaw gateway diagnostics export
```

This creates a sanitized zip at `~/.openclaw/logs/support/` with:
- Stability bundle (event loop, memory, session state)
- Sanitized log metadata
- Gateway status/health snapshots
- Config shape (secrets redacted)

## Standard Fix Playbook

### Gateway Unresponsive (Port 18789 bound but health times out)

1. Check for stuck background tasks (see #4)
2. Check for event loop degradation (see #2)
3. If prewarm issue: add `OPENCLAW_SKIP_PROVIDER_AUTH_PREWARM=1`
4. **WARNING — Nuclear option:** `pkill -9 node` — **This kills ALL Node.js processes on your machine**, including unrelated applications, active development servers, and background workers. It can cause data loss in unsaved work. Use only as a last resort when the gateway is completely unresponsive and other steps have failed. Prefer restarting only the gateway: `systemctl --user restart openclaw-gateway` (Linux), `launchctl kickstart -k gui/$UID/com.openclaw.gateway` (macOS), or `Stop-ScheduledTask -TaskName "OpenClaw Gateway"; Start-ScheduledTask -TaskName "OpenClaw Gateway"` (Windows).

### WhatsApp Not Receiving Messages

1. `openclaw channels status --probe` — verify WhatsApp
2. Check sender is in `channels.whatsapp.allowFrom`
3. Check `dmPolicy` is not "disabled"
4. If `loggedOut` in logs: `openclaw channels logout --channel whatsapp; openclaw channels login --channel whatsapp`

### Slow Agent Responses

1. Check event loop health (see #2)
2. Check model selection — is V4 Pro rate-limited?
3. Check `agents.defaults.timeoutSeconds` — should be ≥ 300s
4. Check for session store bloat — prune old sessions

### After OpenClaw Upgrade (Version Change)

1. `openclaw config validate` — check for schema changes
2. `openclaw doctor --fix` — repair config drift
3. Check gateway log for new warnings/errors
4. Re-apply any source patches that were overwritten

## Integration with OpenClaw WinHealth Plugin

When the companion plugin (`@jordan-thirkle/openclaw-winhealth`) is installed, automated background monitoring is active. Use the tool `winhealth_check` for the current snapshot, `winhealth_diagnostics` for a full bundle, and `winhealth_alerts` to manage alert state.

## Security Considerations

- **External alerts are off by default** (`alertChannel: "none"`). Enable only after reviewing [SECURITY.md](https://github.com/jordan-thirkle/openclaw-winhealth/blob/main/SECURITY.md).
- **Diagnostic bundles** are sanitized by OpenClaw but may still contain system metadata — review before sharing.
- **Dashboard token** is stored in browser `sessionStorage` by default and cleared on tab close.
- **Command execution:** Some diagnostic commands use `pkill -9 node` which kills all Node.js processes — use only as a last resort.
- Full disclosure: [SkillSpector Security Audit](https://clawhub.ai/plugins/@jordan-thirkle/openclaw-winhealth/security-audit)
