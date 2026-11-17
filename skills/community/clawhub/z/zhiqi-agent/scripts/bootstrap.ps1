# 一次性准备：创建本地虚拟环境并安装依赖（幂等，可重复执行）
$ErrorActionPreference = 'Stop'
$SkillDir = Split-Path -Parent $PSScriptRoot
$VenvDir  = Join-Path $SkillDir '.venv'
$Mirror   = if ($env:ZHIQI_PIP_MIRROR) { $env:ZHIQI_PIP_MIRROR } else { 'https://pypi.tuna.tsinghua.edu.cn/simple' }
$MinMinor = 9   # 需要 Python 3.9+

# 遍历候选解释器，挑出【版本最高且 >= 3.9】的那个
function Find-Python {
  $cands = @(
    @('py', '-3.13'), @('py', '-3.12'), @('py', '-3.11'), @('py', '-3.10'), @('py', '-3.9'), @('py', '-3'),
    @('python3.13'), @('python3.12'), @('python3.11'), @('python3.10'), @('python3.9'),
    @('python3'), @('python')
  )
  $best = $null; $bestScore = -1
  foreach ($c in $cands) {
    $exe = $c[0]
    $prefix = @()
    if ($c.Count -gt 1) { $prefix = @($c[1]) }
    if (-not (Get-Command $exe -ErrorAction SilentlyContinue)) { continue }
    try {
      $out = & $exe @prefix -c "import sys;print('%d %d'%sys.version_info[:2])" 2>$null
      if ($LASTEXITCODE -ne 0 -or -not $out) { continue }
      $mm = ($out.Trim() -split '\s+')
      $maj = [int]$mm[0]; $min = [int]$mm[1]
      if ($maj -ne 3 -or $min -lt $MinMinor) { continue }
      $score = $maj * 1000 + $min
      if ($score -gt $bestScore) {
        $bestScore = $score
        $best = [pscustomobject]@{ Exe = $exe; Prefix = $prefix; Version = "$maj.$min" }
      }
    } catch { }
  }
  return $best
}

$Py = Find-Python
if (-not $Py) {
  Write-Error "未找到 Python 3.9+。请安装后重试（Windows 可从 python.org 或 Microsoft Store 安装）。"
  exit 3
}
Write-Host ("[bootstrap] 使用解释器: {0} {1} (Python {2})" -f $Py.Exe, ($Py.Prefix -join ' '), $Py.Version)

$VenvPy = Join-Path $VenvDir 'Scripts\python.exe'

# 若已有 venv 但版本不达标，则重建
if (Test-Path $VenvPy) {
  $vv = & $VenvPy -c "import sys;print('%d %d'%sys.version_info[:2])" 2>$null
  $needRebuild = $true
  if ($LASTEXITCODE -eq 0 -and $vv) {
    $mm = ($vv.Trim() -split '\s+')
    if ([int]$mm[0] -eq 3 -and [int]$mm[1] -ge $MinMinor) { $needRebuild = $false }
  }
  if ($needRebuild) {
    Write-Host "[bootstrap] 现有虚拟环境 Python 版本过低，重建"
    Remove-Item -Recurse -Force $VenvDir
  }
}

if (-not (Test-Path $VenvPy)) {
  Write-Host "[bootstrap] 创建虚拟环境 $VenvDir"
  & $Py.Exe @($Py.Prefix + @('-m', 'venv', $VenvDir))
  if ($LASTEXITCODE -ne 0) { Write-Error "创建虚拟环境失败"; exit 3 }
  $VenvPy = Join-Path $VenvDir 'Scripts\python.exe'
}

Write-Host "[bootstrap] 安装依赖 cryptography / requests"
& $VenvPy -m pip install -q --disable-pip-version-check -i $Mirror --upgrade pip 2>$null
& $VenvPy -m pip install -q --disable-pip-version-check -i $Mirror cryptography requests
if ($LASTEXITCODE -ne 0) { Write-Error "依赖安装失败"; exit 3 }

# 内置 Python 包（若安装器未拷贝，则尝试从源码目录补齐）
$Vendor = Join-Path $SkillDir 'vendor'
$need = @('zhiqi_agent', 'zhiqi_mcp') | Where-Object { -not (Test-Path (Join-Path $Vendor $_)) }
if ($need.Count -gt 0) {
  $src = $env:ZHIQI_AGENT_SRC
  if (-not $src) {
    $pointer = Join-Path $SkillDir '.source'
    if (Test-Path $pointer) { $src = (Get-Content $pointer -Raw).Trim() }
  }
  if ($src -and (Test-Path (Join-Path $src 'zhiqi_agent'))) {
    New-Item -ItemType Directory -Force -Path $Vendor | Out-Null
    foreach ($p in @('zhiqi_agent', 'zhiqi_mcp')) {
      $from = Join-Path $src $p
      if (Test-Path $from) { Copy-Item -Recurse -Force $from (Join-Path $Vendor $p) }
    }
    Write-Host "[bootstrap] 已内置 Python 包 -> $Vendor"
  } else {
    Write-Error "缺少内置包目录 $Vendor，且未找到源码目录。请用 deploy/install-openclaw-skill.ps1 安装本技能。"
    exit 3
  }
}

& $VenvPy -c "import sys, cryptography, requests; print('[bootstrap] 就绪 Python', sys.version.split()[0], '| cryptography', cryptography.__version__)"
exit 0
