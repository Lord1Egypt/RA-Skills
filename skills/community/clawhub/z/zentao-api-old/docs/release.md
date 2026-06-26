# 发布 (Release) API 文档

## 概述
产品发布管理相关的API接口。

## API 列表

### 通用操作

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/release-commonAction-[productID]-[branch].json` |
| 描述 | 获取发布通用操作 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |
| branch | int | 否 | 分支ID |

---

### 浏览发布

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/release-browse-[productID]-[branch]-[type].json` |
| 描述 | 浏览产品发布列表 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |
| branch | int | 否 | 分支ID |
| type | string | 否 | 类型 |

---

### 创建发布

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/release-create-[productID]-[branch].json` |
| 描述 | 创建产品发布 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |
| branch | int | 否 | 分支ID |

---

### 编辑发布

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/release-edit-[releaseID].json` |
| 描述 | 编辑发布信息 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| releaseID | int | 否 | 发布ID |

---

### 查看发布

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/release-view-[releaseID]-[type]-[link]-[param]-[orderBy]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 查看发布详情 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| releaseID | int | 否 | 发布ID |
| type | string | 否 | 类型 |
| link | string | 否 | 链接 |
| param | string | 否 | 参数 |
| orderBy | string | 否 | 排序方式 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 删除发布

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/release-delete-[releaseID]-[confirm].json` |
| 描述 | 删除发布 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| releaseID | int | 否 | 发布ID |
| confirm | string | 否 | 确认 |

---

### 导出发布

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/release-export.json` |
| 描述 | 导出发布的需求到HTML |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| 无参数 | - | - | - |

---

### 关联需求

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/release-linkStory-[releaseID]-[browseType]-[param]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 关联需求到发布 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| releaseID | int | 否 | 发布ID |
| browseType | string | 否 | 浏览类型 |
| param | int | 否 | 参数 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 取消关联需求

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/release-unlinkStory-[releaseID]-[storyID].json` |
| 描述 | 取消关联需求 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| releaseID | int | 否 | 发布ID |
| storyID | int | 否 | 需求ID |

---

### 批量取消关联需求

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/release-batchUnlinkStory-[releaseID].json` |
| 描述 | 批量取消关联需求 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| releaseID | int | 否 | 发布ID |

---

### 关联Bug

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/release-linkBug-[releaseID]-[browseType]-[param]-[type]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 关联Bug到发布 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| releaseID | int | 否 | 发布ID |
| browseType | string | 否 | 浏览类型 |
| param | int | 否 | 参数 |
| type | string | 否 | 类型 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 取消关联Bug

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/release-unlinkBug-[releaseID]-[bugID]-[type].json` |
| 描述 | 取消关联Bug |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| releaseID | int | 否 | 发布ID |
| bugID | int | 否 | BugID |
| type | string | 否 | 类型 |

---

### 批量取消关联Bug

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/release-batchUnlinkBug-[releaseID]-[type].json` |
| 描述 | 批量取消关联Bug |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| releaseID | int | 否 | 发布ID |
| type | string | 否 | 类型 |

---

### 更改状态

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/release-changeStatus-[releaseID]-[status].json` |
| 描述 | 更改发布状态 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| releaseID | int | 否 | 发布ID |
| status | string | 否 | 状态 |