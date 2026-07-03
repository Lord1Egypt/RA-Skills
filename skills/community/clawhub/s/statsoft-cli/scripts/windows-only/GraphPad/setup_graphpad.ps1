# setup_graphpad.ps1 — GraphPad Prism 检测与配置脚本
# 用法: powershell -ExecutionPolicy Bypass -File setup_graphpad.ps1

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



    Write-Lang "=== GraphPad Prism 检测与配置 ===" "=== GraphPad Prism Detection & Configuration ===" -Color Cyan

# 1. 检测 GraphPad 安装
$graphPadInstalled = $false
$graphPadPath = ""
$graphPadVersion = ""

# 典型安装路径
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
        Write-Lang "[OK] [CN] 检测到 GraphPad Prism $graphPadVersion : $graphPadPath" "[OK] [CN] 检测到 GraphPad Prism $graphPadVersion : $graphPadPath" -ForegroundColor Green
        Write-Lang "[OK] [EN] GraphPad Prism $graphPadVersion detected: $graphPadPath" "[OK] [EN] GraphPad Prism $graphPadVersion detected: $graphPadPath" -ForegroundColor Green
        break
    }
}

# 2. 如果未找到，尝试注册表
if (-not $graphPadInstalled) {
    Write-Lang "[!] [CN] 在常见路径未找到 GraphPad，尝试注册表..." "[!] [CN] 在常见路径未找到 GraphPad，尝试注册表..." -ForegroundColor Yellow
    Write-Lang "[!] [EN] GraphPad not found in common paths, trying registry..." "[!] [EN] GraphPad not found in common paths, trying registry..." -ForegroundColor Yellow
    
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
                        Write-Lang "[OK] [CN] 从注册表找到 GraphPad : $graphPadPath" "[OK] [CN] 从注册表找到 GraphPad : $graphPadPath" -ForegroundColor Green
                        Write-Lang "[OK] [EN] Found GraphPad from registry: $graphPadPath" "[OK] [EN] Found GraphPad from registry: $graphPadPath" -ForegroundColor Green
                        break
                    }
                }
            }
        }
    }
}

# 3. 如果仍未找到，提示用户（支持非交互回退）
if (-not $graphPadInstalled) {
    Write-Lang "[!] [CN] 未检测到 GraphPad Prism" "[!] [CN] 未检测到 GraphPad Prism" -ForegroundColor Yellow
    Write-Lang "[!] [EN] GraphPad Prism not detected" "[!] [EN] GraphPad Prism not detected" -ForegroundColor Yellow
    Write-Lang "请确认以下信息:" "Please confirm the following:" -Color Yellow
  Write-Lang "1. [CN] GraphPad Prism 是否已安装？" "[EN] Is GraphPad Prism installed?" -Color White
  Write-Lang "2. [CN] 安装路径是什么？" "[EN] What is the installation path?" -Color White

    # L-5: 非交互回退 — Read-Host 带超时
    $manualPath = $null
    try {
        $manualPath = Read-Host -Prompt "`n[CN] 请输入 GraphPad Prism 安装路径 / [EN] Enter GraphPad Prism installation path"
    } catch {
  Write-Lang "[!] [CN] 非交互模式，跳过手动输入" "[EN] Non-interactive mode, skipping manual input" -Color Yellow
    }

    if ($manualPath -and (Test-Path $manualPath)) {
        $exe = Join-Path $manualPath "prism.exe"
        if (Test-Path $exe) {
            $graphPadInstalled = $true
            $graphPadPath = $exe
            $graphPadVersion = ($manualPath -split 'Prism ')[-1].Trim()
            Write-Lang "[OK] [CN] 已确认 GraphPad Prism 路径: $graphPadPath" "[OK] [CN] 已确认 GraphPad Prism 路径: $graphPadPath" -ForegroundColor Green
            Write-Lang "[OK] [EN] GraphPad Prism path confirmed: $graphPadPath" "[OK] [EN] GraphPad Prism path confirmed: $graphPadPath" -ForegroundColor Green
        }
    }
}

# 4. 输出配置结果
if ($graphPadInstalled) {
    Write-Host "`n[CN] === 配置结果 ===" -ForegroundColor Cyan
    Write-Host "[EN] === Configuration Result ===" -ForegroundColor Cyan
    Write-Lang "GraphPad Prism 路径: $graphPadPath" "GraphPad Prism path: $graphPadPath" -Color White
    Write-Lang "版本: $graphPadVersion" "Version: $graphPadVersion" -Color White
    Write-Lang "环境变量: STATSOFT_GRAPHPAD_PATH=$graphPadPath" "Environment variable: STATSOFT_GRAPHPAD_PATH=$graphPadPath" -Color White
    
    # 设置环境变量
    [System.Environment]::SetEnvironmentVariable("STATSOFT_GRAPHPAD_PATH", $graphPadPath, "User")
    
    # 显示调用示例
    Write-Host "`n[CN] === 调用示例 ===" -ForegroundColor Cyan
    Write-Host "[EN] === Usage Examples ===" -ForegroundColor Cyan
    Write-Lang "打开 .pzfx 文件:" "Open .pzfx file:" -Color White
    Write-Host "  `"$graphPadPath`" `"C:\path\to\file.pzfx`""
    Write-Lang "" ""
    Write-Lang "Python 自动化 (prismWriter):" "Python automation (prismWriter):" -Color White
    Write-Host "  pip install prismwriter"
    Write-Host "  from prismwriter import PrismFile"
    Write-Host "  pf = PrismFile('template.pzfx')"
    Write-Host "  pf.save('output.pzfx')"
}
