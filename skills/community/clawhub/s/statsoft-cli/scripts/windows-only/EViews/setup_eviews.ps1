# setup_eviews.ps1 - EViews 统计软件环境检测与配置脚本
# EViews: 计量经济学软件，Windows-only，有批处理模式

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



  Write-Lang "=== EViews 环境检测" "EViews Environment Detection ===" -Color White
  Write-Lang "平台" "Platform: Windows" -Color White
Write-Lang "" ""

# 检测 EViews 是否安装
function Detect-EViews {
    $eviews_path = ""
    
    # 检查常见安装路径
    $paths = @(
        "C:\Program Files\EViews\EViews 13\EViews64.exe",
        "C:\Program Files\EViews\EViews 12\EViews64.exe",
        "C:\Program Files\EViews\EViews 11\EViews64.exe",
        "C:\Program Files (x86)\EViews\EViews 10\EViews.exe"
    )
    
    foreach ($path in $paths) {
        if (Test-Path $path) {
            $eviews_path = $path
            break
        }
    }
    
    # 检查 PATH
    if (-not $eviews_path) {
        $eviews_path = (Get-Command EViews64 -ErrorAction SilentlyContinue).Source
        if (-not $eviews_path) {
            $eviews_path = (Get-Command EViews -ErrorAction SilentlyContinue).Source
        }
    }
    
    return $eviews_path
}

# 主流程
$eviews_path = Detect-EViews

if ($eviews_path) {
  Write-Lang "✅ 检测到 EViews 安装" "EViews installation detected:" -Color White
  Write-Lang "路径" "Path: $eviews_path" -Color White
    
    # 输出配置信息（供 AI Agent 读取）
    Write-Lang "" ""
  Write-Lang "=== 配置信息" "Configuration Info ===" -Color White
    Write-Lang "EVIEWS_PATH=$eviews_path" "EVIEWS_PATH=$eviews_path"
    Write-Lang "EVIEWS_OS=windows" "EVIEWS_OS=windows"
    
    # 输出使用说明
    Write-Lang "" ""
  Write-Lang "=== 使用说明" "Usage Instructions ===" -Color White
  Write-Lang "批处理命令" "Batch command:" -Color White
  Write-Lang "& '$eviews_path'" "run script.prg" -Color White
    Write-Lang "" ""
  Write-Lang "脚本示例" "Script example:" -Color White
    Write-Host "  ' script.prg"
    Write-Host "  read(r) data.csv"
    Write-Host "  equation eq1.ls y c x1 x2"
    Write-Host "  eq1.output(table) results.csv"
    Write-Lang "" ""
  Write-Lang "⚠️ 注意事项" "Notes:" -Color White
    Write-Host "  - EViews 运行时可能有闪屏（GUI 程序）"
    Write-Host "  - 脚本末尾加 'exit' 命令可自动退出 EViews"
    
} else {
  Write-Lang "❌ 未检测到 EViews 安装" "EViews installation not found" -Color White
    Write-Lang "" ""
  Write-Lang "=== 安装指南" "Installation Guide ===" -Color White
  Write-Lang "Windows 安装步骤" "Windows installation steps:" -Color White
  Write-Lang "1. 访问 EViews 官网: https:" "/www.eviews.com/" -Color White
    Write-Host "  2. 下载 EViews 试用版或输入许可证"
    Write-Host "  3. 运行安装程序，按默认设置安装"
    Write-Host "  4. 安装完成后，EViews64.exe 通常在 C:\Program Files\EViews\EViews XX\"
}
