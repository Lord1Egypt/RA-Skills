# S2: 消息推送

## 触发

用户问句含「推送/发送/通知」+「渠道名称」。

> 若问句不含推送语义或不含渠道名称，本场景不适用，回退到 Part 1 通用流程。

| 条件 | 关键词 |
|------|--------|
| **推送动作** | 发送/推送/通知/发到/推到/上报 |
| **渠道名称** | 企业微信/企微/微信/WeChat/钉钉/DingTalk/飞书/Feishu/邮件/email/系统消息/站内消息 |

**示例**：
- "发送今天的销售额报表到企微群"
- "推送客户流失报告到钉钉"
- "邮件通知管理员系统状态"

> 若问句**同时**含「定时/每天/每周」+「推送」→ 走 S1 定时计划任务（脚本中调用 push API），非本场景。

## 意图解析

| 参数 | 来源 | 示例 |
|------|------|------|
| channelType | 渠道名称 | "企微/企微群"→WECHAT_WORK, "钉钉"→DINGTALK, "邮件"→MAIL |
| content | 用户描述/上下文数据 | Agent 拼接的 Markdown/HTML |
| config | 渠道专属 | webhookUrl（群机器人）/ agentId（企微应用）/ recipients（邮件/消息） |

## 执行步骤

```
Step 1: smartbi list --domain push --agent
   ↓    确认 push 接口可用，记录 operationKey
Step 2: smartbi describe push.sendMessage --agent
   ↓    理解 config 参数结构，加载关联文档
Step 3: 按渠道 + 内容构造 JSON 请求体
   ↓
Step 4: smartbi call push.sendMessage -d @body.json --agent
   ↓    返回 {"ok":true, "data": {"platformTaskId": "..."}}
Step 5 (可选): smartbi call push.getSendProgress -d @progress.json --agent
        查询推送结果
```

## API 请求体

### 发送消息

```
POST /api/v1/push/send-message
```

**企微群机器人**：

```json
{
  "sendMessageRequest": {
    "channelType": "WECHAT_WORK",
    "content": "## 每日销售额\n\n今日销售额：**¥1,234,567**\n较昨日增长：8.5%",
    "contentType": "MARKDOWN",
    "title": "每日销售额报表",
    "config": {
      "webhookUrl": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
    }
  }
}
```

**企微企业应用**：

```json
{
  "sendMessageRequest": {
    "channelType": "WECHAT_WORK",
    "content": "## 告警通知\n\n服务器 CPU 使用率超过 90%",
    "config": {
      "agentId": "1000002",
      "toUsers": "zhangsan|lisi"
    }
  }
}
```

**钉钉群机器人（带加签）**：

```json
{
  "sendMessageRequest": {
    "channelType": "DINGTALK",
    "content": "## 客户流失报告\n\n本月流失客户数：12\n流失率：3.2%",
    "title": "客户流失报告",
    "config": {
      "webhookUrl": "https://oapi.dingtalk.com/robot/send?access_token=xxx",
      "secret": "SECxxx"
    }
  }
}
```

**邮件**：

```json
{
  "sendMessageRequest": {
    "channelType": "MAIL",
    "content": "<h1>系统状态报告</h1><p>各服务正常运行</p>",
    "contentType": "HTML",
    "title": "系统状态报告",
    "recipients": ["admin@company.com", "ops@company.com"]
  }
}
```

**系统消息**：

```json
{
  "sendMessageRequest": {
    "channelType": "MESSAGE",
    "content": "审批流程已完成，请查看。",
    "title": "审批通知",
    "recipients": ["userId1", "userId2"]
  }
}
```

### 查询进度

```
POST /api/v1/push/get-send-progress
```

```json
{
  "platformTaskId": "<sendMessage 返回的 platformTaskId>"
}
```

## 渠道识别映射

| 用户说… | channelType | config 模式 |
|---------|-------------|------------|
| 企微/企业微信/微信/WeChat + 群里/机器人/webhook | `WECHAT_WORK` | `config.webhookUrl` |
| 企微/企业微信 + 应用/通知/agentId | `WECHAT_WORK` | `config.agentId` |
| 钉钉/DingTalk + 群里/机器人/webhook | `DINGTALK` | `config.webhookUrl` |
| 钉钉/DingTalk + 工作通知/toUsers | `DINGTALK` | `config.toUsers` |
| 飞书/Feishu | `FEISHU` | `config.webhookUrl` |
| 邮件/email/邮箱 | `MAIL` | `recipients`（邮箱地址） |
| 系统消息/站内消息/消息通知 | `MESSAGE` | `recipients`（用户 ID） |

> 如用户未明确群机器人/企业应用，默认使用群机器人模式（更简单，只需 webhookUrl）。

## 注意

- 企微群机器人和钉钉群机器人的 webhookUrl 需用户提供——Agent 应主动询问"请提供企微/钉钉群机器人 webhook 地址"
- `WECHAT_WORK` 和 `DINGTALK` 通过 `config` 内容区分群机器人/企业应用模式，无需用户手动选择子类型
- 推送是异步的——`sendMessage` 返回 `platformTaskId` 后，可通过 `getSendProgress` 查询最终结果
- content 默认 Markdown 格式，也可指定 TEXT（纯文本）或 HTML（仅邮件渠道推荐）

## 在定时任务脚本中调用（S1 场景）

当推送作为 S1 定时计划任务的组成部分时，**不走 CLI `smartbi call`**，而是在 Rhino JS 脚本中通过 HTTP 调用 push API。详见 `references/rhino-template.md` 中的 `pushMessage()` 辅助函数和多渠道路由模式。

核心差异：
- 认证：脚本中复用 `TOKEN`（环境变量或 RMI `generateTempToken`），无需重新鉴权
- 序列化：使用 `Packages.smartbi.net.sf.json.JSONObject.fromObject(payload).toString()`
- 路径：sdk-server 为 `/api/v1/push/push/send-message`（双 push），Smartbi 直连为 `/api/v1/push/send-message`
- 邮件渠道：脚本中优先用 `sendToMail` 内置 Routine（更简洁），非邮件渠道才走 push API
