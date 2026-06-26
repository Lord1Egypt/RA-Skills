# 阿里邮箱API参考文档

## 目录
- [API概述](#api概述)
- [用户信息查询](#用户信息查询)
- [邮件详情获取](#邮件详情获取)
- [邮件搜索](#邮件搜索)
- [KQL查询语法](#kql查询语法)
- [常见字段说明](#常见字段说明)

## API概述

阿里邮箱开放API基于OAuth2认证，使用client_credentials模式获取access_token。

### 认证方式
- 授权模式：OAuth2 client_credentials
- 请求头：`Authorization: Bearer {access_token}`
- 限流：单域总流量不超过40次/秒

### 基础URL
```
https://alimail-cn.aliyuncs.com
```

### 错误处理
SDK会自动处理以下情况：
- 401未授权：自动刷新token后重试
- 429限流：指数退避重试
- 5xx服务器错误：自动重试

## 用户信息查询

### 接口
```
GET /v2/users/{id | email}
```

### 权限要求
- User.Read.All
- User.ReadWrite.All

### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| identifier | string | 是 | 用户ID或邮箱地址 |
| select | string或string[] | 否 | 要返回的可选字段 |

### 常用$select字段
- `phone` - 电话号码
- `managerInfo` - 经理信息
- `homeLocation` - 位置信息
- `departmentPath` - 部门路径
- `lastLoginTime` - 最后登录时间
- `customFields` - 自定义字段

### 返回字段
```json
{
  "id": "用户ID",
  "email": "邮箱地址",
  "name": "姓名",
  "phone": "电话",
  "department": "部门",
  "jobTitle": "职位"
}
```

## 邮件详情获取

### 接口
```
GET /v2/users/{email}/messages/{id}
```

### 权限要求
- Mail.Read.All
- Mail.ReadWrite.All

### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| email | string | 是 | 用户邮箱地址 |
| messageId | string | 是 | 邮件唯一标识 |
| select | string或string[] | 否 | 要返回的字段 |
| unwrapMessage | boolean | 否 | 是否仅返回message字段，默认true |

### 常用$select字段
- `internetMessageId` - 互联网消息ID
- `body` - 邮件正文
- `toRecipients` - 收件人列表
- `ccRecipients` - 抄送人列表
- `bccRecipients` - 密送人列表
- `sender` - 发件人
- `replyTo` - 回复地址
- `receivedDateTime` - 接收时间
- `lastModifiedDateTime` - 最后修改时间
- `tags` - 标签
- `subject` - 主题

### 返回字段
```json
{
  "id": "邮件ID",
  "internetMessageId": "互联网消息ID",
  "subject": "邮件主题",
  "body": {
    "contentType": "HTML",
    "content": "邮件正文内容"
  },
  "sender": {
    "emailAddress": {
      "name": "发件人姓名",
      "address": "发件人邮箱"
    }
  },
  "toRecipients": [
    {
      "emailAddress": {
        "name": "收件人姓名",
        "address": "收件人邮箱"
      }
    }
  ],
  "receivedDateTime": "2025-01-01T00:00:00Z"
}
```

## 邮件搜索

### 接口
```
POST /v2/users/{email}/messages/query
```

### 权限要求
- Mail.Read.All
- Mail.ReadWrite.All

### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| email | string | 是 | 用户邮箱地址 |
| query | string | 是 | KQL查询语句 |
| cursor | string | 是 | 分页游标，首次传空字符串 |
| size | number | 是 | 每页数量，取值1-100 |
| select | string或string[] | 否 | 要返回的字段 |

### 返回字段
```json
{
  "messages": [...],
  "nextCursor": "下一页游标"
}
```

### 分页查询
1. 第一次请求：cursor传空字符串 `""`
2. 后续请求：使用返回的 `nextCursor` 作为新的 cursor
3. 当 `nextCursor` 为空时，表示没有更多数据

## KQL查询语法

### 基本语法
KQL (Keyword Query Language) 用于构造复杂的查询条件。

### 常用操作符
- `=` 等于
- `>` 大于
- `<` 小于
- `>=` 大于等于
- `<=` 小于等于
- `AND` 逻辑与
- `OR` 逻辑或
- `NOT` 逻辑非

### 常用查询字段

#### 邮件相关
- `fromEmail` - 发件人邮箱
- `toRecipients` - 收件人
- `subject` - 邮件主题
- `receivedDateTime` - 接收时间
- `isRead` - 是否已读

#### 示例查询

**查询来自特定发件人的邮件**
```
fromEmail="alice@example.com"
```

**查询特定时间之后的邮件**
```
date>2025-01-01T00:00:00Z
```

**查询特定主题的邮件**
```
subject="项目周报"
```

**组合查询（时间+发件人）**
```
date>2025-01-01T00:00:00Z AND fromEmail="alice@example.com"
```

**排除已删除文件夹**
```
date>2025-01-01T00:00:00Z AND (NOT folderId:3)
```

**查询包含多个条件的邮件**
```
fromEmail="alice@example.com" OR fromEmail="bob@example.com"
```

**使用引号处理特殊字符**
```
subject="项目: Q1报告"
```

## 常见字段说明

### 用户字段
| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 用户唯一ID |
| email | string | 邮箱地址 |
| name | string | 姓名 |
| phone | string | 电话号码 |
| department | string | 部门名称 |
| jobTitle | string | 职位 |
| managerInfo | object | 经理信息 |
| homeLocation | object | 位置信息 |

### 邮件字段
| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 邮件唯一ID |
| internetMessageId | string | 互联网消息ID |
| subject | string | 邮件主题 |
| body | object | 邮件正文 |
| sender | object | 发件人信息 |
| toRecipients | array | 收件人列表 |
| ccRecipients | array | 抄送人列表 |
| bccRecipients | array | 密送人列表 |
| replyTo | array | 回复地址 |
| receivedDateTime | string | 接收时间（ISO8601格式） |
| lastModifiedDateTime | string | 最后修改时间（ISO8601格式） |
| tags | array | 标签列表 |
| isReadReceiptRequested | boolean | 是否要求已读回执 |

## 注意事项

1. **限流处理**：API限流为40次/秒，超出会返回429状态码，SDK会自动重试
2. **分页查询**：使用cursor机制，每次最多返回100条邮件
3. **字段选择**：使用`$select`参数可以减少返回数据量，提高性能
4. **时间格式**：所有时间字段使用ISO8601格式，例如 `2025-01-01T00:00:00Z`
5. **查询语法**：KQL查询语句需要使用引号包裹字符串值
6. **权限要求**：不同的API需要不同的权限，确保应用已正确配置
