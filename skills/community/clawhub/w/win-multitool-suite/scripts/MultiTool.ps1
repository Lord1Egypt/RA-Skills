# MultiTool.ps1 - launcher menu for the three suite workflows.
#
# Every entry runs a script from an installed skill and writes the output into
# the workspace. Nothing is sent anywhere on your behalf: no email, no order,
# no upload.
#
# Usage (PowerShell 5.1+ on Windows 10/11):
#   .\scripts\MultiTool.ps1
#   .\scripts\MultiTool.ps1 -Menu "market"

[CmdletBinding()]
param(
    [string]$Menu = "",
    [string]$Workspace = ""
)

$ErrorActionPreference = "Stop"

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BundleRoot = Split-Path -Parent $ScriptRoot
if (-not $Workspace) { $Workspace = Join-Path $env:LOCALAPPDATA "MultiToolSuite" }

function Find-SkillDir($name) {
    $roots = @(
        (Join-Path $env:USERPROFILE ".openclaw\skills"),
        (Join-Path $env:USERPROFILE ".config\openclaw\skills"),
        (Join-Path (Get-Location) "skills")
    )
    foreach ($root in $roots) {
        $candidate = Join-Path $root $name
        if (Test-Path $candidate) { return $candidate }
    }
    return $null
}

function Get-Python {
    foreach ($candidate in @("python", "python3", "py")) {
        $found = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($found) { return $found.Source }
    }
    return $null
}

function Run-Workflow($title, $skill, $script, $argsList) {
    Write-Host ""
    Write-Host "--- $title ---" -ForegroundColor Cyan
    $dir = Find-SkillDir $skill
    if (-not $dir) {
        Write-Host "Skill '$skill' is not installed yet." -ForegroundColor Yellow
        Write-Host "Install it with:  clawhub install @rapidworker1/$skill"
        return
    }
    $scriptPath = Join-Path $dir $script
    if (-not (Test-Path $scriptPath)) {
        Write-Host "Script not found: $scriptPath" -ForegroundColor Yellow
        return
    }
    $python = Get-Python
    if (-not $python) {
        Write-Host "Python was not found. Install Python 3.9+ and try again." -ForegroundColor Yellow
        return
    }
    & $python $scriptPath @argsList
    Write-Host ""
    Write-Host "Output folder: $Workspace\output" -ForegroundColor DarkGray
}

$menuItems = [ordered]@{
    "creative" = @{
        Title  = "Creative brief and ad copy pack"
        Skill  = "ai-creative-studio"
        Script = "scripts\creative_brief.py"
        Args   = @()
    }
    "market" = @{
        Title  = "Market snapshot and risk plan"
        Skill  = "ai-trading"
        Script = "scripts\market_snapshot.py"
        Args   = @()
    }
    "portfolio" = @{
        Title  = "Portfolio risk and position sizing"
        Skill  = "ai-trading"
        Script = "scripts\portfolio_risk.py"
        Args   = @()
    }
    "leads" = @{
        Title  = "Lead sheet (ICP, scored prospects)"
        Skill  = "b2b-lead-research-agent"
        Script = "scripts\lead_sheet.py"
        Args   = @()
    }
    "compliance" = @{
        Title  = "Outreach compliance check (CAN-SPAM)"
        Skill  = "b2b-lead-research-agent"
        Script = "scripts\compliance_check.py"
        Args   = @()
    }
}

if ($Menu) {
    if (-not $menuItems.Contains($Menu)) {
        Write-Host "Unknown menu entry: $Menu" -ForegroundColor Red
        Write-Host ("Available: " + ($menuItems.Keys -join ", "))
        exit 2
    }
    $item = $menuItems[$Menu]
    Run-Workflow $item.Title $item.Skill $item.Script $item.Args
    exit 0
}

Write-Host ""
Write-Host "Windows Multi-Tool Suite" -ForegroundColor White
Write-Host "---------------------------"
Write-Host "1. Creative brief and ad copy pack"
Write-Host "2. Market snapshot and risk plan"
Write-Host "3. Portfolio risk and position sizing"
Write-Host "4. Lead sheet (ICP, scored prospects)"
Write-Host "5. Outreach compliance check (CAN-SPAM)"
Write-Host "6. Status (installed skills, workspace, config)"
Write-Host "0. Quit"
Write-Host ""

$choice = Read-Host "Pick a workflow"
switch ($choice) {
    "1" { Run-Workflow $menuItems["creative"].Title $menuItems["creative"].Skill $menuItems["creative"].Script $menuItems["creative"].Args }
    "2" { Run-Workflow $menuItems["market"].Title $menuItems["market"].Skill $menuItems["market"].Script $menuItems["market"].Args }
    "3" { Run-Workflow $menuItems["portfolio"].Title $menuItems["portfolio"].Skill $menuItems["portfolio"].Script $menuItems["portfolio"].Args }
    "4" { Run-Workflow $menuItems["leads"].Title $menuItems["leads"].Skill $menuItems["leads"].Script $menuItems["leads"].Args }
    "5" { Run-Workflow $menuItems["compliance"].Title $menuItems["compliance"].Skill $menuItems["compliance"].Script $menuItems["compliance"].Args }
    "6" {
        $python = Get-Python
        if ($python) { & $python (Join-Path $ScriptRoot "verify_install.py") }
        else { Write-Host "Python was not found." -ForegroundColor Yellow }
    }
    "0" { Write-Host "Bye." }
    default { Write-Host "Not a number. Pick 0-6." -ForegroundColor Yellow }
}
