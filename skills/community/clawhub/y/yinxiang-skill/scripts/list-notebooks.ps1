. "$PSScriptRoot\_common.ps1"

Invoke-YinxiangPost `
    -Uri "https://app.yinxiang.com/third/ai-chat-note/grpc-api/search/listNoteBooks" `
    -Body '{"source":"skill"}'
