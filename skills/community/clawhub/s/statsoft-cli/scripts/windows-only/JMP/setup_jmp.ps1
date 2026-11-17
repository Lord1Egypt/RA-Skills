# setup_jmp.ps1 — JMP detection and configuration script
# Usage: powershell -ExecutionPolicy Bypass -File setup_jmp.ps1
# ⚠️ SETUP tool: DETECTION-ONLY. Detects installed software and prints manual configuration guidance. It does NOT write config.json or user environment variables.

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
function Test-StatSoftReveal {
    return ($env:STATSOFT_REVEAL -eq '1')
}
function Test-StatSoftVerify {
    return ($env:STATSOFT_VERIFY -eq '1')
}

Write-Lang "=== JMP 检测与配置 ===" "=== JMP Detection & Configuration ===" -Color Cyan

# 1. Detect JMP installation
$jmpInstalled = $false
$jmpPath = ""
$jmpVersion = ""

# Typical installation paths
$commonPaths = @(
    "C:\Program Files\JMP\16",
    "C:\Program Files\JMP\15",
    "C:\Program Files\JMP\14",
    "C:\Program Files (x86)\JMP\16",
    "D:\JMP\16"
)

foreach ($dir in $commonPaths) {
    $exe = Join-Path $dir "JMP.exe"
    if (Test-Path $exe) {
        $jmpInstalled = $true
        $jmpPath = $exe
        $jmpVersion = $dir -replace ".*JMP\\", ''
        if (Test-StatSoftReveal) {
            Write-Lang "检测到 JMP $jmpVersion : $jmpPath" "Detected JMP $jmpVersion : $jmpPath" -ForegroundColor Green
        } else {
            Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
        }
        break
    }
}

# 2. If not found, try the registry
if (-not $jmpInstalled) {
    Write-Lang "常见路径未找到 JMP，尝试注册表..." "JMP not found in common paths, trying registry..." -ForegroundColor Yellow
    $regPaths = @(
        "HKLM:\SOFTWARE\JMP",
        "HKLM:\SOFTWARE\Wow6432Node\JMP"
    )
    foreach ($regPath in $regPaths) {
        if (Test-Path $regPath) {
            $jmpKey = Get-ChildItem $regPath -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($jmpKey) {
                $installDir = (Get-ItemProperty $jmpKey.PSPath -ErrorAction SilentlyContinue).InstallLocation
                if ($installDir -and (Test-Path $installDir)) {
                    $exe = Join-Path $installDir "JMP.exe"
                    if (Test-Path $exe) {
                        $jmpInstalled = $true
                        $jmpPath = $exe
                        $jmpVersion = $installDir -replace ".*JMP\\", ''
                        if (Test-StatSoftReveal) {
                            Write-Lang "从注册表找到 JMP : $jmpPath" "Found JMP from registry: $jmpPath" -ForegroundColor Green
                        } else {
                            Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
                        }
                        break
                    }
                }
            }
        }
    }
}

# 3. If still not found, prompt the user (supports non-interactive fallback)
if (-not $jmpInstalled) {
    Write-Lang "未检测到 JMP" "JMP not detected" -ForegroundColor Yellow
    Write-Lang "请确认以下信息:" "Please confirm the following:" -Color Yellow
    Write-Lang "1. JMP 是否已安装？" "1. Is JMP installed?" -Color White
    Write-Lang "2. 安装路径是什么？" "2. What is the installation path?" -Color White

    # Non-interactive fallback — Read-Host wrapped in try/catch
    $manualPath = $null
    try {
        $manualPath = Read-Host -Prompt (if ($script:isZH){"`n请输入 JMP 安装路径（例如 C:\Program Files\JMP\16）"}else{"`nEnter JMP installation path (e.g. C:\Program Files\JMP\16)"})
    } catch {
        Write-Lang "非交互模式，跳过手动输入" "Non-interactive mode, skipping manual input" -Color Yellow
    }

    if ($manualPath -and (Test-Path $manualPath)) {
        $exe = Join-Path $manualPath "JMP.exe"
        if (Test-Path $exe) {
            $jmpInstalled = $true
            $jmpPath = $exe
            $jmpVersion = $manualPath -replace ".*JMP\\", ''
            if (Test-StatSoftReveal) {
                Write-Lang "已确认 JMP 路径: $jmpPath" "JMP path confirmed: $jmpPath" -ForegroundColor Green
            } else {
                Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
            }
        }
    }
}

# 4. Output configuration result
if ($jmpInstalled) {
    Write-Lang "`n=== 配置结果 ===" "`n=== Configuration Result ===" -ForegroundColor Cyan
    if (Test-StatSoftReveal) {
        Write-Lang "JMP 路径: $jmpPath" "JMP path: $jmpPath" -Color White
    } else {
        Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
    }
    if (Test-StatSoftReveal) {
        Write-Lang "版本: $jmpVersion" "Version: $jmpVersion" -Color White
    } else {
        Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
    }

    # This setup script is DETECTION-ONLY: it reports the detected path and
    # prints manual configuration guidance. It does NOT modify any persistent
    # state (no env-var writes, no config.json writes) — the runner
    # statsoft-jmp.ps1 auto-detects JMP from the common paths above.
    # This setup script is DETECTION-ONLY: it does NOT write env vars or
    # config.json. The runner statsoft-jmp.ps1 auto-detects JMP from the common
    # paths above by default; if a custom path must be pinned, persist it to
    # config.json with explicit opt-in (STATSOFT_AUTO_WRITE=1 / STATSOFT_CONFIRM=1)
    # — NOT a shell environment variable.
    Write-Lang "`n本脚本仅做检测，不写入任何配置（环境变量或 config.json）。" "`nDetection-only: no configuration is written (neither env vars nor config.json)." -ForegroundColor Yellow
    Write-Lang "运行器默认按上述路径自动检测，无需手动设置环境变量。" "  The runner auto-detects these paths by default — no manual env var needed." -Color Gray
    Write-Lang "如需固定自定义路径，请以 opt-in 写入 config.json（STATSOFT_AUTO_WRITE=1 / STATSOFT_CONFIRM=1）。" "  To pin a custom path, persist it to config.json with opt-in (STATSOFT_AUTO_WRITE=1 / STATSOFT_CONFIRM=1)." -Color Gray

    # Show usage examples
    Write-Lang "`n=== 调用示例 ===" "`n=== Usage Examples ===" -ForegroundColor Cyan
    Write-Lang "运行 JSL 脚本:" "Run JSL script:" -Color White
    if (Test-StatSoftReveal) {
        Write-Host "  `"$jmpPath`" script.jsl"
    } else {
        Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
    }
    Write-Lang "" ""
    Write-Lang "静默模式:" "Silent mode:" -Color White
    if (Test-StatSoftReveal) {
        Write-Host "  `"$jmpPath`" -jsl script.jsl"
    } else {
        Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
    }
    Write-Lang "" ""
}
