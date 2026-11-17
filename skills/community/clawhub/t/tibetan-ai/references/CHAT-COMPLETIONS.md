# 对话补全

接口：`POST /api/v1/tibetan-ai/chat/completions`

JSON 字段：

- `messages`：必填，1–100 项；`role` 只能为 `system`、`user`、`assistant`，
  每项 `content` 最多 200000 个字符。
- `temperature`：可选，0–2。
- `max_tokens`：可选，1–8192。
- `model`：可选。通常省略；若填写，必须与平台为该 Skill 配置的模型一致。

输出位于 `choices[0].message.content`。若该字段不存在、为空或响应结构不完整，应报告
服务响应异常，不要猜测答案。

使用对话接口处理藏语问答、解释、润色、总结和创作。纯翻译仍使用 `/translation`，
避免模型添加用户未要求的内容。
