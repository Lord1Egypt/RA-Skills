# 项目 (Project) API 文档

## 概述
项目管理相关的API接口。

## API 列表

### 项目首页

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/project-index-[locate]-[status]-[projectID].json` |
| 描述 | 项目首页视图 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| locate | - | 否 | 定位 |
| status | - | 否 | 状态 |
| projectID | - | 否 | 项目ID |

---

### 浏览项目

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/project-browse-[projectID].json` |
| 描述 | 浏览项目详情 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |

---

### 项目任务

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/project-task-[projectID]-[status]-[orderBy]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 获取项目任务列表 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |
| status | string | 否 | 状态 |
| orderBy | string | 否 | 排序方式 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 分组任务

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/project-grouptask-[projectID]-[groupBy].json` |
| 描述 | 按组获取项目任务 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |
| groupBy | string | 否 | 分组方式 |

---

### 项目需求

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/project-story-[projectID]-[orderBy].json` |
| 描述 | 获取项目需求列表 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |
| orderBy | string | 否 | 排序方式 |

---

### 项目Bug

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/project-bug-[projectID]-[orderBy]-[build]-[type]-[param]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 获取项目Bug列表 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |
| orderBy | string | 否 | 排序方式 |
| build | - | 否 | 版本 |
| type | - | 否 | 类型 |
| param | - | 否 | 参数 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 项目燃尽图

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/project-burn-[projectID]-[type]-[interval].json` |
| 描述 | 获取项目燃尽图数据 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |
| type | - | 否 | 类型 |
| interval | - | 否 | 间隔 |

---

### 创建项目

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/project-create-[projectID]-[copyProjectID]-[planID].json` |
| 描述 | 创建项目 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |
| copyProjectID | int | 否 | 复制项目ID |
| planID | int | 否 | 计划ID |

---

### 编辑项目

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/project-edit-[projectID]-[action]-[extra].json` |
| 描述 | 编辑项目信息 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |
| action | string | 否 | 操作 |
| extra | string | 否 | 额外参数 |

---

### 开始项目

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/project-start-[projectID].json` |
| 描述 | 开始项目 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |

---

### 关闭项目

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/project-close-[projectID].json` |
| 描述 | 关闭项目 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |

---

### 查看项目

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/project-view-[projectID].json` |
| 描述 | 查看项目详情 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |

---

### 项目看板视图

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/project-kanban-[projectID]-[type]-[orderBy].json` |
| 描述 | 项目看板视图 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |
| type | string | 否 | 类型 |
| orderBy | string | 否 | 排序方式 |

---

### 管理项目成员

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/project-manageMembers-[projectID]-[team2Import].json` |
| 描述 | 管理项目成员 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |
| team2Import | - | 否 | 团队导入 |

---

### 关联需求

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/project-linkStory-[projectID].json` |
| 描述 | 关联需求到项目 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |

---

### 移除需求

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/project-unlinkStory-[projectID]-[storyID].json` |
| 描述 | 从项目中移除需求 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |
| storyID | int | 否 | 需求ID |

---

### 批量移除需求

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/project-batchUnlinkStory-[projectID].json` |
| 描述 | 批量从项目中移除需求 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |

---

### 项目进度

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/project-progress-[projectID].json` |
| 描述 | 获取项目进度信息 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |

---

### 项目动态

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/project-dynamic-[projectID]-[type]-[orderBy]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 获取项目动态信息 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |
| type | - | 否 | 类型 |
| orderBy | - | 否 | 排序方式 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 项目统计

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/project-statistic-[projectID]-[by]-[type].json` |
| 描述 | 获取项目统计信息 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |
| by | - | 否 | 按什么统计 |
| type | - | 否 | 类型 |

---

### 项目报表

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/project-report-[projectID]-[reportType].json` |
| 描述 | 获取项目报表 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |
| reportType | string | 否 | 报表类型 |

---

### 项目甘特图

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/project-gantt-[projectID].json` |
| 描述 | 获取项目甘特图数据 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |

---

### 项目风险

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/project-risk-[projectID].json` |
| 描述 | 获取项目风险信息 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |

---

### 项目团队

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/project-team-[projectID].json` |
| 描述 | 获取项目团队信息 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |

---

### 项目里程碑

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/project-milestone-[projectID].json` |
| 描述 | 获取项目里程碑信息 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |

---

### 项目预算

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/project-budget-[projectID].json` |
| 描述 | 获取项目预算信息 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |

---

### 项目文档

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/project-document-[projectID].json` |
| 描述 | 获取项目文档信息 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |

---

### 项目附件

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/project-attachment-[projectID].json` |
| 描述 | 获取项目附件信息 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |

---

### 项目审批

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/project-approval-[projectID].json` |
| 描述 | 获取项目审批信息 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| projectID | int | 否 | 项目ID |