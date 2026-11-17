# Screen Coord Locator - (c) 2026. Commercial license, redistribution prohibited.
# pick.ps1 - 取景遮罩：由用户点选或框选，得到绝对屏幕坐标
# 输出：单个 JSON 对象到 stdout

[CmdletBinding()]
param(
    [ValidateSet('point', 'rect')]
    [string]$Mode = 'point',

    [int]$TimeoutMs = 0,

    [int]$MagnifierSize = 205,
    [int]$MagnifierZoom = 5,

    [switch]$NoVeil,
    [switch]$AllowRightClickPick
)

. (Join-Path $PSScriptRoot 'lib\common.ps1')
. (Join-Path $PSScriptRoot 'lib\permit.ps1')

try {
    Assert-ScfWindows
    $script:ScfPermit = Assert-ScfPermit
    Initialize-ScfEnvironment -NeedForms -NeedDrawing
} catch {
    Fail-Scf -Code 'INTERNAL' -Message '初始化失败' -Detail $_.Exception.Message
}

try {
    $vs = [System.Windows.Forms.SystemInformation]::VirtualScreen

    # 放大镜要用到桌面底图，必须在遮罩显示之前拍，否则会把遮罩自己拍进去
    $script:bg = New-Object System.Drawing.Bitmap($vs.Width, $vs.Height)
    $bgGfx = [System.Drawing.Graphics]::FromImage($script:bg)
    $bgGfx.CopyFromScreen($vs.X, $vs.Y, 0, 0, (New-Object System.Drawing.Size($vs.Width, $vs.Height)))
    $bgGfx.Dispose()

    # 统一提到 script 作用域，保证事件回调里读得到
    $script:vsX = $vs.X
    $script:vsY = $vs.Y
    $script:vsW = $vs.Width
    $script:vsH = $vs.Height
    $script:mode = $Mode
    $script:magSize = $MagnifierSize
    $script:magZoom = $MagnifierZoom
    $script:allowRightPick = [bool]$AllowRightClickPick
    $script:veilAlpha = 55
    if ($NoVeil) { $script:veilAlpha = 0 }

    $script:cursor = New-Object System.Drawing.Point(0, 0)
    $script:dragging = $false
    $script:startPt = New-Object System.Drawing.Point(0, 0)
    $script:endPt = New-Object System.Drawing.Point(0, 0)
    $script:finished = $false
    $script:canceled = $false
    $script:resultPoint = $null
    $script:resultRect = $null
    $script:deadline = [DateTime]::MaxValue
    if ($TimeoutMs -gt 0) { $script:deadline = [DateTime]::Now.AddMilliseconds($TimeoutMs) }

    $keyColor = [System.Drawing.Color]::FromArgb(1, 1, 1)

    $form = New-Object System.Windows.Forms.Form
    $form.FormBorderStyle = [System.Windows.Forms.FormBorderStyle]::None
    $form.StartPosition = [System.Windows.Forms.FormStartPosition]::Manual
    $form.Location = New-Object System.Drawing.Point($script:vsX, $script:vsY)
    $form.Size = New-Object System.Drawing.Size($script:vsW, $script:vsH)
    $form.TopMost = $true
    $form.ShowInTaskbar = $false
    $form.KeyPreview = $true
    $form.BackColor = $keyColor
    $form.TransparencyKey = $keyColor
    $form.Text = '屏幕坐标助手 - 取景'
    Set-ScfDoubleBuffered -Control $form

    $script:fontCoord = New-Object System.Drawing.Font('Consolas', 20, [System.Drawing.FontStyle]::Bold)
    $script:fontHint = New-Object System.Drawing.Font('Microsoft YaHei', 11)
    $script:fontSmall = New-Object System.Drawing.Font('Consolas', 10, [System.Drawing.FontStyle]::Bold)

    $script:brushText = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 0, 235, 130))
    $script:brushHint = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 235, 235, 235))
    $script:brushPanel = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(228, 22, 22, 30))
    $script:brushVeil = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb($script:veilAlpha, 0, 0, 0))
    $script:penCross = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(220, 0, 235, 130), 1)
    $script:penPanel = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 90, 90, 115), 1)
    $script:penMark = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 255, 90, 60), 1)
    $script:penRect = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 255, 200, 60), 2)

    $form.Add_Paint({
        param($sender, $e)
        $g = $e.Graphics
        $cw = $form.ClientSize.Width
        $ch = $form.ClientSize.Height

        if ($script:veilAlpha -gt 0) { $g.FillRectangle($script:brushVeil, 0, 0, $cw, $ch) }

        $cx = $script:cursor.X - $script:vsX
        $cy = $script:cursor.Y - $script:vsY

        if ($script:mode -eq 'rect' -and $script:dragging) {
            $sx = $script:startPt.X - $script:vsX
            $sy = $script:startPt.Y - $script:vsY
            $rx = [math]::Min($sx, $cx); $ry = [math]::Min($sy, $cy)
            $rw = [math]::Abs($cx - $sx); $rh = [math]::Abs($cy - $sy)
            if ($rw -gt 0 -and $rh -gt 0) {
                $g.DrawRectangle($script:penRect, $rx, $ry, $rw, $rh)
                $label = '{0} x {1}' -f $rw, $rh
                $sz = $g.MeasureString($label, $script:fontSmall)
                $ty = $ry - 20
                if ($ty -lt 0) { $ty = $ry + 2 }
                $g.FillRectangle($script:brushPanel, $rx, $ty, ($sz.Width + 8), 18)
                $g.DrawString($label, $script:fontSmall, $script:brushHint, ($rx + 4), ($ty + 1))
            }
        }

        $arm = 28
        $g.DrawLine($script:penCross, ($cx - $arm), $cy, ($cx + $arm), $cy)
        $g.DrawLine($script:penCross, $cx, ($cy - $arm), $cx, ($cy + $arm))
        $g.DrawRectangle($script:penMark, ($cx - 3), ($cy - 3), 6, 6)

        $half = [int]($script:magSize / 2)
        $mx = $cx + 34
        $my = $cy + 34
        if (($mx + $script:magSize) -gt $cw) { $mx = $cx - $script:magSize - 34 }
        if (($my + $script:magSize) -gt $ch) { $my = $cy - $script:magSize - 34 }
        if ($mx -lt 0) { $mx = 0 }
        if ($my -lt 0) { $my = 0 }

        $srcSize = [int]($script:magSize / $script:magZoom)
        if ($srcSize -lt 5) { $srcSize = 5 }
        $srcHalf = [int]($srcSize / 2)

        $g.FillRectangle($script:brushPanel, $mx, $my, $script:magSize, $script:magSize)
        try {
            $destRect = New-Object System.Drawing.Rectangle($mx, $my, $script:magSize, $script:magSize)
            $srcRect = New-Object System.Drawing.Rectangle(
                ($script:cursor.X - $srcHalf - $script:vsX),
                ($script:cursor.Y - $srcHalf - $script:vsY),
                $srcSize, $srcSize)
            $g.DrawImage($script:bg, $destRect, $srcRect, [System.Drawing.GraphicsUnit]::Pixel)
        } catch { }
        $g.DrawRectangle($script:penPanel, $mx, $my, $script:magSize, $script:magSize)
        $midX = $mx + $half
        $midY = $my + $half
        $g.DrawLine($script:penMark, ($midX - 10), $midY, ($midX + 10), $midY)
        $g.DrawLine($script:penMark, $midX, ($midY - 10), $midX, ($midY + 10))

        $coordText = 'X: {0}   Y: {1}' -f $script:cursor.X, $script:cursor.Y
        $sz2 = $g.MeasureString($coordText, $script:fontCoord)
        $px = $cx + 34
        $py = $cy - 76
        if ($py -lt 4) { $py = $cy + 40 }
        if (($px + $sz2.Width + 16) -gt $cw) { $px = $cw - $sz2.Width - 20 }
        if ($px -lt 4) { $px = 4 }
        $g.FillRectangle($script:brushPanel, $px, $py, ($sz2.Width + 16), ($sz2.Height + 10))
        $g.DrawRectangle($script:penPanel, $px, $py, ($sz2.Width + 16), ($sz2.Height + 10))
        $g.DrawString($coordText, $script:fontCoord, $script:brushText, ($px + 8), ($py + 5))

        $hint = '左键确定   右键 / ESC 取消'
        if ($script:mode -eq 'rect') { $hint = '按住左键拖拽框选   右键 / ESC 取消' }
        if ($script:allowRightPick) { $hint = '左键 / 右键确定   ESC 取消' }
        $sz3 = $g.MeasureString($hint, $script:fontHint)
        $hx = [int](($cw - $sz3.Width) / 2)
        $g.FillRectangle($script:brushPanel, $hx, 24, $sz3.Width, $sz3.Height)
        $g.DrawString($hint, $script:fontHint, $script:brushHint, $hx, 24)
    })

    $form.Add_MouseMove({
        param($sender, $e)
        $script:cursor = New-Object System.Drawing.Point(($script:vsX + $e.X), ($script:vsY + $e.Y))
        if ($script:mode -eq 'rect' -and $script:dragging) { $script:endPt = $script:cursor }
        $form.Invalidate()
    })

    $form.Add_MouseDown({
        param($sender, $e)
        $script:cursor = New-Object System.Drawing.Point(($script:vsX + $e.X), ($script:vsY + $e.Y))

        if ($e.Button -eq [System.Windows.Forms.MouseButtons]::Right) {
            if ($script:allowRightPick) {
                $script:resultPoint = $script:cursor
                $script:finished = $true
            } else {
                $script:canceled = $true
            }
            $form.Close()
            return
        }

        if ($e.Button -eq [System.Windows.Forms.MouseButtons]::Left) {
            if ($script:mode -eq 'point') {
                $script:resultPoint = $script:cursor
                $script:finished = $true
                $form.Close()
            } else {
                $script:dragging = $true
                $script:startPt = $script:cursor
                $script:endPt = $script:cursor
            }
        }
    })

    $form.Add_MouseUp({
        param($sender, $e)
        if ($e.Button -ne [System.Windows.Forms.MouseButtons]::Left) { return }
        if ($script:mode -ne 'rect' -or -not $script:dragging) { return }

        $script:dragging = $false
        $script:endPt = New-Object System.Drawing.Point(($script:vsX + $e.X), ($script:vsY + $e.Y))

        $rx = [math]::Min($script:startPt.X, $script:endPt.X)
        $ry = [math]::Min($script:startPt.Y, $script:endPt.Y)
        $rw = [math]::Abs($script:endPt.X - $script:startPt.X)
        $rh = [math]::Abs($script:endPt.Y - $script:startPt.Y)

        if ($rw -lt 4 -or $rh -lt 4) {
            $script:resultPoint = $script:endPt
        } else {
            $script:resultRect = [ordered]@{ x = $rx; y = $ry; width = $rw; height = $rh }
        }
        $script:finished = $true
        $form.Close()
    })

    $form.Add_KeyDown({
        param($sender, $e)
        if ($e.KeyCode -eq [System.Windows.Forms.Keys]::Escape) {
            $script:canceled = $true
            $form.Close()
        }
    })

    $timer = New-Object System.Windows.Forms.Timer
    $timer.Interval = 30
    $timer.Add_Tick({
        $p = [System.Windows.Forms.Cursor]::Position
        if ($p.X -ne $script:cursor.X -or $p.Y -ne $script:cursor.Y) {
            $script:cursor = New-Object System.Drawing.Point($p.X, $p.Y)
            if ($script:mode -eq 'rect' -and $script:dragging) { $script:endPt = $script:cursor }
            $form.Invalidate()
        }
        if ([DateTime]::Now -gt $script:deadline) {
            $script:canceled = $true
            $form.Close()
        }
    })

    $form.Add_Shown({
        $form.Activate()
        $timer.Start()
    })
    $form.Add_FormClosed({
        $timer.Stop()
        $timer.Dispose()
    })

    [void]$form.ShowDialog()

    $canceled = $script:canceled
    $point = $script:resultPoint
    $rect = $script:resultRect
    $done = $script:finished

    # 先释放 GDI 资源，避免长时间占用
    $script:fontCoord.Dispose(); $script:fontHint.Dispose(); $script:fontSmall.Dispose()
    $script:brushText.Dispose(); $script:brushHint.Dispose(); $script:brushPanel.Dispose()
    $script:brushVeil.Dispose()
    $script:penCross.Dispose(); $script:penPanel.Dispose(); $script:penMark.Dispose(); $script:penRect.Dispose()
    $script:bg.Dispose()
    $form.Dispose()

    if ($canceled -or (-not $done)) {
        Fail-Scf -Code 'CANCELED' -Message '用户取消了取景'
    }

    if ($rect) {
        Complete-ScfLocated -Data @{
            ok       = $true
            action   = 'pick'
            mode     = 'rect'
            canceled = $false
            rect     = $rect
            center   = [ordered]@{
                x = ($rect.x + [int]($rect.width / 2))
                y = ($rect.y + [int]($rect.height / 2))
            }
            points   = @()
        }
    }

    if ($point) {
        Complete-ScfLocated -Data @{
            ok       = $true
            action   = 'pick'
            mode     = 'point'
            canceled = $false
            points   = @([ordered]@{ x = $point.X; y = $point.Y })
            rect     = $null
        }
    }

    Fail-Scf -Code 'CANCELED' -Message '取景未取得有效结果'
} catch {
    Fail-Scf -Code 'INTERNAL' -Message '取景失败' -Detail ($_.Exception.Message + ' @ ' + $_.InvocationInfo.ScriptLineNumber)
}
