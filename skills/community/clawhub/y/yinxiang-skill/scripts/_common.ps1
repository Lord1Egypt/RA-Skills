# 公共：多来源加载 Token（PowerShell / Windows）
# OpenClaw 自动注入 YX_AUTH_TOKEN；Claude Code / Codex / Cursor 从本地文件读取
$raw = Get-Content "$HOME\.config\yinxiang-skill\token" -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
$TOKEN = if ($raw) { $raw.Trim() } elseif ($env:YX_AUTH_TOKEN) { $env:YX_AUTH_TOKEN.Trim() }
if (-not $TOKEN) {
    Write-Output '{"code":1,"message":"未授权，请说「授权印象笔记」完成授权"}'
    exit 1
}

function Invoke-YinxiangPost {
    param(
        [Parameter(Mandatory)][string]$Uri,
        [Parameter(Mandatory)][string]$Body,
        [string]$ContentType = "application/json; charset=utf-8",
        [hashtable]$ExtraHeaders = @{}
    )

    $headers = @{ auth = $TOKEN }
    foreach ($key in $ExtraHeaders.Keys) {
        $headers[$key] = $ExtraHeaders[$key]
    }

    $response = Invoke-WebRequest `
        -Uri $Uri `
        -Method POST `
        -Headers $headers `
        -Body ([System.Text.Encoding]::UTF8.GetBytes($Body)) `
        -ContentType $ContentType `
        -UseBasicParsing

    if ($response.RawContentStream) {
        if ($response.RawContentStream.CanSeek) {
            $response.RawContentStream.Position = 0
        }
        $reader = New-Object System.IO.StreamReader($response.RawContentStream, [System.Text.Encoding]::UTF8)
        try {
            $reader.ReadToEnd()
        } finally {
            $reader.Dispose()
        }
    } else {
        $response.Content
    }
}
