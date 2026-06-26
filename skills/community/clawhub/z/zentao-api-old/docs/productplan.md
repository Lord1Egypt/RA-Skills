# 产品计划 (Productplan) API 文档

## 概述
产品计划管理相关的API接口。

## API 列表

### 产品计划首页

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/productplan.json` |
| 描述 | 产品计划首页 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| 无参数 | - | - | - |

---

### 浏览产品计划

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/productplan-browse-[productID]-[branch]-[orderBy]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 浏览产品计划列表 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |
| branch | int | 否 | 分支ID |
| orderBy | string | 否 | 排序方式 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 创建产品计划

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/productplan-create-[productID]-[branch].json` |
| 描述 | 创建产品计划 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |
| branch | int | 否 | 分支ID |

---

### 编辑产品计划

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/productplan-edit-[planID].json` |
| 描述 | 编辑产品计划 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| planID | int | 否 | 计划ID |

---

### 查看产品计划

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/productplan-view-[planID].json` |
| 描述 | 查看产品计划详情 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| planID | int | 否 | 计划ID |

---

### 删除产品计划

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/productplan-delete-[planID]-[confirm].json` |
| 描述 | 删除产品计划 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| planID | int | 否 | 计划ID |
| confirm | string | 否 | 确认删除 |

---

### 关联需求到计划

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/productplan-linkStory-[planID]-[browseType]-[param]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 关联需求到产品计划 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| planID | int | 否 | 计划ID |
| browseType | string | 否 | 浏览类型 |
| param | - | 否 | 参数 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 取消关联需求

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/productplan-unlinkStory-[planID]-[storyID].json` |
| 描述 | 取消需求与计划的关联 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| planID | int | 否 | 计划ID |
| storyID | int | 否 | 需求ID |

---

### 批量取消关联需求

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/productplan-batchUnlinkStory-[planID].json` |
| 描述 | 批量取消需求与计划的关联 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| planID | int | 否 | 计划ID |

---

### 产品计划排序

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/productplan-updateOrder.json` |
| 描述 | 更新产品计划排序 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| 无参数 | - | - | - |

---

### 产品计划统计

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/productplan-statistic-[productID].json` |
| 描述 | 获取产品计划统计信息 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |