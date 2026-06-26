# 数据表格 (Datatable) API 文档

## 概述
数据表格相关的API接口。

## API 列表

### 数据表格首页

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/datatable.json` |
| 描述 | 数据表格首页 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| 无参数 | - | - | - |

---

### 获取表格数据

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/datatable-getData-[tableName]-[conditions]-[orderBy]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 获取表格数据 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| tableName | string | 否 | 表名 |
| conditions | string | 否 | 查询条件 |
| orderBy | string | 否 | 排序方式 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 保存表格配置

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/datatable-saveConfig-[tableName].json` |
| 描述 | 保存表格配置 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| tableName | string | 否 | 表名 |