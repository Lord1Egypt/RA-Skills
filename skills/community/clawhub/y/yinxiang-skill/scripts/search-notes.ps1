param(
    [string]$Keyword = "",
    [string]$Json = ""
)
. "$PSScriptRoot\_common.ps1"

$resultSpec = @{
    includeContent = $false
    includeResources = $false
    includeTags = $true
    includeResourceContent = $false
}

if ($Json) {
    try {
        $bodyObject = $Json | ConvertFrom-Json
        $bodyObject | Add-Member -NotePropertyName source -NotePropertyValue "skill" -Force
        if (-not $bodyObject.PSObject.Properties.Name.Contains("resultSpec")) {
            $bodyObject | Add-Member -NotePropertyName resultSpec -NotePropertyValue $resultSpec
        }
        $body = $bodyObject | ConvertTo-Json -Compress -Depth 10
    } catch {
        Write-Output '{"code":1,"message":"查询JSON格式错误"}'
        exit 1
    }
} elseif ($Keyword) {
    $body = @{
        keyword = $Keyword
        source = "skill"
        resultSpec = $resultSpec
    } | ConvertTo-Json -Compress -Depth 10
} else {
    Write-Output "用法: .\search-notes.ps1 -Keyword <关键词> 或 .\search-notes.ps1 -Json '<查询JSON>'"
    exit 1
}

Invoke-YinxiangPost `
    -Uri "https://app.yinxiang.com/third/ai-chat-note/grpc-api/search/searchNotesByFilter" `
    -Body $body
