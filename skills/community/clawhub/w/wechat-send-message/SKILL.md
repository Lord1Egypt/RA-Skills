---
name: wechat-send-message
description: 在微信 Mac 版发送消息。当用户提到"微信发消息"、"发微信"、"给 XXX 发微信"时触发。
---

# 微信 Mac 版消息发送

## 微信界面结构

```
┌─────────┬──────────────────┬─────────────┐
│ 功能区   │ 搜索框  联系人列表 │ 聊天区域    │
│ 聊天     │ [🔍]              │             │
│ 联系人   │ [小+号]           │ 输入框...   │
│ 收藏     │ 联系人1           │             │
│ 朋友圈   │ 联系人2           │             │
│ ...     │ ...              │             │
└─────────┴──────────────────┴─────────────┘
```

## 执行流程

### Step 1: 打开微信

```bash
open /Applications/WeChat.app
sleep 1
```

### Step 2: 点击搜索框并输入

```javascript
// 点击第二列搜索框 (约坐标 180, 45)
cliclick c:180,45
osascript -e 'set the clipboard to "CONTACT_NAME"'
osascript -e 'tell application "System Events" to keystroke "v" using command down'
sleep 0.3
```

### Step 3: 按 Enter 直接选中最上面的搜索结果

```javascript
osascript -e 'tell application "System Events" to keystroke return'
sleep 0.5
```

### Step 4: 直接输入消息（第三列已聚焦）

```javascript
osascript -e 'tell application "System Events" to keystroke "MESSAGE_CONTENT"'
sleep 0.2
```

### Step 5: 按 Enter 发送

```javascript
osascript -e 'tell application "System Events" to keystroke return'
```

## 关键坐标

| 元素 | 坐标 |
|------|------|
| 搜索框 | 180, 45 |
| 搜索结果（单个） | 180, 90 |
| 聊天输入框 | 350, 560 |

## 注意事项

- **必须先点击搜索框再输入**，否则中文字符无法输入
- **Enter 搜索后直接选中第一个结果**，不需要双击
- **输入消息前不需要再次点击输入框**，Enter 后第三列自动聚焦
- 使用 `keystroke` 而非剪贴板输入消息
- 搜索时用名字的部分字符即可匹配

## 性能

- 目标总耗时：**3-5 秒**

## 联系人配合

发送前可先调用 `person-relation-manager` 查询微信昵称：
- 微信名 ≠ 真实姓名
- 优先使用已记忆的微信昵称
