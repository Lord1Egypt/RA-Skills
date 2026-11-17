# API 密钥配置

推荐在平台创建通用 Key，并执行 `openclaw config set env.AI_SKILLS_API_KEY "你的平台APIKey"` 和 `openclaw gateway restart`，全平台 Skill 只需配置一次。仍需开通目标产品。下列 `SPREADSHEET_ANALYSIS_API_KEY` 配置是兼容的产品专用覆盖项；调用优先使用该变量，为空时回退到 `AI_SKILLS_API_KEY`。两个变量均缺失时停止调用，不发送空 Bearer 请求。不要把旧请求换 Key 自动重试；幂等记录按 Key 隔离。


在平台开通表格分析并创建或复制现有通用 Key。请求使用 `Authorization: Bearer ${SPREADSHEET_ANALYSIS_API_KEY:-$AI_SKILLS_API_KEY}`，不要在日志或对话中输出密钥。
