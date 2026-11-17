param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("cli-path", "status", "capabilities", "health", "connectors", "android-devices", "runs", "pause-run", "resume-run", "stop-run", "target", "task-begin", "task-status", "task-refresh", "task-restore", "task-activate", "task-ensure-visible", "task-move", "task-resize", "window-arrange", "task-observe", "task-find", "task-wait", "task-click", "task-long-press", "task-drag", "task-scroll", "task-write", "task-hotkey", "task-end", "list", "show", "prepare-update", "inspect", "validate", "install", "remove", "start", "latest", "debug", "next", "stop", "experience-create", "experience-list", "experience-show", "experience-note", "demonstrate-start", "demonstrate-status", "demonstrate-pause", "demonstrate-resume", "demonstrate-stop", "demonstrate-export")]
    [string]$Action,
    [string]$Target,
    [string]$Executable,
    [string]$DevelopmentRoot = (Join-Path ([Environment]::GetFolderPath("MyDocuments")) "屏幕自动化小助手\流程开发"),
    [int]$Count,
    [int]$Limit = 10,
    [double]$Timeout = 30,
    [switch]$NoScreen,
    [string]$Name,
    [string]$Project,
    [string]$Goal,
    [string]$ExpectedResult,
    [string]$Forbidden,
    [ValidateSet("normal", "exception", "boundary", "supplement")]
    [string]$FragmentType = "normal",
    [string]$Purpose,
    [ValidateSet("rule", "exception", "success", "variable", "constraint", "context")]
    [string]$Kind = "context",
    [string]$Message,
    [int]$Handle,
    [int[]]$Handles,
    [string]$Process,
    [string]$Text,
    [string]$Point,
    [string]$End,
    [ValidateSet("left", "right", "middle")][string]$Button = "left",
    [int]$Amount,
    [ValidateSet("up", "down", "left", "right")][string]$Direction,
    [double]$Interval = 0,
    [double]$Duration = 1.0,
    [string[]]$Keys,
    [int]$X,
    [int]$Y,
    [int]$Width,
    [int]$Height,
    [ValidateSet("grid", "columns", "rows", "two-by-two")][string]$Layout = "grid",
    [string]$Monitor
)

$ErrorActionPreference = "Stop"

$isMacOS = $false
try {
    if (Get-Variable IsMacOS -ErrorAction SilentlyContinue) {
        $isMacOS = [bool]$IsMacOS
    } elseif ($PSVersionTable.PSEdition -eq "Core") {
        $isMacOS = [System.Runtime.InteropServices.RuntimeInformation]::IsOSPlatform(
            [System.Runtime.InteropServices.OSPlatform]::OSX
        )
    }
} catch {
    $isMacOS = $false
}
if ($isMacOS) {
    Write-Output '{"ok": false, "platform": "macos", "error": "本机是 macOS：请使用 Skill 包内的 workflow_dev.sh，不要执行 Windows 版 workflow_dev.ps1。"}'
    exit 2
}

function Resolve-HelperExecutable {
    param([string]$RequestedPath)

    $candidates = [System.Collections.Generic.List[string]]::new()
    if (-not [string]::IsNullOrWhiteSpace($RequestedPath)) {
        $candidates.Add($RequestedPath)
    }
    if (-not [string]::IsNullOrWhiteSpace($env:SCREEN_AUTOMATION_HELPER_EXE)) {
        $candidates.Add($env:SCREEN_AUTOMATION_HELPER_EXE)
    }

    $environmentKey = "HKCU:\Environment"
    if (Test-Path -LiteralPath $environmentKey) {
        $registeredEnvironment = (Get-ItemProperty -LiteralPath $environmentKey -Name "SCREEN_AUTOMATION_HELPER_EXE" -ErrorAction SilentlyContinue).SCREEN_AUTOMATION_HELPER_EXE
        if (-not [string]::IsNullOrWhiteSpace($registeredEnvironment)) {
            $candidates.Add($registeredEnvironment)
        }
    }

    $appPathKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\App Paths\ScreenAutomationHelper.exe"
    if (Test-Path -LiteralPath $appPathKey) {
        $registeredAppPath = (Get-Item -LiteralPath $appPathKey).GetValue("")
        if (-not [string]::IsNullOrWhiteSpace($registeredAppPath)) {
            $candidates.Add([string]$registeredAppPath)
        }
    }

    $uninstallKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\{F174BA6D-570B-4F87-A453-84AA66C4A0CB}_is1"
    if (Test-Path -LiteralPath $uninstallKey) {
        $installLocation = (Get-ItemProperty -LiteralPath $uninstallKey -ErrorAction SilentlyContinue).InstallLocation
        if (-not [string]::IsNullOrWhiteSpace($installLocation)) {
            $candidates.Add((Join-Path $installLocation "ScreenAutomationHelper.exe"))
        }
    }

    $candidates.Add((Join-Path $env:LOCALAPPDATA "Programs\Xiaozs\ScreenAutomationHelper\ScreenAutomationHelper.exe"))

    $command = Get-Command "ScreenAutomationHelper.exe" -ErrorAction SilentlyContinue
    if ($null -ne $command -and -not [string]::IsNullOrWhiteSpace($command.Source)) {
        $candidates.Add($command.Source)
    }

    foreach ($candidate in $candidates) {
        if ([string]::IsNullOrWhiteSpace($candidate)) {
            continue
        }
        $fullPath = [IO.Path]::GetFullPath([Environment]::ExpandEnvironmentVariables($candidate))
        if (Test-Path -LiteralPath $fullPath -PathType Leaf) {
            return $fullPath
        }
    }

    throw '未找到屏幕自动化小助手 Windows。请先安装并启动桌面端；如安装在特殊位置，可设置 SCREEN_AUTOMATION_HELPER_EXE，或使用 -Executable 指定程序路径。'
}

function Require-Target {
    param([string]$Value, [string]$ActionName)
    if ([string]::IsNullOrWhiteSpace($Value)) {
        throw "操作 $ActionName 需要提供 -Target。"
    }
}

$resolvedExecutable = Resolve-HelperExecutable -RequestedPath $Executable

# 仅 cli-path 与 prepare-update 是当前 Skill 的规范入口；其余 Action 为兼容已安装的旧流程保留。
switch ($Action) {
    "cli-path" { $resolvedExecutable }
    "status" {
        $desktopStatus = (& $resolvedExecutable cli status | Out-String | ConvertFrom-Json)
        [ordered]@{
            ok = $true
            executable = $resolvedExecutable
            desktop = $desktopStatus
        } | ConvertTo-Json -Depth 12
    }
    "capabilities" { & $resolvedExecutable cli capabilities }
    "connectors" { & $resolvedExecutable cli connectors list }
    "android-devices" { & $resolvedExecutable cli connectors discover android-screen }
    "runs" { & $resolvedExecutable cli runs list }
    "pause-run" { & $resolvedExecutable cli pause --run-id $Target }
    "resume-run" { & $resolvedExecutable cli resume --run-id $Target }
    "stop-run" { & $resolvedExecutable cli stop --run-id $Target }
    "health" {
        $healthArgs = @("cli", "health")
        if (-not [string]::IsNullOrWhiteSpace($Target)) {
            $healthArgs += @("--workflow", $Target)
        }
        if ($NoScreen) {
            $healthArgs += "--no-screen"
        }
        & $resolvedExecutable @healthArgs
    }
    "experience-create" {
        if ([string]::IsNullOrWhiteSpace($Name)) { throw "操作 $Action 需要提供 -Name。" }
        $experienceArgs = @("cli", "experience", "create", "--name", $Name)
        if (-not [string]::IsNullOrWhiteSpace($Goal)) { $experienceArgs += @("--goal", $Goal) }
        if (-not [string]::IsNullOrWhiteSpace($ExpectedResult)) { $experienceArgs += @("--expected-result", $ExpectedResult) }
        if (-not [string]::IsNullOrWhiteSpace($Forbidden)) { $experienceArgs += @("--forbidden", $Forbidden) }
        & $resolvedExecutable @experienceArgs
    }
    "experience-list" { & $resolvedExecutable cli experience list }
    "experience-show" {
        Require-Target -Value $Project -ActionName $Action
        & $resolvedExecutable cli experience show $Project
    }
    "experience-note" {
        Require-Target -Value $Project -ActionName $Action
        if ([string]::IsNullOrWhiteSpace($Message)) { throw "操作 $Action 需要提供 -Message。" }
        & $resolvedExecutable cli experience note $Project --kind $Kind --message $Message
    }
    "demonstrate-start" {
        Require-Target -Value $Project -ActionName $Action
        $demonstrateArgs = @("cli", "recording", "start", "--project", $Project, "--fragment-type", $FragmentType)
        if (-not [string]::IsNullOrWhiteSpace($Purpose)) { $demonstrateArgs += @("--purpose", $Purpose) }
        & $resolvedExecutable @demonstrateArgs
    }
    "demonstrate-status" { & $resolvedExecutable cli recording status }
    "demonstrate-pause" { & $resolvedExecutable cli recording pause }
    "demonstrate-resume" { & $resolvedExecutable cli recording resume }
    "demonstrate-stop" { & $resolvedExecutable cli recording stop }
    "demonstrate-export" {
        Require-Target -Value $Target -ActionName $Action
        & $resolvedExecutable cli recording export $Target
    }
    "target" {
        if ($Timeout -le 0) {
            throw "等待时间必须大于 0 秒。"
        }
        & $resolvedExecutable cli window wait-selection --timeout $Timeout
    }
    "task-begin" {
        $taskArgs = @("cli", "task", "begin")
        if ($PSBoundParameters.ContainsKey("Handle")) { $taskArgs += @("--handle", $Handle) }
        if (-not [string]::IsNullOrWhiteSpace($Target)) { $taskArgs += @("--title", $Target) }
        if (-not [string]::IsNullOrWhiteSpace($Process)) { $taskArgs += @("--process", $Process) }
        & $resolvedExecutable @taskArgs
    }
    "task-status" { & $resolvedExecutable cli task status }
    "task-refresh" { & $resolvedExecutable cli window refresh }
    "task-restore" { & $resolvedExecutable cli window restore }
    "task-activate" { & $resolvedExecutable cli window activate }
    "task-ensure-visible" { & $resolvedExecutable cli window ensure-visible }
    "task-move" {
        if (-not $PSBoundParameters.ContainsKey("X") -or -not $PSBoundParameters.ContainsKey("Y")) { throw "操作 $Action 需要提供 -X 和 -Y。" }
        & $resolvedExecutable cli window move --x $X --y $Y
    }
    "task-resize" {
        if (-not $PSBoundParameters.ContainsKey("Width") -or -not $PSBoundParameters.ContainsKey("Height")) { throw "操作 $Action 需要提供 -Width 和 -Height。" }
        & $resolvedExecutable cli window resize --width $Width --height $Height
    }
    "window-arrange" {
        if ($null -eq $Handles -or $Handles.Count -lt 2) { throw "操作 $Action 需要通过 -Handles 提供二至四个窗口句柄。" }
        $arrangeArgs = @("cli", "window", "arrange", "--handles") + $Handles + @("--layout", $Layout)
        if (-not [string]::IsNullOrWhiteSpace($Monitor)) { $arrangeArgs += @("--monitor", $Monitor) }
        & $resolvedExecutable @arrangeArgs
    }
    "task-observe" { & $resolvedExecutable cli task observe }
    "task-find" {
        if ([string]::IsNullOrWhiteSpace($Text)) { throw "操作 $Action 需要提供 -Text。" }
        & $resolvedExecutable cli task find --text $Text
    }
    "task-wait" {
        if ([string]::IsNullOrWhiteSpace($Text)) { throw "操作 $Action 需要提供 -Text。" }
        $waitInterval = if ($Interval -gt 0) { $Interval } else { 0.8 }
        & $resolvedExecutable cli task wait --text $Text --timeout $Timeout --interval $waitInterval
    }
    "task-click" {
        if ([string]::IsNullOrWhiteSpace($Point)) { throw "操作 $Action 需要提供 -Point。" }
        & $resolvedExecutable cli task click --point $Point --button $Button
    }
    "task-long-press" {
        if ([string]::IsNullOrWhiteSpace($Point)) { throw "操作 $Action 需要提供 -Point。" }
        & $resolvedExecutable cli task long-press --point $Point --duration $Duration --button $Button
    }
    "task-drag" {
        if ([string]::IsNullOrWhiteSpace($Point) -or [string]::IsNullOrWhiteSpace($End)) { throw "操作 $Action 需要提供 -Point 和 -End。" }
        & $resolvedExecutable cli task drag --start $Point --end $End --duration $Duration --button $Button
    }
    "task-scroll" {
        if ([string]::IsNullOrWhiteSpace($Point)) { throw "操作 $Action 需要提供 -Point。" }
        $scrollArguments = @("cli", "task", "scroll", "--point", $Point, "--amount", $Amount)
        if (-not [string]::IsNullOrWhiteSpace($Direction)) {
            $scrollArguments += @("--direction", $Direction)
        }
        & $resolvedExecutable @scrollArguments
    }
    "task-write" {
        if ($null -eq $Text) { throw "操作 $Action 需要提供 -Text。" }
        & $resolvedExecutable cli task write --text $Text --interval $Interval
    }
    "task-hotkey" {
        if ($null -eq $Keys -or $Keys.Count -eq 0) { throw "操作 $Action 需要提供 -Keys。" }
        & $resolvedExecutable cli task hotkey @Keys
    }
    "task-end" { & $resolvedExecutable cli task end }
    "list" { & $resolvedExecutable cli workflow list }
    "show" {
        Require-Target -Value $Target -ActionName $Action
        & $resolvedExecutable cli workflow show $Target
    }
    "prepare-update" {
        Require-Target -Value $Target -ActionName $Action
        $workflow = (& $resolvedExecutable cli workflow show $Target | Out-String | ConvertFrom-Json)
        $source = [string]$workflow._meta.package_dir
        if ([string]::IsNullOrWhiteSpace($source) -or -not (Test-Path -LiteralPath $source -PathType Container)) {
            throw "无法取得自动化流程 $Target 的已安装程序包目录。"
        }

        New-Item -ItemType Directory -Path $DevelopmentRoot -Force | Out-Null
        $safeId = ([string]$workflow.id) -replace '[^A-Za-z0-9._-]', '-'
        $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
        $destination = Join-Path $DevelopmentRoot "$safeId-$stamp"
        New-Item -ItemType Directory -Path $destination | Out-Null
        Get-ChildItem -LiteralPath $source -Force | ForEach-Object {
            Copy-Item -LiteralPath $_.FullName -Destination $destination -Recurse -Force
        }

        [ordered]@{
            ok = $true
            action = "prepare-update"
            workflow_id = $workflow.id
            current_version = $workflow.version
            development_path = $destination
            instruction = "只修改 development_path 中的副本；完成后提升版本号，再执行 inspect、install 和受监督验收。"
        } | ConvertTo-Json -Depth 8
    }
    "inspect" {
        Require-Target -Value $Target -ActionName $Action
        & $resolvedExecutable cli workflow inspect $Target
    }
    "validate" {
        Require-Target -Value $Target -ActionName $Action
        if (Test-Path -LiteralPath $Target) {
            & $resolvedExecutable cli workflow inspect $Target
        } else {
            & $resolvedExecutable cli workflow validate $Target
        }
    }
    "install" {
        Require-Target -Value $Target -ActionName $Action
        & $resolvedExecutable cli workflow install $Target
    }
    "remove" {
        Require-Target -Value $Target -ActionName $Action
        & $resolvedExecutable cli workflow remove $Target
    }
    "start" {
        Require-Target -Value $Target -ActionName $Action
        $startArgs = @("cli", "start-workflow", $Target)
        if ($PSBoundParameters.ContainsKey("Count")) {
            $startArgs += @("--count", $Count)
        }
        & $resolvedExecutable @startArgs
    }
    "latest" {
        & $resolvedExecutable cli latest --limit $Limit
    }
    "debug" {
        Require-Target -Value $Target -ActionName $Action
        & $resolvedExecutable cli start-workflow $Target --debug --step-mode
    }
    "next" { & $resolvedExecutable cli debug-next }
    "stop" { & $resolvedExecutable cli stop }
}
exit $LASTEXITCODE
