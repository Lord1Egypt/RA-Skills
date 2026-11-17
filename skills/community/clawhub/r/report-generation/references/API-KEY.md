# API 密钥配置与价格

推荐在平台创建通用 Key，并执行 `openclaw config set env.AI_SKILLS_API_KEY "你的平台APIKey"` 和 `openclaw gateway restart`，全平台 Skill 只需配置一次。仍需开通目标产品。下列 `REPORT_GENERATION_API_KEY` 配置是兼容的产品专用覆盖项；调用优先使用该变量，为空时回退到 `AI_SKILLS_API_KEY`。两个变量均缺失时停止调用，不发送空 Bearer 请求。不要把旧请求换 Key 自动重试；幂等记录按 Key 隔离。


默认 API 根地址为 `https://ai-skills.open-idea.net/api/v1`；密钥环境变量为 `REPORT_GENERATION_API_KEY`，可选覆盖 `AI_SKILLS_API_URL`。从 ClawHub 安装免费；平台只对成功操作扣费。

- `report.inspect`：免费
- `report.generate`：输入 ¥0.006、输出 ¥0.012/千 tokens
- `report.export`：¥0.15/份

实际价格以[经营报告生成产品页面](https://ai-skills.open-idea.net/skills/report-generation)和响应头 `X-AI-Skills-Billing-Currency`、`X-AI-Skills-Billing-Charged`、`X-AI-Skills-Billing-Balance` 为准。不要记录、回显或提交完整 API Key。
