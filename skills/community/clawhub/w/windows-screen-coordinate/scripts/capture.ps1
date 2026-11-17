# Screen Coord Locator - (c) 2026. Commercial license, redistribution prohibited.
# capture.ps1 - 截取全屏 / 指定显示器 / 指定区域 / 指定窗口
# 输出：单个 JSON 对象到 stdout

[CmdletBinding()]
param(
    [ValidateSet('full', 'monitor', 'region', 'window')]
    [string]$Mode = 'full',

    [int]$Monitor = 0,

    [int]$X = 0,
    [int]$Y = 0,
    [int]$W = 0,
    [int]$H = 0,

    [string]$WindowTitle = '',
    [switch]$WindowClientOnly,

    [string]$Out = '',

    [ValidateSet('png', 'jpg', 'jpeg')]
    [string]$Format = 'png',

    [double]$Scale = 1.0,
    [int]$Quality = 92
)

. (Join-Path $PSScriptRoot 'lib\common.ps1')

try {
    Assert-ScfWindows
    Initialize-ScfEnvironment -NeedForms -NeedDrawing
} catch {
    Fail-Scf -Code 'INTERNAL' -Message '初始化失败' -Detail $_.Exception.Message
}

function Get-ScfWindowRect {
    param([string]$Title, [bool]$ClientOnly)

    $procs = Get-Process -ErrorAction SilentlyContinue |
             Where-Object { $_.MainWindowTitle -and $_.MainWindowTitle.Length -gt 0 }
    if (-not $procs) { return $null }

    $hit = $procs | Where-Object { $_.MainWindowTitle -like ('*' + $Title + '*') } | Select-Object -First 1
    if (-not $hit) { return $null }

    $handle = $hit.MainWindowHandle
    if ($handle -eq [IntPtr]::Zero) { return $null }

    $r = New-Object ScfNative+ScfRect
    if (-not [ScfNative]::GetWindowRect($handle, [ref]$r)) { return $null }

    return [ordered]@{
        title  = $hit.MainWindowTitle
        pid    = $hit.Id
        handle = [int64]$handle
        left   = $r.Left
        top    = $r.Top
        width  = ($r.Right - $r.Left)
        height = ($r.Bottom - $r.Top)
    }
}

try {
    $displays = Get-ScfDisplayInfo
    $srcX = 0; $srcY = 0; $srcW = 0; $srcH = 0
    $windowInfo = $null

    switch ($Mode) {
        'full' {
            $vs = $displays.virtualScreen
            $srcX = $vs.x; $srcY = $vs.y; $srcW = $vs.width; $srcH = $vs.height
        }
        'monitor' {
            $mons = $displays.monitors
            if ($Monitor -lt 0 -or $Monitor -ge $mons.Count) {
                Fail-Scf -Code 'NO_TARGET' -Message ('显示器序号越界，当前共 {0} 块屏幕' -f $mons.Count)
            }
            $m = $mons[$Monitor]
            $srcX = $m.bounds.x; $srcY = $m.bounds.y
            $srcW = $m.bounds.width; $srcH = $m.bounds.height
        }
        'region' {
            if ($W -le 0 -or $H -le 0) {
                Fail-Scf -Code 'INTERNAL' -Message 'region 模式需要提供有效的 -W 与 -H'
            }
            $srcX = $X; $srcY = $Y; $srcW = $W; $srcH = $H
        }
        'window' {
            if (-not $WindowTitle) {
                Fail-Scf -Code 'NO_TARGET' -Message 'window 模式需要提供 -WindowTitle'
            }
            $windowInfo = Get-ScfWindowRect -Title $WindowTitle -ClientOnly $WindowClientOnly.IsPresent
            if (-not $windowInfo) {
                Fail-Scf -Code 'NO_TARGET' -Message ('没有找到标题包含「{0}」的可见窗口' -f $WindowTitle)
            }
            $srcX = $windowInfo.left; $srcY = $windowInfo.top
            $srcW = $windowInfo.width; $srcH = $windowInfo.height
        }
    }

    if ($srcW -le 0 -or $srcH -le 0) {
        Fail-Scf -Code 'INTERNAL' -Message '计算出的截取区域为空'
    }

    $bmp = New-Object System.Drawing.Bitmap($srcW, $srcH)
    $gfx = [System.Drawing.Graphics]::FromImage($bmp)
    $gfx.CopyFromScreen($srcX, $srcY, 0, 0, (New-Object System.Drawing.Size($srcW, $srcH)))
    $gfx.Dispose()

    if ($Scale -ne 1.0 -and $Scale -gt 0) {
        $nw = [int][math]::Max(1, [math]::Round($srcW * $Scale))
        $nh = [int][math]::Max(1, [math]::Round($srcH * $Scale))
        $resized = New-Object System.Drawing.Bitmap($nw, $nh)
        $g2 = [System.Drawing.Graphics]::FromImage($resized)
        $g2.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $g2.DrawImage($bmp, 0, 0, $nw, $nh)
        $g2.Dispose()
        $bmp.Dispose()
        $bmp = $resized
    }

    if (-not $Out) {
        $ext = 'png'
        if ($Format -eq 'jpg' -or $Format -eq 'jpeg') { $ext = 'jpg' }
        $Out = New-ScfFilePath -Prefix 'capture' -Extension $ext
    }
    $outDir = Split-Path -Parent $Out
    if ($outDir -and -not (Test-Path $outDir)) {
        New-Item -ItemType Directory -Path $outDir -Force | Out-Null
    }

    if ($Format -eq 'jpg' -or $Format -eq 'jpeg') {
        $codec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() |
                 Where-Object { $_.MimeType -eq 'image/jpeg' } | Select-Object -First 1
        $ep = New-Object System.Drawing.Imaging.EncoderParameters(1)
        $ep.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter(
            [System.Drawing.Imaging.Encoder]::Quality, [int64]$Quality)
        $bmp.Save($Out, $codec, $ep)
    } else {
        $bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)
    }

    $imgW = $bmp.Width
    $imgH = $bmp.Height
    $bmp.Dispose()

    $result = @{
        ok     = $true
        action = 'capture'
        mode   = $Mode
        image  = [ordered]@{
            path    = $Out
            width   = $imgW
            height  = $imgH
            format  = $Format
            scale   = $Scale
        }
        origin = [ordered]@{ x = $srcX; y = $srcY }
        source = [ordered]@{ x = $srcX; y = $srcY; width = $srcW; height = $srcH }
        virtualScreen = $displays.virtualScreen
        monitors      = $displays.monitors
        note   = '该图左上角对应绝对屏幕坐标 (origin.x, origin.y)。在图内量到的坐标需加上 origin 才是真实屏幕坐标。'
    }
    if ($windowInfo) { $result['window'] = $windowInfo }

    Complete-Scf -Data $result
} catch {
    Fail-Scf -Code 'INTERNAL' -Message '截屏失败' -Detail ($_.Exception.Message + ' @ ' + $_.InvocationInfo.ScriptLineNumber)
}
