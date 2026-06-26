# 会话名称修改 (Session Rename)

> 直接编辑 `sessions.json` 给 OpenClaw 会话设置显示名称，弥补 CLI/RPC 没有改标题功能的空白。

## 安装

```bash
clawhub install session-rename-zh
```

## 它能干什么

OpenClaw 的会话标题（`derivedTitle`）是系统自动从第一条消息截取的，没有 CLI 命令或 RPC 方法可以修改。

这个技能通过直接编辑 `~/.openclaw/agents/main/sessions/sessions.json`，给目标会话添加 `label` 字段，实现会话名称的修改。

## 效果演示

修改前，`sessions_list` 显示的默认标题：
```
derivedTitle: "[Sun 2026-05-24 12:54 GMT+8] 这个对话是watchdose项目的..."
```

修改后，显示自定义名称：
```
displayName: "WatchDose · 吃药提醒"
derivedTitle: "WatchDose · 吃药提醒"
```

![效果对比](https://raw.githubusercontent.com/fhekg/openclaw-session-rename/main/assets/demo.png)

## 使用方式

只需对 OpenClaw 说：

- 「把这个会话叫 WatchDose」
- 「改会话名为 吃药提醒项目」
- 「rename this session to My Project」

技能会自动：
1. 获取当前会话 key
2. 安全读取 `sessions.json`（python3 操作，不动其他字段）
3. 写入 `label` 字段
4. 验证生效

## 原理

```jsonc
// ~/.openclaw/agents/main/sessions/sessions.json
{
  "agent:main:main": {
    "sessionId": "1311a7de-...",
    // 加这一行：
    "label": "WatchDose · 吃药提醒"
  }
}
```

OpenClaw 的 JSON store 设计上是安全可编辑的，`label` 会自动映射为 `displayName` 和 `derivedTitle`。

## 仓库

https://github.com/fhekg/openclaw-session-rename
