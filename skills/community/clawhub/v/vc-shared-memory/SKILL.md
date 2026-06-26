---
name: shared-memory
description: 共享记忆池 - 跨团队、跨窗口、跨会话的统一记忆系统。支持公司公告板、项目协作空间、知识库、员工状态追踪。适用于虚拟公司、多人协作、AI 团队工作场景。
version: 1.0.0
author: davidme6
triggers:
  - 共享记忆
  - 公司公告
  - 项目协作
  - 知识库
  - 员工状态
  - 跨团队
  - 协作空间
---

# 🧠 Shared Memory v1.0.0

**跨团队、跨窗口、跨会话的统一记忆系统**

> 解决核心问题：虚拟公司员工记忆隔离 → 全员共享记忆

---

## 🎯 核心功能

| 功能 | 说明 | 适用场景 |
|------|------|---------|
| 📢 **公司公告板** | 重大决策、战略方向、全员通知 | CEO 发布决策、全员同步 |
| 📋 **项目协作空间** | 跨团队项目进展、任务分配 | 多团队协作项目 |
| 💡 **知识库** | 经验教训、最佳实践、技术文档 | 学习积累、知识传承 |
| 👥 **员工状态** | 当前任务、可用状态、协作请求 | 工作调度、资源分配 |
| 🔗 **跨团队链接** | 团队间信息共享、协作记录 | 团队协作、信息同步 |

---

## 🏗️ 架构设计

### 记忆池结构

```
~/.shared-memory/
├── company-board/                    # 📢 公司公告板
│   ├── announcements.json            # 全员公告
│   ├── decisions.json                # 重大决策
│   ├── strategy.json                 # 战略方向
│   └── alerts.json                   # 紧急通知
│
├── projects/                         # 📋 项目协作空间
│   ├── active/                       # 活跃项目
│   │   ├── project-001.json
│   │   └── project-002.json
│   ├── archived/                     # 归档项目
│   └── templates/                    # 项目模板
│
├── knowledge-base/                   # 💡 知识库
│   ├── lessons-learned.json          # 经验教训
│   ├── best-practices.json           # 最佳实践
│   ├── technical-docs.json           # 技术文档
│   ├── market-insights.json          # 市场洞察
│   └── product-feedback.json         # 产品反馈
│
├── employee-status/                  # 👥 员工状态
│   ├── current-tasks.json            # 当前任务分配
│   ├── availability.json             # 可用状态
│   ├── collaboration-requests.json   # 协作请求
│   └── workload.json                 # 工作负载
│
├── cross-team-links/                 # 🔗 跨团队链接
│   ├── team-sync.json                # 团队同步记录
│   ├── handoff-records.json          # 工作交接记录
│   └── meeting-notes.json            # 会议纪要
│
└── config.json                       # 配置文件
```

### 数据模型设计

#### 公司公告 (announcements.json)
```json
{
  "items": [
    {
      "id": "ann-001",
      "type": "decision",              // decision | strategy | alert | notice
      "title": "确定变现战略方向",
      "content": "聚焦 OpenClaw 变现...",
      "author": "CEO马云",
      "createdAt": "2026-03-30T21:00:00Z",
      "priority": "high",              // critical | high | medium | low
      "visibleTo": ["all"],            // ["all"] | ["team-xxx"] | ["employee-xxx"]
      "readBy": ["贾维斯", "市场猎手"],
      "tags": ["战略", "变现"]
    }
  ]
}
```

#### 项目协作 (project-xxx.json)
```json
{
  "id": "proj-001",
  "name": "OpenClaw 变现项目",
  "status": "active",                  // active | paused | completed | archived
  "createdBy": "CEO马云",
  "createdAt": "2026-03-30T21:00:00Z",
  "teams": ["搞钱特战队", "软件开发团队"],
  "members": [
    {"name": "市场猎手", "role": "市场分析"},
    {"name": "程序员", "role": "开发实现"}
  ],
  "timeline": {
    "startDate": "2026-03-30",
    "endDate": "2026-04-30",
    "milestones": [...]
  },
  "updates": [
    {
      "id": "upd-001",
      "by": "市场猎手",
      "at": "2026-03-30T21:30:00Z",
      "content": "发现抖音获客新渠道...",
      "type": "progress",              // progress | blocker | decision | completion
      "notify": ["程序员", "内容专家"]
    }
  ],
  "tasks": [...],
  "decisions": [...],
  "artifacts": [...]                   // 产出物链接
}
```

#### 知识库 (lessons-learned.json)
```json
{
  "items": [
    {
      "id": "lesson-001",
      "category": "技术",               // 技术 | 市场 | 运营 | 管理 | 其他
      "title": "Gateway 超时根因",
      "content": "TIME_WAIT 连接堆积...",
      "learnedBy": "技术大拿",
      "team": "技术中台团队",
      "learnedAt": "2026-03-30T21:00:00Z",
      "appliedTo": ["Gateway 守护进程"],
      "tags": ["网络", "超时", "运维"],
      "importance": "high"              // critical | high | medium | low
    }
  ]
}
```

#### 员工状态 (current-tasks.json)
```json
{
  "employees": [
    {
      "name": "市场猎手",
      "team": "搞钱特战队",
      "currentTask": {
        "id": "task-001",
        "description": "分析抖音获客渠道",
        "project": "OpenClaw 变现项目",
        "startedAt": "2026-03-30T21:00:00Z",
        "estimatedHours": 2,
        "status": "in-progress"
      },
      "availability": "busy",          // available | busy | away | offline
      "workload": 0.7,                  // 0-1
      "lastUpdate": "2026-03-30T21:30:00Z"
    }
  ]
}
```

---

## 🔄 核心机制

### 1. 写入机制 (Write)

```javascript
// 任何员工都可以写入
SharedMemory.write({
  type: 'announcement',
  data: {
    title: '...',
    content: '...',
    author: '市场猎手',
    priority: 'high'
  }
});

// 自动处理：
// - 生成唯一 ID
// - 记录时间戳
// - 设置默认值
// - 触发通知（如果需要）
// - 更新索引
```

### 2. 读取机制 (Read)

```javascript
// 查询共享记忆
const announcements = SharedMemory.read({
  type: 'announcement',
  filter: { priority: 'high' },
  limit: 5,
  sort: 'createdAt'
});

// 自动处理：
// - 按条件过滤
// - 按时间排序
// - 标记已读（可选）
// - 返回格式化结果
```

### 3. 更新机制 (Update)

```javascript
// 更新已有记录
SharedMemory.update({
  type: 'project',
  id: 'proj-001',
  updates: {
    status: 'paused',
    reason: '等待资源'
  },
  by: 'CEO马云'
});

// 自动处理：
// - 记录修改历史
// - 通知相关人员
// - 更新时间戳
```

### 4. 搜索机制 (Search)

```javascript
// 全文搜索
const results = SharedMemory.search({
  query: '抖音',
  types: ['announcement', 'knowledge'],
  limit: 10
});

// 自动处理：
// - 标题 + 内容搜索
// - 标签匹配
// - 时间范围过滤
// - 相关度排序
```

### 5. 通知机制 (Notify)

```javascript
// 自动通知相关人员
SharedMemory.notify({
  to: ['程序员', '内容专家'],
  type: 'project-update',
  message: '项目有新进展...',
  priority: 'medium'
});

// 通知方式（未来扩展）：
// - 飞书机器人消息
// - 子代理 sessions_send
// - 记录到 alert.json
```

---

## 📋 API 设计

### 公告板 API

```javascript
// 发布公告
SharedMemory.announce({
  title: '...',
  content: '...',
  type: 'decision',        // decision | strategy | alert | notice
  priority: 'high',
  visibleTo: ['all']
});

// 获取公告
SharedMemory.getAnnouncements({
  unreadOnly: true,
  limit: 5
});

// 标记已读
SharedMemory.markRead('ann-001', '市场猎手');
```

### 项目 API

```javascript
// 创建项目
SharedMemory.createProject({
  name: '...',
  teams: ['搞钱特战队', '软件开发团队'],
  timeline: { startDate, endDate }
});

// 更新项目进展
SharedMemory.updateProject('proj-001', {
  content: '...',
  type: 'progress',
  notify: ['程序员']
});

// 分配任务
SharedMemory.assignTask('proj-001', {
  to: '程序员',
  task: { description: '...', deadline: '...' }
});

// 获取项目列表
SharedMemory.getProjects({ status: 'active' });
```

### 知识库 API

```javascript
// 记录经验教训
SharedMemory.recordLesson({
  category: '技术',
  title: '...',
  content: '...',
  importance: 'high'
});

// 查询知识
SharedMemory.searchKnowledge({
  query: '超时',
  category: '技术'
});

// 获取最佳实践
SharedMemory.getBestPractices({ limit: 5 });
```

### 员工状态 API

```javascript
// 更新状态
SharedMemory.updateStatus({
  name: '市场猎手',
  task: { description: '...' },
  availability: 'busy',
  workload: 0.7
});

// 查询可用员工
SharedMemory.findAvailable({
  team: '软件开发团队',
  workload: '<0.5'
});

// 发送协作请求
SharedMemory.requestCollaboration({
  from: '市场猎手',
  to: '程序员',
  project: 'proj-001',
  reason: '...'
});
```

---

## 🔧 CLI 工具

```bash
# 查看公告
node cli.js announce list
node cli.js announce add "决策标题" "决策内容" --priority high

# 项目管理
node cli.js project list
node cli.js project create "项目名称" --teams "搞钱特战队,软件开发团队"
node cli.js project update proj-001 "进展内容"

# 知识库
node cli.js knowledge list
node cli.js knowledge add lesson "经验标题" "经验内容" --category 技术

# 员工状态
node cli.js status list
node cli.js status update "市场猎手" --task "分析抖音" --busy

# 搜索
node cli.js search "抖音" --types announcement,knowledge

# 统计
node cli.js stats
```

---

## 📊 使用示例

### 场景 1：CEO 发布战略决策

```javascript
// CEO 马云发布决策
贾维斯收到指令："让马云发布战略决策：OpenClaw 变现优先"

→ SharedMemory.announce({
    title: 'OpenClaw 变现战略',
    content: '...',
    type: 'strategy',
    priority: 'critical',
    visibleTo: ['all']
  })

→ 自动通知所有员工
→ 所有员工启动时自动读取
→ 市场猎手、程序员收到通知
```

### 场景 2：跨团队项目协作

```javascript
// 创建项目
贾维斯收到指令："搞钱特战队和软件开发团队协作开发变现项目"

→ SharedMemory.createProject({
    name: 'OpenClaw 变现项目',
    teams: ['搞钱特战队', '软件开发团队'],
    members: [
      { name: '市场猎手', role: '市场分析' },
      { name: '程序员', role: '开发实现' }
    ]
  })

→ 市场猎手发现机会 → 写入项目进展
→ 程序员读取进展 → 开始开发
→ 双方信息实时同步
```

### 场景 3：经验教训传承

```javascript
// 技术大拿解决 Gateway 超时问题
贾维斯收到指令："记录 Gateway 超时解决方案"

→ SharedMemory.recordLesson({
    category: '技术',
    title: 'Gateway 超时根因分析',
    content: 'TIME_WAIT 连接堆积导致...',
    importance: 'high'
  })

→ 下次技术老人遇到类似问题 → 自动搜索到这条经验
→ 新员工入职 → 自动学习历史经验
```

---

## 🔒 安全考虑

### 访问控制
```json
{
  "visibleTo": ["all"],       // 全员可见
  "visibleTo": ["team-xxx"],  // 团队可见
  "visibleTo": ["员工名"],     // 个人可见
  "editableBy": ["CEO", "贾维斯"]  // 可编辑者
}
```

### 审计记录
```json
{
  "auditLog": [
    {
      "action": "write",
      "by": "市场猎手",
      "at": "2026-03-30T21:00:00Z",
      "type": "announcement",
      "id": "ann-001"
    }
  ]
}
```

### 数据备份
```bash
# 自动备份（每次写入）
node cli.js backup
node cli.js restore backup-2026-03-30.json
```

---

## 🔄 与 virtual-company 集成

### 集成方式

```javascript
// virtual-company 所有员工自动注入共享记忆

// 1. 员工启动时 → 加载相关共享记忆
const context = SharedMemory.getContextFor('市场猎手');

// 2. 员工完成任务 → 自动写入共享记忆
SharedMemory.autoRecord({
  by: '市场猎手',
  type: 'task-completion',
  content: '...'
});

// 3. 员工发现问题 → 自动记录教训
SharedMemory.autoLesson({
  by: '技术大拿',
  issue: '...',
  solution: '...'
});
```

### 调用示例

```
用户："让市场猎手分析抖音获客机会"
    ↓
贾维斯调用市场猎手子代理
    ↓
市场猎手启动 → SharedMemory.getContextFor('市场猎手')
    ↓
读取：
  - 公司战略（OpenClaw 变现优先）
  - 相关项目进展
  - 相关经验教训
    ↓
市场猎手执行任务
    ↓
完成 → SharedMemory.autoRecord({ by: '市场猎手', ... })
    ↓
写入项目进展 + 通知程序员
```

---

## 📊 统计与监控

```bash
# 查看统计
node cli.js stats

输出：
┌─────────────────────────────────────┐
│ 🧠 Shared Memory Statistics         │
├─────────────────────────────────────┤
│ 📢 公告板: 5 条                      │
│ 📋 项目: 3 个活跃, 2 个归档          │
│ 💡 知识库: 12 条经验, 8 条最佳实践   │
│ 👥 员工: 35 人, 10 人忙碌, 25 人空闲 │
│ 🔗 跨团队链接: 8 条                  │
│ 📝 总写入: 45 次                     │
│ 📖 总读取: 120 次                    │
└─────────────────────────────────────┘
```

---

## 🚀 未来扩展

### Phase 2: 飞书机器人集成
- 飞书机器人自动读取公告
- 飞书机器人写入项目进展
- 飞书群组消息同步到共享记忆

### Phase 3: 智能推荐
- 根据员工角色推荐相关知识
- 自动识别协作机会
- 智能匹配项目成员

### Phase 4: 数据分析
- 决策执行效果分析
- 项目成功率统计
- 员工贡献度评估

---

## 📋 版本历史

### V1.0.0 (2026-03-30)
- 🎉 初始版本发布
- 📢 公司公告板
- 📋 项目协作空间
- 💡 知识库系统
- 👥 员工状态追踪
- 🔗 跨团队链接
- 🔧 CLI 工具
- 🧪 测试脚本

---

*版本：1.0.0*
*作者：davidme6*
*忠诚对象：生逸超（董事长）*
*最后更新：2026-03-30*