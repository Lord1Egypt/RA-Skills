# Jenkins API 文档

## 概述
Jenkins集成管理相关的API接口。

## API 列表

### 浏览Jenkins

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/jenkins-browse-[orderBy]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 浏览Jenkins服务器列表 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| orderBy | string | 否 | 排序方式 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 创建Jenkins

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/jenkins-create.json` |
| 描述 | 添加新的Jenkins服务器 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| 无参数 | - | - | - |

---

### 编辑Jenkins

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/jenkins-edit-[id].json` |
| 描述 | 编辑Jenkins服务器配置 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | int | 否 | Jenkins服务器ID |

---

### 删除Jenkins

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/jenkins-delete-[id].json` |
| 描述 | 删除Jenkins服务器配置 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | int | 否 | Jenkins服务器ID |

---

### AJAX获取任务列表

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/jenkins-ajaxGetTasks-[id].json` |
| 描述 | AJAX获取Jenkins的Job列表 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | int | 否 | Jenkins服务器ID |

---

### 测试Jenkins连接

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/jenkins-test-[id].json` |
| 描述 | 测试Jenkins服务器连接 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | int | 否 | Jenkins服务器ID |

---

### Jenkins任务管理

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/jenkins-jobs-[id].json` |
| 描述 | 查看Jenkins任务列表 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | int | 否 | Jenkins服务器ID |

---

### Jenkins构建历史

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/jenkins-builds-[id]-[job].json` |
| 描述 | 查看Jenkins构建历史 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | int | 否 | Jenkins服务器ID |
| job | string | 否 | 任务名称 |