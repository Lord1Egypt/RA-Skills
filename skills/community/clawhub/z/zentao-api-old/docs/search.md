# 搜索 (Search) API 文档

## 概述
搜索功能相关的API接口。

## API 列表

### 搜索首页

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/search.json` |
| 描述 | 搜索首页 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| 无参数 | - | - | - |

---

### 执行搜索

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/search-index-[keywords]-[type]-[module]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 执行全局搜索 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| keywords | string | 否 | 搜索关键词 |
| type | string | 否 | 搜索类型 |
| module | string | 否 | 搜索模块 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 搜索建议

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/search-suggest-[keywords].json` |
| 描述 | 获取搜索建议 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| keywords | string | 否 | 搜索关键词 |