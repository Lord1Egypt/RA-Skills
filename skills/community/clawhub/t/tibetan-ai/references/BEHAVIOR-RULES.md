# 行为、错误与重试规则

## 必须遵守

- 只传递完成用户请求所必需的内容；上传文件或敏感文本前先取得同意。
- 同一逻辑请求始终复用同一个 `Idempotency-Key`；新请求使用新值。
- 不输出密钥、完整原始响应或用户未要求的内部诊断。
- 翻译使用业务字段 `data.tgtText`，对话使用 `choices[0].message.content`。
- 响应字段缺失、解析失败或语义不确定时明确失败，不伪造结果。

## 错误处理

- `validation_failed`（验证失败）：修正字段、语言代码或长度后再提交。
- `insufficient_balance`（余额不足）：提示充值，不自动重复扣费请求。
- `rate_limited`（受到速率限制）：尊重 `Retry-After`；否则指数退避并限制次数。
- `upstream_unavailable`（上游服务不可用）：短暂退避后最多重试少量次数，复用原幂等键。
- `idempotency_in_progress`（幂等请求处理中）：等待原请求完成，不换新密钥并发提交。
- `idempotency_key_reused`（幂等键已被重复使用）：仅当请求内容确实不同才生成新密钥。
- `idempotency_indeterminate`（幂等结果不确定）：停止自动重试，先核对原请求和账单。
- `document_extraction_failed`（文档提取失败）：请用户更换可解析文件或提供纯文本。

普通文本翻译、对话和 Word 请求的幂等重放返回首次响应及首次计费头；这不代表再次扣费，
也不能把头中的金额擅自改成 0。

图片和 PDF 翻译是隐私例外：客户端必须在收到时保留首次完整响应。成功重放只返回带
`replayed=true`、`content_retained=false` 的无内容摘要，不包含 `srcText`、`tgtText` 或 `pages`，
且不会再次调用上游或扣费。
