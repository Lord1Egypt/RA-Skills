# yufluentcn-chat-assist

跨境电商 **Amazon / Shopify / TikTok Shop** 买家消息回复草稿，经 Harness `chat_reply` + `messaging-guard` 云端执行。

## 调用

```powershell
cd skills\yufluentcn-chat-assist
pip install -r requirements.txt
$env:TOKENAPI_KEY = "tk-你的密钥"

python scripts\run.py `
  --message "Where is my order?" `
  --platform amazon `
  --lang en `
  --order-context "Order #123, shipped May 20, in transit"
```

Agent 工作流与输入格式见 [SKILL.md](./SKILL.md)。

API：`POST /v1/skills/chat-assist/run` · 必填字段：`message`
