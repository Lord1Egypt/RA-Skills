# Token 管理详细指引

本文档包含 Token 获取、保存和错误处理的完整操作细节。仅在脚本退出码为 2/3/4 且涉及 Token 问题时才需查阅。

## Token 获取指引

当脚本退出码为 2（Token 不存在）或 3（Token 为空）时，向用户展示以下指引：

> 🔑 需要先获取妙问 API KEY（Access Token）才能使用。
>
> **获取步骤**：
> 1. 打开 [妙问官网](https://miaowen.qq.com/) 并登录
> 2. 在左侧导航栏点击【Skill 社区】，弹出「skill」操作页
> 3. 在弹出的页面中可以看到「你的 API KEY」，格式为 `sk-mw-xxxxx`
> 4. 点击 API KEY 右侧的「刷新」按钮获取新 Token，点击「复制」按钮复制
> 5. 将复制的 Token 粘贴给我
>
> **操作示意图**：
>
> ![妙问 Token 获取指南](../assets/miaowen_token_guide.png)

## Token 保存

用户提供 Token 后执行：

```bash
node scripts/setup_token.js "<TOKEN_VALUE>"
```

保存后即可立即使用，无需重启终端或配置环境变量。

## Token 相关退出码处理

| 退出码 | 前缀 | 含义 | 处理 |
|--------|------|------|------|
| 2 | `[TOKEN_NOT_FOUND]` | Token 不存在 | 展示上方「Token 获取指引」，用户提供后执行 `setup_token.js` 保存，再重试 |
| 3 | `[TOKEN_EMPTY]` | Token 为空 | 同上 |
| 4 | `[API_ERROR]` 且涉及 Token | Token 失效 | 引导用户回到妙问官网点击「刷新」获取新 Token，重新执行 `setup_token.js` 保存 |
