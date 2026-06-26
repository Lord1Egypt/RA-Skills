# Bug 管理 API 文档

## 概述
Bug管理相关的API接口。

## API 列表

### Bug首页

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/bug.json` |
| 描述 | Bug管理首页 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| 无参数 | - | - | - |

---

### 浏览Bug

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/bug-browse-[productID]-[branch]-[browseType]-[param]-[orderBy]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 浏览产品Bug列表 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |
| branch | int | 否 | 分支ID |
| browseType | string | 否 | 浏览类型 |
| param | - | 否 | 参数 |
| orderBy | string | 否 | 排序方式 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 创建Bug

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/bug-create-[productID]-[branch]-[extras].json` |
| 描述 | 创建新的Bug |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |
| branch | int | 否 | 分支ID |
| extras | - | 否 | 额外参数 |

---

### 编辑Bug

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/bug-edit-[bugID].json` |
| 描述 | 编辑Bug信息 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| bugID | int | 否 | BugID |

---

### 查看Bug

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/bug-view-[bugID]-[form].json` |
| 描述 | 查看Bug详情 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| bugID | int | 否 | BugID |
| form | string | 否 | 表单类型 |

---

### 分配Bug

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/bug-assignTo-[bugID].json` |
| 描述 | 分配Bug给处理人员 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| bugID | int | 否 | BugID |

---

### 确认Bug

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/bug-confirmBug-[bugID].json` |
| 描述 | 确认Bug有效性 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| bugID | int | 否 | BugID |

---

### 解决Bug

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/bug-resolve-[bugID].json` |
| 描述 | 标记Bug已解决 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| bugID | int | 否 | BugID |

---

### 激活Bug

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/bug-activate-[bugID].json` |
| 描述 | 激活Bug |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| bugID | int | 否 | BugID |

---

### 关闭Bug

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/bug-close-[bugID].json` |
| 描述 | 关闭Bug |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| bugID | int | 否 | BugID |

---

### 删除Bug

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/bug-delete-[bugID]-[confirm].json` |
| 描述 | 删除Bug |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| bugID | int | 否 | BugID |
| confirm | string | 否 | 确认删除 |

---

### 关联需求

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/bug-linkStory-[bugID]-[storyID].json` |
| 描述 | 关联需求到Bug |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| bugID | int | 否 | BugID |
| storyID | int | 否 | 需求ID |

---

### 移除关联需求

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/bug-unlinkStory-[bugID]-[storyID].json` |
| 描述 | 移除Bug与需求的关联 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| bugID | int | 否 | BugID |
| storyID | int | 否 | 需求ID |

---

### 批量移除关联需求

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/bug-batchUnlinkStory-[bugID].json` |
| 描述 | 批量移除Bug与需求的关联 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| bugID | int | 否 | BugID |

---

### 关联任务

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/bug-linkTask-[bugID]-[taskID].json` |
| 描述 | 关联任务到Bug |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| bugID | int | 否 | BugID |
| taskID | int | 否 | 任务ID |

---

### 移除关联任务

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/bug-unlinkTask-[bugID]-[taskID].json` |
| 描述 | 移除Bug与任务的关联 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| bugID | int | 否 | BugID |
| taskID | int | 否 | 任务ID |

---

### 批量移除关联任务

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/bug-batchUnlinkTask-[bugID].json` |
| 描述 | 批量移除Bug与任务的关联 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| bugID | int | 否 | BugID |

---

### 关联版本

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/bug-linkBuild-[bugID]-[buildID].json` |
| 描述 | 关联版本到Bug |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| bugID | int | 否 | BugID |
| buildID | int | 否 | 版本ID |

---

### 移除关联版本

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/bug-unlinkBuild-[bugID]-[buildID].json` |
| 描述 | 移除Bug与版本的关联 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| bugID | int | 否 | BugID |
| buildID | int | 否 | 版本ID |

---

### 批量移除关联版本

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/bug-batchUnlinkBuild-[bugID].json` |
| 描述 | 批量移除Bug与版本的关联 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| bugID | int | 否 | BugID |

---

### 更新Bug状态

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/bug-changeStatus-[bugID]-[status].json` |
| 描述 | 更新Bug状态 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| bugID | int | 否 | BugID |
| status | string | 否 | 状态 |

---

### Bug统计

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/bug-statistic-[productID]-[branch].json` |
| 描述 | 获取Bug统计数据 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |
| branch | int | 否 | 分支ID |

---

### Bug趋势分析

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/bug-trend-[productID]-[type].json` |
| 描述 | 获取Bug趋势分析数据 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |
| type | string | 否 | 趋势类型 |

---

### Bug报告导出

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/bug-export.json` |
| 描述 | 导出Bug报告 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| 无参数 | - | - | - |

---

### Bug优先级分析

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/bug-priority-[productID].json` |
| 描述 | 获取Bug优先级分布 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |

---

### Bug严重性分析

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/bug-severity-[productID].json` |
| 描述 | 获取Bug严重性分布 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |

---

### Bug处理时间分析

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/bug-resolutionTime-[productID].json` |
| 描述 | 获取Bug处理时间分析 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |

---

### Bug重复检测

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/bug-duplicate-[bugID].json` |
| 描述 | 检测重复Bug |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| bugID | int | 否 | BugID |

---

### Bug附件管理

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/bug-attachment-[bugID].json` |
| 描述 | 获取Bug附件列表 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| bugID | int | 否 | BugID |

---

### Bug评论管理

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/bug-comment-[bugID].json` |
| 描述 | 获取Bug评论列表 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| bugID | int | 否 | BugID |

---

### 添加Bug评论

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/bug-addComment-[bugID].json` |
| 描述 | 添加Bug评论 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| bugID | int | 否 | BugID |