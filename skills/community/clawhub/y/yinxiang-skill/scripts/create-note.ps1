param(
    [Parameter(Mandatory)][string]$Title,
    [Parameter(Mandatory)][string]$Content,
    [string]$NotebookGuid = "",
    [string[]]$TagNames = @()
)
. "$PSScriptRoot\_common.ps1"

$body = @{ title = $Title; content = $Content; source = "skill" }
if ($NotebookGuid) { $body.notebookGuid = $NotebookGuid }
if ($TagNames.Count -gt 0) { $body.tagNames = $TagNames }
$bodyJson = $body | ConvertTo-Json -Compress

Invoke-YinxiangPost `
    -Uri "https://app.yinxiang.com/third/third-party-note-service/restful/v1/createNoteFromMCP" `
    -Body $bodyJson
