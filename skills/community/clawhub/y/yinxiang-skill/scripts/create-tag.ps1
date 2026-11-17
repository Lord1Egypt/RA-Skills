param([Parameter(Mandatory)][string]$TagName)
. "$PSScriptRoot\_common.ps1"

$body = @{ tagName = $TagName; source = "skill" } | ConvertTo-Json -Compress

Invoke-YinxiangPost `
    -Uri "https://app.yinxiang.com/third/third-party-note-service/restful/v1/createTagFromMCP" `
    -Body $body
