param(
  [switch]$DryRun,
  [int]$MaxTotal = 0
)
$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ArxivDailyRoot = Resolve-Path (Join-Path $ScriptDir '..')
$PythonScript = Join-Path $ScriptDir 'arxiv_daily.py'

$PythonExe = $null
$PythonPrefixArgs = @()

$PythonCommand = Get-Command python.exe -ErrorAction SilentlyContinue
if ($null -ne $PythonCommand) {
  $PythonExe = $PythonCommand.Source
} else {
  $PyCommand = Get-Command py.exe -ErrorAction SilentlyContinue
  if ($null -ne $PyCommand) {
    $PythonExe = $PyCommand.Source
    $PythonPrefixArgs = @('-3')
  } else {
    throw "Unable to find python.exe or py.exe on PATH. Install Python or the Python Launcher."
  }
}

$PythonArgs = @()
$PythonArgs += $PythonPrefixArgs
$PythonArgs += $PythonScript
$PythonArgs += '--root'
$PythonArgs += $ArxivDailyRoot.Path
if ($DryRun) {
  $PythonArgs += '--dry-run'
}
if ($MaxTotal -gt 0) {
  $PythonArgs += '--max-total'
  $PythonArgs += "$MaxTotal"
}

& $PythonExe @PythonArgs
$exitCode = $LASTEXITCODE
exit $exitCode
