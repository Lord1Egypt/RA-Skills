---
name: webhook-push
description: 多平台群机器人消息推送。支持企业微信、钉钉、飞书的 webhook 推送。当用户说"发送到微信群"、"发钉钉消息"、"推送到飞书"时使用此技能。
metadata:
  files:
    - path: webhook-config.json
      description: 用户 webhook key 配置文件，由用户在安装后自行创建，技能仅读取此文件获取 key
      required: false
      user_provided: true
---

# 多平台群机器人消息推送

## 快速开始

### 首次配置

用户需要先配置各平台的 webhook key。支持的平台：

| 平台 | 说明 |
|------|------|
| 企业微信 | 群机器人 webhook |
| 钉钉 | 自定义机器人 |
| 飞书 | 自定义机器人 |

将配置保存到 `webhook-config.json`（放在脚本同目录下）：
```json
{
  "wechat": {
    "群名称": {
      "key": "YOUR_WECHAT_KEY_HERE"
    }
  },
  "dingtalk": {},
  "feishu": {}
}
```

---

## 支持的平台

### 1. 企业微信

**API 地址**: `https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}`

**支持的消息类型**:
- `text` - 文本消息（支持 @mention）
- `image` - 图片（base64 + md5）
- `markdown` - Markdown（部分支持）

**发送示例**:
```python
import json
import urllib.request

def send_wechat(key, content):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}"
    data = {"msgtype": "text", "text": {"content": content}}
    
    req = urllib.request.Request(url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
    req.add_header("Content-Type", "application/json; charset=utf-8")
    
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))
```

---

### 2. 钉钉

**API 地址**: `https://oapi.dingtalk.com/robot/send?access_token={key}`

**支持的消息类型**:
- `text` - 文本消息（支持 @手机号）
- `markdown` - Markdown
- `link` - 链接卡片
- `actionCard` -  ActionCard 卡片
- `feedCard` - FeedCard 卡片

**发送示例**:
```python
import json
import urllib.request

def send_dingtalk(key, content, at_mobiles=None):
    url = f"https://oapi.dingtalk.com/robot/send?access_token={key}"
    data = {
        "msgtype": "text",
        "text": {"content": content},
        "at": {"atMobiles": at_mobiles or []}
    }
    
    req = urllib.request.Request(url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
    req.add_header("Content-Type", "application/json; charset=utf-8")
    
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))
```

---

### 3. 飞书

**API 地址**: `https://open.feishu.cn/open-apis/bot/v2/hook/{key}`

**支持的消息类型**:
- `text` - 纯文本
- `post` - 富文本
- `image` - 图片（需先上传获取 media_id）
- `share_chat` - 分享群会话
- `interactive` - 卡片消息

**发送示例**:
```python
import json
import urllib.request

def send_feishu(key, content):
    url = f"https://open.feishu.cn/open-apis/bot/v2/hook/{key}"
    data = {"msg_type": "text", "content": {"text": content}}
    
    req = urllib.request.Request(url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
    req.add_header("Content-Type", "application/json; charset=utf-8")
    
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))
```

---

## 使用示例

**用户说**：「把天气发到钉钉项目群」

**执行流程**：
1. 从配置中查找「钉钉-项目群」对应的 key
2. 获取天气数据
3. 调用 send_dingtalk 发送

---

## @mentioned 功能（企业微信）

### @所有人 ✅ 推荐方式

```python
from webhook_push import send_wechat_text

key = "YOUR_WEBHOOK_KEY"
content = "明天晚上公司聚餐，大家都来！"  # 内容里不要写 @all
send_wechat_text(key, content, mentioned_list=["@all"])
```

**注意**：内容里**不要写 @all**，只需要传 `mentioned_list=["@all"]`。如果内容里写了 @all，消息会显示两个 @all。

### @个人（临时方案）

企业微信 webhook 的 @ 个人功能需要获取成员的 userid 或手机号。如果无法获取，可用以下方式：

```python
# 在内容前面直接写 @姓名（这是临时方案，不会触发系统通知）
content = "@张三 明天上午10点开会"
send_wechat_text(key, content)
```

**效果**：消息中会显示 "@张三"，但这是纯文本显示，不会触发系统的 @ 通知。

### @个人（正确方式，需要 userid/手机号）

如果能获取到成员的 userid 或手机号，可以使用官方支持的 @ 方式：

```python
# 通过 userid @（userid 需要管理员在企业微信后台获取）
send_wechat_text(key, content, mentioned_list=["userid"])

# 通过手机号 @（需要在群里绑定过手机号）
send_wechat_text(key, content, mentioned_mobile_list=["13800001111"])
```

**注意**：
- `mentioned_list` 里 userid 前**不要加 @ 符号**，如 `["wangqing"]` 而不是 `["@wangqing"]`
- `mentioned_list=["@all"]` 里 @all **需要带 @ 符号**

### 权限要求

群聊设置中需要开启「允许机器人 @ 所有人」权限（需群主/管理员操作）。

---

## 常见错误

| 平台 | errcode | 解决方案 |
|------|---------|----------|
| 企业微信 | 301019 | 图片 MD5 不匹配 |
| 企业微信 | 93000 | webhook key 无效 |
| 钉钉 | 40014 | access_token 无效 |
| 钉钉 | 40035 | at_mobiles 格式错误 |
| 飞书 | 99991663 | webhook URL 无效 |
| 飞书 | 230001 | 消息内容过长 |

---

## 注意事项

1. **频率限制**：
   - 企业微信：每分钟 20 条
   - 钉钉：每分钟 20 条
   - 飞书：每分钟 100 条

2. **内容限制**：
   - 钉钉 Markdown 支持有限标题、列表、链接等
   - 飞书卡片支持更丰富的交互

3. **敏感词**：各平台都会对内容进行过滤