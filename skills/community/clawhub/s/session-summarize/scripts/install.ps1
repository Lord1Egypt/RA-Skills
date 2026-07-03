# summarize skill — multi-platform one-line installer (Windows PowerShell)
# iwr https://raw.githubusercontent.com/gtbwpkwjnb-alt/summarize-skill/master/install.ps1 | iex

$ErrorActionPreference = "Stop"

$RepoSSH   = "git@github.com:gtbwpkwjnb-alt/summarize-skill.git"
$RepoHTTPS = "https://github.com/gtbwpkwjnb-alt/summarize-skill.git"

# --- Platform auto-detect ---
function Get-InstallDir {
    # ZCode
    if (Test-Path "$env:USERPROFILE\.zcode\skills") {
        return "$env:USERPROFILE\.zcode\skills\summarize"
    }
    # Claude Code
    if (Test-Path "$env:USERPROFILE\.claude\skills") {
        return "$env:USERPROFILE\.claude\skills\summarize"
    }
    # Cursor
    if (Test-Path "$env:USERPROFILE\.cursor\extensions") {
        return "$env:USERPROFILE\.cursor\agent-skills\summarize"
    }
    # Codex
    if (Test-Path "$env:USERPROFILE\.codex\skills") {
        return "$env:USERPROFILE\.codex\skills\summarize"
    }
    # Windsurf
    if (Test-Path "$env:USERPROFILE\.windsurf\skills") {
        return "$env:USERPROFILE\.windsurf\skills\summarize"
    }
    # Fallback
    return "$env:USERPROFILE\.agent-skills\summarize"
}

$InstallDir = Get-InstallDir

Write-Host "📦 summarize skill installer"
Write-Host "   Target: $InstallDir"

if (Test-Path $InstallDir) {
    Write-Host "   Already installed at $InstallDir"
    Write-Host "🔄 Updating to latest version..."
    Push-Location $InstallDir
    try {
        git pull --rebase 2>$null
    } catch {
        Pop-Location
        Remove-Item -Recurse -Force $InstallDir -ErrorAction SilentlyContinue
        try { git clone $RepoSSH $InstallDir } catch { git clone $RepoHTTPS $InstallDir }
    }
    Pop-Location
} else {
    Write-Host "   Cloning into $InstallDir ..."
    New-Item -ItemType Directory -Force -Path (Split-Path $InstallDir) | Out-Null
    try { git clone $RepoSSH $InstallDir } catch { git clone $RepoHTTPS $InstallDir }
}

$ver = Get-Content "$InstallDir\VERSION" -Raw
Write-Host ""
Write-Host "✅ summarize skill installed!  v$ver"
Write-Host "   Path:    $InstallDir"
Write-Host "   Trigger: 总结 / summarize"
Write-Host ""
Write-Host "📊 Manage:"
Write-Host "   Update:  cd $InstallDir; git pull"
Write-Host "   Issues:  https://github.com/gtbwpkwjnb-alt/summarize-skill/issues"
