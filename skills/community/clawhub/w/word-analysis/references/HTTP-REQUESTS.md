# HTTP 请求与任务轮询

向 `${AI_SKILLS_API_URL:-https://ai-skills.open-idea.net}/api/v1/word-analysis/word.analyze` POST JSON，携带 `Authorization: Bearer`、`Content-Type: application/json` 和唯一 `Idempotency-Key`。问答、对比、导出替换对应 operation；异步任务使用响应中的查询地址轮询。读取 `X-AI-Skills-Billing-Currency`、`X-AI-Skills-Billing-Charged` 与 `X-AI-Skills-Billing-Balance` 了解本次人民币计费。
