---
name: sign-off
description: "在每次完整输出后追加个性化落款签名。像对讲机的 Over，让用户明确知道 AI 说完了。Use when completing any response or after tool calls return results."
---

# Sign-Off — AI 输出结束标记

在每次完整输出的末尾追加一个个性化落款，让用户明确知道你说完了。

## 触发时机

在以下情况的**最后**追加签名：

- 完成一次完整回复后
- 工具调用返回结果并给出总结后
- 多段输出的最后一段

## 不触发

- 还在思考/输出中（不要在中间段落加）
- 只是状态更新（如"正在处理..."）
- NO_REPLY 场景

## 签名格式

另起一行，在回复内容的最末尾追加：

```
回复内容...

      {签名内容}
```

签名前加缩进（4空格或1个Tab），视觉上与正文区分。

## 读取配置

每次输出前，检查 workspace 根目录下是否有 `sign-off.json`：

**有配置文件：** 读取模板和变量，渲染签名
**无配置文件：** 使用默认签名 `{agentName} · {location}`

## 变量渲染

替换模板中的变量。对于自动变量（season、weather、time 等），可使用 `render.js` 脚本自动填充：

```bash
node render.js              # 默认模板
node render.js --work       # 使用 work 模板
node render.js --casual     # 使用 casual 模板
```

变量列表：

| 变量 | 来源 | 示例 |
|------|------|------|
| `{name}` | sign-off.json → name | 小橘 |
| `{location}` | sign-off.json → location | 杭州 |
| `{emoji}` | sign-off.json → emoji | 🏮 |
| `{seal}` | sign-off.json → seal | [橘印] |
| `{season}` | 自动判断 | 春/夏/秋/冬 |
| `{weather}` | 自动（可查天气API） | 晴/雨 |
| `{time}` | 自动（当前时段） | 午后/深夜/清晨 |
| `{greeting}` | 自动（时段问候） | 早安/午安/夜安 |
| `{dayOfWeek}` | 自动 | 周五 |
| `{zodiac}` | 自动 | 蛇年 |
| `{mood}` | sign-off.json → mood | 慵懒 |

## 上下文模式

如果配置了 `contextMode`，根据当前对话场景选择模板：

- **work**：技术讨论、执行命令 → 使用 work 模板
- **casual**：闲聊、回答问题 → 使用 casual 模板
- **auto**（默认）：AI 自行判断

如果 `contextMode` 未配置，统一使用 `template` 字段。

## 口头配置

用户可以口头修改签名：

> "你的签名改成 From 小橘, Hangzhou, with 🧡"

收到此类指令时，更新 `sign-off.json` 中的对应字段。

## 模板安装

用户也可以从模板库安装预设风格：

> "给我换个书法风的签名"

此时读取 `templates/` 目录下对应的 JSON 文件，合并到 `sign-off.json`。
