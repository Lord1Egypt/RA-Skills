<#
.SYNOPSIS
  Local git release for skill-template repo.

.DESCRIPTION
  Handles git commit / push / semver tag / push tag only.
  Encryption, ZIP packaging, and marketplace sync are done by CI
  (.github/workflows/release_skill.yaml → reusable-release-skill.yaml@main).

  Requires: git, PowerShell 5+
#>

[CmdletBinding()]
param(
  [string]$Prefix = "v",
  [string]$Message = "正式发布",
  [switch]$AutoCommit,
  [switch]$RequireClean,
  [string]$CommitMessage,
  [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Remove-GitNoise {
  param([string[]]$Lines)
  return @($Lines | Where-Object {
    $_ -and ($_ -notmatch '^warning:\s+unable to access ')
  })
}

function Invoke-Git {
  param([Parameter(Mandatory = $true)][string]$Args)
  Write-Host ">> git $Args" -ForegroundColor DarkGray
  & cmd /c "git $Args 2>&1" | Out-Null
  if ($LASTEXITCODE -ne 0) {
    throw "git command failed: git $Args"
  }
}

function Get-GitOutput {
  param([Parameter(Mandatory = $true)][string]$Args)
  $output = & cmd /c "git $Args 2>&1"
  if ($LASTEXITCODE -ne 0) {
    throw "git command failed: git $Args"
  }
  return @(Remove-GitNoise -Lines @($output))
}

function Test-Repo {
  $output = & cmd /c "git rev-parse --is-inside-work-tree 2>&1"
  if ($LASTEXITCODE -ne 0) {
    return $false
  }
  $clean = Remove-GitNoise -Lines @($output)
  return (($clean | Select-Object -First 1) -eq "true")
}

function Get-CurrentBranch {
  $b = (Get-GitOutput "branch --show-current" | Select-Object -First 1).Trim()
  return $b
}

function Get-StatusPorcelain {
  $lines = @(Get-GitOutput "status --porcelain")
  return $lines
}

function Parse-SemVerTag {
  param(
    [string]$Tag,
    [string]$TagPrefix
  )
  $escaped = [regex]::Escape($TagPrefix)
  $m = [regex]::Match($Tag, "^${escaped}(\d+)\.(\d+)\.(\d+)$")
  if (-not $m.Success) { return $null }

  return [pscustomobject]@{
    Raw   = $Tag
    Major = [int]$m.Groups[1].Value
    Minor = [int]$m.Groups[2].Value
    Patch = [int]$m.Groups[3].Value
  }
}

function Get-NextTag {
  param([string]$TagPrefix)

  $tags = Get-GitOutput "tag --list"
  $parsed = @()

  foreach ($t in $tags) {
    $t = $t.Trim()
    if (-not $t) { continue }
    $obj = Parse-SemVerTag -Tag $t -TagPrefix $TagPrefix
    if ($null -ne $obj) { $parsed += $obj }
  }

  if ($parsed.Count -eq 0) {
    return "${TagPrefix}1.0.1"
  }

  $latest = $parsed | Sort-Object Major, Minor, Patch | Select-Object -Last 1
  return "$TagPrefix$($latest.Major).$($latest.Minor).$([int]$latest.Patch + 1)"
}

function Assert-SkillReleasePackagingSources {
  param([Parameter(Mandatory = $true)][string]$SkillRoot)

  $scriptsDir = Join-Path $SkillRoot "scripts"
  $mainPy = Join-Path $scriptsDir "main.py"
  if (-not (Test-Path -LiteralPath $mainPy)) {
    return
  }

  $text = Get-Content -LiteralPath $mainPy -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
  if ([string]::IsNullOrWhiteSpace($text)) {
    return
  }

  $need = @()
  if ($text -match '(?m)^\s*from\s+cli\.') { $need += 'cli' }
  if ($text -match '(?m)^\s*import\s+cli\b') { $need += 'cli' }
  if ($text -match '(?m)^\s*from\s+service\.') { $need += 'service' }
  if ($text -match '(?m)^\s*import\s+service\b') { $need += 'service' }
  if ($text -match '(?m)^\s*from\s+db\.') { $need += 'db' }
  if ($text -match '(?m)^\s*import\s+db\b') { $need += 'db' }
  if ($text -match '(?m)^\s*from\s+util\.') { $need += 'util' }
  if ($text -match '(?m)^\s*import\s+util\b') { $need += 'util' }

  foreach ($p in ($need | Select-Object -Unique)) {
    $folder = Join-Path $scriptsDir $p
    if (-not (Test-Path -LiteralPath $folder)) {
      throw "Release check failed: scripts/main.py imports from '$p' but folder is missing: $folder"
    }
  }

  $pyFiles = @(Get-ChildItem -LiteralPath $scriptsDir -Filter *.py -Recurse -File -ErrorAction SilentlyContinue)
  Write-Host "Packaging check: $($pyFiles.Count) Python file(s) under scripts/ (CI will obfuscate all recursively)." -ForegroundColor DarkGray
}

function Ensure-CleanOrAutoCommit {
  param(
    [switch]$DoAutoCommit,
    [switch]$NeedClean,
    [switch]$IsDryRun,
    [string]$Msg
  )

  $status = @(Get-StatusPorcelain)
  if ($status.Length -eq 0) { return }

  if ($NeedClean) {
    Write-Host "Working tree is not clean and -RequireClean is enabled." -ForegroundColor Yellow
    Remove-GitNoise -Lines @(& cmd /c "git status --short 2>&1") | ForEach-Object { Write-Host $_ }
    throw "Abort: dirty working tree."
  }

  $commitMsg = $Msg
  if ([string]::IsNullOrWhiteSpace($commitMsg)) {
    $commitMsg = "chore: auto release commit ($(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))"
  }

  if (-not $DoAutoCommit) {
    Write-Host "Detected uncommitted changes, auto-committing before release..." -ForegroundColor Yellow
  }

  if ($IsDryRun) {
    Write-Host "[DryRun] Would run: git add -A" -ForegroundColor Yellow
    Write-Host "[DryRun] Would run: git commit -m `"$commitMsg`"" -ForegroundColor Yellow
    return
  }

  Invoke-Git "add -A"
  Invoke-Git "commit -m `"$commitMsg`""
}

try {
  Write-Host "=== Release Script Start ===" -ForegroundColor Cyan

  if (-not (Test-Repo)) {
    throw "Current directory is not a git repository."
  }

  $branch = Get-CurrentBranch
  if ([string]::IsNullOrWhiteSpace($branch)) {
    throw "Unable to determine current branch."
  }

  if ($branch -notin @("main", "master")) {
    throw "Current branch is '$branch'. Release is only allowed from main/master."
  }

  if ($DryRun) {
    Write-Host "[DryRun] Would run: git fetch --tags --prune origin" -ForegroundColor Yellow
  } else {
    Invoke-Git "fetch --tags --prune origin"
  }

  Ensure-CleanOrAutoCommit -DoAutoCommit:$AutoCommit -NeedClean:$RequireClean -IsDryRun:$DryRun -Msg $CommitMessage

  $skillRoot = (Get-GitOutput "rev-parse --show-toplevel" | Select-Object -First 1).Trim()
  if (Test-Path -LiteralPath (Join-Path $skillRoot "SKILL.md")) {
    Assert-SkillReleasePackagingSources -SkillRoot $skillRoot
  }

  $null = Remove-GitNoise -Lines @(& cmd /c 'git rev-parse --abbrev-ref --symbolic-full-name "@{u}" 2>&1')
  $hasUpstream = ($LASTEXITCODE -eq 0)

  if ($DryRun) {
    if ($hasUpstream) {
      Write-Host "[DryRun] Would run: git push" -ForegroundColor Yellow
    } else {
      Write-Host "[DryRun] Would run: git push -u origin $branch" -ForegroundColor Yellow
    }
  } else {
    if ($hasUpstream) {
      Invoke-Git "push"
    } else {
      Invoke-Git "push -u origin $branch"
    }
  }

  $nextTag = Get-NextTag -TagPrefix $Prefix
  Write-Host "Next tag: $nextTag" -ForegroundColor Green

  $existing = @(Get-GitOutput "tag --list `"$nextTag`"")
  if ($existing.Length -gt 0) {
    throw "Tag already exists: $nextTag"
  }

  if ($DryRun) {
    Write-Host "[DryRun] Would run: git tag -a $nextTag -m `"$Message`"" -ForegroundColor Yellow
    Write-Host "[DryRun] Would run: git push origin $nextTag" -ForegroundColor Yellow
    Write-Host "=== DryRun Complete ===" -ForegroundColor Cyan
    exit 0
  }

  Invoke-Git "tag -a $nextTag -m `"$Message`""
  Invoke-Git "push origin $nextTag"

  Write-Host "Release success: $nextTag" -ForegroundColor Green
  Write-Host "=== Release Script Done ===" -ForegroundColor Cyan
  exit 0
}
catch {
  Write-Host "Release failed: $($_.Exception.Message)" -ForegroundColor Red
  exit 1
}
