# 错误处理

- **401 Unauthorized**：API Key 无效或过期，提示用户在微排版平台重新生成 API Key
- **403 Forbidden**：用户角色权限不足，需要 admin 或 developer 角色
- **404 Not Found**：模板或作品不存在，检查 ID 是否正确
- **429 Too Many Requests**：请求频率超限（60次/分钟），等待后重试
- **模板搜索无结果**：按级联降级策略自动重试（tags+search → 仅search → 仅tags → 默认模板），全部无果时使用默认模板兜底
