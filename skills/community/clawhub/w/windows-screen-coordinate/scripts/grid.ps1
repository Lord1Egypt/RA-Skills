# Screen Coord Locator - (c) 2026. Commercial license, redistribution prohibited.
# grid.ps1 - 在截图上叠加坐标标尺与网格，供模型读图换算绝对坐标
# 输出：单个 JSON 对象到 stdout

[CmdletBinding()]
param(
    [string]$Image = '',

    [int]$Spacing = 100,
    [int]$MajorEvery = 5,

    [int]$OriginX = 0,
    [int]$OriginY = 0,

    [string]$Out = '',

    [switch]$NoLabels,
    [int]$MaxLabels = 400
)

. (Join-Path $PSScriptRoot 'lib\common.ps1')
. (Join-Path $PSScriptRoot 'lib\permit.ps1')

try {
    Assert-ScfWindows
    $script:ScfPermit = Assert-ScfPermit
    Initialize-ScfEnvironment -NeedDrawing
} catch {
    Fail-Scf -Code 'INTERNAL' -Message '初始化失败' -Detail $_.Exception.Message
}

if ($Spacing -lt 10) { $Spacing = 10 }
if ($MajorEvery -lt 1) { $MajorEvery = 1 }

try {
    if (-not $Image -or -not (Test-Path $Image)) {
        Fail-Scf -Code 'NO_IMAGE' -Message ('图片不存在：{0}' -f $Image)
    }

    $src = $null
    try {
        $src = [System.Drawing.Image]::FromFile($Image)
    } catch {
        Fail-Scf -Code 'NO_IMAGE' -Message '图片无法读取，可能不是有效的图片文件' -Detail $_.Exception.Message
    }

    $iw = $src.Width
    $ih = $src.Height

    $canvas = New-Object System.Drawing.Bitmap($iw, $ih, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $g = [System.Drawing.Graphics]::FromImage($canvas)
    $g.DrawImage($src, 0, 0, $iw, $ih)
    $src.Dispose()

    $penMinor = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(70, 0, 150, 255), 1)
    $penMajor = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(150, 255, 90, 60), 1)

    $labelFont = New-Object System.Drawing.Font('Consolas', 10, [System.Drawing.FontStyle]::Bold)
    $labelBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(235, 255, 255, 255))
    $chipBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(190, 20, 20, 28))
    $edgeBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(160, 20, 20, 28))

    $labelCount = 0
    $skipLabels = $NoLabels.IsPresent

    # 顶部与左侧各留一条 22px 的标尺带，保证边界处的坐标也能读出来
    $band = 22
    $g.FillRectangle($edgeBrush, 0, 0, $iw, $band)
    $g.FillRectangle($edgeBrush, 0, 0, $band, $ih)

    $vx = 0
    while ($vx -le $iw) {
        $major = ((($vx % ($Spacing * $MajorEvery)) -eq 0))
        $pen = $penMinor
        if ($major) { $pen = $penMajor }
        $g.DrawLine($pen, $vx, 0, $vx, $ih)

        if ((-not $skipLabels) -and $labelCount -lt $MaxLabels) {
            if ($major -or ($Spacing -ge 50)) {
                $abs = $OriginX + $vx
                $text = [string]$abs
                $size = $g.MeasureString($text, $labelFont)
                $tx = $vx + 3
                if ($tx + $size.Width -gt $iw) { $tx = $vx - $size.Width - 3 }
                if ($tx -lt 0) { $tx = 0 }
                $g.FillRectangle($chipBrush, $tx, 2, $size.Width, $band - 4)
                $g.DrawString($text, $labelFont, $labelBrush, $tx, 3)
                $labelCount++
            }
        }
        $vx += $Spacing
    }

    $hy = 0
    while ($hy -le $ih) {
        $major = ((($hy % ($Spacing * $MajorEvery)) -eq 0))
        $pen = $penMinor
        if ($major) { $pen = $penMajor }
        $g.DrawLine($pen, 0, $hy, $iw, $hy)

        if ((-not $skipLabels) -and $labelCount -lt $MaxLabels) {
            if ($major -or ($Spacing -ge 50)) {
                $abs = $OriginY + $hy
                $text = [string]$abs
                $size = $g.MeasureString($text, $labelFont)
                $ty = $hy + 3
                if ($ty + $size.Height -gt $ih) { $ty = $hy - $size.Height - 3 }
                if ($ty -lt 0) { $ty = 0 }
                $g.FillRectangle($chipBrush, 2, $ty, $size.Width, $size.Height)
                $g.DrawString($text, $labelFont, $labelBrush, 2, $ty)
                $labelCount++
            }
        }
        $hy += $Spacing
    }

    $g.Dispose()
    $penMinor.Dispose(); $penMajor.Dispose()
    $labelFont.Dispose(); $labelBrush.Dispose(); $chipBrush.Dispose(); $edgeBrush.Dispose()

    if (-not $Out) {
        $Out = New-ScfFilePath -Prefix 'grid' -Extension 'png'
    }
    $outDir = Split-Path -Parent $Out
    if ($outDir -and -not (Test-Path $outDir)) {
        New-Item -ItemType Directory -Path $outDir -Force | Out-Null
    }
    $canvas.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)
    $canvas.Dispose()

    $result = @{
        ok     = $true
        action = 'grid'
        image  = [ordered]@{
            path   = $Out
            width  = $iw
            height = $ih
            format = 'png'
        }
        sourceImage = $Image
        grid = [ordered]@{
            spacing    = $Spacing
            majorEvery = $MajorEvery
            majorStep  = ($Spacing * $MajorEvery)
            originX    = $OriginX
            originY    = $OriginY
            labels     = (-not $skipLabels)
        }
        mapping = '屏幕坐标 = 图上读到的刻度值（标签已是绝对屏幕坐标，无需再次加上 origin）'
    }
    Complete-ScfLocated -Data $result
} catch {
    Fail-Scf -Code 'INTERNAL' -Message '叠加网格失败' -Detail ($_.Exception.Message + ' @ ' + $_.InvocationInfo.ScriptLineNumber)
}
