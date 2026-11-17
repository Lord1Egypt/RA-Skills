# 智契接入端运行器（Windows PowerShell）
# 用法: powershell -ExecutionPolicy Bypass -File zhiqi.ps1 --home <dir> <命令> [参数]
$ErrorActionPreference = 'Stop'
$SkillDir = Split-Path -Parent $PSScriptRoot
$Vendor   = Join-Path $SkillDir 'vendor'
$VenvPy   = Join-Path $SkillDir '.venv\Scripts\python.exe'

# 0) 默认把 --home 指向技能自身的 .zhiqi：技能应当自包含。
#    不默认的话 CLI 会退到 .\.zhiqi（当前目录），于是"给技能配的模型"与
#    "实际调用读到的配置"可能不是同一个 —— 症状是"明明配了模型还报未申报"。
#    必须放在"复用全局 zhiqi"之前，否则装了全局命令时仍会用错 home。
$hasHome = $false
foreach ($a in $args) { if ($a -eq '--home') { $hasHome = $true } }
$allArgs = if ($hasHome) { $args } else { @('--home', (Join-Path $SkillDir '.zhiqi')) + $args }

# 1) 已全局安装则直接复用
$global = Get-Command zhiqi -ErrorAction SilentlyContinue
if ($global -and -not $env:ZHIQI_FORCE_LOCAL) {
  & zhiqi @allArgs
  exit $LASTEXITCODE
}

# 2) 确保本地环境就绪
$needBootstrap = $true
if (Test-Path $VenvPy) {
  & $VenvPy -c "import cryptography, requests" 2>$null
  if ($LASTEXITCODE -eq 0 -and (Test-Path (Join-Path $Vendor 'zhiqi_agent'))) { $needBootstrap = $false }
}
if ($needBootstrap) {
  Write-Host "[zhiqi] 首次运行，正在准备本地环境（约 10~30 秒）..."
  & powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'bootstrap.ps1')
  if ($LASTEXITCODE -ne 0) { Write-Error "环境准备失败"; exit 3 }
}

$env:PYTHONPATH = $Vendor
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONUTF8 = '1'
& $VenvPy -m zhiqi_agent.cli @allArgs
exit $LASTEXITCODE
