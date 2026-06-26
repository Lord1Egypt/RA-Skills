---
name: wechat-forward
description: >
  按需将当前对话内容转发到用户自己的微信。仅在用户明确要求"把这个发微信"时才执行，
  将最近的消息内容通过 wxclawbot CLI 推送到用户微信，用于手机端查看。
  Trigger ONLY when explicit: 发微信, 推送到微信, 发到微信, forward to wechat, 发给我微信,
  帮我把这段话发微信, 帮我把这个发微信, forward this to wechat, send to wechat, 微信转发。
  DO NOT TRIGGER when: 定时任务、自动推送、每日总结、告警通知、未提及"微信"的任何请求。
  ⚠️ CRITICAL: 数据仅发送给用户自己的微信账号，不发送给任何第三方。
  消息仅在用户明确要求时发送，绝不主动推送。
metadata:
  openclaw:
    requires:
      bins: [wxclawbot]
      config: [~/.openclaw/openclaw-weixin/accounts/]
    os: [macos]
    author: luzhu (卤煮火烧)
    security:
      dataFlow: self-only
      autoTrigger: false
      destination: self-wechat
---

# wechat-forward · 按需转发到微信

## 核心原则

- **响应式执行**：仅在用户明确说"发微信"时才执行
- **仅发给自己**：消息只发送到用户本人的微信账号
- **无需额外配置**：复用 openclaw-weixin 已有凭证

这个技能解决的是：用户在 Webchat 聊天时，偶尔想切换到手机微信上查看对话内容。

## 工作流程

```
用户说"把这个发微信"
  ↓
Agent 将当前消息整理后
  ↓
wxclawbot CLI 发送到用户微信
  ↓
用户手机微信收到消息
```

## 何时使用（仅限显式指令）

用户明确说出或写道：

| 触发词 | 示例 |
|--------|------|
| 发微信 | "把这个发微信" |
| 发到微信 | "把这段发到微信" |
| forward to wechat | "forward this to wechat" |
| 发消息 | "给我微信发个消息" |

## 何时禁用（坚决不触发）

| 场景 | 理由 |
|------|------|
| 定时任务 | 未授权，不主动推 |
| 每日自动总结 | 同左 |
| 告警通知 | 除非用户设置过 |
| 内容生成（没提微信） | 只有明确说"微信"才触发 |

## 发送方式

### 纯文本

将当前消息整理后发送：

```bash
wxclawbot send --text "消息内容" --json
```

### 附带文件

如需同时发送文件：

```bash
wxclawbot send --file /path/to/file --text "说明" --json
```

### 检查结果

成功时：`{"ok":true,"to":"user@im.wechat","clientId":"..."}`
失败时：检查 `errorKind`（timeout/connection/dns/tls）和 `retryable` 字段

## 频率说明

- 同一 bot 约 **7 条 / 5 分钟**（所有客户端共享）
- 收到 `ret=-2` 时等 60-120 秒重试
- 建议一次发送，不要拆成多条

## 内容整理指南

当用户说"把这个发微信"时：

1. **简短回复**：直接转发最新消息
2. **长对话**：归纳要点，保持手机可读
3. **报告类**：含标题、关键数据、结论
4. **决策类**：含选项和最终决定

**原则**：让用户手机上一眼能看懂，不啰嗦、不丢重点。

## 前置条件

已安装 wxclawbot CLI 并登录微信账号（openclaw-weixin 已配置即可）。

验证方法：

```bash
wxclawbot accounts --json
```

## 错误处理

| 现象 | 原因 | 处理 |
|------|------|------|
| `ok:false`, `ret=-2` | 频率限制 | 等 60-120 秒重试 |
| `ok:false`, `ret=-14` | 会话过期 | 重新登录微信 |
| No account found | 凭证缺失 | 检查 accounts 目录 |
| `ok:true` 但用户没收到 | Context token 过期 | 用户给机器人发条消息刷新 |

## 安全说明

- ✅ **自转发**：消息仅发到用户自己的微信账号，不接触第三方
- ✅ **仅响应式**：仅在用户明确要求时执行，无自动触发
- ✅ **数据流向**：当前对话 → 用户微信（闭环，不外泄）
- ✅ **可审计**：所有发送记录在 wxclawbot 日志中
