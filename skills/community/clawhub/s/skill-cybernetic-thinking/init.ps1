# init.ps1 — Harness verification for cybernetic-thinking skill
# Required by AGENTS.md. Run before claiming a feature done.

param()

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$allOk = $true

function Test-FileExists {
    param([string]$Name, [string]$Path)
    if (Test-Path -LiteralPath $Path) {
        Write-Host "[PASS] $Name exists"
        return $true
    } else {
        Write-Host "[FAIL] $Name missing: $Path"
        $script:allOk = $false
        return $false
    }
}

Write-Host "=== Harness Verification ==="
Write-Host "Root: $root"

# 1. Required reference files exist
$required = @(
    "evals/checks.json",
    "references/closed-loop-workflow.md",
    "references/state-and-control.md",
    "references/stability.md",
    "references/modeling.md",
    "references/multivariable.md",
    "references/disturbance.md",
    "references/bounded-control.md",
    "references/discrete-systems.md",
    "references/original-text.md",
    "references/possibility-space.md",
    "references/black-box-epistemology.md",
    "references/system-evolution.md",
    "references/information-and-control.md",
    "templates/debugging-checklist.md",
    "templates/change-proposal.md",
    "CHANGELOG.md",
    "README.md",
    "README_CN.md",
    "SKILL.md",
    "AGENTS.md",
    "feature_list.json",
    "progress.md",
    "session-handoff.md"
)
foreach ($f in $required) {
    Test-FileExists -Name $f -Path (Join-Path $root $f)
}

# 2. evals/checks.json is valid JSON
$jsonPath = Join-Path $root "evals/checks.json"
try {
    python -m json.tool $jsonPath | Out-Null
    Write-Host "[PASS] evals/checks.json is valid JSON"
} catch {
    Write-Host "[FAIL] evals/checks.json JSON validation failed"
    $allOk = $false
}

# 3. Installer registry count matches README agent tables (anti-drift guard)
$installJs = Join-Path $root "scripts/install.js"
$readmeEn  = Join-Path $root "README.md"
$readmeCn  = Join-Path $root "README_CN.md"

$regCount = (Select-String -Pattern "slug:\s*'" -Path $installJs | Measure-Object).Count
$enCount  = (Select-String -Pattern "^\s*\|.*/skills/.*\|" -Path $readmeEn | Measure-Object).Count
$cnCount  = (Select-String -Pattern "^\s*\|.*/skills/.*\|" -Path $readmeCn | Measure-Object).Count

if ($regCount -gt 0 -and $regCount -eq $enCount -and $enCount -eq $cnCount) {
    Write-Host "[PASS] installer ($regCount) matches README EN ($enCount) and CN ($cnCount) agent tables"
} else {
    Write-Host "[FAIL] agent count drift: installer=$regCount README_EN=$enCount README_CN=$cnCount"
    $allOk = $false
}

Write-Host ""
if ($allOk) {
    Write-Host "Verification Complete — OK"
} else {
    Write-Host "Verification Complete — ISSUES FOUND"
    exit 1
}
