# Screen Coord Locator - (c) 2026. Commercial license, redistribution prohibited.
# uia.ps1 - 通过 UI Automation 遍历控件树，自动取得控件精确矩形
# 输出：单个 JSON 对象到 stdout

[CmdletBinding()]
param(
    [ValidateSet('windows', 'find', 'tree', 'point')]
    [string]$Action = 'windows',

    [string]$NameContains = '',
    [string]$TypeContains = '',
    [string]$AutomationIdContains = '',

    [int64]$Handle = 0,
    [int]$X = 0,
    [int]$Y = 0,

    [int]$MaxDepth = 6,
    [int]$MaxElements = 600,
    [int]$MaxWindows = 12,

    [switch]$IncludeOffscreen
)

. (Join-Path $PSScriptRoot 'lib\common.ps1')
. (Join-Path $PSScriptRoot 'lib\permit.ps1')

try {
    Assert-ScfWindows
    $script:ScfPermit = Assert-ScfPermit
    Initialize-ScfEnvironment -NeedForms -NeedUia
} catch {
    Fail-Scf -Code 'INTERNAL' -Message '初始化失败' -Detail $_.Exception.Message
}

function Get-ScfElementInfo {
    param($Element, [int]$Depth)

    $info = [ordered]@{
        name         = ''
        controlType  = ''
        automationId = ''
        className    = ''
        depth        = $Depth
        enabled      = $false
        offscreen    = $false
        usable       = $false
        rect         = $null
        center       = $null
    }
    try { $info.name = [string]$Element.Current.Name } catch { }
    try { $info.controlType = ([string]$Element.Current.ControlType.ProgrammaticName) -replace '^ControlType\.', '' } catch { }
    try { $info.automationId = [string]$Element.Current.AutomationId } catch { }
    try { $info.className = [string]$Element.Current.ClassName } catch { }
    try { $info.enabled = [bool]$Element.Current.IsEnabled } catch { }
    try { $info.offscreen = [bool]$Element.Current.IsOffscreen } catch { }

    try {
        $r = $Element.Current.BoundingRectangle
        if (-not $r.IsEmpty -and $r.Width -gt 0 -and $r.Height -gt 0) {
            $rx = [int][math]::Round($r.X)
            $ry = [int][math]::Round($r.Y)
            $rw = [int][math]::Round($r.Width)
            $rh = [int][math]::Round($r.Height)
            $info.rect = [ordered]@{ x = $rx; y = $ry; width = $rw; height = $rh }
            $info.center = [ordered]@{ x = ($rx + [int]($rw / 2)); y = ($ry + [int]($rh / 2)) }
        }
    } catch { }

    # 最小化窗口会被 Windows 放到 (±32000, ±32000) 之类的假坐标上，不能当真实落点用
    if (-not (Test-ScfRectSane -Rect $info.rect)) {
        if ($info.rect) { $info.rectRaw = $info.rect }
        $info.rect = $null
        $info.center = $null
        $info.offscreen = $true
        $info.usable = $false
    } else {
        $info.usable = $true
    }

    return $info
}

function Test-ScfElementMatch {
    param($Info)
    if ($NameContains -and ($Info.name -notlike ('*' + $NameContains + '*'))) { return $false }
    if ($TypeContains -and ($Info.controlType -notlike ('*' + $TypeContains + '*'))) { return $false }
    if ($AutomationIdContains -and ($Info.automationId -notlike ('*' + $AutomationIdContains + '*'))) { return $false }
    if (-not $IncludeOffscreen -and $Info.offscreen) { return $false }
    return $true
}

try {
    $root = [System.Windows.Automation.AutomationElement]::RootElement
    $walker = [System.Windows.Automation.TreeWalker]::ControlViewWalker
    $result = @()

    if ($Action -eq 'point') {
        $pt = New-Object System.Windows.Point($X, $Y)
        $el = $null
        try { $el = [System.Windows.Automation.AutomationElement]::FromPoint($pt) } catch { }
        if (-not $el) {
            Fail-Scf -Code 'NO_TARGET' -Message ('坐标 ({0}, {1}) 上没有取到任何控件' -f $X, $Y)
        }
        $chain = @()
        $cur = $el
        $guard = 0
        while ($cur -and $guard -lt 12) {
            $chain += (Get-ScfElementInfo -Element $cur -Depth $guard)
            try { $cur = $walker.GetParent($cur) } catch { $cur = $null }
            $guard++
        }
        Complete-ScfLocated -Data @{
            ok       = $true
            action   = 'point'
            point    = [ordered]@{ x = $X; y = $Y }
            element  = $chain[0]
            ancestors = $chain
            note     = 'ancestors[0] 为最内层控件，依次向上为父容器，可用于判断命中的是哪个窗口的哪一块。'
        }
        exit 0
    }

    if ($Action -eq 'windows') {
        $children = $root.FindAll([System.Windows.Automation.TreeScope]::Children,
                                  [System.Windows.Automation.Condition]::TrueCondition)
        $usableList = @()
        $ghostList = @()
        $handleHit = ($Handle -eq 0)
        foreach ($w in $children) {
            $info = Get-ScfElementInfo -Element $w -Depth 0
            $h = 0
            try { $h = [int64]$w.Current.NativeWindowHandle } catch { }
            # 指定了 -Handle 时只保留对应顶层窗口
            if ($Handle -ne 0 -and $h -ne $Handle) { continue }
            $handleHit = $true
            $info['handle'] = $h
            $info['process'] = Get-ScfProcessName -Handle ([IntPtr]$h)
            if ($info.usable) {
                $usableList += $info
            } else {
                if ((-not $IncludeOffscreen) -and (-not $info.name)) { continue }
                $ghostList += $info
            }
        }
        if (-not $handleHit) {
            Fail-Scf -Code 'NO_TARGET' -Message ('没有找到句柄为 {0} 的顶层窗口' -f $Handle)
        }
        $result = @($usableList) + @($ghostList)
        Complete-ScfLocated -Data @{
            ok       = $true
            action   = 'windows'
            count    = $result.Count
            usable   = $usableList.Count
            windows  = $result
            note     = 'usable=true 的窗口可直接点击；usable=false 的多为最小化或已隐藏窗口，没有有效坐标。'
        }
        exit 0
    }

    if ($Action -eq 'tree' -or $Action -eq 'find') {
        $hasFilter = ($NameContains -or $TypeContains -or $AutomationIdContains)
        $roots = @()
        if ($Action -eq 'tree') {
            $children = $root.FindAll([System.Windows.Automation.TreeScope]::Children,
                                      [System.Windows.Automation.Condition]::TrueCondition)
            foreach ($w in $children) {
                $h = 0
                try { $h = [int64]$w.Current.NativeWindowHandle } catch { }
                if ($Handle -eq 0 -or $h -eq $Handle) { $roots += $w }
                if ($Handle -ne 0 -and $h -eq $Handle) { break }
            }
            if ($roots.Count -eq 0) {
                Fail-Scf -Code 'NO_TARGET' -Message ('没有找到句柄为 {0} 的顶层窗口' -f $Handle)
            }
        } else {
            $children = $root.FindAll([System.Windows.Automation.TreeScope]::Children,
                                      [System.Windows.Automation.Condition]::TrueCondition)
            $n = 0
            foreach ($w in $children) {
                try { if ($w.Current.IsOffscreen) { continue } } catch { }
                $roots += $w
                $n++
                if ($n -ge $MaxWindows) { break }
            }
        }

        $visited = 0
        $truncated = $false

        foreach ($r in $roots) {
            if ($visited -ge $MaxElements) { $truncated = $true; break }

            $queue = New-Object System.Collections.Queue
            $queue.Enqueue(@{ el = $r; depth = 0 })

            while ($queue.Count -gt 0) {
                if ($visited -ge $MaxElements) { $truncated = $true; break }
                $node = $queue.Dequeue()
                $el = $node.el
                $d = [int]$node.depth
                $visited++

                $info = Get-ScfElementInfo -Element $el -Depth $d

                $isRoot = ($d -eq 0)
                # 非根节点必须命中过滤条件；根节点仅在「没有指定任何过滤条件」时随枚举通过。
                # 一旦指定了名称 / 类型 / 自动化 ID 过滤，顶层窗口也要参与匹配，
                # 否则结果里会混入所有无关顶层窗口，让 Agent 误以为命中。
                $matched = Test-ScfElementMatch -Info $info
                if ($matched -or ($isRoot -and -not $hasFilter)) {
                    if ($info.rect -ne $null -or $isRoot) {
                        $h = 0
                        try { $h = [int64]$el.Current.NativeWindowHandle } catch { }
                        if ($isRoot) {
                            $info['handle'] = $h
                            $info['process'] = Get-ScfProcessName -Handle ([IntPtr]$h)
                        }
                        $result += $info
                    }
                }

                if ($d -ge $MaxDepth) { continue }

                try {
                    $child = $walker.GetFirstChild($el)
                    while ($child) {
                        $queue.Enqueue(@{ el = $child; depth = ($d + 1) })
                        $child = $walker.GetNextSibling($child)
                        if ($queue.Count -gt ($MaxElements * 2)) { break }
                    }
                } catch { }
            }
        }

        # 指定了过滤条件却一个都没命中 = 没拿到坐标，属 NO_TARGET，不消费授权。
        # （无过滤的纯枚举至少会返回根节点，count 为 0 属异常，保持原样返回。）
        if ($hasFilter -and $result.Count -eq 0) {
            Fail-Scf -Code 'NO_TARGET' -Message '没有找到匹配的元素' `
                -Detail ('已扫描 {0} 个元素，条件：NameContains={1} / TypeContains={2} / AutomationIdContains={3}' `
                    -f $visited, $NameContains, $TypeContains, $AutomationIdContains)
        }

        Complete-ScfLocated -Data @{
            ok        = $true
            action    = $Action
            count     = $result.Count
            scanned   = $visited
            truncated = $truncated
            elements  = $result
            note      = 'rect 为绝对屏幕坐标，center 可直接交给 act.ps1 点击。'
        }
        exit 0
    }
} catch {
    Fail-Scf -Code 'INTERNAL' -Message 'UI Automation 查询失败' -Detail ($_.Exception.Message + ' @ ' + $_.InvocationInfo.ScriptLineNumber)
}
