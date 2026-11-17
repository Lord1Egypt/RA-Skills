# HTTP 请求示例

```bash
API_ROOT="${AI_SKILLS_API_URL:-https://ai-skills.open-idea.net}/api/v1"

curl --fail-with-body "$API_ROOT/uyghur-ai/translation" \
  -H "Authorization: Bearer ${UYGHUR_AI_SKILL_API_KEY:-$AI_SKILLS_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: uyghur-translate-001" \
  -d '{"from":"zh","to":"ug","content":"你好，世界。"}'
```

```bash
curl --fail-with-body "$API_ROOT/uyghur-ai/chat/completions" \
  -H "Authorization: Bearer ${UYGHUR_AI_SKILL_API_KEY:-$AI_SKILLS_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: uyghur-chat-001" \
  -d '{"messages":[{"role":"user","content":"请用维吾尔语写一句欢迎语。"}],"temperature":0.4}'
```

```bash
curl --fail-with-body "$API_ROOT/uyghur-ai/pdf/translation" \
  -H "Authorization: Bearer ${UYGHUR_AI_SKILL_API_KEY:-$AI_SKILLS_API_KEY}" \
  -H "Idempotency-Key: uyghur-pdf-001" \
  -F "file=@document.pdf" -F "from=ug" -F "to=zh" -F "mode=all_text"
```

图片 OCR 翻译使用 multipart/form-data；每次新图片都生成唯一幂等键：

```bash
IMAGE_REQUEST_KEY="uyghur-image-$(date +%s)-$RANDOM"

curl --fail-with-body "$API_ROOT/uyghur-ai/image/translation" \
  -H "Authorization: Bearer ${UYGHUR_AI_SKILL_API_KEY:-$AI_SKILLS_API_KEY}" \
  -H "Idempotency-Key: $IMAGE_REQUEST_KEY" \
  -F "file=@notice.png" \
  -F "from=ug" \
  -F "to=zh"
```

成功计费头为 `X-AI-Skills-Billing-Currency`、`X-AI-Skills-Billing-Charged`、
`X-AI-Skills-Billing-Balance`。固定幂等键仅为示例；生产调用应使用 UUID 等唯一值。
文件只能在用户明确提供时上传；绝不把文件字节或 Base64 Data URL 写入日志或对话正文。
