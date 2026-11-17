# 三峰智能家居 — PowerShell 内部函数
# 由 SKILL.md 在运行时 dot-source 加载。
# {baseDir} 由 WorkBuddy 替换为技能目录的绝对路径。
param(
    [string]$BaseDir = '{baseDir}'
)

# 加载 DPAPI 程序集（若环境中 Add-Type 被限制，可改用 Python ctypes 替代方案）
try { Add-Type -AssemblyName System.Security } catch {}

$statePath = Join-Path $BaseDir 'state.json'

# PowerShell 5.1 默认使用 TLS 1.0，现代 API 需要 TLS 1.2+
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

function Protect-AuthToken {
    param([Parameter(Mandatory = $true)][string]$Value)
    $plainBytes = [System.Text.Encoding]::UTF8.GetBytes($Value)
    try {
        $cipherBytes = [System.Security.Cryptography.ProtectedData]::Protect(
            $plainBytes,
            $null,
            [System.Security.Cryptography.DataProtectionScope]::CurrentUser
        )
        return [Convert]::ToBase64String($cipherBytes)
    }
    finally {
        [Array]::Clear($plainBytes, 0, $plainBytes.Length)
    }
}

function Unprotect-AuthToken {
    param([Parameter(Mandatory = $true)][string]$Value)
    $cipherBytes = [Convert]::FromBase64String($Value)
    $plainBytes = [System.Security.Cryptography.ProtectedData]::Unprotect(
        $cipherBytes,
        $null,
        [System.Security.Cryptography.DataProtectionScope]::CurrentUser
    )
    try {
        return [System.Text.Encoding]::UTF8.GetString($plainBytes)
    }
    finally {
        [Array]::Clear($plainBytes, 0, $plainBytes.Length)
    }
}

function Read-SufnState {
    if (-not (Test-Path -LiteralPath $statePath)) {
        return $null
    }
    try {
        return Get-Content -LiteralPath $statePath -Raw -Encoding UTF8 | ConvertFrom-Json
    }
    catch {
        return $null
    }
}

function Write-SufnState {
    param([Parameter(Mandatory = $true)]$State)
    $json = $State | ConvertTo-Json -Depth 12 -Compress
    $tempPath = "$statePath.tmp"
    [System.IO.File]::WriteAllText($tempPath, $json, [System.Text.Encoding]::UTF8)
    Move-Item -LiteralPath $tempPath -Destination $statePath -Force
}

function Invoke-SufnPlatform {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)]$Body,
        [string]$AuthToken,
        [string]$Method = 'POST'
    )

    # TLS 1.2+（函数级别保障，即使模块级设置被覆盖）
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

    $params = @{
        Method      = $Method
        Uri         = "https://open.aibasis.cc$Path"
        ContentType = 'application/json'
        ErrorAction = 'Stop'
    }
    if ($Method -eq 'POST' -and $Body) {
        $params.Body = ($Body | ConvertTo-Json -Depth 12 -Compress)
    }
    if ($AuthToken) {
        $params.Headers = @{ Authorization = "Bearer $AuthToken" }
    }

    try {
        $response = Invoke-RestMethod @params
        # 检查业务层返回码
        if ($response.PSObject.Properties.Name -contains 'code' -and $response.code -ne 0) {
            return $null
        }
        return $response
    }
    catch {
        return $null
    }
}

function Get-SufnTimestamp {
    return [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
}
