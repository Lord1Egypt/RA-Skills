param(
    [Parameter(Mandatory)][string]$NoteGuid,
    [string]$Title = "",
    [string]$Content = "",
    [string]$NotebookGuid = "",
    [AllowEmptyCollection()][string[]]$TagNames,
    [switch]$ClearTags
)
. "$PSScriptRoot\_common.ps1"

$body = @{ noteGuid = $NoteGuid; source = "skill" }
if ($Title) { $body.title = $Title }
if ($Content) { $body.content = $Content }
if ($NotebookGuid) { $body.notebookGuid = $NotebookGuid }
if ($ClearTags -or ($PSBoundParameters.ContainsKey("TagNames") -and $TagNames.Count -eq 0)) {
    $body.clearTags = $true
} elseif ($PSBoundParameters.ContainsKey("TagNames")) {
    $body.tagNames = $TagNames
}
$bodyJson = $body | ConvertTo-Json -Compress

Invoke-YinxiangPost `
    -Uri "https://app.yinxiang.com/third/third-party-note-service/restful/v1/updateNoteFromMCP" `
    -Body $bodyJson
