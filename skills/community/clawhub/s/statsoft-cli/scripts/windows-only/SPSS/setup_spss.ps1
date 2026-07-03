# setup_spss.ps1 — SPSS Statistics 检测与配置（后台静默运行）
# 用法: powershell -ExecutionPolicy Bypass -File setup_spss.ps1 [-Version "26"]
# 注意：SPSS 26+ 版主程序为 stats.exe，无 spsswin.exe
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

$drives = Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Used -gt 0 } | Select-Object -ExpandProperty Name

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
        Write-Lang "检测到 SPSS Statistics ${Version}: $dir" "SPSS Statistics ${Version} detected: $dir" -Color Green
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
                        Write-Lang "从注册表找到 SPSS: $installDir" "Found SPSS from registry: $installDir" -Color Green
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
    Write-Lang "  3. 版本号是多少? (默认参考 26)" "  3. Version number? (default 26)"
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
        Write-Lang "已确认 SPSS 路径: $manualPath" "SPSS path confirmed: $manualPath" -Color Green
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
            Write-Lang "检测到 SPSS 内置 Python: $pythonPath" "SPSS embedded Python detected: $pythonPath" -Color Green

            try {
                $versionOutput = & $pyPath --version 2>&1
                $pythonVersion = $versionOutput.ToString().Trim()

                if ($pythonVersion -match "3\.(\d+)") {
                    $minorVersion = [int]$matches[1]
                    if ($minorVersion -ge 8) {
                        $useFString = $true
                    }
                }

                Write-Lang "  Python 版本: $pythonVersion" "  Python version: $pythonVersion" -Color Cyan
                $fstringLabel = if ($useFString) { "✅ 支持 / supported" } else { "❌ 不支持 / not supported (use %s or .format())" }
                Write-Lang "  f-string 支持: $fstringLabel" "  f-string support: $fstringLabel" -Color Cyan
            } catch {
                Write-Lang "  无法获取 Python version" "  Unable to get Python version" -Color Yellow
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
        Write-Lang "Python 插件目录存在: $pythonPlugin" "Python plugin directory exists: $pythonPlugin" -Color Green
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
    Write-Lang "=== 配置结果 / Configuration Result ===" "=== Configuration Result ===" -Color Cyan
    Write-Lang "SPSS 安装目录: $spssHome" "SPSS installation directory: $spssHome"

    $comLabel = if ($statsComExists) { $statsComPath } else { "not found" }
    Write-Lang "  控制台版 (stats.com): $comLabel" "  Console version (stats.com): $comLabel"
    Write-Lang "  GUI 版 (stats.exe): $spssPath" "  GUI version (stats.exe): $spssPath"
    Write-Lang "  内置 Python 路径: $pythonPath" "  Embedded Python path: $pythonPath"
    Write-Lang "  Python 版本: $pythonVersion" "  Python version: $pythonVersion"

    $fstringShort = if ($useFString) { "✅ supported" } else { "❌ not supported" }
    Write-Lang "  f-string: $fstringShort" "  f-string: $fstringShort"

    # ============================================================
    # 8. Set environment variables
    # ============================================================
    Write-Lang "" ""
    Write-Lang "即将设置用户环境变量:" "About to set user environment variables:" -Color Yellow
    Write-Host "  STATSOFT_SPSS_PATH=$spssHome"
  Write-Lang "STATSOFT_SPSS_COM=$(if ($statsComExists) { $statsComPath } else { 'N" "A' })" -Color White
    Write-Host "  STATSOFT_SPSS_PYTHON=$pythonPath"
    Write-Host "  STATSOFT_SPSS_FSTRING=$useFString"

    $confirm = "Y"
    try {
        $promptText = if ($script:isZH) { "确认设置环境变量? (y/N)" } else { "Confirm setting env vars? (y/N)" }
        $confirm = Read-Host $promptText
    } catch {
        Write-Lang "非交互模式，自动应用" "Non-interactive mode, auto-applying" -Color Yellow
    }

    if ($confirm -eq 'y' -or $confirm -eq 'Y') {
        [System.Environment]::SetEnvironmentVariable("STATSOFT_SPSS_PATH", $spssHome, "User")
        [System.Environment]::SetEnvironmentVariable("STATSOFT_SPSS_COM", $(if ($statsComExists) { $statsComPath } else { "" }), "User")
        [System.Environment]::SetEnvironmentVariable("STATSOFT_SPSS_PYTHON", $pythonPath, "User")
        [System.Environment]::SetEnvironmentVariable("STATSOFT_SPSS_FSTRING", $useFString.ToString(), "User")
        Write-Lang "环境变量已设置" "Environment variables set" -Color Green
    } else {
        Write-Lang "跳过环境变量设置" "Skipping env var setup" -Color Yellow
    }

    # ============================================================
    # 9. Show usage examples
    # ============================================================
    Write-Lang "" ""
    Write-Lang "=== 调用示例 / Usage Examples ===" "=== Usage Examples ===" -Color Cyan

    Write-Lang "1. 方案1 (首选, 万无一失):" "1. Method 1 (preferred, foolproof):"
    if ($statsComExists) {
        Write-Host "   `"$statsComPath`" -production silent -nologo `"job.spj`""
    } else {
        Write-Lang "   # stats.com 未找到，使用 stats.exe (可能有闪屏)" "   # stats.com not found, use stats.exe (may flash)"
        Write-Host "   `"$spssPath`" -production silent -nologo `"job.spj`""
    }
    Write-Lang "" ""

    Write-Lang "2. 方案2 (Python 备用, 无闪屏):" "2. Method 2 (Python backup, no splash):"
    Write-Host "   `"$pythonPath`" spss_helper.py run-internal `"syntax.sps`""
  Write-Lang "$(if ($script:isZH) { '⚠️ 只能跑纯分析语法（不能含 OUTPUT SAVE" "EXPORT/HOST COMMAND）' } else { 'WARNING: Pure analysis syntax only (no OUTPUT SAVE/EXPORT/HOST COMMAND)' })" -Color White
    Write-Lang "" ""

    Write-Lang "3. 方案3 (最后备选, 可能有闪屏):" "3. Method 3 (last resort, may flash):"
    Write-Host "   `"$spssPath`" -production `"job.spj`" silent -nologo"
}
