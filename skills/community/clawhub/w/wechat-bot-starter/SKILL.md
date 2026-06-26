---
name: wechat-bot-starter
version: 1.0.0
description: 微信机器人快速搭建 - 基于 wechaty/itchat 的微信机器人模板。适合：想做微信自动化的开发者。
metadata:
  openclaw:
    emoji: "🤖"
    requires:
      bins: ["node", "npm"]
---

# 微信机器人快速搭建 Skill

快速搭建微信机器人，支持自动回复、消息监控、群管理。

## 技术选型

| 方案 | 优点 | 缺点 | 推荐场景 |
|------|------|------|----------|
| Wechaty | 跨平台、生态好 | 需要付费 Pad 协议 | 生产环境 |
| itchat | 免费、简单 | 易封号 | 个人测试 |
| 企业微信 | 官方支持、稳定 | 功能受限 | 企业应用 |
| ComWechat | 免费、Web 协议 | 需登录 | 小规模 |

## 快速开始

### 方案 1：Wechaty（推荐）

```bash
# 安装
npm install wechaty wechaty-puppet-wechat

# 创建机器人
cat > bot.js << 'EOF'
const { Wechaty } = require('wechaty')
const bot = new Wechaty()

bot
  .on('scan', (qrcode) => console.log('扫码登录:\n' + qrcode))
  .on('login', (user) => console.log('登录成功:', user))
  .on('message', async (msg) => {
    if (msg.text() === 'ping') {
      await msg.say('pong')
    }
  })

bot.start()
EOF

node bot.js
```

### 方案 2：itchat（简单）

```bash
# 安装
pip install itchat

# 创建机器人
cat > bot.py << 'EOF'
import itchat

@itchat.msg_register(itchat.content.TEXT)
def reply(msg):
    if msg['Text'] == 'ping':
        return 'pong'
    return None

itchat.auto_login(hotReload=True)
itchat.run()
EOF

python bot.py
```

## 功能模板

### 1. 自动回复

```python
import itchat

# 关键词回复
REPLIES = {
    '你好': '你好！有什么可以帮你的？',
    '价格': '我们的产品价格如下...',
    '联系方式': '电话：xxx，微信：xxx'
}

@itchat.msg_register(itchat.content.TEXT)
def auto_reply(msg):
    text = msg['Text']
    for keyword, reply in REPLIES.items():
        if keyword in text:
            return reply
    return None
```

### 2. 群管理

```python
import itchat

@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def group_admin(msg):
    # 进群欢迎
    if msg['Type'] == 'note' and '加入群聊' in msg['Text']:
        return '欢迎新成员！请阅读群公告。'
    
    # 禁言词检测
    banned_words = ['广告', '推广', '加微信']
    for word in banned_words:
        if word in msg['Text']:
            # 可以调用踢人 API
            return None
```

### 3. 消息转发

```python
import itchat

TARGET_GROUP = '目标群名称'

@itchat.msg_register(itchat.content.TEXT)
def forward(msg):
    # 转发到指定群
    if msg['Text'].startswith('#转发'):
        groups = itchat.search_chatrooms(name=TARGET_GROUP)
        if groups:
            groups[0].send(msg['Text'][3:])
```

### 4. 定时发送

```python
import itchat
import schedule
import time

def morning_greeting():
    groups = itchat.search_chatrooms(name='工作群')
    if groups:
        groups[0].send('早上好！今天也要加油💪')

schedule.every().day.at('09:00').do(morning_greeting)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 接入 OpenClaw

```python
import itchat
import requests

OPENCLAW_URL = 'http://localhost:3000/api/chat'

@itchat.msg_register(itchat.content.TEXT)
def ai_reply(msg):
    # 发送给 OpenClaw
    response = requests.post(OPENCLAW_URL, json={
        'message': msg['Text'],
        'user_id': msg['FromUserName']
    })
    
    return response.json().get('reply')
```

## 配置文件

### ~/.openclaw/workspace/WECHAT-BOT.md

```yaml
# 机器人配置
bot:
  name: "小助手"
  welcome: "你好！我是小助手，有什么可以帮你？"

# 自动回复规则
auto_reply:
  - keyword: "价格"
    reply: "请查看产品目录：https://example.com"
  - keyword: "客服"
    reply: "正在为您转接人工客服..."

# 群管理
group_admin:
  banned_words: ["广告", "推广"]
  welcome_msg: "欢迎加入！请阅读群公告。"

# 定时任务
schedule:
  - time: "09:00"
    msg: "早上好！"
    target: "工作群"
```

## 注意事项

### 防封号技巧

1. **不要频繁登录** - 使用 hotReload=True
2. **控制发送频率** - 每秒不超过 1 条
3. **避免营销内容** - 容易被举报
4. **使用企业微信** - 官方支持更安全

### Web 微信限制

- 部分账号无法登录 Web 微信
- 新注册账号通常不支持
- 建议使用企业微信替代

## 推荐架构

```
微信消息
    ↓
消息队列（Redis）
    ↓
OpenClaw Agent 处理
    ↓
回复消息
```

---

创建：2026-03-12
版本：1.0