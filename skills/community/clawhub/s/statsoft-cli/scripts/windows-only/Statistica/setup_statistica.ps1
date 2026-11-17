# Statistica detection & manual-guidance script
# Supported platform: Windows-only
#
# IMPORTANT (SkillSpector SDI-1 / SDI-4 fix):
# Statistica is a GUI-oriented statistical package. This script is strictly
# DETECTION-ONLY + manual-launch guidance. It performs NO persistent write and
# never modifies config.json. Any execution of Statistica (e.g. running an SVB
# script) is handled by statsoft-statistica.ps1, which requires explicit user
# confirmation via the Test-UserAuthorizedToRun gate.

# ============================================================
# Language Detection
# ============================================================
$systemLang = [System.Globalization.CultureInfo]::CurrentUICulture.Name
$script:isZH = $systemLang.StartsWith("zh")

function Write-Lang {
    param(
        [string]$CN,
        [string]$EN,
        [System.ConsoleColor]$Color = "White"
    )
    if ($script:isZH) { Write-Host $CN -ForegroundColor $Color }
    else { Write-Host $EN -ForegroundColor $Color }
}

# Color helpers (language-aware: CN / EN)
function Write-Info {
    param([string]$CN, [string]$EN)
    if ($script:isZH) { Write-Host "[INFO] $CN" -ForegroundColor Green }
    else { Write-Host "[INFO] $EN" -ForegroundColor Green }
}
function Write-Warn {
    param([string]$CN, [string]$EN)
    if ($script:isZH) { Write-Host "[WARN] $CN" -ForegroundColor Yellow }
    else { Write-Host "[WARN] $EN" -ForegroundColor Yellow }
}
function Write-Error {
    param([string]$CN, [string]$EN)
    if ($script:isZH) { Write-Host "[ERROR] $CN" -ForegroundColor Red }
    else { Write-Host "[ERROR] $EN" -ForegroundColor Red }
}

# Detect Statistica
function Detect-Statistica {
    Write-Info "检测 Statistica..." "Detecting Statistica..."

    $possiblePaths = @(
        "C:\Program Files\StatSoft\Statistica 13\Statistica.exe",
        "C:\Program Files\StatSoft\Statistica 12\Statistica.exe",
        "C:\Program Files (x86)\StatSoft\Statistica 13\Statistica.exe",
        "C:\Program Files (x86)\StatSoft\Statistica 12\Statistica.exe",
        "C:\Program Files\Statistica\Statistica.exe",
        "C:\Program Files (x86)\Statistica\Statistica.exe"
    )

    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            Write-Info "找到 Statistica: $path" "Found Statistica: $path"
            return $path
        }
    }

    # Check PATH
    $statisticaInPath = Get-Command "Statistica.exe" -ErrorAction SilentlyContinue
    if ($statisticaInPath) {
        Write-Info "在 PATH 中找到 Statistica: $($statisticaInPath.Source)" "Found Statistica in PATH: $($statisticaInPath.Source)"
        return $statisticaInPath.Source
    }

    Write-Warn "未找到 Statistica" "Statistica not found"
    return $null
}

# Verify Statistica (read-only)
function Verify-Statistica {
    param([string]$StatisticaPath)

    Write-Info "验证 Statistica..." "Verifying Statistica..."

    if (-not (Test-Path $StatisticaPath)) {
        Write-Error "Statistica 可执行文件不存在: $StatisticaPath" "Statistica executable not found: $StatisticaPath"
        return $false
    }

    try {
        $versionInfo = (Get-Item $StatisticaPath).VersionInfo
        Write-Info "Statistica 版本: $($versionInfo.ProductVersion)" "Statistica version: $($versionInfo.ProductVersion)"
        Write-Info "Statistica 验证成功" "Statistica verification successful"
        return $true
    }
    catch {
        Write-Warn "无法获取 Statistica 版本信息: $_" "Unable to get Statistica version info: $_"
        return $false
    }
}

# Print manual guidance (no config write)
function Print-ManualGuidance {
    param([string]$StatisticaPath)

    Write-Info ""
    Write-Info "══════════════════════════════════════════════" "══════════════════════════════════════════════"
    Write-Info "📋 检测完成 — 本脚本仅检测、不写入任何配置" "Detection complete — this script is detection-only, writes nothing"
    Write-Info "══════════════════════════════════════════════" "══════════════════════════════════════════════"
    Write-Info ""
    Write-Info "⚠️ 手动启动与执行指引" "Manual launch & execution guidance:"
    Write-Info "  • GUI: 直接打开 Statistica（图形界面）" "  • GUI: open Statistica GUI directly"
    Write-Info "  • 运行 SVB 脚本（需显式确认）" "  • Run an SVB script (requires explicit confirmation):"
    Write-Info "      `"$StatisticaPath`" /run `"your-script.svb`""
    Write-Info "  • 本技能不自动持久化 Statistica 配置" "  • This skill does NOT persist Statistica config"
    Write-Info "  • 如需执行，请使用受控的运行器（会要求确认）" "  • To execute, use the guarded runner (asks for confirmation):"
    Write-Info "      statsoft-statistica run your-script.svb"
    Write-Info ""
}

# Main
function Main {
    Write-Info "开始 Statistica 检测（仅检测，不写入配置）..." "Starting Statistica detection (detection-only, no config write)..."

    $statisticaPath = Detect-Statistica

    if (-not $statisticaPath) {
        Write-Warn "未找到 Statistica，请手动指定路径" "Statistica not found, please specify path manually"

        # Non-interactive fallback — Read-Host with timeout
        $userPath = $null
        try {
            $userPath = Read-Host (if ($script:isZH) { "请输入 Statistica 安装路径（按 Enter 跳过）" } else { "Enter Statistica installation path (press Enter to skip)" })
        }
        catch {
            Write-Lang "[!] 非交互模式，跳过手动输入" "[!] Non-interactive mode, skipping manual input" -Color Yellow
        }

        if ($userPath) {
            $statisticaPath = $userPath
        }
        else {
            Write-Error "未配置 Statistica" "Statistica not configured"
            Write-Info "提示: 本脚本仅检测，不写入配置。如需执行请手动启动 Statistica 或使用受控运行器。" "Hint: this script only detects; it writes no config. To execute, launch Statistica manually or use the guarded runner."
            exit 1
        }
    }

    if (-not (Verify-Statistica $statisticaPath)) {
        Write-Error "Statistica 验证失败" "Statistica verification failed"
        exit 1
    }

    Print-ManualGuidance -StatisticaPath $statisticaPath
    return 0
}

# Run main
Main
