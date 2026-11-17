param([Parameter(Mandatory)][string]$Token)
$dir = "$HOME\.config\yinxiang-skill"
if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
Set-Content -Path "$dir\token" -Value $Token -NoNewline -Encoding UTF8
Write-Host "Token 已保存到 $dir\token"
