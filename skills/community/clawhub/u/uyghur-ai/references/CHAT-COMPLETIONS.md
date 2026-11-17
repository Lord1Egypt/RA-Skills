# 对话补全

接口：`POST /api/v1/uyghur-ai/chat/completions`

- `messages`：必填，1–100 项；角色只能为 `system`、`user`、`assistant`，
  每项 `content` 最多 200000 个字符。
- `temperature`：可选，0–2。
- `max_tokens`：可选，1–8192。
- `model`：通常省略；若填写，必须与平台为本 Skill 配置的模型一致。

输出位于 `choices[0].message.content`。结构不完整或内容为空时报告服务响应异常，不猜测
答案。此接口用于维吾尔语问答、解释、润色、总结和创作；纯翻译使用 `/translation`。
