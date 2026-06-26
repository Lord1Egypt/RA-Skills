# 飞书 Bot 本地测试指南

## 当前配置

- **App ID**: `cli_a9436b52d0b81bcd`
- **App Secret**: 已配置（不显示）
- **监听端口**: 8080
- **AI 引擎**: Claude（需配置 API Key）

## 快速启动

### 1. 配置 AI 引擎

编辑 `.env`，填入 Claude API Key：

```bash
vim .env
# 找到 CLAUDE_API_KEY，填入真实 Key
```

### 2. 启动 Bot

```bash
./start.sh
```

### 3. 配置 ngrok（本地开发必需）

飞书需要公网 URL，用 ngrok 提供：

```bash
# 另开终端
ngrok http 8080

# 复制 ngrok 输出的 URL（格式：https://xxxx.ngrok-free.app/）
```

### 4. 配置飞书开放平台

1. 访问 [飞书开放平台](https://open.feishu.cn/app)
2. 找到你的应用（App ID: cli_a9436b52d0b81bcd）
3. 进入「事件订阅」页面
4. 配置请求 URL：`https://xxxx.ngrok-free.app/`（ngrok 的 URL）
5. 添加事件：`im.message.receive_v1`
6. 保存配置

### 5. 测试

在飞书中找到你的 Bot，发送消息测试。

## 常见问题

### Q: 启动失败，提示缺少 AI_ENGINE

A: 编辑 `.env`，确保 `AI_ENGINE=claude` 且 `CLAUDE_API_KEY` 已填入。

### Q: 飞书收不到回复

A: 检查：
1. ngrok 是否正常运行（`ngrok http 8080`）
2. 飞书开放平台的请求 URL 是否配置正确
3. Bot 日志是否有错误（查看终端输出）

### Q: 签名验证失败

A: 在飞书开放平台「事件订阅」页面，复制 Verification Token 和 Encrypt Key，填入 `.env`。

## 文件说明

| 文件 | 说明 | 是否提交 |
|------|------|---------|
| `.env` | 真实配置（含敏感信息） | ❌ 不提交 |
| `.env.example` | 配置模板 | ✅ 提交 |
| `start.sh` | 启动脚本 | ✅ 提交 |
| `bot.py` | Bot 主程序 | ✅ 提交 |

## 安全提醒

⚠️ **不要把 .env 文件提交到 git！**

已配置 `.gitignore` 保护，但请确认：

```bash
git check-ignore .env
# 应输出：.env
```
