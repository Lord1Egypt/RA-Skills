# 飞书 Bot 完整部署文档

## 环境要求

- Python 3.8+
- 网络连接（无需公网 IP）
- 飞书企业自建应用（App ID + App Secret）

## 一、飞书开放平台配置

### 1. 创建应用

1. 访问 https://open.feishu.cn/app
2. 点击「创建企业自建应用」
3. 填写应用名称和描述
4. 记录 **App ID** 和 **App Secret**

### 2. 配置机器人

1. 进入「应用功能」→「机器人」
2. 启用机器人功能
3. 配置机器人名称和头像

### 3. 配置事件订阅（重要）

1. 进入「事件订阅」页面
2. **订阅方式**：选择「长连接模式」（不是 Webhook）
3. 添加事件：搜索并订阅 `im.message.receive_v1`
4. 记录 **Verification Token**（可选）
5. 记录 **Encrypt Key**（可选）

### 4. 配置权限（必需）

⚠️ **不配置权限，Bot 无法收发消息！**

进入「权限管理」页面（https://open.feishu.cn/app/你的AppID/permission），添加以下权限：

**必需权限：**
1. **`im:message`** - 获取与发送单聊、群组消息
   - 权限说明：允许 Bot 发送消息
   - 搜索关键词：`消息` 或 `im:message`

2. **`im:message.receive_v1`** - 接收消息事件
   - 权限说明：允许 Bot 接收用户发来的消息
   - 搜索关键词：`接收消息` 或 `im:message.receive_v1`

**可选权限（如需群聊）：**
- `im:message.group_at_msg` - 获取群组中所有消息

**权限配置步骤：**
1. 点击「添加权限」
2. 搜索 `im:message`，勾选
3. 搜索 `im:message.receive_v1`，勾选
4. 点击「保存」
5. 如果提示需要重新发布应用，按提示操作

### 5. 发布应用

申请发布 → 等待管理员审批（或在测试用户中添加自己）

---

## 二、本地部署

### 1. 克隆代码

```bash
git clone https://gitee.com/sihj/smart-agent-template.git
cd smart-agent-template/integrations/feishu
```

### 2. 安装依赖

```bash
pip3 install lark-oapi anthropic
```

### 3. 配置环境变量

复制配置模板：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```bash
# 飞书 Bot 配置
FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx          # 从飞书开放平台获取
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx  # 从飞书开放平台获取
FEISHU_VERIFICATION_TOKEN=                  # 可选
FEISHU_ENCRYPT_KEY=                         # 可选
FEISHU_PORT=8080                            # 默认 8080

# AI 引擎配置（选一个）

# 方案一：使用本地多模型代理（推荐）
AI_ENGINE=claude
CLAUDE_API_KEY=your_api_key_here
CLAUDE_MODEL=GLM-5                          # 或 Hunyuan-T1, Kimi-K2.5
CLAUDE_BASE_URL=http://192.168.1.99:3200   # 你的本地代理地址

# 方案二：使用 Claude 官方 API
# AI_ENGINE=claude
# CLAUDE_API_KEY=sk-ant-xxxxxxxx
# CLAUDE_MODEL=claude-sonnet-4

# 方案三：使用 OpenAI
# AI_ENGINE=openai
# OPENAI_API_KEY=sk-xxxxxxxx
# OPENAI_MODEL=gpt-4

# 方案四：使用 DeepSeek
# AI_ENGINE=deepseek
# DEEPSEEK_API_KEY=sk-xxxxxxxx
# DEEPSEEK_MODEL=deepseek-chat
```

### 4. 启动 Bot

```bash
./start_longconn.sh
```

启动成功后会显示：

```
✅ 飞书 Bot 已启动（长链接模式）
💬 无需公网 URL，通过 SDK 长连接接收消息
[Lark] [INFO] connected to wss://msg-frontier.feishu.cn/ws/v2
```

### 5. 测试

在飞书中找到你的 Bot，发送消息测试。

---

## 三、后台运行（生产环境）

### 方式一：nohup

```bash
nohup ./start_longconn.sh > bot.log 2>&1 &
```

查看日志：

```bash
tail -f bot.log
```

停止：

```bash
pkill -f bot_longconn
```

### 方式二：systemd（推荐）

创建服务文件 `/etc/systemd/system/feishu-bot.service`：

```ini
[Unit]
Description=Feishu Bot Service
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/smart-agent-template/integrations/feishu
ExecStart=/usr/bin/python3 bot_longconn.py
Restart=always
RestartSec=10
EnvironmentFile=/path/to/smart-agent-template/integrations/feishu/.env

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable feishu-bot
sudo systemctl start feishu-bot
sudo systemctl status feishu-bot
```

查看日志：

```bash
sudo journalctl -u feishu-bot -f
```

---

## 四、常见问题

### Q1: SSL 证书验证失败

**现象：** `[SSL: CERTIFICATE_VERIFY_FAILED]`

**原因：** 本地网络有代理或自签名证书

**解决：** 启动脚本 `start_longconn.sh` 会自动修复 SDK 的 SSL 验证

### Q2: Bot 收不到消息

**检查清单：**
1. 飞书开放平台「事件订阅」是否选择「长连接模式」
2. 是否订阅了 `im.message.receive_v1` 事件
3. Bot 是否有「接收消息」权限
4. 应用是否已发布或添加测试用户

### Q3: 回复的是 DeepSeek 而不是 Claude

**原因：** 本地 API 代理可能路由到了其他模型

**解决：** 
1. 检查 `.env` 中的 `CLAUDE_MODEL` 配置
2. 使用代理支持的模型名（如 `GLM-5`、`Hunyuan-T1`）
3. 或改用官方 Claude API

### Q4: 如何查看日志

```bash
# 实时查看
tail -f bot.log

# 查看最近 50 行
tail -50 bot.log

# 搜索错误
grep ERROR bot.log
```

### Q5: 如何重启 Bot

```bash
# 停止
pkill -f bot_longconn

# 启动
./start_longconn.sh
```

---

## 五、架构说明

```
用户发消息（飞书客户端）
    ↓
飞书服务器
    ↓
WebSocket 长连接推送事件
    ↓
bot_longconn.py（本地）
    ↓
ai_adapter.py（调用 AI）
    ↓
本地 AI 代理 / Claude API
    ↓
返回回复
    ↓
飞书 API 发送消息
    ↓
用户收到回复
```

**关键特性：**
- 长连接模式，无需公网 IP
- 支持多种 AI 引擎（Claude / OpenAI / DeepSeek / 本地代理）
- 自动处理 SSL 证书问题
- 支持记忆管理和任务解析

---

## 六、文件说明

| 文件 | 说明 | 是否提交 Git |
|------|------|-------------|
| `bot_longconn.py` | Bot 主程序 | ✅ |
| `config.py` | 配置管理 | ✅ |
| `handlers.py` | 消息处理器 | ✅ |
| `start_longconn.sh` | 启动脚本（自动修复 SSL） | ✅ |
| `.env` | 真实配置（含敏感信息） | ❌ 不提交 |
| `.env.example` | 配置模板 | ✅ |
| `bot.log` | 运行日志 | ❌ 不提交 |

---

## 七、安全提醒

⚠️ **不要把 `.env` 文件提交到 Git！**

已配置 `.gitignore` 保护敏感信息：
- `FEISHU_APP_SECRET`
- `CLAUDE_API_KEY`
- 其他 API Key

验证：

```bash
git check-ignore .env
# 应输出：.env
```

---

## 八、更新日志

- 2026-03-30：初始版本，支持长连接模式
- 2026-03-30：修复 SSL 证书验证问题
- 2026-03-30：修复 asyncio event loop 错误
- 2026-03-30：支持本地多模型 API 代理

---

**部署完成后，在飞书中给 Bot 发消息测试即可！**
