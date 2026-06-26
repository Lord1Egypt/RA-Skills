---
name: feishu-card
description: 飞书互动卡片发送技能（国际版 Feishu 兼容）。当需要发送格式丰富的飞书卡片消息时使用。支持标题、Markdown 内容、颜色主题。关键：必须使用 schema 2.0 格式 + 双重 JSON stringify，否则国际版飞书（Feishu）无法渲染。
---

# 飞书互动卡片发送技能

## 核心要点（必读）

飞书卡片有新旧两种格式：
- **旧版 components 格式**：部分版本不兼容，显示"请升级至最新版本客户端"
- **schema 2.0 格式**：✅ 推荐，飞书 7.x 均支持

统一用 schema 2.0 即可，不管飞书是中文界面还是英文界面都能用。

## 关键：双重 JSON.stringify

```python
import json

card = { ... }  # 卡片对象
content = json.dumps(json.dumps(card))  # 必须 dumps 两次！
```

一次 stringify 不够，飞书 API 的 `content` 字段要求是 JSON 字符串。

## 卡片结构（schema 2.0）

```json
{
  "schema": "2.0",
  "header": {
    "title": {
      "tag": "plain_text",
      "content": "标题文字"
    },
    "template": "blue"
  },
  "body": {
    "elements": [
      {
        "tag": "markdown",
        "content": "**加粗** 普通文字\n\n支持换行"
      }
    ]
  }
}
```

### header.template 颜色选项
- `blue` — 蓝色（默认推荐）
- `green` — 绿色
- `red` — 红色
- `orange` — 橙色
- `purple` — 紫色
- `grey` — 灰色

### body.elements 支持的 tag
- `markdown` — Markdown 文本（支持 **加粗**、*斜体*、`代码`、链接）
- `hr` — 分割线：`{"tag": "hr"}`
- `note` — 底部备注

## 发送方式

### 方法一：用脚本（推荐）

```bash
python3 /root/.openclaw/workspace/skills/feishu-card/scripts/send_card.py \
  --open-id "ou_xxxx" \
  --title "标题" \
  --content "**内容** 支持 Markdown" \
  --template "blue"
```

### 方法二：用 message tool

直接调用 `message` tool，`msg_type` 需要写 `interactive`，`content` 需要双重 stringify（先序列化卡片对象，再序列化整个字符串）。

### 方法三：curl（手动）

```bash
APP_SECRET=$(cat /root/.openclaw/openclaw.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['channels']['feishu']['appSecret'])")
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"cli_a9f5877b3378dbd8\",\"app_secret\":\"$APP_SECRET\"}" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['tenant_access_token'])")

python3 -c "
import json
card = {
    'schema': '2.0',
    'header': {'title': {'tag': 'plain_text', 'content': '标题'}, 'template': 'blue'},
    'body': {'elements': [{'tag': 'markdown', 'content': '内容'}]}
}
print(json.dumps(json.dumps(card)))
" | xargs -I{} curl -s -X POST \
  "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"ou_xxxx\",\"msg_type\":\"interactive\",\"content\":{}}"
```

## 已知信息（猫南北账号）

- **open_id**: `ou_22f2eefd5abe63e0cd67f4882cec06d4`
- **app_id**: `cli_a9f5877b3378dbd8`
- **app_secret**: 从 `/root/.openclaw/openclaw.json` 读取
- **客户端版本**: 飞书 7.62.6，schema 2.0 验证通过

## 排错

| 现象 | 原因 | 解决 |
|------|------|------|
| "请升级至最新版本客户端" | 用了旧版 components 格式 | 换成 schema 2.0 |
| code 400 JSON parse error | content 没有双重 stringify | `json.dumps(json.dumps(card))` |
| 消息发出但内容为空 | schema 字段缺失 | 确保 `"schema": "2.0"` |
