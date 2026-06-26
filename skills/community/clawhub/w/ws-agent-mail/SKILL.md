---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 30450220270e35dac14285ad85a59ef4ea08be446e67377133a38d9ef80cb5d29b82fe19022100f07dbedeeb931aa5c3f8f12e77486e89885d175d77a0f9c81bb0efc44c46aedd
    ReservedCode2: 3044022041fd22373ed72d76ce85e2e467eb3d054387fde8fa80de0a812052ace31adf270220720b01010a024ef307b9a3a8da0920857bcef8e27a949aeb6ff415499e93799e
description: 邮件智能处理。使用 AgentMail API 收发邮件。
metadata:
    category: 生产力
    emoji: "\U0001F4E7"
    triggers:
        - 邮件
        - email
        - 发邮件
        - 收邮件
        - mail
name: agent-mail
---

# Agent Mail 技能

基于 AgentMail 的智能邮件处理。

## 功能

- 📬 **收发邮件** - 通过 AgentMail API 发送和接收邮件
- 📋 **邮箱管理** - 创建和管理邮箱
- 📎 **附件处理** - 支持附件发送和接收
- 💬 **邮件会话** - 管理邮件对话线程

## 配置

- API Key: 已配置
- 邮箱: fhbillwer@agentmail.to

## 使用方式

```
帮我发一封邮件给 xxx@example.com
主题：xxx
内容：xxx

查看我的收件箱
```

---

**数据存储**: 邮件数据保存在 `/workspace/data/emails/`
