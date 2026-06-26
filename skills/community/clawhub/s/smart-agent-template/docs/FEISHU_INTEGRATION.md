# 飞书 Bot 集成文档

## 概述

smart-agent-template 的飞书 Bot 集成，支持多 AI 引擎（OpenAI / Claude / DeepSeek / Ollama），与 Telegram Bot 共用同一套 AI 适配器和记忆管理架构。

## 飞书开放平台配置步骤

### 第一步：创建企业自建应用

1. 访问 [飞书开放平台](https://open.feishu.cn/app)
2. 点击「创建企业自建应用」
3. 填写应用名称和描述
4. 记录 App ID 和 App Secret（在「凭证与基础信息」页面）

### 第二步：配置机器人能力

1. 进入「应用功能」→「机器人」
2. 启用机器人功能
3. 配置机器人名称和头像

### 第三步：配置事件订阅

1. 进入「事件订阅」页面
2. 配置请求 URL：`https://your-domain.com/webhook/feishu`
   - 本地开发用 ngrok：`ngrok http 8080`
   - 把 ngrok URL 填入（格式：`https://xxxx.ngrok-free.app/`）
3. 记录 Verification Token 和 Encrypt Key
4. 添加事件：搜索并订阅 `im.message.receive_v1`

### 第四步：配置权限

在「权限管理」页面添加以下权限：
- `im:message` - 获取与发送单聊、群组消息
- `im:message.group_at_msg` - 获取群组中所有消息（如需群聊）

### 第五步：发布应用

申请发布 → 等待管理员审批（或直接在测试用户中添加自己测试）

---

## 环境变量配置

```bash
# 飞书 Bot 核心配置
FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FEISHU_VERIFICATION_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FEISHU_ENCRYPT_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  # 可选，建议配置
FEISHU_PORT=8080  # Webhook 监听端口，默认 8080

# AI 引擎（选一个）
AI_ENGINE=claude

# Claude
CLAUDE_API_KEY=sk-ant-xxxxxxxx
CLAUDE_MODEL=claude-sonnet-4

# 或 OpenAI
# AI_ENGINE=openai
# OPENAI_API_KEY=sk-xxxxxxxx
# OPENAI_MODEL=gpt-4

# 或 DeepSeek
# AI_ENGINE=deepseek
# DEEPSEEK_API_KEY=sk-xxxxxxxx
# DEEPSEEK_MODEL=deepseek-chat

# 或本地 Ollama
# AI_ENGINE=ollama
# OLLAMA_BASE_URL=http://localhost:11434
# OLLAMA_MODEL=llama2
```

---

## 本地开发指南

### 方案一：ngrok（推荐）

```bash
# 1. 安装 ngrok
brew install ngrok  # macOS
# 或 https://ngrok.com/download

# 2. 启动飞书 Bot
cd integrations/feishu
python bot.py

# 3. 另开终端，启动 ngrok 隧道
ngrok http 8080

# 4. 把 ngrok 输出的 URL 配置到飞书开放平台
# 例：https://abc123.ngrok-free.app/
```

### 方案二：内网穿透（frp）

```ini
# frpc.ini
[common]
server_addr = your-vps-ip
server_port = 7000

[feishu-bot]
type = http
local_port = 8080
custom_domains = feishu-bot.your-domain.com
```

---

## 启动命令

```bash
# 基础启动
cd integrations/feishu
python bot.py

# 带环境变量启动
FEISHU_APP_ID=xxx FEISHU_APP_SECRET=xxx AI_ENGINE=claude CLAUDE_API_KEY=xxx python bot.py

# 生产环境（后台运行）
nohup python bot.py > feishu-bot.log 2>&1 &
```

---

## 架构说明

```
用户发消息
    ↓
飞书服务器推送事件（HTTP POST）
    ↓
bot.py - FeishuWebhookHandler.do_POST()
    ↓ 验证签名 + 解析事件
handlers.py - FeishuMessageHandlers.handle_message()
    ↓ 加载记忆 / 解析任务
ai_adapter.py（来自 telegram/）- AIAdapter.get_response()
    ↓ 调用 AI 引擎
handlers.py - 保存记忆 / 追踪任务
    ↓
bot.py - _send_feishu_message()
    ↓ 调用飞书 API
用户收到回复
```

**关键设计：飞书 Bot 直接复用 `integrations/telegram/ai_adapter.py`，不重复实现 AI 逻辑。**

---

## 与 Telegram Bot 对比

| 特性 | Telegram Bot | 飞书 Bot |
|------|-------------|---------|
| 通信模式 | 轮询（polling） | Webhook（HTTP 回调） |
| 需要公网 IP | ❌ | ✅（或 ngrok） |
| 外部依赖 | `python-telegram-bot` | 无（标准库 http.server） |
| AI 适配器 | `telegram/ai_adapter.py` | 复用同一文件 |
| 记忆管理 | `MemoryManager` | 复用同一模块 |
| 任务追踪 | `TaskTracker` | 复用同一模块 |

---

## 生产部署建议

### Nginx 反向代理 + HTTPS

```nginx
server {
    listen 443 ssl;
    server_name feishu-bot.your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/feishu-bot.your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/feishu-bot.your-domain.com/privkey.pem;
    
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### systemd 服务

```ini
# /etc/systemd/system/feishu-bot.service
[Unit]
Description=Feishu Bot Service
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/smart-agent-template/integrations/feishu
ExecStart=/usr/bin/python3 bot.py
Restart=always
EnvironmentFile=/opt/smart-agent-template/.env

[Install]
WantedBy=multi-user.target
```

```bash
systemctl enable feishu-bot
systemctl start feishu-bot
systemctl status feishu-bot
```
