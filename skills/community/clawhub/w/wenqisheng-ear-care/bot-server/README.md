# Bot Server — 闻其声耳轻松多平台接入

将闻其声耳轻松 AI 客服接入飞书、钉钉、企业微信。

## 快速启动

```bash
cd bot-server

# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置
cp .env.example .env
# 编辑 .env，填入 ANTHROPIC_API_KEY

# 3. 启动
python main.py
```

访问 http://localhost:8000 确认服务正常。

## 测试

```bash
# 直接测试 AI 回复
curl -X POST http://localhost:8000/test \
  -H "Content-Type: application/json" \
  -d '{"msg": "你们几点开门？"}'
```

返回:
```json
{
  "reply": "您好！我们的营业时间是每天 10:00 - 22:00...",
  "data_version": "2026-05-13"
}
```

## 对接各平台

### 飞书

1. 打开 [飞书开放平台](https://open.feishu.cn) → 创建企业自建应用
2. 开启「机器人」能力
3. 事件订阅 → 添加 `im.message.receive_v1` 事件
4. 请求地址填: `https://你的域名/api/feishu`
5. `.env` 中设置:
   - `FEISHU_ENABLED=true`
   - `FEISHU_APP_ID` / `FEISHU_APP_SECRET`（从飞书后台获取）
6. 发布上线

### 钉钉

1. 打开 [钉钉开放平台](https://open.dingtalk.com) → 创建应用
2. 机器人 → 消息接收 → HTTP 回调
3. 回调地址填: `https://你的域名/api/dingtalk`
4. `.env` 中设置:
   - `DINGTALK_ENABLED=true`
   - `DINGTALK_APP_KEY` / `DINGTALK_APP_SECRET`

### 企业微信

1. 企业微信管理后台 → 应用管理 → 自建应用
2. 接收消息 → 设置 API 接收
3. URL 填: `https://你的域名/api/wecom`
4. `.env` 中设置:
   - `WECOM_ENABLED=true`
   - `WECOM_TOKEN` / `WECOM_ENCODING_AES_KEY`

## 部署

### Railway（推荐）

```bash
# 在项目根目录
railway up
# 设置环境变量
railway variables set ANTHROPIC_API_KEY=sk-ant-xxx
```

### 自行部署

```bash
# 用 screen 或 systemd 保持后台运行
screen -S wqs-bot
python main.py
# Ctrl+A D 分离
```

### Docker（可选）

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY bot-server/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
WORKDIR /app/bot-server
CMD ["python", "main.py"]
```

## 对话记忆

服务内置内存级对话记忆（40条/会话，1000个会话）。生产环境建议换 Redis：

```python
# ai_client.py 中替换 ConversationStore 为 Redis 实现
```

## 自定义

AI 模型在 `.env` 中切换:

```
AI_MODEL=claude-opus-4-7    # 更高质量
AI_MODEL=claude-haiku-4-5   # 更快更便宜
```
