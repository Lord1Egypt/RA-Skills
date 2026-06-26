# Published Bootstrap Helper

Use this reference when you need a **published, inspectable bootstrap path** for Workhorse Duo.

Why this file exists:
- ClawHub reliably exposes markdown/reference files in the published package
- some script file types may not appear in the remote file list
- this document provides the exact bootstrap logic in a form operators can inspect, review, and copy locally

If you prefer a local script workflow, this markdown file is the canonical published source. Operators can copy the script block below into `bootstrap-workhorse-duo.ps1` locally and run it.

## What the helper does

The bootstrap helper:
1. checks whether `xiaoma` and `xiaoniu` already exist
2. creates missing agents if needed
3. checks whether cross-agent config prerequisites are present
4. optionally patches bootstrap-safe config and restarts the gateway
5. runs a ping check unless the operator skips ping
6. prints a clear `READY` or `NOT READY` result

## PowerShell helper (published source)

```powershell
param(
  [string]$Workspace = ".",
  [string]$Model = "",
  [switch]$SkipPing,
  [switch]$AutoFixConfig
)

$ErrorActionPreference = "Stop"

function Write-Step($text) {
  Write-Host "[workhorse-duo] $text"
}

function Write-Ready($text) {
  Write-Host "[workhorse-duo] READY: $text"
}

function Write-NotReady($text) {
  Write-Host "[workhorse-duo] NOT READY: $text"
}

function Invoke-JsonAgentPing {
  param(
    [Parameter(Mandatory = $true)][string]$AgentId,
    [Parameter(Mandatory = $true)][string]$RoleText
  )

  $msg = "$RoleText. Reply only: PONG"
  $output = openclaw agent --agent $AgentId --message $msg --timeout 120 --json | Out-String
  return $output
}

Write-Host ""
Write-Host "=== Workhorse Duo Bootstrap ==="
Write-Host "This helper checks setup, creates missing agents, optionally patches config, and verifies readiness."
Write-Host ""

if ([string]::IsNullOrWhiteSpace($Model)) {
  Write-Step "No model override provided; using the current OpenClaw default model."
}

Write-Step "Checking whether xiaoma and xiaoniu already exist..."
$agentsBefore = openclaw agents list | Out-String

if ($agentsBefore -notmatch "(?m)^- xiaoma$") {
  Write-Step "Creating xiaoma..."
  if ([string]::IsNullOrWhiteSpace($Model)) {
    openclaw agents add xiaoma --workspace $Workspace --non-interactive | Out-Host
  } else {
    openclaw agents add xiaoma --workspace $Workspace --model $Model --non-interactive | Out-Host
  }
}

if ($agentsBefore -notmatch "(?m)^- xiaoniu$") {
  Write-Step "Creating xiaoniu..."
  if ([string]::IsNullOrWhiteSpace($Model)) {
    openclaw agents add xiaoniu --workspace $Workspace --non-interactive | Out-Host
  } else {
    openclaw agents add xiaoniu --workspace $Workspace --model $Model --non-interactive | Out-Host
  }
}

Write-Step "Verifying agent list..."
$agentsAfter = openclaw agents list | Out-String
$agentsAfter | Out-Host

$missing = @()
if ($agentsAfter -notmatch "(?m)^- xiaoma$") { $missing += "xiaoma" }
if ($agentsAfter -notmatch "(?m)^- xiaoniu$") { $missing += "xiaoniu" }
if ($missing.Count -gt 0) {
  Write-NotReady "missing agent(s): $($missing -join ', ')"
  exit 2
}

$configPath = Join-Path $HOME ".openclaw\openclaw.json"
Write-Step "Checking config prerequisites..."
$configRaw = Get-Content $configPath -Raw
$hasAgentToAgent = $configRaw -match '"agentToAgent"\s*:\s*\{'
$hasEnabled = $configRaw -match '"agentToAgent"[\s\S]*?"enabled"\s*:\s*true'
$hasSessionsAll = $configRaw -match '"sessions"\s*:\s*\{\s*"visibility"\s*:\s*"all"'
$hasAllow = $configRaw -match '"agentToAgent"[\s\S]*?"allow"\s*:\s*\['

if ((-not $hasAgentToAgent -or -not $hasEnabled -or -not $hasSessionsAll -or -not $hasAllow) -and $AutoFixConfig) {
  Write-Step "Config is incomplete. Applying bootstrap-safe config and restarting gateway..."
  $config = Get-Content $configPath -Raw | ConvertFrom-Json -Depth 100
  if (-not $config.tools) {
    $config | Add-Member -NotePropertyName tools -NotePropertyValue ([pscustomobject]@{})
  }
  if (-not $config.tools.agentToAgent) {
    $config.tools | Add-Member -NotePropertyName agentToAgent -NotePropertyValue ([pscustomobject]@{})
  }
  $config.tools.agentToAgent.enabled = $true
  $config.tools.agentToAgent.allow = @("*")
  if (-not $config.tools.sessions) {
    $config.tools | Add-Member -NotePropertyName sessions -NotePropertyValue ([pscustomobject]@{})
  }
  $config.tools.sessions.visibility = "all"
  $json = $config | ConvertTo-Json -Depth 100
  Copy-Item $configPath "$configPath.bak" -Force
  Set-Content -Path $configPath -Value $json -Encoding UTF8
  openclaw gateway restart | Out-Host
  Start-Sleep -Seconds 3
  $configRaw = Get-Content $configPath -Raw
  $hasAgentToAgent = $configRaw -match '"agentToAgent"\s*:\s*\{'
  $hasEnabled = $configRaw -match '"agentToAgent"[\s\S]*?"enabled"\s*:\s*true'
  $hasSessionsAll = $configRaw -match '"sessions"\s*:\s*\{\s*"visibility"\s*:\s*"all"'
  $hasAllow = $configRaw -match '"agentToAgent"[\s\S]*?"allow"\s*:\s*\['
}

if (-not $hasAgentToAgent -or -not $hasEnabled -or -not $hasSessionsAll -or -not $hasAllow) {
  Write-NotReady "cross-agent config is incomplete"
  Write-Host "Required settings:"
  Write-Host '  tools.agentToAgent.enabled = true'
  Write-Host '  tools.sessions.visibility = "all"'
  Write-Host '  tools.agentToAgent.allow must permit the target setup'
  Write-Host "Re-run with -AutoFixConfig to patch bootstrap-safe defaults automatically."
  exit 3
}

if ($SkipPing) {
  Write-Ready "agents exist and config prerequisites are present (ping skipped)."
  exit 0
}

Write-Step "Running xiaoma ping..."
$xiaomaPing = Invoke-JsonAgentPing -AgentId "xiaoma" -RoleText "You are Xiaoma, the execution worker"
$xiaomaOk = $xiaomaPing -match '"text"\s*:\s*"PONG"'

Write-Step "Running xiaoniu ping..."
$xiaoniuPing = Invoke-JsonAgentPing -AgentId "xiaoniu" -RoleText "You are Xiaoniu, the QA worker"
$xiaoniuOk = $xiaoniuPing -match '"text"\s*:\s*"PONG"'

if ($xiaomaOk -and $xiaoniuOk) {
  Write-Ready "xiaoma and xiaoniu both responded with PONG. Next step: run one tiny real execute -> review task."
  exit 0
}

Write-NotReady "ping failed"
Write-Host "xiaoma ping matched PONG: $xiaomaOk"
Write-Host "xiaoniu ping matched PONG: $xiaoniuOk"
Write-Host "--- xiaoma raw ---"
Write-Host $xiaomaPing
Write-Host "--- xiaoniu raw ---"
Write-Host $xiaoniuPing
exit 4
```

## Operator notes

- `-AutoFixConfig` changes `~/.openclaw/openclaw.json`, writes a `.bak`, and restarts the gateway.
- Bootstrap-safe defaults are meant for validation, not automatically the best long-term production posture.
- After validation, review `references/risk-and-rollback.md` and tighten policy if needed.
