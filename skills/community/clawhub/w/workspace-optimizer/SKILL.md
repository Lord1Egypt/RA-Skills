---
name: workspace-optimizer
description: "Audit, optimize, and maintain your OpenClaw agent workspace. Use when workspace needs health check, skill audit, memory cleanup, or performance tuning."
version: 1.0.0
author: AgentricAI-Owner
license: MIT
---

# Workspace Optimizer

Comprehensive workspace audit and optimization skill for OpenClaw agents. Identifies issues, suggests improvements, and provides actionable remediation steps.

## Quick Reference

| Situation | Action |
|-----------|--------|
| Workspace health check | Run full audit |
| Skill audit | Check installed vs available skills |
| Memory bloat | Cleanup and prune old files |
| Performance tuning | Optimize cron jobs and heartbeats |

## Background

Agent workspaces drift over time — stale cron jobs, orphaned memory files, unused skills, bloated context. This skill provides systematic audit and remediation to keep your workspace lean and performant.

## Solution

### Step-by-Step Audit

1. **Core Files Check**
```powershell
# Verify required files exist
$files = @("AGENTS.md","SOUL.md","IDENTITY.md","USER.md","TOOLS.md","MEMORY.md","HEARTBEAT.md")
foreach($f in $files) {
    $path = Join-Path $env:USERPROFILE ".openclaw\workspace\$f"
    if (Test-Path $path) { Write-Host "✅ $f" -ForegroundColor Green }
    else { Write-Host "❌ $f MISSING" -ForegroundColor Red }
}
```

2. **Skill Audit**
```bash
# List installed skills with status
clawhub list
# Check for updates
clawhub outdated
```

3. **Memory Health**
```powershell
# Check memory directory structure
Get-ChildItem "$env:USERPROFILE\.openclaw\workspace\memory" -Recurse |
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) } |
    Select-Object FullName, LastWriteTime, Length
```

4. **Cron Job Audit**
```bash
# List all cron jobs including disabled
openclaw cron list --include-disabled
# Check for orphaned or failed jobs
openclaw cron list --include-disabled | grep -i "disabled\|failed"
```

### Optimization Recommendations

- **Remove unused skills:** `clawhub uninstall <skill-name>`
- **Prune old memory files:** Archive files older than 30 days
- **Disable stale cron jobs:** `openclaw cron update <jobId> --enabled false`
- **Trim MEMORY.md:** Keep only active, relevant entries

## Common Variations

- **Quick Check:** Just run core files check + cron audit
- **Deep Clean:** Full audit + memory pruning + skill cleanup
- **Pre-Flight:** Run before major workspace changes

## Gotchas

- Don't delete daily memory files — archive them instead
- Check cron job run history before disabling
- Some skills have dependencies — check before uninstalling

## Source

- **Author:** AgentricAI-Owner
- **Created:** 2026-06-23
- **Origin:** DarkCluster workspace optimization patterns
