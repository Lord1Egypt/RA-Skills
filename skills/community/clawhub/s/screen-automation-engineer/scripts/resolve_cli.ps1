param([string]$Executable)

$ErrorActionPreference = "Stop"
$candidates = [System.Collections.Generic.List[string]]::new()
foreach ($candidate in @(
    $Executable,
    $env:SCREEN_AUTOMATION_HELPER_EXE,
    (Join-Path $env:LOCALAPPDATA "Programs\Xiaozs\ScreenAutomationHelper\ScreenAutomationHelper.exe")
)) {
    if (-not [string]::IsNullOrWhiteSpace($candidate)) { $candidates.Add($candidate) }
}

$appPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\App Paths\ScreenAutomationHelper.exe"
if (Test-Path -LiteralPath $appPath) {
    $registered = (Get-Item -LiteralPath $appPath).GetValue("")
    if ($registered) { $candidates.Add([string]$registered) }
}

$command = Get-Command "ScreenAutomationHelper.exe" -ErrorAction SilentlyContinue
if ($command -and $command.Source) { $candidates.Add($command.Source) }

foreach ($candidate in $candidates) {
    $fullPath = [IO.Path]::GetFullPath([Environment]::ExpandEnvironmentVariables($candidate))
    if (Test-Path -LiteralPath $fullPath -PathType Leaf) { return $fullPath }
}

throw "未找到屏幕自动化小助手。请先安装桌面端，或使用 -Executable 指定路径。"
