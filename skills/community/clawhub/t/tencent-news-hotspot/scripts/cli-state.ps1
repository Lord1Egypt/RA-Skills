#!/usr/bin/env pwsh

# cli-state.ps1 — Output install state, version/update status, and API key status.
# Usage: powershell scripts/cli-state.ps1

$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "cli-runtime.ps1")
$Command = if ($args.Count -gt 0) { $args[0] } else { $null }
if ($args.Count -gt 1) { Fail "expected one state command" }

if ($Command -in @("help", "-h", "--help")) {
  Show-CliUsage
  exit 0
}

if ($Command -and $Command -ne "status") {
  Fail "unknown argument: $Command"
}

# ── helpers ──────────────────────────────────────────────────────────

function Get-WindowsArch {
  $rawArch = (Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment").PROCESSOR_ARCHITECTURE
  switch ($rawArch) {
    "AMD64" { return "amd64" }
    "ARM64" { return "arm64" }
    default { Fail "unsupported architecture: $rawArch" }
  }
}

function Get-CommandOutput {
  param(
    [string]$Command,
    [string[]]$CommandArgs = @()
  )

  if ([string]::IsNullOrWhiteSpace($Command)) {
    return @{
      ExitCode = 1
      Output = "command path is empty"
    }
  }

  try {
    $output = & $Command @CommandArgs 2>&1
    $exitCode = if ($null -ne $LASTEXITCODE) { [int]$LASTEXITCODE } else { 0 }
    return @{
      ExitCode = $exitCode
      Output = ($output | Out-String).Trim()
    }
  } catch {
    $exitCode = if ($null -ne $LASTEXITCODE -and $LASTEXITCODE -ne 0) { [int]$LASTEXITCODE } else { 1 }
    return @{
      ExitCode = $exitCode
      Output = ($_ | Out-String).Trim()
    }
  }
}

function Resolve-CommandCliPath([string]$CliCommandName) {
  $resolved = $null
  try {
    $resolved = (Get-Command $CliCommandName -ErrorAction SilentlyContinue).Source
  } catch {
    return $null
  }

  if (-not $resolved) { return $null }

  # Verify the resolved path actually works
  try {
    $null = & $resolved help 2>&1
    if ($LASTEXITCODE -ne 0) { return $null }
  } catch {
    return $null
  }

  return $resolved.Replace("\", "/")
}

function Normalize-ApiKey([string]$Raw) {
  $key = $Raw.Trim().Trim('"').Trim("'")
  $key = [regex]::Replace($key, '^api[\s_-]*key\s*[:=]\s*', '', 'IgnoreCase')
  return $key.Trim()
}

function ConvertTo-JsonEscaped([string]$Value) {
  return $Value.Replace("\", "\\").Replace('"', '\"').Replace("`t", "\t").Replace("`r", "").Replace("`n", " ")
}

# ── platform detection ───────────────────────────────────────────────

$Os = "windows"
$Arch = Get-WindowsArch
$CliCommandName = "tencent-news-cli"
$CliFilename = "tencent-news-cli.exe"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillDir = Split-Path -Parent $ScriptDir
$LocalCliPath = Join-Path $SkillDir $CliFilename

$InstallEnvName = "TENCENT_NEWS_INSTALL"
$InstallRoot = [Environment]::GetEnvironmentVariable($InstallEnvName, "Process")
if (-not $InstallRoot) {
  $InstallRoot = Join-Path $HOME ".tencent-news-cli"
}
$GlobalCliPath = Join-Path (Join-Path $InstallRoot "bin") $CliFilename

# ── cli detection: global command > global install path > legacy local path ──

$CliSource = "none"
$CliPath = $GlobalCliPath

$CommandCliPath = Resolve-CommandCliPath $CliCommandName
if ($CommandCliPath) {
  $CliPath = $CommandCliPath
  $CliSource = "global"
} elseif (Test-Path $GlobalCliPath) {
  $CliSource = "global"
} elseif (Test-Path $LocalCliPath) {
  $CliPath = $LocalCliPath.Replace("\", "/")
  $CliSource = "local"
}

$CliExists = $CliSource -ne "none"

# ── update check ────────────────────────────────────────────────────

$UpdateNeedUpdate = "null"
$UpdateError = "null"

if ($CliExists) {
  $versionResult = Get-CommandOutput -Command $CliPath -CommandArgs @("version")

  if ($versionResult.ExitCode -eq 0) {
    try {
      $parsed = $versionResult.Output | ConvertFrom-Json
      if ($null -ne $parsed.need_update) {
        $needUpdate = [string]$parsed.need_update
        if ($needUpdate -eq "True") {
          $UpdateNeedUpdate = "true"
        } elseif ($needUpdate -eq "False") {
          $UpdateNeedUpdate = "false"
        } else {
          $errMsg = ConvertTo-JsonEscaped "$CliPath version did not return valid need_update value: $($versionResult.Output)"
          $UpdateError = "`"$errMsg`""
        }
      } else {
        $errMsg = ConvertTo-JsonEscaped "$CliPath version did not return valid need_update value: $($versionResult.Output)"
        $UpdateError = "`"$errMsg`""
      }
    } catch {
      $rawOut = if ($versionResult.Output) { $versionResult.Output } else { "(empty output)" }
      $errMsg = ConvertTo-JsonEscaped "$CliPath version did not return valid JSON: $rawOut"
      $UpdateError = "`"$errMsg`""
    }
  } else {
    if ($versionResult.Output) {
      $errMsg = ConvertTo-JsonEscaped $versionResult.Output
      $UpdateError = "`"$errMsg`""
    } else {
      $errMsg = ConvertTo-JsonEscaped "$CliPath version failed with exit code $($versionResult.ExitCode)."
      $UpdateError = "`"$errMsg`""
    }
  }
}

# ── api key state ────────────────────────────────────────────────────

$ApiKeyStatus = "error"
$ApiKeyPresent = "false"
$ApiKeyError = "null"

if ($CliExists) {
  $apikeyResult = Get-CommandOutput -Command $CliPath -CommandArgs @("apikey-get")

  if ($apikeyResult.ExitCode -eq 0) {
    $keyMatch = [regex]::Match($apikeyResult.Output, 'API Key\s*:\s*(.+)$', [System.Text.RegularExpressions.RegexOptions]::Multiline)
    if ($keyMatch.Success) {
      $key = Normalize-ApiKey $keyMatch.Groups[1].Value
      if ($key) {
        $ApiKeyStatus = "configured"
        $ApiKeyPresent = "true"
      } else {
        $ApiKeyStatus = "error"
        $ApiKeyError = "`"CLI apikey-get succeeded, but API key could not be parsed from output.`""
      }
    } else {
      $ApiKeyStatus = "error"
      $ApiKeyError = "`"CLI apikey-get succeeded, but API key could not be parsed from output.`""
    }
  } elseif ($apikeyResult.Output -match '未设置 API Key|not set' -or $apikeyResult.ExitCode -eq 2) {
    $ApiKeyStatus = "missing"
  } else {
    $ApiKeyStatus = "error"
    if ($apikeyResult.Output) {
      $errMsg = ConvertTo-JsonEscaped $apikeyResult.Output
      $ApiKeyError = "`"$errMsg`""
    } else {
      $ApiKeyError = "`"apikey-get failed with exit code $($apikeyResult.ExitCode).`""
    }
  }
} else {
  $ApiKeyStatus = "error"
  $ApiKeyError = "`"CLI not found, cannot check API key.`""
}

# ── output JSON ──────────────────────────────────────────────────────

$code = if (-not $CliExists) {
  "CLI_NOT_INSTALLED"
} elseif ($ApiKeyStatus -eq "missing") {
  "API_KEY_MISSING"
} elseif ($ApiKeyStatus -ne "configured") {
  if ($ApiKeyError -match 'invalid api key|unauthorized|401|403|API Key 无效|鉴权|认证失败') { "API_KEY_UNAUTHORIZED" } else { "ENVIRONMENT_CHECK_FAILED" }
} else {
  "READY"
}
$result = Get-CliResult $code
$result.platform = @{ os = $Os; arch = $Arch; cliPath = $CliPath.Replace("\", "/"); cliSource = $CliSource }
$result.cliExists = $CliExists
$result.update = @{
  needUpdate = if ($UpdateNeedUpdate -eq "null") { $null } else { $UpdateNeedUpdate -eq "true" }
  error = if ($UpdateError -eq "null") { $null } else { "Unable to check CLI updates." }
}
$result.apiKey = @{
  status = $ApiKeyStatus; present = $ApiKeyPresent -eq "true"
  error = if ($ApiKeyError -eq "null") { $null } else { "Unable to verify API key state; see error.code and the setup guide." }
}
$result | ConvertTo-Json -Depth 5
