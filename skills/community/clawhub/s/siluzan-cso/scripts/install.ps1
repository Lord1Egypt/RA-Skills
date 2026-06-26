#Requires -Version 5.1
# =============================================================================
# siluzan-cso-cli - One-click install script (PowerShell)
# Supported: Windows 10/11 (PowerShell 5.1+ or PowerShell 7+)
# =============================================================================

$ErrorActionPreference = 'Stop'

# -- Package info (injected at build time) ------------------------------------
$PKG_NAME    = 'siluzan-cso-cli'
# PKG_VERSION 锁定到与本脚本同批构建产物一致的版本，避免与 dist/skill 错位
$PKG_VERSION = '1.1.29'
$CLI_BIN     = 'siluzan-cso'
$SKILL_LABEL = 'Siluzan CSO'
$INSTALL_CMD = 'npm install -g siluzan-cso-cli'
$WEB_BASE    = 'https://www.siluzan.com'

# -- Constants ----------------------------------------------------------------
$NODE_MAJOR_MIN    = 18
$NPM_MIRROR        = 'https://registry.npmmirror.com'
# Git for Windows installer (mirrored on Siluzan CDN; bump version here when needed)
$GIT_INSTALLER_URL = 'https://staticpn.siluzan.com/assets/git/Git-2.54.0-64-bit.exe'

# -- Helpers ------------------------------------------------------------------
function Write-Info  { param([string]$Msg) Write-Host "[OK] $Msg" -ForegroundColor Green }
function Write-Warn  { param([string]$Msg) Write-Host "[!]  $Msg" -ForegroundColor Yellow }
function Write-Err   { param([string]$Msg) Write-Host "[X]  $Msg" -ForegroundColor Red }
function Write-Step  { param([string]$Msg) Write-Host "`n-- $Msg --" -ForegroundColor White }

function Refresh-Path {
    $machinePath = [Environment]::GetEnvironmentVariable('Path', 'Machine')
    $userPath    = [Environment]::GetEnvironmentVariable('Path', 'User')
    $env:Path    = "$machinePath;$userPath"
}

# -- Node.js ------------------------------------------------------------------
function Test-NodeVersion {
    try {
        $nodeCmd = Get-Command node -ErrorAction SilentlyContinue
        if (-not $nodeCmd) { return $false }
        $ver = (node -v) -replace '^v', ''
        $major = [int]($ver.Split('.')[0])
        return $major -ge $NODE_MAJOR_MIN
    } catch {
        return $false
    }
}

function Get-NodeVersionString {
    try { return (node -v) } catch { return 'N/A' }
}

function Install-NodeJS {
    $hasWinget = $null -ne (Get-Command winget -ErrorAction SilentlyContinue)
    if ($hasWinget) {
        Write-Info 'Installing Node.js LTS via winget...'
        winget install -e --id OpenJS.NodeJS.LTS --silent --accept-package-agreements --accept-source-agreements
        if ($LASTEXITCODE -ne 0) {
            Write-Warn 'winget returned non-zero, trying fallback...'
            Install-NodeFallback
            return
        }
    } else {
        Install-NodeFallback
        return
    }
    Refresh-Path
    if (-not (Test-NodeVersion)) {
        Write-Warn 'Node.js not found after PATH refresh, locating install dir...'
        $nodePath = "$env:ProgramFiles\nodejs"
        if (Test-Path "$nodePath\node.exe") {
            $env:Path = "$nodePath;$env:Path"
        }
    }
}

function Install-NodeFallback {
    Write-Err 'Cannot auto-install Node.js'
    Write-Host ''
    Write-Host '  Please install Node.js manually:' -ForegroundColor Cyan
    Write-Host '  https://nodejs.org/en/download/'
    Write-Host ''
    Write-Host '  After installation, reopen PowerShell and run this script again.'
    throw 'Node.js is required'
}

# -- Git for Windows ----------------------------------------------------------
# Some agent clients (Cursor / Claude Code / etc.) have known quirks running
# PowerShell or cmd commands. We install Git for Windows ahead of time so the
# user always has a Git Bash fallback to run the equivalent bash installer
# (`bash <(curl -fsSL .../install.sh)`) when the PowerShell channel misbehaves.
function Test-GitInstalled {
    return $null -ne (Get-Command git -ErrorAction SilentlyContinue)
}

function Test-IsAdmin {
    try {
        $id = [Security.Principal.WindowsIdentity]::GetCurrent()
        $principal = New-Object Security.Principal.WindowsPrincipal($id)
        return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    } catch {
        return $false
    }
}

function Install-Git {
    $tmpFile = Join-Path $env:TEMP 'siluzan-git-installer.exe'

    Write-Info "Downloading Git for Windows: $GIT_INSTALLER_URL"
    try {
        $prevProgress = $ProgressPreference
        $ProgressPreference = 'SilentlyContinue'
        Invoke-WebRequest -Uri $GIT_INSTALLER_URL -OutFile $tmpFile -UseBasicParsing
        $ProgressPreference = $prevProgress
    } catch {
        Write-Warn "Git installer download failed: $($_.Exception.Message)"
        return $false
    }

    if (-not (Test-Path $tmpFile)) {
        Write-Warn 'Git installer file not found after download'
        return $false
    }

    # Inno Setup silent flags. When not admin we point /DIR to %LOCALAPPDATA% so
    # the installer doesn't try to write to Program Files (which would trigger UAC
    # or just fail). The installer auto-detects ALLUSERS vs CURRENTUSER mode based
    # on whether the current process is elevated, so we don't pass /CURRENTUSER
    # explicitly (not all Git for Windows builds accept that flag).
    $installArgs = @('/VERYSILENT', '/NORESTART', '/NOCANCEL', '/SP-', '/CLOSEAPPLICATIONS', '/RESTARTAPPLICATIONS')
    if (Test-IsAdmin) {
        Write-Info 'Installing Git for Windows system-wide (admin detected)...'
    } else {
        $userDir = Join-Path $env:LOCALAPPDATA 'Programs\Git'
        Write-Info "Installing Git for Windows for current user: $userDir"
        $installArgs += @("/DIR=$userDir")
    }

    try {
        Start-Process -FilePath $tmpFile -ArgumentList $installArgs -Wait -NoNewWindow
    } catch {
        Write-Warn "Git installer launch failed: $($_.Exception.Message)"
        Remove-Item $tmpFile -ErrorAction SilentlyContinue
        return $false
    }
    Remove-Item $tmpFile -ErrorAction SilentlyContinue

    Refresh-Path
    if (-not (Test-GitInstalled)) {
        # 安装器有时不会立刻刷新 PATH，按已知路径手动补一次
        $candidates = @(
            (Join-Path $env:LOCALAPPDATA 'Programs\Git\cmd'),
            (Join-Path $env:ProgramFiles 'Git\cmd')
        )
        foreach ($p in $candidates) {
            if (Test-Path (Join-Path $p 'git.exe')) {
                $env:Path = "$p;$env:Path"
                break
            }
        }
    }

    return Test-GitInstalled
}

# -- Main ---------------------------------------------------------------------
function Main {
    Write-Host ''
    Write-Host '+---------------------------------------------+' -ForegroundColor White
    Write-Host "|  $SKILL_LABEL -- Install                    |" -ForegroundColor White
    Write-Host '+---------------------------------------------+' -ForegroundColor White
    Write-Host ''

    # Step 1: Environment check
    Write-Step 'Step 1/4: Environment check'

    if (Test-NodeVersion) {
        Write-Info "Node.js $(Get-NodeVersionString) found"
    } else {
        $nodeCmd = Get-Command node -ErrorAction SilentlyContinue
        if ($nodeCmd) {
            Write-Warn "Node.js $(Get-NodeVersionString) is too old (need >= $NODE_MAJOR_MIN), upgrading..."
        } else {
            Write-Warn 'Node.js not found, installing...'
        }
        Install-NodeJS
        if (-not (Test-NodeVersion)) {
            Write-Err 'Node.js installation failed. Please install manually: https://nodejs.org/'
            return
        }
        Write-Info "Node.js $(Get-NodeVersionString) installed"
    }

    $npmCmd = Get-Command npm -ErrorAction SilentlyContinue
    if (-not $npmCmd) {
        Refresh-Path
        $npmCmd = Get-Command npm -ErrorAction SilentlyContinue
    }
    if (-not $npmCmd) {
        Write-Err 'npm not found (Node.js installation may be incomplete)'
        return
    }
    Write-Info 'npm ready'

    # Git for Windows: pre-install as a Bash fallback path for agent clients
    # whose PowerShell/cmd channel is unreliable. Failure here is non-fatal.
    if (Test-GitInstalled) {
        Write-Info 'Git for Windows already installed (Git Bash fallback ready)'
    } else {
        Write-Warn 'Git for Windows not found, installing as Bash fallback for agent clients...'
        $gitOk = $false
        try { $gitOk = Install-Git } catch { Write-Warn "Git install error: $($_.Exception.Message)" }
        if ($gitOk) {
            Write-Info 'Git for Windows installed (Git Bash fallback ready)'
        } else {
            Write-Warn 'Git for Windows install was skipped or failed; CLI install will continue.'
            Write-Host '  If your agent later fails to run PowerShell commands, install Git manually:' -ForegroundColor DarkGray
            Write-Host "  $GIT_INSTALLER_URL" -ForegroundColor DarkGray
        }
    }

    $currentRegistry = ''
    try { $currentRegistry = (npm config get registry 2>$null).Trim() } catch {}
    if ($currentRegistry -ne $NPM_MIRROR -and $currentRegistry -ne "$NPM_MIRROR/") {
        Write-Info 'Switching npm registry to China mirror for faster downloads...'
        npm config set registry $NPM_MIRROR
        Write-Info "npm registry set to $NPM_MIRROR"
    } else {
        Write-Info 'npm registry already set to China mirror'
    }

    # Step 2: Install CLI
    Write-Step "Step 2/4: Install $PKG_NAME"

    # 用打包时锁定的 PKG_VERSION，保证脚本与同批 dist/skill 行为对齐
    $installTarget = "$PKG_NAME@$PKG_VERSION"
    Write-Info "Running: npm install -g $installTarget"
    & npm install -g $installTarget
    if ($LASTEXITCODE -ne 0) { Write-Err "npm install -g $installTarget failed"; return }
    Write-Info "$installTarget installed"

    Write-Info 'Registering Skill to all AI platform global directories...'
    & $CLI_BIN init --global --force

    # Step 3: Configure API Key
    Write-Step 'Step 3/4: Configure API Key'
    Write-Host ''
    & $CLI_BIN login

    # Step 4: Done
    Write-Step 'Step 4/4: Complete'
    Write-Host ''
    Write-Host "  $SKILL_LABEL installed successfully!" -ForegroundColor Green
    Write-Host ''
    Write-Host '  Skill registered to these global directories (all AI assistants):'
    Write-Host '  ~/.cursor/skills/  ~/.claude/skills/  ~/.agents/skills/' -ForegroundColor DarkGray
    Write-Host '  ~/.gemini/skills/  ~/.codex/skills/   ~/.kilo/skills/' -ForegroundColor DarkGray
    Write-Host '  ~/.codeium/windsurf/skills/  ~/.config/opencode/skills/' -ForegroundColor DarkGray
    Write-Host '  ~/.openclaw/skills/  ~/.workbuddy/skills/' -ForegroundColor DarkGray
    Write-Host ''
    Write-Host "  Update CLI & Skill files: $CLI_BIN update"
    Write-Host ''
    if (Test-GitInstalled) {
        Write-Host '  Tip: if your agent client has trouble running PowerShell/cmd commands later,' -ForegroundColor DarkGray
        Write-Host '       open Git Bash and re-run the equivalent bash installer instead.' -ForegroundColor DarkGray
        Write-Host ''
    }
    Write-Info "Need help? Visit $WEB_BASE"
    Write-Host ''
}

Main
