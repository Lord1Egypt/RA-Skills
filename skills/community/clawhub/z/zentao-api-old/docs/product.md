# 产品 (Product) API 文档

## 概述
产品管理相关的API接口。

## API 列表

### 产品列表页

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/product-index-[locate]-[productID]-[orderBy]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 获取产品列表页面 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| locate | - | 否 | 定位 |
| productID | - | 否 | 产品ID |
| orderBy | - | 否 | 排序方式 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 项目列表

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/product-project-[status]-[productID].json` |
| 描述 | 获取产品关联的项目列表 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| status | - | 否 | 状态 |
| productID | - | 否 | 产品ID |

---

### 浏览产品

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/product-browse-[productID]-[browseType]-[param]-[storyType]-[orderBy]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 浏览产品需求 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | - | 否 | 产品ID |
| browseType | - | 否 | 浏览类型 |
| param | - | 否 | 参数 |
| storyType | - | 否 | 需求类型 |
| orderBy | - | 否 | 排序方式 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 创建产品

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/product-create.json` |
| 描述 | 创建新产品 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| 无参数 | - | - | - |

---

### 编辑产品

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/product-edit-[productID].json` |
| 描述 | 编辑产品信息 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |

---

### 批量编辑产品

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/product-batchEdit-[productID].json` |
| 描述 | 批量编辑产品 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |

---

### 关闭产品

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/product-close-[productID].json` |
| 描述 | 关闭产品 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |

---

### 查看产品

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/product-view-[productID].json` |
| 描述 | 查看产品详情 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |

---

### 删除产品

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/product-delete-[productID]-[confirm].json` |
| 描述 | 删除产品 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |
| confirm | string | 否 | 确认 |

---

### 产品路线图

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/product-roadmap-[productID].json` |
| 描述 | 查看产品路线图 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |

---

### 产品动态

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/product-dynamic-[type]-[orderBy]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 查看产品动态 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| type | - | 否 | 类型 |
| orderBy | - | 否 | 排序方式 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### AJAX获取项目

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/product-ajaxGetProjects-[productID]-[projectID]-[number].json` |
| 描述 | AJAX获取产品关联的项目 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |
| projectID | - | 否 | 项目ID |
| number | - | 否 | 数量 |

---

### AJAX获取计划

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/product-ajaxGetPlans-[productID]-[planID]-[needCreate]-[expired].json` |
| 描述 | AJAX获取产品计划 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |
| planID | - | 否 | 计划ID |
| needCreate | - | 否 | 是否需要创建 |
| expired | - | 否 | 是否过期 |

---

### 更新排序

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/product-updateOrder.json` |
| 描述 | 更新产品排序 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| 无参数 | - | - | - |

---

### 导出产品

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/product-export-[status]-[orderBy].json` |
| 描述 | 导出产品数据 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| status | - | 否 | 状态 |
| orderBy | - | 否 | 排序方式 |