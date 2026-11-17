# API 密钥配置

推荐在平台创建通用 Key，并执行 `openclaw config set env.AI_SKILLS_API_KEY "你的平台APIKey"` 和 `openclaw gateway restart`，全平台 Skill 只需配置一次。仍需开通目标产品。下列 `UYGHUR_AI_SKILL_API_KEY` 配置是兼容的产品专用覆盖项；调用优先使用该变量，为空时回退到 `AI_SKILLS_API_KEY`。两个变量均缺失时停止调用，不发送空 Bearer 请求。不要把旧请求换 Key 自动重试；幂等记录按 Key 隔离。



```bash
export UYGHUR_AI_SKILL_API_KEY="ais_..."
export AI_SKILLS_API_URL="https://ai-skills.open-idea.net" # 可选
```

请求根地址为 `${AI_SKILLS_API_URL:-https://ai-skills.open-idea.net}/api/v1`，
鉴权头为：

```text
Authorization: Bearer ${UYGHUR_AI_SKILL_API_KEY:-$AI_SKILLS_API_KEY}
```

通用 Key 可调用账号已开通的 API 产品；产品专用 Key 仅能调用对应产品。密钥缺失时引导用户在
平台控制台创建；不要要求用户把完整密钥发到对话中，也不要把密钥写进代码、日志、
文件名或错误信息。

常见鉴权错误包括 `invalid_api_key`、`key_expired`、`key_revoked`、
`skill_not_active`、`user_skill_suspended` 和 `account_suspended`。
