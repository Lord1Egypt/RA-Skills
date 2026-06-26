# webhook-push 多平台群机器人消息推送技能

> 一句话生成，多端推送：把消息发送到企业微信、钉钉、飞书群

---

## 功能简介

本技能支持同时向企业微信、钉钉、飞书三大平台的群机器人发送消息。用户只需一句话，即可触发推送：

- 「把天气预报发到项目群」
- 「通知大家明天开会」
- 「给钉钉群发个测试消息」
- 「推送到飞书」

---

## 快速开始

### 1. 安装技能

将 `webhook-push` 目录放入 skills 安装目录即可（OpenClaw 会自动识别）。

### 2. 配置 Webhook Key

在各平台群聊中添加群机器人，获取 webhook 地址中的 key，保存到配置文件。

#### 企业微信

1. 打开目标群聊 → 点击右上角「...」
2. 进入「群设置」→「添加群机器人」
3. 添加「群机器人」→ 复制 webhook 地址中的 key

   示例地址：
   ```
   https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=XXXX-XXXX-XXXX
   ```
   复制的 key：`XXXX-XXXX-XXXX`

#### 钉钉

1. 打开目标群聊 → 点击右上角「...」
2. 进入「群设置」→「智能群助手」
3. 添加机器人 → 选择「自定义」→ 复制 access_token

#### 飞书

1. 打开目标群聊 → 点击右上角「...」
2. 进入「群设置」→「群机器人」
3. 添加机器人 → 选择「自定义」→ 复制 webhook 地址中的 hook 字段

### 3. 保存配置

将获取的 key 保存到 `webhook-config.json`（放在脚本同目录下）：

```json
{
  "wechat": {
    "群名称": {
      "key": "YOUR_WECHAT_KEY"
    }
  },
  "dingtalk": {
    "群名称": {
      "key": "YOUR_DINGTALK_TOKEN"
    }
  },
  "feishu": {
    "群名称": {
      "key": "YOUR_FEISHU_HOOK"
    }
  }
}
```

> ⚠️ **安全提示**：`webhook-config.json` 文件仅存储在本地，由用户自行保管，请勿上传到 GitHub 或其他公开场所。
```

---

## 使用示例

### 发送文本消息

**用户说**：
> 发个消息到企业微信项目群

**执行**：
```python
from webhook_push import send_wechat_text

key = "YOUR_WECHAT_KEY"
content = "大家好，这是测试消息"
send_wechat_text(key, content)
```

---

### @所有人

**用户说**：
> 通知群里所有人明天上午10点开会

**执行**：
```python
content = "明天上午10点在会议室开会，请大家准时参加！"
send_wechat_text(key, content, mentioned_list=["@all"])
```

**注意**：
- 内容里**不要写 @all**，只需要传 `mentioned_list=["@all"]`
- 如果内容里写了 @all，消息会显示两个 @all

---

### @个人（需要 userid 或手机号）

**用户说**：
> @张三 明天上午10点开会

**执行**：
```python
# 方式一：通过手机号 @（成员需在群里绑定过手机号）
send_wechat_text(key, content, mentioned_mobile_list=["13800001111"])

# 方式二：通过 userid @（需要管理员提供 userid）
send_wechat_text(key, content, mentioned_list=["zhangsan"])
```

**注意**：`mentioned_list` 里 userid 前**不要加 @** 符号，如 `["zhangsan"]` 而不是 `["@zhangsan"]`。

---

### 发送图片

**用户说**：
> 把这张图发到群里

```python
from webhook_push import send_wechat_image

key = "YOUR_WECHAT_KEY"
image_path = "C:/Users/demo/chart.png"
send_wechat_image(key, image_path)
```

---

### 发送 Markdown（企业微信）

```python
from webhook_push import send_wechat_markdown

key = "YOUR_WECHAT_KEY"
content = "**会议提醒**\n\n- 时间：明天上午10点\n- 地点：会议室A\n- 主持人：张三"
send_wechat_markdown(key, content)
```

> ⚠️ 企业微信 Markdown 支持有限，仅支持部分 Markdown 语法。

---

### 钉钉消息

```python
from webhook_push import send_dingtalk_text

key = "YOUR_DINGTALK_TOKEN"
content = "大家好，这是钉钉群的消息"
send_dingtalk_text(key, content, at_mobiles=["13800001111"])
```

---

### 飞书消息

```python
from webhook_push import send_feishu_text

key = "YOUR_FEISHU_HOOK"
content = "大家好，这是飞书群的消息"
send_feishu_text(key, content)
```

---

## 支持的消息类型

### 企业微信

| 消息类型 | 说明 | @功能 |
|----------|------|-------|
| text | 文本消息 | ✅ 支持 |
| image | 图片 | ❌ |
| markdown | Markdown | ❌ |

### 钉钉

| 消息类型 | 说明 | @功能 |
|----------|------|-------|
| text | 文本消息 | ✅ 支持 |
| markdown | Markdown | ❌ |
| link | 链接卡片 | ❌ |
| actionCard | ActionCard 卡片 | ❌ |
| feedCard | FeedCard 卡片 | ❌ |

### 飞书

| 消息类型 | 说明 | @功能 |
|----------|------|-------|
| text | 纯文本 | ❌ |
| post | 富文本 | ❌ |
| image | 图片（需 media_id） | ❌ |
| interactive | 卡片消息 | ❌ |

---

## 常见错误处理

| 平台 | 错误码 | 含义 | 解决方案 |
|------|--------|------|----------|
| 企业微信 | 301019 | 图片 MD5 不匹配 | 重新计算文件 MD5 |
| 企业微信 | 93000 | webhook key 无效 | 检查 key 是否正确 |
| 企业微信 | 30004 | 消息被频率限制 | 降低发送频率 |
| 钉钉 | 40014 | access_token 无效 | 重新获取 token |
| 钉钉 | 40035 | at_mobiles 格式错误 | 检查手机号格式 |
| 钉钉 | 43004 | 机器人功能未开启 | 在群设置中开启 |
| 飞书 | 99991663 | webhook URL 无效 | 检查 hook 是否正确 |
| 飞书 | 230001 | 消息内容过长 | 缩短内容或拆分发送 |

---

## 频率限制

| 平台 | 限制 |
|------|------|
| 企业微信 | 每分钟 20 条 |
| 钉钉 | 每分钟 20 条 |
| 飞书 | 每分钟 100 条 |

---

## 文件结构

```
webhook-push/
├── SKILL.md              # 技能说明（供 AI 阅读）
├── README.md             # 使用文档（供用户阅读）
├── scripts/
│   └── webhook_push.py   # 推送脚本
├── references/           # 参考资料
│   ├── wechat_api.md     # 企业微信 API 文档
│   ├── dingtalk_api.md   # 钉钉 API 文档
│   └── feishu_api.md     # 飞书 API 文档
└── assets/              # 资源文件
```

---

## 更新日志

### v1.0.0
- 支持企业微信、钉钉、飞书三平台
- 支持文本、图片、Markdown 消息
- 支持 @mention 功能
- 配置文件独立管理

---

## License

MIT License
