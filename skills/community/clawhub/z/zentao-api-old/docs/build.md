# 版本 (Build) API 文档

## 概述
项目版本/Build管理相关的API接口。

## API 列表

### 创建版本

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/build-create-[projectID]-[productID].json` |
| 描述 | 创建项目版本 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |
| productID | int | 否 | 产品ID |

---

### 编辑版本

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/build-edit-[buildID].json` |
| 描述 | 编辑版本信息 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| buildID | int | 否 | 版本ID |

---

### 查看版本

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/build-view-[buildID]-[type]-[link]-[param]-[orderBy]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 查看版本详情 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| buildID | int | 否 | 版本ID |
| type | string | 否 | 类型 |
| link | string | 否 | 链接 |
| param | string | 否 | 参数 |
| orderBy | string | 否 | 排序方式 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 删除版本

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/build-delete-[buildID]-[confirm].json` |
| 描述 | 删除版本 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| buildID | int | 否 | 版本ID |
| confirm | string | 否 | 确认 |

---

### 获取产品版本列表

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/build-ajaxGetProductBuilds-[productID]-[varName]-[build]-[branch]-[index]-[type].json` |
| 描述 | AJAX获取产品的版本下拉列表 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |
| varName | string | 否 | 变量名 |
| build | string | 否 | 版本 |
| branch | int | 否 | 分支ID |
| index | int | 否 | 索引 |
| type | string | 否 | 类型 |

---

### 获取项目版本列表

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/build-ajaxGetProjectBuilds-[projectID]-[varName]-[build]-[branch]-[index]-[needCreate]-[type].json` |
| 描述 | AJAX获取项目的版本下拉列表 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |
| varName | string | 否 | 变量名 |
| build | string | 否 | 版本 |
| branch | int | 否 | 分支ID |
| index | int | 否 | 索引 |
| needCreate | bool | 否 | 是否需要创建 |
| type | string | 否 | 类型 |

---

### 关联需求

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/build-linkStory-[buildID]-[browseType]-[param]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 关联需求到版本 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| buildID | int | 否 | 版本ID |
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
| 路径 | `/build-unlinkStory-[storyID]-[confirm].json` |
| 描述 | 取消关联需求 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| storyID | int | 否 | 需求ID |
| confirm | string | 否 | 确认 |

---

### 批量取消关联需求

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/build-batchUnlinkStory-[confirm].json` |
| 描述 | 批量取消关联需求 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| confirm | string | 否 | 确认 |

---

### 关联Bug

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/build-linkBug-[buildID]-[browseType]-[param]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 关联Bug到版本 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| buildID | int | 否 | 版本ID |
| browseType | string | 否 | 浏览类型 |
| param | int | 否 | 参数 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 取消关联Bug

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/build-unlinkBug-[buildID]-[bugID].json` |
| 描述 | 取消关联Bug |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| buildID | int | 否 | 版本ID |
| bugID | int | 否 | BugID |

---

### 批量取消关联Bug

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/build-batchUnlinkBug-[buildID].json` |
| 描述 | 批量取消关联Bug |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| buildID | int | 否 | 版本ID |