---
name: alimail-manager
description: 提供阿里邮箱API调用能力，支持用户信息查询、邮件详情获取、邮件搜索；当用户需要查询企业邮箱用户信息、查看特定邮件内容、搜索符合条件的邮件时使用
required_env:
  - ALMAIL_APP_ID
  - ALMAIL_SECRET
auth:
  type: oauth2_client_credentials
dependency:
  system:
    - npm install alimail-node-sdk
---

# 阿里邮箱管理

## 任务目标
- 本 Skill 用于：管理阿里邮箱用户和邮件数据
- 能力包含：用户信息查询、邮件详情获取、邮件列表搜索、分页查询
- 触发条件：用户需要查询企业邮箱用户、查看邮件内容、搜索邮件列表

## 前置准备
- 依赖说明：需要安装阿里邮箱SDK
  ```bash
  npm install alimail-node-sdk
  ```
- 认证方式：OAuth2 `client_credentials`
- 必填环境变量：
  - `ALMAIL_APP_ID`：阿里邮箱应用 ID
  - `ALMAIL_SECRET`：阿里邮箱应用 Secret

## 操作步骤

### 标准流程

1. **执行具体操作**
   - 获取用户信息：调用 `scripts/get_user.js`
   - 获取邮件详情：调用 `scripts/get_message.js`
   - 搜索邮件：调用 `scripts/search_messages.js`

2. **处理结果**
   - 解析返回的JSON数据
   - 根据业务需求提取关键信息
   - 提供清晰的总结和建议

### 可选分支

- 当 **需要获取扩展字段**：在参数中指定 `select` 字段
- 当 **需要分页查询**：使用 `search_messages.js` 的 cursor 机制
- 当 **遇到API限流**：SDK会自动处理重试，建议适当降低请求频率

## 资源索引

- API参考：
  - [references/alimail-api.md](references/alimail-api.md) (何时读取：需要了解API参数、字段定义、KQL查询语法)

## 注意事项

- 邮件搜索支持KQL查询语法，详见参考文档
- 使用时必须配置 `ALMAIL_APP_ID` 和 `ALMAIL_SECRET`

## 使用示例

### 示例1：获取用户信息
```bash
node scripts/get_user.js --email "zhangsan@example.com" --select "phone,managerInfo"
```

### 示例2：获取邮件详情
```bash
node scripts/get_message.js --email "zhangsan@example.com" --message-id "AAMkAGI2T..." --select "body,toRecipients"
```

### 示例3：搜索邮件
```bash
node scripts/search_messages.js --email "zhangsan@example.com" --query 'fromEmail="alice@example.com"' --size 20
```
