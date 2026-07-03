# setup_jmp.ps1 — JMP 检测与配置脚本
# 用法: powershell -ExecutionPolicy Bypass -File setup_jmp.ps1

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



    Write-Lang "=== JMP 检测与配置 ===" "=== JMP Detection & Configuration ===" -Color Cyan

# 1. 检测 JMP 安装
$jmpInstalled = $false
$jmpPath = ""
$jmpVersion = ""

# 典型安装路径
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
        Write-Lang "[OK] [CN] 检测到 JMP $jmpVersion : $jmpPath" "[OK] [CN] 检测到 JMP $jmpVersion : $jmpPath" -ForegroundColor Green
        Write-Lang "[OK] [EN] JMP $jmpVersion detected: $jmpPath" "[OK] [EN] JMP $jmpVersion detected: $jmpPath" -ForegroundColor Green
        break
    }
}

# 2. 如果未找到，尝试注册表
if (-not $jmpInstalled) {
    Write-Lang "[!] [CN] 在常见路径未找到 JMP，尝试注册表..." "[!] [CN] 在常见路径未找到 JMP，尝试注册表..." -ForegroundColor Yellow
    Write-Lang "[!] [EN] JMP not found in common paths, trying registry..." "[!] [EN] JMP not found in common paths, trying registry..." -ForegroundColor Yellow
    
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
                        Write-Lang "[OK] [CN] 从注册表找到 JMP : $jmpPath" "[OK] [CN] 从注册表找到 JMP : $jmpPath" -ForegroundColor Green
                        Write-Lang "[OK] [EN] Found JMP from registry: $jmpPath" "[OK] [EN] Found JMP from registry: $jmpPath" -ForegroundColor Green
                        break
                    }
                }
            }
        }
    }
}

# 3. 如果仍未找到，提示用户（支持非交互回退）
if (-not $jmpInstalled) {
    Write-Lang "[!] [CN] 未检测到 JMP" "[!] [CN] 未检测到 JMP" -ForegroundColor Yellow
    Write-Lang "[!] [EN] JMP not detected" "[!] [EN] JMP not detected" -ForegroundColor Yellow
    Write-Lang "请确认以下信息:" "Please confirm the following:" -Color Yellow
  Write-Lang "1. [CN] JMP 是否已安装？" "[EN] Is JMP installed?" -Color White
  Write-Lang "2. [CN] 安装路径是什么？" "[EN] What is the installation path?" -Color White

    # L-5: 非交互回退 — Read-Host 带超时
    $manualPath = $null
    try {
        $manualPath = Read-Host -Prompt "`n[CN] 请输入 JMP 安装路径（例如 C:\Program Files\JMP\16）/ [EN] Enter JMP installation path (e.g. C:\Program Files\JMP\16)"
    } catch {
  Write-Lang "[!] [CN] 非交互模式，跳过手动输入" "[EN] Non-interactive mode, skipping manual input" -Color Yellow
    }

    if ($manualPath -and (Test-Path $manualPath)) {
        $exe = Join-Path $manualPath "JMP.exe"
        if (Test-Path $exe) {
            $jmpInstalled = $true
            $jmpPath = $exe
            $jmpVersion = $manualPath -replace ".*JMP\\", ''
            Write-Lang "[OK] [CN] 已确认 JMP 路径: $jmpPath" "[OK] [CN] 已确认 JMP 路径: $jmpPath" -ForegroundColor Green
            Write-Lang "[OK] [EN] JMP path confirmed: $jmpPath" "[OK] [EN] JMP path confirmed: $jmpPath" -ForegroundColor Green
        }
    }
}

# 4. 输出配置结果
if ($jmpInstalled) {
    Write-Host "`n[CN] === 配置结果 ===" -ForegroundColor Cyan
    Write-Host "[EN] === Configuration Result ===" -ForegroundColor Cyan
    Write-Lang "JMP 路径: $jmpPath" "JMP path: $jmpPath" -Color White
    Write-Lang "版本: $jmpVersion" "Version: $jmpVersion" -Color White
    
    # 请求用户确认后再修改环境变量
    Write-Lang "`n[CN] 即将设置用户环境变量:" "`n[CN] 即将设置用户环境变量:" -ForegroundColor Yellow
    Write-Lang "[EN] About to set environment variables:" "[EN] About to set environment variables:" -ForegroundColor Yellow
    Write-Host "  STATSOFT_JMP_PATH=$jmpPath" -ForegroundColor Gray

    # L-5: 非交互回退
    $confirm = "Y"
    try {
        $confirm = Read-Host "[CN] 确认设置环境变量? (y/N) / [EN] Confirm setting env vars? (y/N)"
    } catch {
  Write-Lang "[!] [CN] 非交互模式，自动应用" "[EN] Non-interactive mode, auto-applying" -Color Yellow
    }

    if ($confirm -eq 'y' -or $confirm -eq 'Y') {
        [System.Environment]::SetEnvironmentVariable("STATSOFT_JMP_PATH", $jmpPath, "User")
  Write-Lang "[OK] [CN] 环境变量已设置" "[EN] Environment variable set" -Color Green
    } else {
  Write-Lang "[!] [CN] 跳过环境变量设置" "[EN] Skipping env var setup" -Color Yellow
    }
    
    # 显示调用示例
    Write-Host "`n[CN] === 调用示例 ===" -ForegroundColor Cyan
    Write-Host "[EN] === Usage Examples ===" -ForegroundColor Cyan
    Write-Lang "运行 JSL 脚本:" "Run JSL script:" -Color White
  Write-Lang "`"$jmpPath`"" "R `" -Color White
    Write-Lang "" ""
    Write-Lang "静默模式:" "Silent mode:" -Color White
  Write-Lang "`"$jmpPath`"" "S /R `" -Color White
    Write-Lang "" ""
    Write-Lang "COM 自动化 (PowerShell):" "COM automation (PowerShell):" -Color White
    Write-Host '  $jmp = New-Object -ComObject JMP.Application'
    Write-Host '  $jmp.RunScriptFile("C:\path\to\script.jsl")'
    Write-Host '  $jmp.Quit()'
}
