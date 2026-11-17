param([Parameter(Mandatory)][string]$BookName)
. "$PSScriptRoot\_common.ps1"

$body = @{ bookName = $BookName; source = "skill" } | ConvertTo-Json -Compress

Invoke-YinxiangPost `
    -Uri "https://app.yinxiang.com/third/third-party-note-service/restful/v1/createNotebookFromMCP" `
    -Body $body
