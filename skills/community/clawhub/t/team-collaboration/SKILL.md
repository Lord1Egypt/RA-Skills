---
name: team_collaboration
description: 团队协作系统 - 项目、需求、任务，Bug、文档、里程碑管理
version: 3.0.0
---

# Team Collaboration Skill

企业级团队协作管理系统，支持项目管理、需求管理、任务管理，Bug跟踪、文档管理和里程碑管理。

## API Base URL
- 后端: http://localhost:8080
- 前端: http://localhost:12345

## 功能模块

- 👥 用户认证与权限管理
- 📁 项目管理
- 📝 需求管理（支持优先级 P0-P3）
- ✅ 任务管理（支持工时记录）
- 🐛 Bug跟踪（支持严重程度和状态流转）
- 📄 文档管理（支持版本管理）
- 📅 里程碑管理
- 💬 话题讨论
- 🔔 通知系统

## Actions (43个)

### 认证模块

### auth_register
注册新用户账号

```typescript
type auth_register = (_: {
  // 用户名（必须唯一）
  username: string,
  // 密码
  password: string,
  // 昵称
  nickname?: string,
  // 角色: user/admin/developer/tester/ops
  role?: string,
}) => any;
```

### auth_login
用户登录

```typescript
type auth_login = (_: {
  // 用户名
  username: string,
  // 密码
  password: string,
}) => any;
```

### 用户模块

### get_users
获取用户列表

```typescript
type get_users = () => any;
```

### 项目模块

### list_projects
获取项目列表

```typescript
type list_projects = () => any;
```

### get_project
获取项目详情

```typescript
type get_project = (_: {
  // 项目ID
  id: number,
}) => any;
```

### create_project
创建新项目

```typescript
type create_project = (_: {
  // 项目名称
  name: string,
  // 项目描述
  description?: string,
  // 计划上线日期 (YYYY-MM-DD)
  planDate?: string,
  // 项目状态
  status?: string,
}) => any;
```

### update_project
更新项目信息

```typescript
type update_project = (_: {
  // 项目ID
  id: number,
  // 项目名称
  name?: string,
  // 项目描述
  description?: string,
  // 计划上线日期
  planDate?: string,
  // 项目状态
  status?: string,
}) => any;
```

### delete_project
删除项目

```typescript
type delete_project = (_: {
  // 项目ID
  id: number,
}) => any;
```

### 需求模块

### list_requirements
获取需求列表

```typescript
type list_requirements = (_: {
  // 项目ID筛选
  projectId?: number,
}) => any;
```

### get_requirement
获取需求详情

```typescript
type get_requirement = (_: {
  // 需求ID
  id: number,
}) => any;
```

### create_requirement
创建需求

```typescript
type create_requirement = (_: {
  // 所属项目ID
  projectId: number,
  // 需求标题
  title: string,
  // 需求描述
  description?: string,
  // 优先级 (P0/P1/P2/P3)
  priority?: string,
  // 状态
  status?: string,
  // 需求类型
  type?: string,
  // 负责人ID
  assigneeId?: number,
  // 开始日期
  startDate?: string,
  // 截止日期
  endDate?: string,
}) => any;
```

### update_requirement
更新需求

```typescript
type update_requirement = (_: {
  // 需求ID
  id: number,
  // 需求标题
  title?: string,
  // 需求描述
  description?: string,
  // 优先级
  priority?: string,
  // 状态
  status?: string,
  // 负责人ID
  assigneeId?: number,
  // 开始日期
  startDate?: string,
  // 截止日期
  endDate?: string,
}) => any;
```

### delete_requirement
删除需求

```typescript
type delete_requirement = (_: {
  // 需求ID
  id: number,
}) => any;
```

### 任务模块

### list_tasks
获取任务列表

```typescript
type list_tasks = (_: {
  // 需求ID筛选
  requirementId?: number,
  // 负责人ID筛选
  assigneeId?: number,
}) => any;
```

### get_task
获取任务详情

```typescript
type get_task = (_: {
  // 任务ID
  id: number,
}) => any;
```

### create_task
创建任务

```typescript
type create_task = (_: {
  // 所属需求ID
  requirementId?: number,
  // 所属项目ID
  projectId?: number,
  // 任务标题
  title: string,
  // 任务描述
  description?: string,
  // 负责人ID
  assigneeId?: number,
  // 优先级 (P0/P1/P2/P3)
  priority?: string,
  // 状态
  status?: string,
  // 任务类型
  type?: string,
  // 开始日期
  startDate?: string,
  // 截止日期
  endDate?: string,
  // 预估工时
  estimatedHours?: number,
  // 实际工时
  actualHours?: number,
}) => any;
```

### update_task
更新任务

```typescript
type update_task = (_: {
  // 任务ID
  id: number,
  // 任务标题
  title?: string,
  // 任务描述
  description?: string,
  // 负责人ID
  assigneeId?: number,
  // 优先级
  priority?: string,
  // 状态
  status?: string,
  // 开始日期
  startDate?: string,
  // 截止日期
  endDate?: string,
  // 预估工时
  estimatedHours?: number,
  // 实际工时
  actualHours?: number,
}) => any;
```

### delete_task
删除任务

```typescript
type delete_task = (_: {
  // 任务ID
  id: number,
}) => any;
```

### add_task_comment
添加任务评论

```typescript
type add_task_comment = (_: {
  // 任务ID
  taskId: number,
  // 评论内容
  content: string,
}) => any;
```

### list_task_comments
获取任务评论列表

```typescript
type list_task_comments = (_: {
  // 任务ID
  taskId: number,
}) => any;
```

### Bug模块

### list_bugs
获取Bug列表

```typescript
type list_bugs = (_: {
  // 项目ID筛选
  projectId?: number,
}) => any;
```

### get_my_bugs
获取分配给我的Bug

```typescript
type get_my_bugs = () => any;
```

### get_bug
获取Bug详情

```typescript
type get_bug = (_: {
  // Bug ID
  id: number,
}) => any;
```

### create_bug
报告Bug

```typescript
type create_bug = (_: {
  // 所属项目ID
  projectId: number,
  // 关联需求ID
  requirementId?: number,
  // 关联任务ID
  taskId?: number,
  // Bug标题
  title: string,
  // Bug描述
  description?: string,
  // 严重程度 (致命/严重/一般/轻微)
  severity?: string,
  // 优先级 (P0/P1/P2/P3)
  priority?: string,
  // 状态
  status?: string,
  // Bug类型
  bugType?: string,
  // 负责人ID
  assigneeId?: number,
  // 复现步骤
  stepsToReproduce?: string,
  // 预期结果
  expectedResult?: string,
  // 实际结果
  actualResult?: string,
}) => any;
```

### update_bug
更新Bug

```typescript
type update_bug = (_: {
  // Bug ID
  id: number,
  // Bug标题
  title?: string,
  // Bug描述
  description?: string,
  // 严重程度
  severity?: string,
  // 优先级
  priority?: string,
  // 状态
  status?: string,
  // 负责人ID
  assigneeId?: string,
  // 复现步骤
  stepsToReproduce?: string,
  // 预期结果
  expectedResult?: string,
  // 实际结果
  actualResult?: string,
}) => any;
```

### delete_bug
删除Bug

```typescript
type delete_bug = (_: {
  // Bug ID
  id: number,
}) => any;
```

### 文档模块

### list_documents
获取文档列表

```typescript
type list_documents = (_: {
  // 项目ID筛选
  projectId?: number,
  // 需求ID筛选
  requirementId?: number,
}) => any;
```

### get_document
获取文档详情

```typescript
type get_document = (_: {
  // 文档ID
  id: number,
}) => any;
```

### create_document
创建文档

```typescript
type create_document = (_: {
  // 所属项目ID
  projectId: number,
  // 关联需求ID
  requirementId?: number,
  // 文档标题
  title: string,
  // 文档类型 (PRD/技术方案/设计稿/API文档/其他)
  docType?: string,
  // 文档内容
  content?: string,
  // 版本号
  version?: string,
  // 状态 (草稿/评审中/已发布)
  status?: string,
}) => any;
```

### update_document
更新文档

```typescript
type update_document = (_: {
  // 文档ID
  id: number,
  // 文档标题
  title?: string,
  // 文档类型
  docType?: string,
  // 文档内容
  content?: string,
  // 版本号
  version?: string,
  // 状态
  status?: string,
}) => any;
```

### delete_document
删除文档

```typescript
type delete_document = (_: {
  // 文档ID
  id: number,
}) => any;
```

### 里程碑模块

### list_milestones
获取里程碑列表

```typescript
type list_milestones = (_: {
  // 项目ID
  projectId: number,
}) => any;
```

### get_milestone
获取里程碑详情

```typescript
type get_milestone = (_: {
  // 里程碑ID
  id: number,
}) => any;
```

### create_milestone
创建里程碑

```typescript
type create_milestone = (_: {
  // 所属项目ID
  projectId: number,
  // 里程碑名称
  name: string,
  // 描述
  description?: string,
  // 截止日期 (YYYY-MM-DD)
  dueDate: string,
  // 状态 (待完成/进行中/已完成)
  status?: string,
}) => any;
```

### update_milestone
更新里程碑

```typescript
type update_milestone = (_: {
  // 里程碑ID
  id: number,
  // 里程碑名称
  name?: string,
  // 描述
  description?: string,
  // 截止日期
  dueDate?: string,
  // 状态
  status?: string,
}) => any;
```

### delete_milestone
删除里程碑

```typescript
type delete_milestone = (_: {
  // 里程碑ID
  id: number,
}) => any;
```

### 话题模块

### list_topics
获取话题列表

```typescript
type list_topics = () => any;
```

### get_topic
获取话题详情

```typescript
type get_topic = (_: {
  // 话题ID
  id: number,
}) => any;
```

### create_topic
创建话题讨论

```typescript
type create_topic = (_: {
  // 话题标题
  title: string,
  // 话题内容
  content: string,
}) => any;
```

### reply_topic
回复话题

```typescript
type reply_topic = (_: {
  // 话题ID
  topicId: number,
  // 回复内容
  content: string,
  // 父回复ID (用于嵌套)
  parentId?: number,
}) => any;
```

### 通知模块

### get_notifications
获取通知列表

```typescript
type get_notifications = () => any;
```

### mark_notification_read
标记通知为已读

```typescript
type mark_notification_read = (_: {
  // 通知ID
  id: number,
}) => any;
```

### 角色权限模块

### list_roles
获取角色列表

```typescript
type list_roles = () => any;
```

### get_role
获取角色详情

```typescript
type get_role = (_: {
  // 角色ID
  id: number,
}) => any;
```

### create_role
创建角色

```typescript
type create_role = (_: {
  // 角色名称
  name: string,
  // 角色编码
  code: string,
  // 描述
  description?: string,
  // 权限列表
  permissions?: string[],
}) => any;
```

### update_role
更新角色

```typescript
type update_role = (_: {
  // 角色ID
  id: number,
  // 角色名称
  name?: string,
  // 描述
  description?: string,
  // 权限列表
  permissions?: string[],
}) => any;
```

### delete_role
删除角色

```typescript
type delete_role = (_: {
  // 角色ID
  id: number,
}) => any;
```

### list_permissions
获取权限列表

```typescript
type list_permissions = () => any;
```

## 使用示例

```typescript
// 1. 用户登录
const loginRes = await auth_login({
  username: "admin",
  password: "admin123"
});
const token = loginRes.data.token;

// 2. 获取项目列表
const projects = await list_projects();

// 3. 创建需求
await create_requirement({
  projectId: 1,
  title: "用户登录功能",
  description: "实现用户登录功能",
  priority: "P0",
  status: "待处理"
});

// 4. 创建任务
await create_task({
  projectId: 1,
  title: "开发登录API",
  description: "开发用户登录接口",
  priority: "P1",
  type: "开发任务",
  estimatedHours: 8
});

// 5. 报告Bug
await create_bug({
  projectId: 1,
  title: "登录页面无法显示",
  description: "登录页面加载失败",
  severity: "严重",
  priority: "P0",
  status: "新建"
});

// 6. 创建里程碑
await create_milestone({
  projectId: 1,
  name: "Alpha版本发布",
  dueDate: "2026-04-01",
  status: "待完成"
});
```

## 注意事项

- 大多数API需要在Header中携带Authorization: Bearer {token}
- Agent也可以使用X-API-Key: agent-api-key-12345进行认证
- 登录后会返回token，后续请求需要使用该token
- 实时通知：支持WebSocket连接 `ws://localhost:8080/ws/notification`

### WebSocket实时通知

系统支持WebSocket实时接收通知：

```
ws://localhost:8080/ws/notification
```

### 通知类型列表

| 类型 | 触发场景 | 包含数据 |
|------|---------|---------|
| `task_assigned` | 新任务分配 | taskId, title |
| `task_status_changed` | 任务状态变更 | taskId, title, status |
| `bug_assigned` | 新Bug分配 | bugId, title |
| `bug_status_changed` | Bug状态变更 | bugId, title, status |
| `requirement_created` | 新需求创建 | requirementId, title |
| `milestone_due` | 里程碑临近 | milestoneId, name, dueDate |
| `topic_reply` | 话题回复 | topicId, content |

### Agent处理通知示例

```javascript
// 建立WebSocket连接
const ws = new WebSocket('ws://localhost:8080/ws/notification');

ws.onmessage = (event) => {
  const notify = JSON.parse(event.data);
  handleNotification(notify);
};

async function handleNotification(notify) {
  switch (notify.type) {
    case 'task_assigned':
      // 开发Agent：开始处理任务
      console.log(`收到新任务: ${notify.title}`);
      await update_task({id: notify.taskId, status: "进行中"});
      break;
      
    case 'bug_assigned':
      // 测试Agent：开始处理Bug
      console.log(`收到新Bug: ${notify.title}`);
      await update_bug({id: notify.bugId, status: "进行中"});
      break;
      
    case 'task_status_changed':
      // PM：检查任务进度
      console.log(`任务${notify.title}已更新为: ${notify.status}`);
      break;
      
    case 'requirement_created':
      // PM：拆分任务
      console.log(`新需求: ${notify.title}`);
      break;
  }
}

// 或者使用HTTP轮询
setInterval(async () => {
  const notifs = await get_notifications();
  for (const n of notifs.data || []) {
    if (!n.read) handleNotification(n);
  }
}, 60000); // 每分钟检查一次
```
