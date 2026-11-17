# setup_spss.ps1 — SPSS Statistics 检测与配置（后台静默运行）
# 用法: powershell -ExecutionPolicy Bypass -File setup_spss.ps1 [-Version "26"]
# 注意：SPSS 26+ 版主程序为 stats.exe，无 spsswin.exe
# ⚠️ SETUP tool: DETECTION-ONLY. Detects installed software and prints manual configuration guidance. It does NOT write config.json or user environment variables.
# Language: auto-detects system locale — Chinese on zh-* systems, English otherwise

param(
    [string]$Version = "26"
)

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
    if ($script:isZH) {
        Write-Host $CN -ForegroundColor $Color
    } else {
        Write-Host $EN -ForegroundColor $Color
function Test-StatSoftReveal {
    return ($env:STATSOFT_REVEAL -eq '1')
}
    }
}

# ============================================================
# 1. Build search paths
# ============================================================
Write-Lang "=== SPSS Statistics 检测与配置 ===" "=== SPSS Statistics Detection & Configuration ===" -Color Cyan

$searchDirs = @()
$versions = @("26", "27", "28", "29", "30")
$patterns = @(
    "{0}:\Program Files\IBM\SPSS\Statistics\{1}",
    "{0}:\Program Files (x86)\IBM\SPSS\Statistics\{1}",
    "{0}:\SPSS\Statistics\{1}",
    "{0}:\IBM\SPSS\Statistics\{1}"
)

# Fixed system drives only (C:, D:) — no full host inventory of mounted volumes
$drives = @("C", "D")

foreach ($d in $drives) {
    foreach ($v in $versions) {
        foreach ($pat in $patterns) {
            $searchDirs += $pat -f $d, $v
        }
    }
}

# ============================================================
# 2. Detect SPSS
# ============================================================
$spssInstalled = $false
$spssPath = ""

foreach ($dir in $searchDirs) {
    $statsExe = Join-Path $dir "stats.exe"
    $spssExe = Join-Path $dir "spss.exe"

    if (Test-Path $statsExe -or Test-Path $spssExe) {
        $spssInstalled = $true
        $spssPath = if (Test-Path $statsExe) { $statsExe } elseif (Test-Path $spssExe) { $spssExe } else { "N/A" }
        if (Test-StatSoftReveal) {
            Write-Lang "检测到 SPSS Statistics ${Version}: $dir" "SPSS Statistics ${Version} detected: $dir" -Color Green
        } else {
            Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
        }
        break
    }
}

# ============================================================
# 3. Registry fallback
# ============================================================
if (-not $spssInstalled) {
    Write-Lang "在常见路径未找到 SPSS，尝试注册表..." "SPSS not found in common paths, trying registry..." -Color Yellow

    $regPaths = @(
        "HKLM:\SOFTWARE\IBM\SPSS",
        "HKLM:\SOFTWARE\Wow6432Node\IBM\SPSS",
        "HKLM:\SOFTWARE\IBM\SPSS Statistics",
        "HKLM:\SOFTWARE\Wow6432Node\IBM\SPSS Statistics",
        "HKCU:\SOFTWARE\IBM\SPSS",
        "HKCU:\SOFTWARE\Wow6432Node\IBM\SPSS"
    )

    foreach ($regPath in $regPaths) {
        if (Test-Path $regPath) {
            $props = Get-ItemProperty $regPath -ErrorAction SilentlyContinue
            foreach ($prop in $props.PSObject.Properties) {
                $val = $prop.Value
                if ($val -is [string] -and $val -like "*SPSS*Statistics*") {
                    $installDir = $val.TrimEnd("\")
                    if (Test-Path $installDir) {
                        $spssInstalled = $true
                        $statsExe = Join-Path $installDir "stats.exe"
                        $spssExe = Join-Path $installDir "spss.exe"
                        $spssPath = if (Test-Path $statsExe) { $statsExe } elseif (Test-Path $spssExe) { $spssExe } else { "N/A" }
                        if (Test-StatSoftReveal) {
                            Write-Lang "从注册表找到 SPSS: $installDir" "Found SPSS from registry: $installDir" -Color Green
                        } else {
                            Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
                        }
                        break
                    }
                }
            }
        }
        if ($spssInstalled) { break }
    }
}

# ============================================================
# 4. Manual input fallback
# ============================================================
if (-not $spssInstalled) {
    Write-Lang "未检测到 SPSS Statistics" "SPSS Statistics not found" -Color Yellow
    Write-Lang "请确认以下信息:" "Please confirm the following:" -Color Yellow
    Write-Lang "  1. SPSS Statistics 是否已安装?" "  1. Is SPSS Statistics installed?"
    Write-Lang "  2. 安装路径是什么?" "  2. What is the installation path?"
    if (Test-StatSoftReveal) {
        Write-Lang "  3. 版本号是多少? (默认参考 26)" "  3. Version number? (default 26)"
    } else {
        Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
    }
    Write-Lang "" ""
    Write-Lang "参考文档:" "Reference docs:" -Color Cyan
  Write-Lang "- Python: https:" "/www.ibm.com/docs/zh/spss-statistics/26.0.0?topic=facility-scripting-python-programming-language" -Color White
  Write-Lang "- Production Facility: https:" "/www.ibm.com/docs/zh/spss-statistics/26.0.0?topic=system-production-jobs" -Color White

    $manualPath = $null
    $promptText = if ($script:isZH) { "请输入 SPSS 安装路径" } else { "Enter SPSS installation path" }
    try {
        $manualPath = Read-Host -Prompt $promptText
    } catch {
        Write-Lang "非交互模式，跳过手动输入" "Non-interactive mode, skipping manual input" -Color Yellow
    }

    if ($manualPath -and (Test-Path $manualPath)) {
        $statsExe = Join-Path $manualPath "stats.exe"
        $spssExe = Join-Path $manualPath "spss.exe"
        $spssPath = if (Test-Path $statsExe) { $statsExe } elseif (Test-Path $spssExe) { $spssExe } else { "N/A" }
        $spssInstalled = $true
        if (Test-StatSoftReveal) {
            Write-Lang "已确认 SPSS 路径: $manualPath" "SPSS path confirmed: $manualPath" -Color Green
        } else {
            Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
        }
    }
}

# ============================================================
# 5. Detect SPSS built-in Python
# ============================================================
$pythonPath = "N/A"
$pythonVersion = "Unknown"
$useFString = $false

if ($spssInstalled) {
    $spssHome = Split-Path $spssPath -Parent

    $detectedVersion = "26"
    if ($spssHome -match "Statistics\\(\d+)") {
        $detectedVersion = $matches[1]
    }

    $pythonPaths = @(
        (Join-Path $spssHome "Python3\python.exe"),
        (Join-Path $spssHome "Python\python.exe"),
        (Join-Path $spssHome "Python3\python3.exe")
    )

    foreach ($pyPath in $pythonPaths) {
        if (Test-Path $pyPath) {
            $pythonPath = $pyPath
            if (Test-StatSoftReveal) {
                Write-Lang "检测到 SPSS 内置 Python: $pythonPath" "SPSS embedded Python detected: $pythonPath" -Color Green
            } else {
                Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
            }

            # Version verification launches the detected third-party binary.
            # It runs ONLY when explicitly opted in (STATSOFT_VERIFY=1); default
            # detection reports the path only and never executes the binary (SDI-4).
            if ($env:STATSOFT_VERIFY -eq '1') {
                try {
                    $versionOutput = & "$pyPath" --version 2>&1
                    $pythonVersion = $versionOutput.ToString().Trim()

                    if ($pythonVersion -match "3\.(\d+)") {
                        $minorVersion = [int]$matches[1]
                        if ($minorVersion -ge 8) {
                            $useFString = $true
                        }
                    }

                    if (Test-StatSoftReveal) {
                        Write-Lang "  Python 版本: $pythonVersion" "  Python version: $pythonVersion" -Color Cyan
                    } else {
                        Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
                    }
                    $fstringLabel = if ($script:isZH) {
                        if ($useFString) { "✅ 支持" } else { "❌ 不支持（请用 %s 或 .format()）" }
                    } else {
                        if ($useFString) { "✅ supported" } else { "❌ not supported (use %s or .format())" }
                    }
                    Write-Lang "  f-string 支持: $fstringLabel" "  f-string support: $fstringLabel" -Color Cyan
                } catch {
                    if (Test-StatSoftReveal) {
                        Write-Lang "  无法获取 Python version" "  Unable to get Python version" -Color Yellow
                    } else {
                        Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
                    }
                }
            } else {
                Write-Lang "  （默认仅检测路径；设置 STATSOFT_VERIFY=1 可查询版本与 f-string 支持）" "  (Detection-only by default; set STATSOFT_VERIFY=1 to query version/f-string support)" -Color Gray
            }
            break
        }
    }

    if ($pythonPath -eq "N/A") {
        Write-Lang "未找到 SPSS 内置 Python" "SPSS embedded Python not found" -Color Yellow
        Write-Lang "  请确认 SPSS 安装时是否包含了 Python plugin" "  Please confirm Python plugin was installed with SPSS" -Color Yellow
    }
}

# ============================================================
# 6. Check Python plugin directory
# ============================================================
if ($spssInstalled) {
    Write-Lang "" ""
    Write-Lang "=== 检查 Python 插件 ===" "=== Checking Python Plugin ===" -Color Cyan

    $pluginDir = Split-Path $spssPath -Parent
    $pythonPlugin = Join-Path $pluginDir "python"

    if (Test-Path $pythonPlugin) {
        if (Test-StatSoftReveal) {
            Write-Lang "Python 插件目录存在: $pythonPlugin" "Python plugin directory exists: $pythonPlugin" -Color Green
        } else {
            Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
        }
    } else {
        Write-Lang "Python 插件可能未安装" "Python plugin may not be installed" -Color Yellow
        Write-Lang "  请通过 SPSS 安装包添加 'Integration Plug-in for Python'" "  Add 'Integration Plug-in for Python' via SPSS installer" -Color Yellow
    }
}

# ============================================================
# 7. Output configuration results
# ============================================================
if ($spssInstalled) {
    $statsComPath = Join-Path (Split-Path $spssPath -Parent) "stats.com"
    $statsComExists = Test-Path $statsComPath

    Write-Lang "" ""
    Write-Lang "=== 配置结果 ===" "=== Configuration Result ===" -Color Cyan
    if (Test-StatSoftReveal) {
        Write-Lang "SPSS 安装目录: $spssHome" "SPSS installation directory: $spssHome"
    } else {
        Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
    }

    $comLabel = if ($statsComExists) { $statsComPath } else { "not found" }
    if (Test-StatSoftReveal) {
        Write-Lang "  控制台版 (stats.com): $comLabel" "  Console version (stats.com): $comLabel"
    } else {
        Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
    }
    if (Test-StatSoftReveal) {
        Write-Lang "  GUI 版 (stats.exe): $spssPath" "  GUI version (stats.exe): $spssPath"
    } else {
        Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
    }
    if (Test-StatSoftReveal) {
        Write-Lang "  内置 Python 路径: $pythonPath" "  Embedded Python path: $pythonPath"
    } else {
        Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
    }
    if (Test-StatSoftReveal) {
        Write-Lang "  Python 版本: $pythonVersion" "  Python version: $pythonVersion"
    } else {
        Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
    }

    $fstringShort = if ($useFString) { "✅ supported" } else { "❌ not supported" }
    Write-Lang "  f-string: $fstringShort" "  f-string: $fstringShort"

    # ============================================================
    # 8. Persistence guidance (DETECTION-ONLY)
    # ============================================================
    # This setup script is DETECTION-ONLY: it reports the detected paths
    # and prints manual configuration guidance. It does NOT modify any
    # persistent state (no env-var writes, no config.json writes).
    Write-Lang "" ""
    # This script is DETECTION-ONLY: it does NOT write env vars or config.json.
    # Persistence is confined to config.json and requires explicit opt-in:
    # re-run with STATSOFT_AUTO_WRITE=1 (non-interactive) or STATSOFT_CONFIRM=1
    # (interactive y/N). The runner auto-detects the paths above by default.
    Write-Lang "`n本脚本仅做检测，不写入任何配置（环境变量或 config.json）。" "`nDetection-only: no configuration is written (neither env vars nor config.json)." -Color Yellow
    Write-Lang "如需持久化，请以 opt-in 方式写入 config.json：STATSOFT_AUTO_WRITE=1 或 STATSOFT_CONFIRM=1" "To persist, write config.json with explicit opt-in: STATSOFT_AUTO_WRITE=1 or STATSOFT_CONFIRM=1" -Color Gray
    Write-Lang "（运行器默认按上述路径自动检测，无需手动设置环境变量）" "  (The runner auto-detects these paths by default — no manual env var needed)" -Color Gray

    # ============================================================
    # 9. Show usage examples
    # ============================================================
    Write-Lang "" ""
    Write-Lang "=== 调用示例 ===" "=== Usage Examples ===" -Color Cyan

    Write-Lang "1. 方案1 (首选, 万无一失):" "1. Method 1 (preferred, foolproof):"
    if ($statsComExists) {
        if (Test-StatSoftReveal) {
            Write-Host "   `"$statsComPath`" -production silent -nologo `"job.spj`""
        } else {
            Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
        }
    } else {
        Write-Lang "   # stats.com 未找到，使用 stats.exe (可能有闪屏)" "   # stats.com not found, use stats.exe (may flash)"
        if (Test-StatSoftReveal) {
            Write-Host "   `"$spssPath`" -production silent -nologo `"job.spj`""
        } else {
            Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
        }
    }
    Write-Lang "" ""

    Write-Lang "2. 方案2 (Python 备用, 无闪屏):" "2. Method 2 (Python backup, no splash):"
    if (Test-StatSoftReveal) {
        Write-Host "   `"$pythonPath`" spss_helper.py run-internal `"syntax.sps`""
    } else {
        Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
    }
  Write-Lang "$(if ($script:isZH) { '⚠️ 只能跑纯分析语法（不能含 OUTPUT SAVE/EXPORT/HOST COMMAND）' } else { 'WARNING: Pure analysis syntax only (no OUTPUT SAVE/EXPORT/HOST COMMAND)' })" -Color White
    Write-Lang "" ""

    Write-Lang "3. 方案3 (最后备选, 可能有闪屏):" "3. Method 3 (last resort, may flash):"
    if (Test-StatSoftReveal) {
        Write-Host "   `"$spssPath`" -production `"job.spj`" silent -nologo"
    } else {
        Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
    }
}
