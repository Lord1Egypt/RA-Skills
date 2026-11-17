# setup_graphpad.ps1 — GraphPad Prism detection and configuration script
# Usage: powershell -ExecutionPolicy Bypass -File setup_graphpad.ps1
# ⚠️ SETUP tool: DETECTION-ONLY. Detects installed software and prints manual configuration guidance. It does NOT write config.json or user environment variables. GUI-only software: detection/launch only, no CLI batch.

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

Write-Lang "=== GraphPad Prism 检测与配置 ===" "=== GraphPad Prism Detection & Configuration ===" -Color Cyan

# 1. Detect GraphPad installation
$graphPadInstalled = $false
$graphPadPath = ""
$graphPadVersion = ""

# Typical installation paths
$commonPaths = @(
    "C:\Program Files\GraphPad\Prism 9",
    "C:\Program Files\GraphPad\Prism 10",
    "C:\Program Files\GraphPad\Prism 8",
    "C:\Program Files\GraphPad\Prism 7",
    "C:\Program Files (x86)\GraphPad\Prism 9",
    "C:\Program Files (x86)\GraphPad\Prism 8",
    "D:\GraphPad\Prism 9",
    "D:\GraphPad\Prism 8"
)

foreach ($dir in $commonPaths) {
    $exe = Join-Path $dir "prism.exe"
    if (Test-Path $exe) {
        $graphPadInstalled = $true
        $graphPadPath = $exe
        $graphPadVersion = ($dir -split 'Prism ')[-1].Trim()
        if (Test-StatSoftReveal) {
            Write-Lang "检测到 GraphPad Prism $graphPadVersion : $graphPadPath" "Detected GraphPad Prism $graphPadVersion : $graphPadPath" -ForegroundColor Green
        } else {
            Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
        }
        break
    }
}

# 2. If not found, try the registry
if (-not $graphPadInstalled) {
    Write-Lang "常见路径未找到 GraphPad，尝试注册表..." "GraphPad not found in common paths, trying registry..." -ForegroundColor Yellow
    $regPaths = @(
        "HKLM:\SOFTWARE\GraphPad",
        "HKLM:\SOFTWARE\Wow6432Node\GraphPad"
    )
    foreach ($regPath in $regPaths) {
        if (Test-Path $regPath) {
            $graphPadKey = Get-ChildItem $regPath -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($graphPadKey) {
                $installDir = (Get-ItemProperty $graphPadKey.PSPath -ErrorAction SilentlyContinue).InstallLocation
                if ($installDir -and (Test-Path $installDir)) {
                    $exe = Join-Path $installDir "prism.exe"
                    if (Test-Path $exe) {
                        $graphPadInstalled = $true
                        $graphPadPath = $exe
                        $graphPadVersion = ($installDir -split 'Prism ')[-1].Trim()
                        if (Test-StatSoftReveal) {
                            Write-Lang "从注册表找到 GraphPad : $graphPadPath" "Found GraphPad from registry: $graphPadPath" -ForegroundColor Green
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
if (-not $graphPadInstalled) {
    Write-Lang "未检测到 GraphPad Prism" "GraphPad Prism not detected" -ForegroundColor Yellow
    Write-Lang "请确认以下信息:" "Please confirm the following:" -Color Yellow
    Write-Lang "1. GraphPad Prism 是否已安装？" "1. Is GraphPad Prism installed?" -Color White
    Write-Lang "2. 安装路径是什么？" "2. What is the installation path?" -Color White

    # Non-interactive fallback — Read-Host wrapped in try/catch
    $manualPath = $null
    try {
        $manualPath = Read-Host -Prompt (if ($script:isZH){"`n请输入 GraphPad Prism 安装路径"}else{"`nEnter GraphPad Prism installation path"})
    } catch {
        Write-Lang "非交互模式，跳过手动输入" "Non-interactive mode, skipping manual input" -Color Yellow
    }

    if ($manualPath -and (Test-Path $manualPath)) {
        $exe = Join-Path $manualPath "prism.exe"
        if (Test-Path $exe) {
            $graphPadInstalled = $true
            $graphPadPath = $exe
            $graphPadVersion = ($manualPath -split 'Prism ')[-1].Trim()
            if (Test-StatSoftReveal) {
                Write-Lang "已确认 GraphPad Prism 路径: $graphPadPath" "GraphPad Prism path confirmed: $graphPadPath" -ForegroundColor Green
            } else {
                Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
            }
        }
    }
}

# 4. Output configuration result
if ($graphPadInstalled) {
    Write-Lang "`n=== 配置结果 ===" "`n=== Configuration Result ===" -ForegroundColor Cyan
    if (Test-StatSoftReveal) {
        Write-Lang "GraphPad Prism 路径: $graphPadPath" "GraphPad Prism path: $graphPadPath" -Color White
    } else {
        Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
    }
    if (Test-StatSoftReveal) {
        Write-Lang "版本: $graphPadVersion" "Version: $graphPadVersion" -Color White
    } else {
        Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
    }
    # This setup script is DETECTION-ONLY: it reports the detected path and
    # prints manual configuration guidance. It does NOT modify any persistent
    # state (no env-var writes, no config.json writes). The runner
    # statsoft-graphpad.ps1 auto-detects GraphPad Prism from the paths above by
    # default, so no manual persistence is required. If a custom path must be
    # pinned, persist it to config.json with explicit opt-in
    # (STATSOFT_AUTO_WRITE=1 or STATSOFT_CONFIRM=1) — NOT a shell environment
    # variable.
    Write-Lang "`n本脚本仅做检测，不写入任何配置（环境变量或 config.json）。" "`nDetection-only: no configuration is written (neither env vars nor config.json)." -ForegroundColor Yellow
    Write-Lang "运行器默认按上述路径自动检测，无需手动设置环境变量。" "  The runner auto-detects these paths by default — no manual env var needed." -Color Gray
    Write-Lang "如需固定自定义路径，请以 opt-in 写入 config.json（STATSOFT_AUTO_WRITE=1 / STATSOFT_CONFIRM=1）。" "  To pin a custom path, persist it to config.json with opt-in (STATSOFT_AUTO_WRITE=1 / STATSOFT_CONFIRM=1)." -Color Gray

    # Show usage examples
    Write-Lang "`n=== 调用示例 ===" "`n=== Usage Examples ===" -ForegroundColor Cyan
    Write-Lang "打开 .pzfx 文件:" "Open .pzfx file:" -Color White
    if (Test-StatSoftReveal) {
        Write-Host "  `"$graphPadPath`" `"C:\path\to\file.pzfx`""
    } else {
        Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
    }
    Write-Lang "" ""
    Write-Lang "Python 自动化 (prismWriter):" "Python automation (prismWriter):" -Color White
    Write-Host "  pip install prismwriter"
    Write-Host "  from prismwriter import PrismFile"
    Write-Host "  pf = PrismFile('template.pzfx')"
    Write-Host "  pf.save('output.pzfx')"
}
