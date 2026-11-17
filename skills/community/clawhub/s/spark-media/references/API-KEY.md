# API 密钥配置

推荐在平台创建通用 Key，并执行 `openclaw config set env.AI_SKILLS_API_KEY "你的平台APIKey"` 和 `openclaw gateway restart`，全平台 Skill 只需配置一次。仍需开通目标产品。调用优先使用 `AI_SKILLS_API_KEY`，为空时才读取兼容变量 `SPARK_MEDIA_API_KEY`。两者均缺失时停止调用，不发送空 Bearer 请求。



```bash
export SPARK_MEDIA_API_KEY="ais_..."
export AI_SKILLS_API_URL="https://ai-skills.open-idea.net" # 可选
```

请求根地址为 `${AI_SKILLS_API_URL:-https://ai-skills.open-idea.net}/api/v1`。

```text
Authorization: Bearer ${AI_SKILLS_API_KEY:-$SPARK_MEDIA_API_KEY}
```

密钥仅绑定 Spark Media，不能跨 Skill 使用。不要要求用户在聊天中粘贴完整密钥，也不要
将密钥写入代码、提示词、日志或生成文件。常见鉴权错误包括 `invalid_api_key`、
`key_expired`、`key_revoked`、`skill_not_active`、`user_skill_suspended` 和
`account_suspended`。

## 配置冲突、迁移与鉴权失败

- 首次调用前选定凭证来源。两种变量同时存在且值不同时，采用 `AI_SKILLS_API_KEY` 并提示忽略了 `SPARK_MEDIA_API_KEY`，仅显示变量名，不输出或记录密钥、密钥片段或 Authorization 请求头。同一逻辑任务固定所选 API Key 和原 `Idempotency-Key`，重试与查询沿用原凭证。
- 迁移前先查询并核对旧 Key 下已提交任务的结果与账单；幂等记录按 Key 隔离，即使 `Idempotency-Key` 相同，换 API Key 仍可能重复执行或扣费。确认旧任务后再清理旧产品变量及 `skills.entries.spark-media.apiKey` / `skills.entries.spark-media.env` 中的遗留凭证，检查实际执行环境（宿主、服务进程或沙箱），重启 Gateway 并在新会话验证。不要自动修改或撤销用户的 Key。产品隔离场景须明确让该执行环境不提供通用变量，再使用产品变量。
- 收到 401（`invalid_api_key`、`key_revoked`、`key_expired`）时停止自动重试，检查当前凭证来源、密钥状态和目标产品范围；不要自动切换到另一把 Key 重发，也不要仅凭间歇性恢复断言是网关或缓存故障。排查保留 `request_id`、接口、时间及变量名，不保留密钥；确需切换凭证前先核对原任务和账单。
