# HTTP 请求示例

```bash
API_ROOT="${AI_SKILLS_API_URL:-https://ai-skills.open-idea.net}/api/v1"
REQUEST_KEY="tibetan-$(date +%s)-translate"

curl --fail-with-body "$API_ROOT/tibetan-ai/translation" \
  -H "Authorization: Bearer ${TIBETAN_AI_SKILL_API_KEY:-$AI_SKILLS_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: $REQUEST_KEY" \
  -d '{"from":"zh","to":"bo","content":"你好，世界。"}'
```

```bash
curl --fail-with-body "$API_ROOT/tibetan-ai/chat/completions" \
  -H "Authorization: Bearer ${TIBETAN_AI_SKILL_API_KEY:-$AI_SKILLS_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: tibetan-chat-001" \
  -d '{"messages":[{"role":"user","content":"请用藏语写一句欢迎语。"}],"temperature":0.4}'
```

```bash
curl --fail-with-body "$API_ROOT/tibetan-ai/word/translation" \
  -H "Authorization: Bearer ${TIBETAN_AI_SKILL_API_KEY:-$AI_SKILLS_API_KEY}" \
  -H "Idempotency-Key: tibetan-doc-001" \
  -F "file=@document.docx" \
  -F "from=zh" \
  -F "to=bo" \
  -F "mode=all_text"
```

图片 OCR 翻译使用 multipart/form-data；每次新图片都生成唯一幂等键：

```bash
IMAGE_REQUEST_KEY="tibetan-image-$(date +%s)-$RANDOM"

curl --fail-with-body "$API_ROOT/tibetan-ai/image/translation" \
  -H "Authorization: Bearer ${TIBETAN_AI_SKILL_API_KEY:-$AI_SKILLS_API_KEY}" \
  -H "Idempotency-Key: $IMAGE_REQUEST_KEY" \
  -F "file=@notice.webp" \
  -F "from=bo" \
  -F "to=zh"
```

扫描 PDF 和混合型 PDF 仍使用文档路由：

```bash
PDF_REQUEST_KEY="tibetan-pdf-$(date +%s)-$RANDOM"

curl --fail-with-body "$API_ROOT/tibetan-ai/pdf/translation" \
  -H "Authorization: Bearer ${TIBETAN_AI_SKILL_API_KEY:-$AI_SKILLS_API_KEY}" \
  -H "Idempotency-Key: $PDF_REQUEST_KEY" \
  -F "file=@scan.pdf" -F "from=bo" -F "to=zh" -F "mode=all_text"
```

成功响应的计费信息位于 `X-AI-Skills-Billing-Currency`、
`X-AI-Skills-Billing-Charged`、`X-AI-Skills-Billing-Balance`。使用真实随机或 UUID
幂等键；示例中的固定值仅用于说明。文件只能在用户明确提供时上传；绝不把文件字节或
Base64 Data URL 写入日志或对话正文。
