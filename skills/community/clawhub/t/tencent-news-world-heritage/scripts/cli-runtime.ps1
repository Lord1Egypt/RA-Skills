# Shared help and structured environment diagnostics for CLI-backed skills.

function Show-CliUsage {
  Write-Output @"
Usage:
  powershell scripts/run-cli.ps1 [--help | <command> [args...]]
  powershell scripts/run-cli.ps1 help          # Current CLI command reference
  powershell scripts/cli-state.ps1 [status]    # JSON environment diagnostics
  powershell scripts/cli-state.ps1 [help | -h | --help]

Help works without installing the CLI or configuring an API key.
Business queries require tencent-news-cli and a user-configured API key.
See references/installation-guide.md and references/env-setup-guide.md.
Diagnostics may exit 0 with success:false; this does not mean a query succeeded.
"@
}

function Get-CliResult([string]$Code) {
  $status = "environment_not_ready"
  switch ($Code) {
    "CLI_NOT_INSTALLED" {
      $message = "Tencent News CLI is not installed or could not be found."
      $steps = @("Follow references/installation-guide.md, then run cli-state status again.")
    }
    "API_KEY_MISSING" {
      $message = "No API key was detected in the current CLI environment."
      $steps = @("Check the shell configuration as described in SKILL.md before setting a new key.", "If missing, obtain a key at https://news.qq.com/exchange?scene=appkey and configure it locally.")
    }
    "ENVIRONMENT_CHECK_FAILED" {
      $message = "The CLI environment could not be verified."
      $steps = @("Follow references/env-setup-guide.md; do not share credentials or raw logs.")
    }
    "API_KEY_UNAUTHORIZED" {
      $message = "The API key is invalid, expired, or unauthorized."
      $steps = @("Obtain an authorized key at https://news.qq.com/exchange?scene=appkey and configure it locally.")
    }
    "READY" {
      return [ordered]@{ success = $true; status = "ready"; data = $null; error = $null; nextSteps = @() }
    }
    default {
      $status = "invalid_request"
      $message = "Invalid script arguments or skill metadata. Read --help and check SKILL.md."
      $steps = @("Run the script with --help.")
    }
  }
  return [ordered]@{
    success = $false; status = $status; data = $null
    error = @{ code = $Code; message = $message }; nextSteps = $steps
  }
}

function Fail([string]$Message) {
  if ($Message -like "cli not found*") {
    if ($script:CliHelpRequest) { Show-CliUsage; exit 0 }
    $code = "CLI_NOT_INSTALLED"
  } else {
    $code = "INVALID_ARGUMENT"
  }
  Get-CliResult $code | ConvertTo-Json -Depth 5
  exit 1
}
