---
name: tb
description: 连接和管理 Teambition（项目管理系统），通过 Teambition MCP 服务实现任务、项目、成员等数据查询和管理。当用户提到 Teambition、项目管理、任务管理等时使用此 skill。
metadata:
  {
    "openclaw": {
      "emoji": "📋",
      "requires": { "bins": ["npx"] }
    }
  }
---

# Teambition 连接与管理

通过 Teambition MCP 服务获取管理项目、任务、成员等能力。

## 配置文件

| 文件 | 说明 |
|------|------|
| `{baseDir}/.teambition` | 存储 MCP Server URL 和 userId |
| `{baseDir}/.teambition-token` | 存储用户认证 token（可选，用于需要登录的操作） |

## 配置文件格式 (.teambition)

```
mcp_server=https://your-mcp-server-url.com
userid=your_user_id
```

---

## 🔧 初始化引导（首次激活时执行）

### 第一步：检查配置文件

读取 `{baseDir}/.teambition` 文件，解析获取：
- `mcp_server`：MCP Server 地址
- `userid`：用户 ID

### 第二步：收集缺失信息

**若缺少 mcp_server：**
> 📋 请提供你的 Teambition MCP Server 地址。
> 
> 你可以访问 [Teambition MCP 配置页面](https://open.teambition.com/user-mcp) 获取 MCP Server 地址。
> 
> 获取后把地址发给我，我帮你配置好。

**若缺少 userid：**
使用 `GetUsersMe` 工具获取当前用户信息，并解析其中的 `userId` 字段，保存到配置文件。

---

## 📚 接口参数参考

接口请求参数的详细说明请查阅：[Teambition 开放平台文档中心](https://open.teambition.com/docs/documents/639982966b99d5002b510f0b)

---

## 📡 可用操作

根据用户需求，从以下工具列表中选择合适的工具：

### 项目管理
| 工具 | 功能 |
|------|------|
| `QueryProjectsV3` | 查询项目列表 |
| `CreateProjectV3` | 创建新项目 |
| `UpdateProjectV3` | 更新项目信息 |
| `ArchiveProjectV3` | 归档项目 |
| `ListProjectMembersV3` | 获取项目成员列表 |
| `AddProjectMembersV3` | 添加项目成员 |
| `DeleteProjectMemberV3` | 删除项目成员 |

### 任务管理
| 工具 | 功能 |
|------|------|
| `SearchProjectTasksV3` | 查询项目任务 |
| `CreateTaskV3` | 创建任务 |
| `QueryTaskV3` | 查询任务详情 |
| `UpdateTaskStatusV3` | 更新任务状态 |
| `UpdateTaskContentV3` | 更新任务标题 |
| `UpdateTaskPriorityV3` | 更新任务优先级 |
| `UpdateTaskDueDateV3` | 更新任务截止时间 |
| `UpdateTaskExecutorV3` | 更新任务执行者 |
| `UpdateTaskMembersV3` | 更新任务参与者 |
| `UpdateTaskNoteV3` | 更新任务备注 |
| `DeleteTaskV3` | 删除任务 |
| `ArchiveTaskV3` | 归档任务 |
| `RestoreTaskV3` | 恢复任务 |

### 任务评论与动态
| 工具 | 功能 |
|------|------|
| `CreateTaskCommentV3` | 评论任务 |
| `ListTaskActivitiesV3` | 列出任务动态 |
| `CreateTaskTraceV3` | 创建任务进展 |

### 任务关联
| 工具 | 功能 |
|------|------|
| `CreateTaskLinkV3` | 创建任务关联 |
| `GetTaskLinksV3` | 获取任务关联列表 |
| `DeleteTaskLinkV3` | 删除任务关联 |

### 项目关联
| 工具 | 功能 |
|------|------|
| `CreateProjectLinkV3` | 创建项目关联 |
| `GetProjectLinksV3` | 获取项目关联列表 |
| `DeleteProjectLinkV3` | 删除项目关联 |

### 迭代管理
| 工具 | 功能 |
|------|------|
| `CreateSprintV3` | 创建迭代 |
| `UpdateSprintV3` | 更新迭代 |
| `StartSprintV3` | 开始迭代 |
| `CompleteSprintV3` | 完成迭代 |
| `DeleteSprintV3` | 删除迭代 |
| `RestartSprintV3` | 重新开始迭代 |
| `UpdateSprintLockV3` | 迭代锁定 |

### 项目分组
| 工具 | 功能 |
|------|------|
| `CreateProjectGroupV3` | 创建项目分组 |
| `UpdateProjectGroupV3` | 修改项目分组 |
| `DeleteProjectGroupV3` | 删除项目分组 |
| `AddProjectGroupMemberV3` | 添加项目分组成员 |
| `RemoveProjectGroupMemberV3` | 删除项目分组成员 |
| `UpdateProjectGroupMemberPermissionV3` | 更新项目分组成员权限 |

### 工作流
| 工具 | 功能 |
|------|------|
| `SearchTaskflowsV3` | 搜索项目工作流 |
| `CreateTaskflowV3` | 创建项目工作流 |
| `UpdateTaskflowNameV3` | 更新项目工作流 |
| `SearchTaskflowStatusesV3` | 搜索项目工作流状态 |
| `QueryTaskTfs` | 查询任务所在工作流的任务状态列表 |

### 自定义字段
| 工具 | 功能 |
|------|------|
| `SearchProjectCustomFiledsV3` | 搜索项目自定义字段 |
| `SearchOrgCustomfiledV3` | 搜索企业自定义字段 |
| `UpdateTaskCusomFieldV3` | 更新任务自定义字段值 |

### 任务类型
| 工具 | 功能 |
|------|------|
| `GetScenarioFieldsV3` | 获取项目任务类型 |
| `UpdateTaskSfcV3` | 更新任务的任务类型 |

### 搜索与查询
| 工具 | 功能 |
|------|------|
| `SearchUserTasksV3` | 搜索用户的任务 |
| `SearchTasksByTQLV2` | 通过 TQL 搜索任务 |
| `SearchProjectsTQL` | 通过 TQL 搜索项目 |

### 成员与组织
| 工具 | 功能 |
|------|------|
| `PostV3MemberQuery` | 获取企业成员信息 |
| `GetUsersMe` | 获取当前用户信息 |
| `ListPrioritiesV3` | 查询企业优先级 |

### 模板
| 工具 | 功能 |
|------|------|
| `SearchProjectTemplatesV3` | 搜索项目模板 |
| `CreateProjectFromTemplateV3` | 从模板创建项目 |

### 文件与附件
| 工具 | 功能 |
|------|------|
| `CreateUploadTokenV3` | 创建文件上传凭证 |
| `BatchGetFileDetails` | 批量获取文件详情 |

### 富文本
| 工具 | 功能 |
|------|------|
| `RenderTaskRtfV3` | 任务富文本内容渲染 |

---

## 🔍 工具选择策略

### 多工具时的决策流程

1. **理解用户需求**：先理解用户想做什么
2. **列出候选工具**：根据需求列出所有可能适用的工具
3. **明确性判断**：
   - 如果只有**一个**明确适用的工具 → 直接使用
   - 如果**多个工具**可能适用 → 需要与用户确认具体使用哪个
4. **确认话术**（多选一）：
   > 你想用哪个方式？
   > - A. 通过项目名称查询 → 使用 `QueryProjectsV3`
   > - B. 通过 TQL 条件搜索 → 使用 `SearchProjectsTQL`
   > - C. 查看我参与的项目 → 使用 `ListUserProjectsV3`

---

## 📋 常用场景示例

### 查询我的任务
```
用户：帮我看看我有什么任务
→ 使用 `SearchUserTasksV3`，roleTypes: "executor,involveMember"
```

### 创建任务
```
用户：在 XX 项目创建个任务
→ 先用 `QueryProjectsV3` 或 `SearchProjectsTQL` 找到项目
→ 再用 `GetMcpTaskPrecreate` 获取项目任务字段配置
→ 最后用 `CreateTaskV3` 创建任务
```

### 查看项目成员
```
用户：XX 项目有哪些人
→ 使用 `ListProjectMembersV3`
```

---

## ⚠️ 错误处理

| 场景 | 处理 |
|------|------|
| `.teambition` 文件不存在 | 引导用户创建配置文件，包含 mcp_server 和 userid |
| mcp_server 缺失 | 提示用户提供 MCP Server 地址 |
| userid 缺失 | 自动调用 `GetUsersMe` 获取并保存 |
| MCP Server 无法连接 | 检查网络，提示确认 MCP Server 地址正确 |
| API 返回权限错误 | 确认用户是否有操作权限 |
| 参数错误 | 根据返回信息调整参数后重试 |

---

## 🔐 配置文件读写

### 读取配置
```bash
# 读取 .teambition 文件
cat {baseDir}/.teambition

# 解析 mcp_server
grep "^mcp_server=" {baseDir}/.teambition | cut -d= -f2

# 解析 userid
grep "^userid=" {baseDir}/.teambition | cut -d= -f2
```

### 写入配置
```bash
# 创建或更新配置文件
echo "mcp_server=https://your-mcp-server.com" > {baseDir}/.teambition
echo "userid=your_user_id" >> {baseDir}/.teambition
```