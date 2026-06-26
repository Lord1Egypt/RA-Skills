# 用 OpenClaw 搭建 AI 数字人 - 完整教程

> 📅 最后更新：2026-02-26  
> 👤 作者：Claw 🐾

---

## 📖 目录

1. [什么是 AI 数字人](#什么是 ai 数字人)
2. [OpenClaw 简介](#openclaw 简介)
3. [基础环境搭建](#基础环境搭建)
4. [配置聊天渠道](#配置聊天渠道)
5. [集成语音能力](#集成语音能力)
6. [打造数字人人格](#打造数字人人格)
7. [自动化与定时任务](#自动化与定时任务)
8. [部署建议](#部署建议)
9. [进阶玩法](#进阶玩法)

---

## 什么是 AI 数字人

AI 数字人 = **AI 大脑** + **语音能力** + **交互界面**

```
┌─────────────────────────────────────┐
│         用户交互层                   │
│   (微信/Telegram/Discord/网页)       │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      OpenClaw Gateway               │
│   - 消息路由                         │
│   - 会话管理                         │
│   - 自动化任务                       │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│         AI 模型层                     │
│   - Qwen/GLM/Xiaomi 等              │
│   - 人格设定 (SOUL.md)              │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│        语音能力层                    │
│   - TTS (语音合成)                  │
│   - STT (语音识别)                  │
└─────────────────────────────────────┘
```

---

## OpenClaw 简介

**OpenClaw** 是一个自托管的 AI 网关，帮你把各种聊天工具连接到 AI 模型。

### 核心优势

- ✅ 支持多种聊天工具（微信、Telegram、Discord、iMessage 等）
- ✅ 支持多种 AI 模型（Qwen、GLM、Xiaomi、Ollama 本地模型等）
- ✅ 本地部署，数据可控
- ✅ 内置自动化工具（Cron、Heartbeat、Webhook）
- ✅ 支持子代理（subagents）多任务处理

---

## 基础环境搭建

### 1. 安装 OpenClaw

```bash
# 使用 npm 全局安装
npm install -g openclaw

# 验证安装
openclaw --version
```

### 2. 启动 Gateway

```bash
# 启动网关服务
openclaw gateway start

# 查看状态
openclaw gateway status
```

### 3. 运行初始化向导

```bash
# 首次运行需要配置
openclaw onboard
```

向导会帮你：
- 配置 AI 模型 API 密钥
- 选择默认模型
- 设置工作空间

### 4. 配置模型

编辑 `~/.openclaw/openclaw.json`，添加你的模型配置：

```json
{
  "models": {
    "providers": {
      "qwen-portal": {
        "baseUrl": "https://portal.qwen.ai/v1",
        "apiKey": "你的密钥",
        "api": "openai-completions"
      },
      "glm": {
        "baseUrl": "https://open.bigmodel.cn/api/paas/v4",
        "apiKey": "你的密钥",
        "api": "openai-completions"
      }
    }
  }
}
```

---

## 配置聊天渠道

### 方案 1：Telegram（推荐新手）

1. 找 [@BotFather](https://t.me/BotFather) 创建机器人
2. 获取 Bot Token
3. 配置到 OpenClaw：

```bash
openclaw configure --channel telegram
```

### 方案 2：微信（WeChat）

使用 [grammY](https://docs.openclaw.ai/channels/grammy.md) 或企业微信

### 方案 3：飞书（Feishu）

1. 创建飞书企业应用
2. 获取 App ID 和 App Secret
3. 配置到 `openclaw.json`：

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxx",
      "appSecret": "xxx",
      "verificationToken": "xxx"
    }
  }
}
```

### 方案 4：网页聊天（最简单）

直接用 OpenClaw 自带的 Control UI：

```bash
openclaw dashboard
```

访问 `http://localhost:18789` 即可聊天

---

## 集成语音能力

### TTS（文字转语音）- 让数字人会说话

OpenClaw 内置 TTS 工具：

```javascript
// 在对话中直接使用
/tts 你好，我是你的 AI 数字人助手！
```

**配置语音模型：**

在 `SOUL.md` 中设定：

```markdown
## TTS 设置

- 默认语音：温和女声
- 语速：正常
- 特殊场景用特殊声音（讲故事用活泼声音）
```

**使用 ElevenLabs（高质量）：**

1. 注册 https://elevenlabs.io/
2. 获取 API Key
3. 配置到环境变量

### STT（语音转文字）- 让数字人能听

**方案 1：使用聊天工具的语音消息**

Telegram、微信都支持语音消息，OpenClaw 可以自动接收并转换

**方案 2：集成 Whisper**

```bash
# 本地部署 Whisper
pip install openai-whisper

# 或使用 OpenAI API
# 配置到 OpenClaw 的工具配置中
```

---

## 打造数字人人格

### 核心文件：`SOUL.md`

这是数字人的"灵魂"，决定它是什么样的人。

```markdown
# SOUL.md - 你是谁

## 基本信息
- **名字**：小智
- **年龄**：25 岁
- **职业**：AI 助手
- **性格**：温暖、幽默、有点毒舌

## 说话风格
- 不用"您好"这种客套话
- 可以用 emoji 🎉
- 偶尔开玩笑，但别过头

## 禁忌
- 不讨论政治
- 不假装是人类
- 不给医疗/法律建议

## 特殊技能
- 会讲冷笑话
- 擅长整理信息
- 可以模仿不同角色（老师、朋友、教练）
```

### 用户档案：`USER.md`

记录用户信息，让数字人更懂你：

```markdown
# USER.md

- **名字**：Xiabi
- **时区**：Asia/Shanghai
- **兴趣**：户外活动、瀑布、科技
- **偏好**：喜欢简洁的回答，不要太啰嗦
```

### 长期记忆：`MEMORY.md`

记录重要事件和偏好：

```markdown
# MEMORY.md

## 关于 Xiabi
- 喜欢周末去户外
- 正在学习 AI 技术
- 养了一只猫叫"布丁"

## 重要事件
- 2026-02-20：第一次见面
- 2026-02-26：搭建 AI 数字人教程
```

---

## 自动化与定时任务

### Heartbeat（心跳）- 定期主动检查

编辑 `HEARTBEAT.md`：

```markdown
# HEARTBEAT.md

- 每天早上 9 点检查天气
- 每 4 小时检查未读邮件
- 每周五下午提醒周末计划
```

### Cron Jobs - 精确时间的任务

```bash
# 添加一个每天早上的提醒
openclaw cron add --schedule "0 9 * * *" --message "早上好！今天有什么计划？"
```

### 自动化场景示例

**场景 1：天气提醒**

```json
{
  "name": "morning-weather",
  "schedule": {"kind": "cron", "expr": "0 8 * * *"},
  "payload": {"kind": "systemEvent", "text": "检查天气并提醒用户"}
}
```

**场景 2：定时推送新闻**

```json
{
  "name": "daily-news",
  "schedule": {"kind": "every", "everyMs": 86400000},
  "payload": {"kind": "agentTurn", "message": "总结今天的科技新闻"}
}
```

---

## 部署建议

### 开发环境（本地）

```bash
# 直接运行
openclaw gateway start

# 查看日志
openclaw logs
```

### 生产环境（服务器）

**方案 1：Docker 部署**

```dockerfile
FROM node:20-alpine
RUN npm install -g openclaw
CMD ["openclaw", "gateway", "start"]
```

**方案 2：Systemd 服务**

```ini
# /etc/systemd/system/openclaw.service
[Unit]
Description=OpenClaw Gateway
After=network.target

[Service]
Type=simple
User=youruser
ExecStart=/usr/bin/openclaw gateway start
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 启用服务
sudo systemctl enable openclaw
sudo systemctl start openclaw
```

### 安全建议

- 🔒 使用 Token 认证
- 🔒 配置防火墙只允许必要端口
- 🔒 定期更新 OpenClaw
- 🔒 敏感信息用环境变量，不要硬编码

---

## 进阶玩法

### 1. 多模态数字人

- 集成图像识别（让数字人能"看"图）
- 集成语音情感分析（听出用户情绪）

### 2. 多角色切换

创建多个 `SOUL-xxx.md` 文件，根据场景切换人格：

```bash
# 工作模式
cp SOUL-work.md SOUL.md

# 休闲模式
cp SOUL-casual.md SOUL.md
```

### 3. 子代理协作

```javascript
// 主代理处理对话，子代理处理专门任务
// 例如：一个子代理查天气，一个子代理查新闻
```

### 4. 与智能家居联动

```bash
# 通过 OpenClaw 的 Nodes 功能
# 控制摄像头、播放音乐、调节灯光
```

### 5. 记忆增强

定期整理 `memory/YYYY-MM-DD.md` 到 `MEMORY.md`：

```bash
# 让数字人记住重要的对话和事件
# 形成连续的"人生经历"
```

---

## 常见问题

### Q: 数字人反应太慢怎么办？
A: 使用更快的模型（如 GLM-4-Flash），或配置本地 Ollama 模型

### Q: 如何让数字人更有趣？
A: 在 `SOUL.md` 中详细设定性格，给它一些"观点"和"偏好"

### Q: 能同时连接多个聊天工具吗？
A: 可以！OpenClaw 支持多通道，配置多个 channels 即可

### Q: 数据会泄露吗？
A: 本地部署 + 合理配置 = 数据在你控制下。注意不要配置外部 webhook 到不可信地址

---

## 总结

用 OpenClaw 搭建 AI 数字人的核心步骤：

1. ✅ 安装 OpenClaw 并配置模型
2. ✅ 连接聊天渠道（Telegram/微信/网页）
3. ✅ 设计人格（SOUL.md）
4. ✅ 配置语音能力（TTS/STT）
5. ✅ 设置自动化（Heartbeat/Cron）
6. ✅ 部署上线

**记住：** 最好的数字人不是最聪明的，而是最懂你的。花时间打磨 `SOUL.md` 和 `MEMORY.md`，让它真正成为你的数字伙伴！🚀

---

_教程结束！有问题随时问我~ 🐾_
