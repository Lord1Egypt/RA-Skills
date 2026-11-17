. "$PSScriptRoot\_common.ps1"

Invoke-YinxiangPost `
    -Uri "https://app.yinxiang.com/third/ai-chat-note/grpc-api/search/searchNotesByFilter" `
    -Body '{"source":"skill","resultSpec":{"includeContent":false,"includeResources":false,"includeTags":true,"includeResourceContent":false}}'
