# Screen Coord Locator - (c) 2026. Commercial license, redistribution prohibited.
# Screen Coordinate Locator - service authorization (pay-per-call gate)
# 本文件提供「授权前置」能力：向授权服务端申请一次性通行证，
# 无有效通行证时定位脚本必须拒绝执行（脱离服务端即不可用）。
# 约定：stdout 只允许出现一个 JSON 对象，其它信息一律走 stderr。

$script:ScfServiceBase = 'https://coord.weituoai.cn'
$script:ScfClientVersion = '1.2.0'

function Get-ScfPermitDir {
    $dir = Join-Path $env:TEMP 'screen-coord-locator'
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    return $dir
}

function Get-ScfPermitPath {
    return (Join-Path (Get-ScfPermitDir) 'permit.json')
}

function Get-ScfMachineId {
    if ($env:SCF_MACHINE_ID) { return $env:SCF_MACHINE_ID }
    if ($env:COMPUTERNAME) { return $env:COMPUTERNAME }
    return 'unknown'
}

function Enable-ScfTls {
    try {
        [Net.ServicePointManager]::SecurityProtocol = `
            [Net.SecurityProtocolType]::Tls12 -bor `
            [Net.SecurityProtocolType]::Tls11 -bor `
            [Net.SecurityProtocolType]::Tls
    } catch { }
}

# --- HTTP -------------------------------------------------------------------

function Invoke-ScfHttpJson {
    param(
        [Parameter(Mandatory = $true)][string]$Url,
        [string]$Method = 'POST',
        [string]$Body = '',
        [hashtable]$Headers = @{},
        [int]$TimeoutSec = 25
    )

    Enable-ScfTls
    try { Add-Type -AssemblyName System.Net.Http -ErrorAction Stop } catch { }

    $result = @{
        statusCode = 0
        body       = ''
        headers    = @{}
        transport  = 'ok'
    }

    $req = $null
    $client = $null
    $resp = $null
    try {
        $handler = New-Object System.Net.Http.HttpClientHandler
        $handler.AllowAutoRedirect = $true
        $client = New-Object System.Net.Http.HttpClient($handler)
        $client.Timeout = [TimeSpan]::FromSeconds($TimeoutSec)

        $verb = $Method.ToUpperInvariant()
        $httpMethod = [System.Net.Http.HttpMethod]::Post
        if ($verb -eq 'GET') { $httpMethod = [System.Net.Http.HttpMethod]::Get }
        elseif ($verb -eq 'PUT') { $httpMethod = [System.Net.Http.HttpMethod]::Put }

        $req = New-Object System.Net.Http.HttpRequestMessage($httpMethod, $Url)
        if ($Body) {
            $req.Content = New-Object System.Net.Http.StringContent(
                $Body, [System.Text.Encoding]::UTF8, 'application/json')
        }
        foreach ($k in $Headers.Keys) {
            [void]$req.Headers.TryAddWithoutValidation($k, [string]$Headers[$k])
        }

        $resp = $client.SendAsync($req).GetAwaiter().GetResult()
        $result.statusCode = [int]$resp.StatusCode
        $result.body = $resp.Content.ReadAsStringAsync().GetAwaiter().GetResult()

        foreach ($h in $resp.Headers) {
            $result.headers[$h.Key] = ($h.Value -join '')
        }
        return $result
    } catch {
        $result.transport = 'error'
        $result.body = $_.Exception.Message
        return $result
    } finally {
        if ($resp) { $resp.Dispose() }
        if ($req) { $req.Dispose() }
        if ($client) { $client.Dispose() }
    }
}

function Get-ScfHeaderValue {
    param(
        [Parameter(Mandatory = $true)][hashtable]$Headers,
        [Parameter(Mandatory = $true)][string]$Name
    )
    foreach ($k in $Headers.Keys) {
        if ($k -ieq $Name) { return [string]$Headers[$k] }
    }
    return ''
}

# --- 通行证本地缓存 ---------------------------------------------------------

function Read-ScfPermit {
    $path = Get-ScfPermitPath
    if (-not (Test-Path $path)) { return $null }
    try {
        $raw = Get-Content -Path $path -Raw -Encoding UTF8
        if (-not $raw) { return $null }
        $obj = $raw | ConvertFrom-Json
        $permit = [string]$obj.permit
        if (-not $permit) { return $null }
        $expiresAt = 0
        try { $expiresAt = [int64]$obj.expiresAtEpoch } catch { }
        return @{
            permit         = $permit
            machineId      = [string]$obj.machineId
            action         = [string]$obj.action
            expiresAtEpoch = $expiresAt
            expiresAt      = [string]$obj.expiresAt
            consumed       = [bool]$obj.consumed
        }
    } catch {
        return $null
    }
}

function Save-ScfPermit {
    param(
        [Parameter(Mandatory = $true)][string]$Permit,
        [Parameter(Mandatory = $true)][string]$MachineId,
        [string]$Action = 'locate',
        [int64]$ExpiresAtEpoch = 0,
        [string]$ExpiresAt = '',
        [bool]$Consumed = $false
    )
    $payload = [ordered]@{
        permit         = $Permit
        machineId      = $MachineId
        action         = $Action
        expiresAtEpoch = $ExpiresAtEpoch
        expiresAt      = $ExpiresAt
        consumed       = $Consumed
    }
    $path = Get-ScfPermitPath
    ($payload | ConvertTo-Json -Compress) | Set-Content -Path $path -Encoding UTF8 -NoNewline
}

function Clear-ScfPermit {
    $path = Get-ScfPermitPath
    if (Test-Path $path) { Remove-Item -Path $path -Force -ErrorAction SilentlyContinue }
}

function Test-ScfPermitFresh {
    param([Parameter(Mandatory = $true)][hashtable]$Record)
    if ($Record.consumed) { return $false }
    if (-not $Record.permit) { return $false }
    if ($Record.expiresAtEpoch -gt 0) {
        $now = [int64][DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
        if ($now -ge $Record.expiresAtEpoch) { return $false }
    }
    return $true
}

# --- 向服务端申请授权 -------------------------------------------------------

function Request-ScfPermit {
    param([string]$Action = 'locate')

    $machineId = Get-ScfMachineId
    $url = '{0}/v1/authorize' -f $script:ScfServiceBase
    $body = @{
        machine_id     = $machineId
        action         = $Action
        client_version = $script:ScfClientVersion
    } | ConvertTo-Json -Compress

    $r = Invoke-ScfHttpJson -Url $url -Method 'POST' -Body $body -Headers @{
        'Accept'       = 'application/json'
        'X-Machine-Id' = $machineId
    }

    if ($r.transport -eq 'error') {
        return @{
            ok        = $false
            error     = @{
                code    = 'NETWORK'
                message = '无法连接授权服务，请检查网络后重试'
                detail  = [string]$r.body
            }
        }
    }

    if ($r.statusCode -eq 200) {
        $data = $null
        try { $data = $r.body | ConvertFrom-Json } catch { }
        if (-not $data -or -not $data.permit) {
            return @{
                ok    = $false
                error = @{ code = 'BAD_RESPONSE'; message = '授权服务返回内容异常' }
            }
        }
        $ttl = 600
        try { $ttl = [int]$data.ttlSeconds } catch { }
        $expEpoch = [int64][DateTimeOffset]::UtcNow.ToUnixTimeSeconds() + $ttl
        Save-ScfPermit -Permit ([string]$data.permit) -MachineId $machineId `
            -Action $Action -ExpiresAtEpoch $expEpoch -ExpiresAt ([string]$data.expiresAt)

        $out = [ordered]@{
            ok             = $true
            permit         = [string]$data.permit
            expiresAt      = [string]$data.expiresAt
            ttlSeconds     = $ttl
            reason         = [string]$data.reason
            machineId      = $machineId
        }
        if ($data.PSObject.Properties.Name -contains 'freeQuotaLeft') {
            $out['freeQuotaLeft'] = [int]$data.freeQuotaLeft
        }
        return $out
    }

    if ($r.statusCode -eq 402) {
        $pn = Get-ScfHeaderValue -Headers $r.headers -Name 'Payment-Needed'
        $bill = @{}
        if ($pn) {
            try {
                $b64 = $pn.Replace('-', '+').Replace('_', '/')
                switch ($b64.Length % 4) {
                    2 { $b64 += '==' }
                    3 { $b64 += '=' }
                }
                $json = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($b64))
                $obj = $json | ConvertFrom-Json
                $p = $obj.protocol
                if ($p) {
                    $bill = @{
                        amount       = [string]$p.amount
                        currency     = [string]$p.currency
                        goodsName    = [string]$p.goods_name
                        outTradeNo   = [string]$p.out_trade_no
                        payBefore    = [string]$p.pay_before
                        resourceId   = [string]$p.resource_id
                        sellerId     = [string]$p.seller_id
                        serviceId    = [string]$p.service_id
                        signatureAlg = [string]$p.seller_sign_type
                    }
                }
                return @{
                    ok    = $false
                    error = @{
                        code    = 'PAYMENT_REQUIRED'
                        message = ('本次定位需支付 {0} {1}，请在支付宝中完成授权支付后重试' -f `
                            $bill.amount, $bill.currency)
                        detail  = $bill.goodsName
                    }
                    bill  = $bill
                }
            } catch {
                return @{
                    ok    = $false
                    error = @{ code = 'PAYMENT_REQUIRED'; message = '本次定位需要付费授权，未获取到有效账单' }
                }
            }
        }
        return @{
            ok    = $false
            error = @{
                code    = 'PAYMENT_REQUIRED'
                message = '本次定位需要付费授权，未获取到有效账单'
                detail  = [string]$r.body
            }
        }
    }

    if ($r.statusCode -eq 409) {
        return @{
            ok    = $false
            error = @{ code = 'REPLAY'; message = '该支付凭证已被使用，请重新申请授权' }
        }
    }

    return @{
        ok    = $false
        error = @{
            code    = 'SERVER_ERROR'
            message = ('授权服务返回异常状态 {0}' -f $r.statusCode)
            detail  = [string]$r.body
        }
    }
}

# --- 前置校验（定位脚本调用）------------------------------------------------

function Assert-ScfPermit {
    $rec = Read-ScfPermit
    if (-not $rec) {
        Fail-Scf -Code 'NO_PERMIT' `
            -Message '缺少定位授权，请先运行 license.ps1 申请授权（每台设备前 10 次免费）' `
            -Detail 'scripts/license.ps1 -Action locate' -ExitCode 3
    }
    if ($rec.consumed) {
        Fail-Scf -Code 'PERMIT_USED' `
            -Message '本次授权已使用，请重新运行 license.ps1 申请新的授权' `
            -Detail 'scripts/license.ps1 -Action locate' -ExitCode 3
    }
    if (-not (Test-ScfPermitFresh -Record $rec)) {
        Clear-ScfPermit
        Fail-Scf -Code 'PERMIT_EXPIRED' `
            -Message '定位授权已过期，请重新运行 license.ps1 申请授权' `
            -Detail 'scripts/license.ps1 -Action locate' -ExitCode 3
    }
    return $rec
}

# --- 成功后消费通行证 -------------------------------------------------------

function Complete-ScfPermit {
    param([string]$Note = '')
    $rec = Read-ScfPermit
    if (-not $rec) { return }

    # 先在本地标记为已消费，保证同一授权绝不会被重复使用；
    # 服务端确认只是回执，任何网络异常都不应影响本次定位结果的交付。
    Save-ScfPermit -Permit $rec.permit -MachineId $rec.machineId -Action $rec.action `
        -ExpiresAtEpoch $rec.expiresAtEpoch -ExpiresAt $rec.expiresAt -Consumed $true

    try {
        $url = '{0}/v1/permit/check' -f $script:ScfServiceBase
        $body = @{
            permit     = $rec.permit
            machine_id = (Get-ScfMachineId)
            note       = $Note
        } | ConvertTo-Json -Compress

        $r = Invoke-ScfHttpJson -Url $url -Method 'POST' -Body $body
        if ($r.transport -ne 'ok' -or $r.statusCode -ne 200) {
            $warn = 'warn: permit check did not confirm (transport={0} status={1})' -f @(
                $r.transport, $r.statusCode)
            [Console]::Error.WriteLine($warn)
        }
    } catch {
        [Console]::Error.WriteLine('warn: permit check failed: ' + $_.Exception.Message)
    }
}

# 成功交付坐标/读图结果时使用：先消费本次授权，再输出结果。
# 失败路径一律走 Fail-Scf，不消费授权，于是同一次授权内允许降级重试。
function Complete-ScfLocated {
    param(
        [Parameter(Mandatory = $true)][hashtable]$Data,
        [int]$ExitCode = 0,
        [string]$Note = ''
    )
    Complete-ScfPermit -Note $Note
    Complete-Scf -Data $Data -ExitCode $ExitCode
}
