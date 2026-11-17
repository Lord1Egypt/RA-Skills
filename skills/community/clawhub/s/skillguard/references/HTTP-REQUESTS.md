# HTTP 请求与响应

接口：`POST /api/v1/skillguard/audit`

```bash
API_ROOT="${AI_SKILLS_API_URL:-https://ai-skills.open-idea.net}/api/v1"

curl --fail-with-body "$API_ROOT/skillguard/audit" \
  -H "Authorization: Bearer ${SKILLGUARD_API_KEY:-$AI_SKILLS_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: audit-uuid-001" \
  -d '{
    "skillName":"example-skill",
    "sourceUrl":"https://example.com/example-skill",
    "skillMd":"# Example Skill\nSafe, redacted instructions.",
    "files":[
      {"path":"references/API.md","content":"Redacted API guidance"}
    ]
  }'
```

成功响应包含 `auditId`、`createdAt`、`skill`、`score`、`verdict`、`riskLevel`、
`summary`、`findings`、`nextActions` 和 `usage`。`usage` 可包含 `charged`、
`balance`、`inputTokens`、`outputTokens`、`upstreamCost`、`evaluationSource`。

规则扫描可能不收费；启用 LLM 评估时按实际 token 计费，不能假设固定价格。规范计费头为
`X-AI-Skills-Billing-Currency`、`X-AI-Skills-Billing-Charged`、
`X-AI-Skills-Billing-Balance`。

示例固定幂等键只用于说明；生产请求应使用 UUID 等唯一值。
