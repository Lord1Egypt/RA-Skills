# Screen Coord Locator - (c) 2026. Commercial license, redistribution prohibited.
# act.ps1 - 把定位结果执行成鼠标动作
# 输出：单个 JSON 对象到 stdout

[CmdletBinding()]
param(
    [ValidateSet('move', 'click', 'doubleclick', 'rightclick', 'middleclick', 'drag', 'wheel')]
    [string]$Action = 'click',

    [int]$X = 0,
    [int]$Y = 0,

    [int]$X2 = 0,
    [int]$Y2 = 0,

    [int]$WheelDelta = -120,

    [int]$HoldMs = 30,
    [int]$Steps = 12,
    [int]$DragHoldMs = 120,

    [switch]$DryRun
)

. (Join-Path $PSScriptRoot 'lib\common.ps1')

try {
    Assert-ScfWindows
    Initialize-ScfEnvironment
} catch {
    Fail-Scf -Code 'INTERNAL' -Message '初始化失败' -Detail $_.Exception.Message
}

function Invoke-ScfMoveTo {
    param([int]$ToX, [int]$ToY, [int]$StepCount)
    [void][ScfNative]::SetCursorPos($ToX, $ToY)
    if ($StepCount -gt 1) {
        $start = New-Object ScfNative+ScfPoint
        [void][ScfNative]::GetCursorPos([ref]$start)
    }
}

try {
    $performed = [ordered]@{ action = $Action }
    $cursor = New-Object ScfNative+ScfPoint
    [void][ScfNative]::GetCursorPos([ref]$cursor)
    $performed['from'] = [ordered]@{ x = $cursor.X; y = $cursor.Y }

    if ($DryRun) {
        $performed['dryRun'] = $true
        Complete-Scf -Data @{
            ok       = $true
            action   = 'act'
            performed = $performed
            note     = 'DryRun 模式：未产生真实鼠标动作'
        }
    }

    switch ($Action) {
        'move' {
            [void][ScfNative]::SetCursorPos($X, $Y)
            $performed['to'] = [ordered]@{ x = $X; y = $Y }
        }
        'click' {
            [void][ScfNative]::SetCursorPos($X, $Y)
            Start-Sleep -Milliseconds 20
            [void][ScfNative]::mouse_event([uint32]0x0002, 0, 0, 0, [IntPtr]::Zero)
            Start-Sleep -Milliseconds $HoldMs
            [void][ScfNative]::mouse_event([uint32]0x0004, 0, 0, 0, [IntPtr]::Zero)
            $performed['to'] = [ordered]@{ x = $X; y = $Y; button = 'left' }
        }
        'doubleclick' {
            [void][ScfNative]::SetCursorPos($X, $Y)
            Start-Sleep -Milliseconds 20
            for ($i = 0; $i -lt 2; $i++) {
                [void][ScfNative]::mouse_event([uint32]0x0002, 0, 0, 0, [IntPtr]::Zero)
                Start-Sleep -Milliseconds $HoldMs
                [void][ScfNative]::mouse_event([uint32]0x0004, 0, 0, 0, [IntPtr]::Zero)
                Start-Sleep -Milliseconds 60
            }
            $performed['to'] = [ordered]@{ x = $X; y = $Y; button = 'left'; clicks = 2 }
        }
        'rightclick' {
            [void][ScfNative]::SetCursorPos($X, $Y)
            Start-Sleep -Milliseconds 20
            [void][ScfNative]::mouse_event([uint32]0x0008, 0, 0, 0, [IntPtr]::Zero)
            Start-Sleep -Milliseconds $HoldMs
            [void][ScfNative]::mouse_event([uint32]0x0010, 0, 0, 0, [IntPtr]::Zero)
            $performed['to'] = [ordered]@{ x = $X; y = $Y; button = 'right' }
        }
        'middleclick' {
            [void][ScfNative]::SetCursorPos($X, $Y)
            Start-Sleep -Milliseconds 20
            [void][ScfNative]::mouse_event([uint32]0x0020, 0, 0, 0, [IntPtr]::Zero)
            Start-Sleep -Milliseconds $HoldMs
            [void][ScfNative]::mouse_event([uint32]0x0040, 0, 0, 0, [IntPtr]::Zero)
            $performed['to'] = [ordered]@{ x = $X; y = $Y; button = 'middle' }
        }
        'drag' {
            if ($Steps -lt 1) { $Steps = 1 }
            [void][ScfNative]::SetCursorPos($X, $Y)
            Start-Sleep -Milliseconds 60
            [void][ScfNative]::mouse_event([uint32]0x0002, 0, 0, 0, [IntPtr]::Zero)
            Start-Sleep -Milliseconds $DragHoldMs
            for ($i = 1; $i -le $Steps; $i++) {
                $nx = [int][math]::Round($X + (($X2 - $X) * $i / $Steps))
                $ny = [int][math]::Round($Y + (($Y2 - $Y) * $i / $Steps))
                [void][ScfNative]::SetCursorPos($nx, $ny)
                Start-Sleep -Milliseconds 12
            }
            Start-Sleep -Milliseconds $DragHoldMs
            [void][ScfNative]::mouse_event([uint32]0x0004, 0, 0, 0, [IntPtr]::Zero)
            $performed['to'] = [ordered]@{ x = $X2; y = $Y2 }
            $performed['from2'] = [ordered]@{ x = $X; y = $Y }
        }
        'wheel' {
            [void][ScfNative]::SetCursorPos($X, $Y)
            Start-Sleep -Milliseconds 20
            [void][ScfNative]::mouse_event([uint32]0x0800, 0, 0, [uint32]([int]$WheelDelta), [IntPtr]::Zero)
            $performed['to'] = [ordered]@{ x = $X; y = $Y; delta = $WheelDelta }
        }
    }

    $after = New-Object ScfNative+ScfPoint
    [void][ScfNative]::GetCursorPos([ref]$after)

    Complete-Scf -Data @{
        ok        = $true
        action    = 'act'
        performed = $performed
        cursorAfter = [ordered]@{ x = $after.X; y = $after.Y }
    }
} catch {
    Fail-Scf -Code 'INTERNAL' -Message '执行鼠标动作失败' -Detail ($_.Exception.Message + ' @ ' + $_.InvocationInfo.ScriptLineNumber)
}
