# 飞书 Bot 集成

基于 smart-agent-template 的飞书 Bot，支持多 AI 引擎，复用 Telegram Bot 的 AI 适配器。

## 架构

```
integrations/
├── telegram/
│   ├── ai_adapter.py  ← 通用 AI 适配器（OpenAI/Claude/DeepSeek/Ollama）
│   └── ...
└── feishu/
    ├── bot.py         ← 飞书 Bot 主程序（HTTP Webhook 服务器）
    ├── config.py      ← 配置管理
    ├── handlers.py    ← 消息处理器（复用 ai_adapter）
    └── README.md      ← 本文档
```

**关键区别：Telegram 用轮询，飞书用事件订阅（Webhook）**

## 快速开始

### 1. 飞书开放平台配置

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 在「事件订阅」页面配置：
   - 请求 URL：`http://your-domain.com:8080/`
   - 事件：`im.message.receive_v1`（接收消息）
4. 记录以下信息：
   - App ID
   - App Secret
   - Verification Token
   - Encrypt Key（可选，建议配置）
5. 在「权限管理」添加权限：
   - `im:message` - 发送消息
   - `im:message:receive_v1` - 接收消息

### 2. 安装依赖

```bash
pip install lark-oapi  # 飞书官方 SDK（可选，本实现使用标准库）
```

### 3. 配置环境变量

**方式一：使用 .env 文件（推荐）**

```bash
# 1. 复制配置模板
cp .env.example .env

# 2. 编辑 .env，填入真实配置
vim .env

# 3. 使用启动脚本（自动加载 .env）
./start.sh
```

**方式二：手动导出环境变量**

```bash
# 飞书 Bot 配置
export FEISHU_APP_ID=cli_xxxxxx
export FEISHU_APP_SECRET=xxxxxxxx
export FEISHU_VERIFICATION_TOKEN=xxxxxxxx
export FEISHU_ENCRYPT_KEY=xxxxxxxx   # 可选
export FEISHU_PORT=8080              # 默认 8080

# AI 引擎配置（选一个）
export AI_ENGINE=claude
export CLAUDE_API_KEY=sk-ant-xxxxx
export CLAUDE_MODEL=claude-sonnet-4

# 或者用 OpenAI
export AI_ENGINE=openai
export OPENAI_API_KEY=sk-xxxxx
export OPENAI_MODEL=gpt-4

# 或者用 DeepSeek
export AI_ENGINE=deepseek
export DEEPSEEK_API_KEY=sk-xxxxx
```

### 4. 启动 Bot

```bash
cd integrations/feishu
python bot.py
```

### 5. 本地开发（ngrok）

飞书需要公网 URL，本地开发用 ngrok：

```bash
# 安装 ngrok
brew install ngrok  # macOS

# 启动隧道
ngrok http 8080

# 把 ngrok 的 URL 配置到飞书开放平台
# 格式：https://xxxx.ngrok.io/
```

## 支持的命令

| 命令 | 说明 |
|------|------|
| /start | 开始对话 |
| /help | 显示帮助 |
| /status | 查看状态（记忆数、健康度、任务数） |
| /memory | 查看记忆摘要 |
| /tasks | 查看任务列表 |

## 支持的 AI 引擎

| 引擎 | 说明 |
|------|------|
| `openai` | OpenAI GPT 系列 |
| `claude` | Anthropic Claude 系列 |
| `deepseek` | DeepSeek 系列 |
| `ollama` | 本地 Ollama 模型 |

## 与 Telegram Bot 的区别

| 特性 | Telegram | 飞书 |
|------|---------|------|
| 通信方式 | 轮询（polling） | Webhook（HTTP 回调） |
| 需要公网 | 否 | 是（或 ngrok） |
| 依赖库 | `python-telegram-bot` | 无（标准库） |
| AI 适配器 | 共用 `telegram/ai_adapter.py` | 共用 `telegram/ai_adapter.py` |

## 注意事项

1. **飞书需要 HTTPS**：生产环境必须配置 HTTPS，建议用 nginx + certbot
2. **签名验证**：配置 Encrypt Key 后会自动验证请求签名
3. **重复消息**：飞书可能重发事件，handlers 需要做幂等处理（已通过 task_tracker 处理）
4. **消息类型**：当前只处理文本消息，图片/文件可在 handlers.py 中扩展
