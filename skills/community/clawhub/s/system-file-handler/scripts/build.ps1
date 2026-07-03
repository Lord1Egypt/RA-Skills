# 从 go-fs-mcp 仓库根目录构建 server 与 skill 二进制。
# 用法：.\publish-skill\scripts\build.ps1
$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $Root

if (-not $env:GOPROXY) {
    $env:GOPROXY = "https://goproxy.cn,direct"
}

Write-Host "==> go mod tidy"
go mod tidy

Write-Host "==> build go-fs-mcp-server"
go build -o go-fs-mcp-server\go-fs-mcp-server.exe .\go-fs-mcp-server\cmd\server

Write-Host "==> build go-fs-mcp-skill"
go build -o go-fs-mcp-skill\go-fs-mcp-skill.exe .\go-fs-mcp-skill\cmd\skill

Write-Host "==> done"
Write-Host "    server: $Root\go-fs-mcp-server\go-fs-mcp-server.exe"
Write-Host "    skill:  $Root\go-fs-mcp-skill\go-fs-mcp-skill.exe"
Write-Host ""
Write-Host "Next: copy binaries to your OpenClaw skill dir and edit skill.json mcp_command."
