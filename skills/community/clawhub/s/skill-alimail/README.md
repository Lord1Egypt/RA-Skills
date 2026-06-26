# 阿里邮箱管理技能 (skill-alimail)

提供阿里邮箱 API 调用能力，支持用户信息查询、邮件详情获取、邮件搜索。

## 🛠️ 前置准备

1. **环境变量**
   使用前需配置阿里邮箱的环境变量：
   - `ALMAIL_APP_ID`：阿里邮箱应用 ID
   - `ALMAIL_SECRET`：阿里邮箱应用 Secret

2. **认证方式**
   当前使用 OAuth2 `client_credentials` 流程，由 `alimail-node-sdk` 在请求时处理令牌申请。

3. **安装依赖**
   ```bash
   npm install alimail-node-sdk
   ```
## ✨ 主要功能

- **用户信息查询** (`scripts/get_user.js`)：获取邮箱用户的详细资料（支持选择扩展字段）
- **邮件详情获取** (`scripts/get_message.js`)：通过 `message-id` 查看特定邮件的具体内容
- **邮件搜索** (`scripts/search_messages.js`)：支持 KQL 查询语法、分页，快速筛选邮件

## 🚀 快速上手

### 1. 获取用户信息
```bash
node scripts/get_user.js --email "user@example.com" --select "phone,managerInfo"
```

### 2. 查看邮件详情
```bash
node scripts/get_message.js --email "user@example.com" --message-id "MESSAGE_ID" --select "body,toRecipients"
```

### 3. 搜索邮件
```bash
node scripts/search_messages.js --email "user@example.com" --query 'fromEmail="alice@example.com"' --size 20
```

---
💡 **更多文档**：
- API 参数及 KQL 查询语法详见：[references/alimail-api.md](references/alimail-api.md)
