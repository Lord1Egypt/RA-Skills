# skills-summarize-audit installer — 手动安装，见 README.md
#
# 🔒 安全说明：
#   - 本脚本通过 git clone/pull 获取代码，依赖 GitHub 传输层安全
#   - 建议安装后运行：python tests/validate.py 验证文件完整性
#   - 生产环境可在 README.md 中获取官方 SHA256 校验和进行比对
#   - 脚本不会修改系统目录，仅写入用户目录下的 skills 文件夹

param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$RepoSSH   = "git@github.com:gtbwpkwjnb-alt/skills-summarize-audit-skill.git"
$RepoHTTPS = "https://github.com/gtbwpkwjnb-alt/skills-summarize-audit-skill.git"

function Get-InstallDir {
    if (Test-Path "$env:USERPROFILE\.zcode\skills") {
        return "$env:USERPROFILE\.zcode\skills\skills-summarize-audit"
    }
    if (Test-Path "$env:USERPROFILE\.claude\skills") {
        return "$env:USERPROFILE\.claude\skills\skills-summarize-audit"
    }
    if (Test-Path "$env:USERPROFILE\.codex\skills") {
        return "$env:USERPROFILE\.codex\skills\skills-summarize-audit"
    }
    if (Test-Path "$env:USERPROFILE\.cursor\agent-skills") {
        return "$env:USERPROFILE\.cursor\agent-skills\skills-summarize-audit"
    }
    return "$env:USERPROFILE\.agent-skills\skills-summarize-audit"
}

$InstallDir = Get-InstallDir

Write-Host "📦 skills-summarize-audit installer"
Write-Host "   Target: $InstallDir"

if ($DryRun) {
    Write-Host "   Dry run: no filesystem or network changes will be made."
    if (Test-Path $InstallDir) {
        Write-Host "   Would verify a clean Git worktree, then run: git pull --ff-only"
    } else {
        Write-Host "   Would clone from SSH, then HTTPS fallback if SSH is unavailable."
    }
    return
}

if (Test-Path $InstallDir) {
    Write-Host "   Already installed. Updating..."
    Push-Location $InstallDir
    try {
        $changes = git status --porcelain
        if ($changes) {
            throw "Local changes detected. Commit, stash, or back up the directory before updating."
        }
        git pull --ff-only
        if ($LASTEXITCODE -ne 0) {
            throw "Update failed. The existing installation was preserved; resolve the Git history manually."
        }
    } finally {
        Pop-Location
    }
} else {
    Write-Host "   Cloning..."
    New-Item -ItemType Directory -Force -Path (Split-Path $InstallDir) | Out-Null
    try { git clone $RepoSSH $InstallDir } catch { git clone $RepoHTTPS $InstallDir }
}

$ver = Get-Content "$InstallDir\VERSION" -Raw
Write-Host ""
Write-Host "✅ skills-summarize-audit installed!  v$ver"
Write-Host "   Trigger: skills-summarize-audit / 技能审查 / 技能总结"
Write-Host "   Issues:  https://github.com/gtbwpkwjnb-alt/skills-summarize-audit-skill/issues"
