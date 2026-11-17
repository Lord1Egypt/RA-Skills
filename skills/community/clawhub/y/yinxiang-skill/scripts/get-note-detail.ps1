param([Parameter(Mandatory)][string]$Guid)
. "$PSScriptRoot\_common.ps1"

$body = "{`"guid`":`"$Guid`",`"source`":`"skill`",`"resultSpec`":{`"includeContent`":true,`"includeResources`":false,`"includeTags`":true,`"includeResourceContent`":false}}"

Invoke-YinxiangPost `
    -Uri "https://app.yinxiang.com/third/ai-chat-note/grpc-api/search/getNoteDetail" `
    -Body $body
