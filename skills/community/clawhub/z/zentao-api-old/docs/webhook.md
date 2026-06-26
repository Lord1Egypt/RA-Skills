# WebHook API 文档

## 概述
WebHook管理相关的API接口。

## API 列表

### 浏览WebHook

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/webhook-browse-[orderBy]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 浏览WebHook列表 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| orderBy | string | 否 | 排序方式 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 创建WebHook

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/webhook-create.json` |
| 描述 | 创建新的WebHook |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| 无参数 | - | - | - |

---

### 编辑WebHook

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/webhook-edit-[id].json` |
| 描述 | 编辑WebHook配置 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | int | 否 | WebHook ID |

---

### 删除WebHook

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/webhook-delete-[id].json` |
| 描述 | 删除WebHook |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | int | 否 | WebHook ID |

---

### 浏览WebHook日志

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/webhook-log-[id]-[orderBy]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 浏览特定WebHook的执行日志 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | int | 否 | WebHook ID |
| orderBy | string | 否 | 排序方式 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 绑钉钉用户ID

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/webhook-bind-[id]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 绑定钉钉用户ID到WebHook |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | int | 否 | WebHook ID |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 选择部门

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/webhook-chooseDept-[id].json` |
| 描述 | 为WebHook选择部门 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | int | 否 | WebHook ID |

---

### 异步发送数据

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/webhook-asyncSend.json` |
| 描述 | 异步发送WebHook数据 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| 无参数 | - | - | - |

---

### 测试WebHook

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/webhook-test-[id].json` |
| 描述 | 测试WebHook是否正常工作 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | int | 否 | WebHook ID |

---

### 暂停WebHook

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/webhook-pause-[id].json` |
| 描述 | 暂停WebHook执行 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | int | 否 | WebHook ID |

---

### 恢复WebHook

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/webhook-resume-[id].json` |
| 描述 | 恢复WebHook执行 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | int | 否 | WebHook ID |

---

### WebHook模板管理

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/webhook-template-[type].json` |
| 描述 | 管理WebHook模板 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| type | string | 否 | 模板类型 |

---

### WebHook事件类型

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/webhook-events.json` |
| 描述 | 获取支持的WebHook事件类型 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| 无参数 | - | - | - |

---

### WebHook认证设置

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/webhook-auth-[id].json` |
| 描述 | 设置WebHook认证信息 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | int | 否 | WebHook ID |

---

### WebHook重试机制

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/webhook-retry-[id].json` |
| 描述 | 配置WebHook重试机制 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | int | 否 | WebHook ID |

---

### WebHook超时设置

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/webhook-timeout-[id].json` |
| 描述 | 设置WebHook超时时间 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | int | 否 | WebHook ID |

---

### WebHook统计信息

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/webhook-statistic-[id].json` |
| 描述 | 获取WebHook统计信息 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | int | 否 | WebHook ID |