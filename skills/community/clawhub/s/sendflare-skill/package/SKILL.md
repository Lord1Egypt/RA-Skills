# Sendflare Skill

通过 Sendflare SDK 发送电子邮件的技能。

## 功能特点

- 📧 发送电子邮件（支持 CC/BCC）
- 🔒 安全的 API 认证

## 功能状态

| 功能 | 状态 | 配置要求 |
|------|------|----------|
| 发送邮件 | ✅ 稳定 | apiToken |
| 获取联系人 | ⚠️ 实验性 | apiToken + appId |
| 保存联系人 | ⚠️ 实验性 | apiToken + appId |
| 删除联系人 | ⚠️ 实验性 | apiToken + appId |

## 重要说明

- ❌ **不支持发送附件**
- 联系人管理功能需要额外配置 appId
- 发件人地址必须在 Sendflare 后台完成 DNS 验证

## 配置要求

| 参数 | 必填 | 说明 |
|------|------|------|
| apiToken | ✅ 是 | Sendflare API 令牌（必需） |
| appId | ❌ 否 | 应用 ID（仅联系人功能需要） |

## 使用方法

### 发送邮件
发送邮件给 test@example.com，主题：测试邮件，内容：这是一封测试邮件

> 注意：不支持发送附件

### 获取联系人列表
获取联系人列表

### 保存联系人
保存联系人 john@example.com，姓名：John Doe

### 删除联系人
删除联系人 john@example.com

### 获取帮助
帮助

## 使用示例

**用户**: "发送邮件给 test@example.com，主题：会议通知，内容：明天下午 3 点开会"
**技能**: "✅ 邮件发送成功！"

**用户**: "获取联系人列表"
**技能**: "📋 联系人列表 (第 1 页，共 10 个联系人): ..."

## 注意事项

- 需要有效的 Sendflare API Token
- 发件人地址必须是你验证过的域名
- 支持 HTML 格式的邮件内容

## 故障排除

**认证失败**
- 检查 API Token 是否正确
- 确认 Token 未过期

**发送失败**
- 检查发件人地址是否已验证
- 确认收件人地址格式正确

## 隐私说明

本技能仅在发送邮件时访问必要的联系信息，不会收集任何个人信息。所有 API 凭证均加密存储。

## 限制

- 速率限制：每分钟 100 次请求
- 每日发送限额：取决于你的 Sendflare 套餐
- ❌ 不支持附件发送

## 链接

- [Sendflare](https://Sendflare.com)
- [Node.js SDK](https://docs.Sendflare.com/docs/sdk/nodejs/)
- [API 文档](https://docs.Sendflare.com/)

## 许可证

MIT
