# 腾讯云邮件推送（SES）API 参考

## 目录

- [API 概览](#api-概览)
- [地域支持](#地域支持)
- [发信域名配置流程](#发信域名配置流程)
- [SendEmail 参数说明](#sendemail-参数说明)
  - [必填参数](#必填参数)
  - [收件人参数](#收件人参数至少填一个)
  - [内容参数](#内容参数二选一)
  - [可选参数](#可选参数)
  - [Attachment 数据结构](#attachment-数据结构)
  - [请求示例](#请求示例)
- [GetSendEmailStatus 状态码](#getsendemailstatus-状态码)
  - [SendStatus（腾讯云处理状态）](#sendstatus腾讯云处理状态)
  - [DeliverStatus（收件方处理状态）](#deliverstatus收件方处理状态)
- [模板状态码](#模板状态码)
- [注意事项](#注意事项)

---

## API 概览

| 接口名称 | 功能描述 | 对应脚本命令 |
|----------|----------|-------------|
| ListEmailIdentities | 获取发信域名列表 | `list-domains` |
| GetEmailIdentity | 获取域名配置详情 | `get-domain` |
| CreateEmailIdentity | 创建发信域名 | `create-domain` |
| UpdateEmailIdentity | 请求验证域名 | `verify-domain` |
| ListEmailAddress | 获取发信地址列表 | `list-addresses` |
| CreateEmailAddress | 创建发信地址 | `create-address` |
| SendEmail | 发送邮件 | `send-template` / `send-simple` |
| GetSendEmailStatus | 获取邮件发送状态 | `get-status` |
| ListEmailTemplates | 获取模板列表 | `list-templates` |
| GetEmailTemplate | 获取模板详情 | `get-template` |
| CreateEmailTemplate | 创建邮件模板 | `create-template` |
| UpdateEmailTemplate | 更新邮件模板 | `update-template` |
| DeleteEmailTemplate | 删除邮件模板 | `delete-template` |

---

## 地域支持

| 地域 | 地域标识 |
|------|----------|
| 广州 | `ap-guangzhou` |
| 香港 | `ap-hongkong` |
| 新加坡（国际站） | `ap-singapore` |

---

## 发信域名配置流程

1. **创建域名**：调用 `CreateEmailIdentity` 接口创建发信域名。
2. **配置 DNS**：根据接口返回的 `Attributes` 字段，在 DNS 服务商处配置所需的 DNS 记录（TXT / CNAME / MX）。
3. **请求验证**：调用 `UpdateEmailIdentity` 接口提交验证请求（DNS 传播可能需要 10 分钟至 72 小时）。
4. **创建发信地址**：域名验证通过后，调用 `CreateEmailAddress` 接口创建发信地址。

### DNS 记录类型说明

| 记录类型 | 用途 |
|----------|------|
| TXT（SPF） | 验证发送权限，值通常为 `v=spf1 include:qcloudmail.com ~all` |
| TXT（DKIM） | DKIM 签名验证，须使用 TXT 记录（不支持 CNAME 模式） |
| CNAME | 用于追踪邮件打开和链接点击等事件 |
| MX | 邮件交换记录（可选，用于接收退信通知） |

---

## SendEmail 参数说明

### 必填参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `FromEmailAddress` | String | 发件人地址，支持别名格式：`别名 <邮箱>` 或直接 `邮箱地址` |
| `Subject` | String | 邮件主题 |

### 收件人参数（至少填一个）

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `Destination` | Array of String | 收件人列表，最多 50 人（逗号分隔传入时自动拆分为数组） |
| `Cc` | Array of String | 抄送人列表，最多 20 人 |
| `Bcc` | Array of String | 密送人列表，最多 20 人，不可与 `Destination` 中的地址重复 |

### 内容参数（二选一）

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `Template` | Template | 模板发送（需提供 TemplateID 和 TemplateData JSON 字符串） |
| `Simple` | Simple | 自定义内容发送（Html / Text 内容须经 Base64 编码）⚠️ 仅支持部分已申请特殊配置的客户使用 |

### 可选参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `ReplyToAddresses` | String | 回复地址，未填写时收件人回复邮件将发送失败 |
| `Attachments` | Array of Attachment | 附件列表，附件总大小 ≤ 4 MB（Base64 编码后请求包 ≤ 8 MB） |
| `Unsubscribe` | String | 退订链接语言：0=不加 1=简中 2=英文 3=繁中 4=西班牙 5=法语 6=德语 7=日语 8=韩语 9=阿拉伯 10=泰语 |
| `TriggerType` | Integer | 邮件触发类型：0=非触发类（营销邮件） 1=触发类（验证码等即时邮件） |
| `SmtpMessageId` | String | SMTP Message-Id |
| `SmtpHeaders` | String | SMTP 自定义头部，JSON 格式 |
| `HeaderFrom` | String | SMTP From 头部值，建议与 `FromEmailAddress` 的域名保持一致 |

### Attachment 数据结构

| 字段名 | 类型 | 是否必填 | 说明 |
|--------|------|:--------:|------|
| `FileName` | String | ✅ | 附件文件名，最长 255 字符 |
| `Content` | String | ✅ | Base64 编码后的附件内容 |

### 请求示例

**模板发送**：

```json
{
  "FromEmailAddress": "别名 <email@domain.com>",
  "Destination": ["to@example.com"],
  "Cc": ["cc@example.com"],
  "Bcc": ["bcc@example.com"],
  "ReplyToAddresses": "reply@example.com",
  "Subject": "邮件主题",
  "Template": {
    "TemplateID": 12345,
    "TemplateData": "{\"key\":\"value\"}"
  },
  "Unsubscribe": "1",
  "Attachments": [
    {"FileName": "doc.pdf", "Content": "<Base64 编码内容>"}
  ]
}
```

**自定义内容发送（HTML / 纯文本）**：

```json
{
  "FromEmailAddress": "sender@domain.com",
  "Destination": ["to@example.com"],
  "Subject": "邮件主题",
  "Simple": {
    "Html": "<Base64 编码的 HTML 内容>",
    "Text": "<Base64 编码的纯文本内容>"
  },
  "ReplyToAddresses": "reply@example.com"
}
```

---

## GetSendEmailStatus 状态码

### SendStatus（腾讯云处理状态）

| 状态码 | 含义 |
|:------:|------|
| 0 | 处理成功 |
| 1001 ~ 1005 | 内部系统异常 |
| 1006 | 触发频率控制（同一发信地址在一小时内向同一收件地址发送邮件超过上限） |
| 1007 | 邮件地址在黑名单中 |
| 1008 | 域名被收件方拒收 |
| 1010 | 超出每日发送限制 |
| 1011 | 无自定义内容发送权限（该功能仅支持部分已申请特殊配置的客户使用） |
| 3007 | 模板 ID 无效或不可用 |
| 3014 | 发件域名未通过认证 |
| 3030 | 退信率过高，暂停发送 |
| 3033 | 账户余额不足或已欠费 |

### DeliverStatus（收件方处理状态）

| 状态码 | 含义 |
|:------:|------|
| 0 | 已进入发送队列 |
| 1 | 邮件递送成功 |
| 2 | 邮件被丢弃 |
| 3 | 收件方 ESP 拒信（通常为邮箱地址不存在） |
| 8 | 延迟递送中 |

---

## 模板状态码

| 状态值 | 含义 |
|:------:|------|
| 0 | 审核通过 |
| 1 | 待审核 |
| 2 | 审核拒绝 |

---

## 注意事项

| 事项 | 说明 |
|------|------|
| **频率限制** | 同一发信地址在一小时内向同一收件地址发送邮件超过上限时，API 将返回 `FailedOperation.FrequencyLimit` 错误。批量发送场景建议拉大发送间隔或使用 `BatchSendEmail` 接口。 |
| **状态查询时效** | `GetSendEmailStatus` 仅支持查询近 30 天内的发送记录。 |
| **状态更新延迟** | 邮件发送后状态不会立即更新，建议等待约 1 分钟后再进行查询。 |
| **查询频率限制** | `GetSendEmailStatus` 接口默认频率限制为 1 次/秒。 |
| **群发显示** | 群发邮件会向所有收件人展示完整的收件人列表。如需隐藏其他收件人信息，请分多次调用接口逐一发送。 |
| **地址数量上限** | 每个账号下的发信地址总数上限为 10 个。 |