# 企微 Agent Ops Center v3.0 — 顶层架构设计

> 设计日期：2026-05-30
> 设计原则：**统一抽象、插件适配、分层解耦、场景驱动**

---

## 一、设计理念

### 核心命题

**企微 Agent Ops Center 的本质是：为接入企业微信的 AI Agent 提供统一的「可观测性层」。**

它不绑定任何特定的 Agent 引擎（WorkBuddy/ADP/OpenClaw/自建），而是通过**插件化适配器**将异构 Agent 的数据归一化为标准模型，再由统一的核心引擎完成存储、分析、告警和可视化。

### 与 WorkBuddy 的关系

WorkBuddy 是「执行层」，监控中心是「运维层」— 互补而非替代：

| WorkBuddy 的短板 | 监控中心如何补齐 |
|-----------------|----------------|
| 缺乏运行状态集中监控 | Agent 级健康仪表板 + 心跳检测 |
| 无法主动推送任务进度 | 任务生命周期追踪 + 企微卡片推送 |
| 无任务执行审计记录 | 决策点留痕 + 执行摘要报告 |
| 多 Agent 协作不可见 | 拓扑视图 + 链路耗时分解 |

### 与不同 Claw 类型的关系

「Claw」在腾讯云生态中指代三个层次，监控中心需**统一管理、差异化适配**：

| Claw 层次 | 具体指代 | 适配策略 |
|----------|---------|---------|
| **ADP 应用模式** | 标准模式 / Multi-Agent / 单工作流 | 通过 ADP 平台 API 采集，区分单任务与协作链路 |
| **产品形态** | WorkBuddy（桌面）/ OpenClaw（开源）/ ClawPro（企业） | 通过各自开放 API 适配，区分个人/社区/企业管控粒度 |
| **运行时环境** | Skill 调度 / 任务执行 / 资源管理 | 深入采集 CPU/内存/队列/沙箱行为指标 |

### ClawHub 发布策略

**企微 Agent Ops Center 的首要分发渠道是 ClawHub**，目标用户分为三个层次：

| 用户群 | Claw 产品 | 核心痛点 | 监控中心价值 |
|-------|----------|---------|------------|
| **ClawHub 个人用户**（最大基数） | WorkBuddy（桌面） | Agent 在后台跑，挂了不知道 | 心跳监控 + 企微告警，让个人 AI 助手「可靠」 |
| **ClawHub 自托管用户**（高价值） | OpenClaw（开源自建） | 自己部署的实例不稳定，无人运维 | 自托管稳定性监控 + 资源告警 + 版本升级追踪 |
| **企业/平台用户**（高客单） | ClawPro / ADP | 多 Agent 协作黑盒，需要审计合规 | 全链路可观测性 + 审计日志 + 拓扑可视化 |

**优先级**：WorkBuddy = OpenClaw > ADP Claw > ClawPro > Multi-Agent > A2A

原因：ClawHub 上 WorkBuddy 和 OpenClaw 用户基数最大，且两者共享相同的 Skill 体系，一次适配覆盖两个最大用户群。

### OpenClaw 适配器的特殊价值

OpenClaw 用户与 WorkBuddy 用户的关键差异：

| 维度 | WorkBuddy | OpenClaw |
|------|----------|----------|
| 部署方式 | 桌面应用，自动管理 | 用户自行部署，手动运维 |
| 稳定性风险 | 低（应用内进程管理） | 高（服务器宕机、依赖冲突、版本不兼容） |
| 监控需求 | 「Agent 还在跑吗？」 | 「我的服务器上的 OpenClaw 还活着吗？资源够不够？」 |
| ClawHub 分发 | 作为 Skill 安装 | 作为 Skill 安装（同一分发渠道） |

**OpenClaw 适配器的特有监控维度**：
- 自托管进程存活（pm2/systemd 状态）
- 磁盘空间预警（日志堆积导致磁盘满）
- Node.js 版本兼容检查
- npm 依赖安全告警
- 升级前后状态快照对比

---

## 二、四层架构总览

```
┌────────────────────────────────────────────────────────────┐
│                     L3 · 企微集成层                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
│  │ 消息通道  │ │ 卡片模板  │ │ 仪表板UI │ │ 机器人告警    │  │
│  │connector │ │ 5种卡片   │ │dashboard │ │ @负责人推送   │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │
├────────────────────────────────────────────────────────────┤
│                   L2 · 核心监控引擎                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
│  │Agent监控  │ │任务追踪  │ │资源采集  │ │审计日志       │  │
│  │monitor   │ │tracker   │ │collector │ │audit-logger  │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                   │
│  │链路追踪  │ │状态存储  │ │通知引擎  │                   │
│  │link-trkr │ │store     │ │notify    │                   │
│  └──────────┘ └──────────┘ └──────────┘                   │
├────────────────────────────────────────────────────────────┤
│                 L1 · 统一抽象层                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  标准化数据模型：Agent / Task / Event / Audit / Link  │  │
│  └──────────────────────────────────────────────────────┘  │
├────────────────────────────────────────────────────────────┤
│                L0 · 数据源适配层                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
│  │WorkBuddy │ │OpenClaw  │ │ADP Claw  │ │ClawPro       │  │
│  │Adapter   │ │Adapter   │ │Adapter   │ │Adapter       │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                   │
│  │ADP Multi │ │Generic   │ │A2A       │                   │
│  │Adapter   │ │Adapter   │ │Adapter   │                   │
│  └──────────┘ └──────────┘ └──────────┘                   │
└────────────────────────────────────────────────────────────┘
```

### 各层职责

| 层 | 职责 | 关键约束 |
|---|------|---------|
| **L0** | 从各类 Agent 采集原始数据，归一化为标准事件/指标 | 插件化接口，新增 Agent 类型 = 新增一个适配器文件 |
| **L1** | 定义统一数据模型，所有上层模块只消费标准模型 | 模型稳定后不可随意变更字段语义 |
| **L2** | 存储、分析、告警、关联 — 所有监控逻辑的核心 | 不感知 Agent 类型差异，只处理标准模型 |
| **L3** | 企微消息推送、仪表板展示 — 差异化呈现逻辑在卡片模板层 | 根据 Agent 类型参数决定卡片格式 |

---

## 三、L1 — 统一数据模型

### 3.1 AgentProfile（Agent 注册信息）

```javascript
{
  id: "workbuddy-main",           // 唯一标识
  name: "WorkBuddy 主实例",        // 显示名称
  type: "workbuddy",              // workbuddy | openclaw | adp-claw | adp-multi | clawpro | generic
  platform: "workbuddy",          // 所属平台（用于归类过滤）
  runtime: {
    mode: "standard",             // standard | multi-agent | workflow
    version: "2.4.0",
    workspace: "/path/to/workspace"
  },
  capabilities: [                 // Agent 能力清单
    "code_exec", "file_ops", "browser", "shell", "skill_invoke"
  ],
  dependencies: [],               // 依赖的其他 Agent ID（multi-agent 场景）
  dependents: [],                 // 依赖此 Agent 的其他 ID
  healthEndpoint: "http://localhost:9527/health",
  taskEndpoint: "http://localhost:9527/api/tasks",   // 任务上报端点
  resourceEndpoint: "http://localhost:9527/api/resources", // 资源采集端点
  metadata: {}                    // 适配器特定元数据
}
```

### 3.2 AgentStatus（Agent 运行时状态）

```javascript
{
  agentId: "workbuddy-main",
  online: true,
  health: "healthy",              // healthy | degraded | unhealthy

  resources: {
    cpu: 45.2,                    // % (0-100)
    memory: { used: 512, total: 2048, unit: "MB" },
    disk:   { used: 10240, total: 51200, unit: "MB" },
    queueDepth: 3,
    concurrency: 2,
    maxConcurrency: 5
  },

  performance: {
    avgLatency: 120,              // ms
    successRate: 98.5,            // %
    tasksToday: { total: 42, success: 41, failed: 1, running: 3 },
    byTaskType: {
      "report_gen":  { avgDuration: 45000, successRate: 99.1, count: 15 },
      "code_exec":   { avgDuration: 12000, successRate: 97.5, count: 20 },
      "file_ops":    { avgDuration: 3000,  successRate: 100,  count: 7 }
    }
  },

  lastUpdate: "2026-05-30T10:30:00.000Z"
}
```

### 3.3 TaskRecord（任务执行记录 — 场景一/三核心）

```javascript
{
  taskId: "task_20260530_001",
  agentId: "workbuddy-main",
  parentTaskId: null,             // multi-agent 链路中的父任务
  traceId: "trace_abc123",        // 跨 Agent 全链路追踪 ID（场景四）

  type: "report_gen",             // report_gen | data_query | code_exec | file_ops | browser | skill_invoke
  name: "生成销售日报",
  priority: 3,                    // 1-5，1=最高

  status: "completed",            // pending | running | completed | failed | cancelled
  progress: {
    current: 3, total: 3,         // 步骤进度
    currentNode: "报告生成",
    percent: 100
  },

  steps: [                        // 执行步骤（场景一进度推送的数据源）
    { name: "数据提取",   status: "done",    startedAt: "...", completedAt: "...", result: { rows: 1420 } },
    { name: "数据分析",   status: "done",    startedAt: "...", completedAt: "...", result: { anomalies: 3 } },
    { name: "报告生成",   status: "done",    startedAt: "...", completedAt: "...", result: { fileUrl: "..." } }
  ],

  resources: {                    // 任务维度的资源消耗
    cpuPeak: 45, memoryPeakMB: 512, queueWaitMs: 2000
  },

  startedAt:   "2026-05-30T02:00:00Z",
  completedAt: "2026-05-30T02:02:30Z",
  duration: 150000,               // ms

  error: null,                    // 失败时填充 { message, stack, step }
  output: {                       // 任务输出摘要
    summary: "成功生成销售日报，14个数据源，1420行数据",
    fileUrl: "https://...",
    rowCount: 1420
  },

  auditRef: "audit_20260530_001"  // 关联审计记录
}
```

### 3.4 AuditEntry（审计记录 — 场景三核心）

```javascript
{
  auditId: "audit_20260530_001",
  taskId: "task_20260530_001",
  agentId: "workbuddy-main",
  timestamp: "2026-05-30T02:02:30Z",

  type: "task_complete",          // task_complete | decision_point | error | handoff | state_change

  summary: "完成销售日报生成，成功处理14个数据源，发现3处异常数据已标记",

  input: {
    query: "生成今日销售日报",
    sources: ["MySQL:sales_db", "API:erp_system"],
    params: { date: "2026-05-30", format: "pdf" }
  },

  output: {
    fileUrl: "https://.../sales_report_0530.pdf",
    rowCount: 1420,
    generatedAt: "2026-05-30T02:02:30Z"
  },

  decisionPoints: [               // 关键决策点
    {
      point: "数据清洗策略",
      choice: "自动填充缺失值",
      reason: "缺失率 < 5%，符合自动填充阈值",
      alternatives: ["跳过缺失行（会丢失 3% 数据）"]
    },
    {
      point: "异常数据标记",
      choice: "标记但不剔除",
      reason: "3处异常需人工复核，保留原始数据",
      alternatives: ["自动剔除（可能丢失有效数据）"]
    }
  ],

  needsHumanReview: false         // 是否需要人工复核
}
```

### 3.5 CollaborationLink（协作链路 — 场景四核心）

```javascript
{
  linkId: "link_001",
  traceId: "trace_20260530_001",   // 全链路追踪 ID

  steps: [
    {
      agentId: "workbuddy-main",
      agentName: "WorkBuddy",
      role: "orchestrator",        // orchestrator | analyst | executor | reviewer
      taskId: "task_001",
      taskName: "用户意图解析",
      status: "completed",
      duration: 2000                // ms
    },
    {
      agentId: "analyst-agent",
      agentName: "数据分析师",
      role: "data_analysis",
      taskId: "task_002",
      taskName: "销售数据多维分析",
      status: "completed",
      duration: 45000
    },
    {
      agentId: "writer-agent",
      agentName: "报告写手",
      role: "report_gen",
      taskId: "task_003",
      taskName: "生成最终报告",
      status: "completed",
      duration: 12000
    }
  ],

  totalDuration: 59000,            // 端到端总耗时
  bottleneck: {
    agentId: "analyst-agent",
    percent: 76.3                   // 占总耗时比例
  },

  status: "completed",
  startedAt: "2026-05-30T02:00:00Z",
  completedAt: "2026-05-30T02:00:59Z"
}
```

### 3.6 MonitorEvent（监控事件 — 统一事件总线）

```javascript
{
  eventId: "evt_abc123",
  timestamp: "2026-05-30T10:30:00Z",

  type: "task",                    // agent | task | resource | audit | link
  subtype: "task_progress",        // 具体子类型
  severity: "info",                // info | warning | critical

  source: {
    agentId: "workbuddy-main",
    taskId: "task_001",            // 可选
    adapterId: "workbuddy-adapter" // 数据来源适配器
  },

  payload: { ... }                 // 事件特定数据（TaskRecord / AgentStatus / 等）
}
```

---

## 四、L0 — 适配器接口规范

### 4.1 抽象基类（BaseAdapter）

```javascript
/**
 * BaseAdapter — 所有适配器的基类
 *
 * 每个适配器负责：
 * 1. 采集：从特定 Agent 类型拉取数据（HTTP / WebSocket / SDK / 平台 API）
 * 2. 归一化：将原始数据转换为 L1 标准模型
 * 3. 上报：通过 EventEmitter 发射到核心引擎
 */
class BaseAdapter extends EventEmitter {
  /**
   * @param {string} id — 适配器唯一标识
   * @param {object} config — 适配器配置（endpoint, apiKey, workspace, etc.）
   * @param {object} targetAgent — 被监控的 Agent 注册信息
   */
  constructor(id, config, targetAgent) {
    super();
    this.id = id;
    this.config = config;
    this.targetAgent = targetAgent;
    this.running = false;
  }

  // ─── 生命周期（子类必须实现） ───
  async start()  { throw new Error('Not implemented'); }
  async stop()   { throw new Error('Not implemented'); }

  // ─── 核心采集方法（子类按需覆盖） ───
  /** Agent 健康检查 → 发射 'agent:health' 事件 */
  async collectHealth()     { /* 默认 HTTP GET healthEndpoint */ }

  /** 资源指标采集 → 发射 'agent:resources' 事件 */
  async collectResources()  { /* 默认不做 */ }

  /** 任务状态拉取 → 发射 'agent:task' 事件 */
  async collectTasks()      { /* 默认不做 */ }

  /** 能力探测 → 更新 capabilities */ 
  async probeCapabilities() { /* 默认不做 */ }

  // ─── 事件发射（子类调用） ───
  emitEvent(type, payload) {
    this.emit(type, {
      source: { adapterId: this.id, agentId: this.targetAgent.id },
      timestamp: Date.now(),
      payload
    });
  }
}
```

### 4.2 七种适配器差异化设计

| 适配器 | 健康采集 | 资源采集 | 任务采集 | 链路采集 | 特有维度 |
|-------|---------|---------|---------|---------|---------|
| **generic-adapter** | HTTP GET + TCP ping | ❌ | ❌ | ❌ | — |
| **workbuddy-adapter** | Claw API 健康端点 | CPU/内存/队列 | 会话/任务事件 | SubAgent 调度链 | 用户满意度、本地文件操作 |
| **openclaw-adapter** | 自建实例健康端点 | CPU/内存/队列（自托管） | OSS Agent 任务事件 | 开源社区 Agent 协作 | 自托管稳定性、版本升级兼容 |
| **adp-claw-adapter** | ADP 平台 API | 工作空间资源 + 代码执行日志 | Skill 调用序列 | ❌ | 工作空间隔离度、外部 API 配额 |
| **adp-multi-adapter** | 各子 Agent 聚合健康 | 同上 + 协作图谱同步 | 多 Agent 任务依赖 | 子 Agent 流转 + 数据一致性 | 协作链路延迟、跨 Agent 传递 |
| **clawpro-adapter** | 管理 API | 集群指标 + 分布式状态 | 组织级任务队列 | 跨实例负载分布 | 企业级安全合规指标 |
| **a2a-adapter** | A2A 协议心跳 | ❌ | A2A 协议任务卡片 | A2A Agent 发现拓扑 | 标准协议兼容性 |

### 4.3 适配器注册示例（config.yaml v3.0）

```yaml
# 监控配置 v3.0
monitor:
  enabled: true

  # 适配器注册（替代旧版 agents 列表）
  adapters:
    # WorkBuddy 适配器（场景一至四的主力）
    - id: "wb-adapter-1"
      type: "workbuddy"
      agent:
        id: "workbuddy-main"
        name: "WorkBuddy 主实例"
        endpoint: "http://localhost:9527"
        apiKey: "${WORKBUDDY_API_KEY}"  # 从环境变量读取

    # OpenClaw 适配器（ClawHub 核心用户群）
    - id: "openclaw-adapter-1"
      type: "openclaw"
      agent:
        id: "openclaw-instance-1"
        name: "OpenClaw 自建实例"
        endpoint: "http://10.0.1.10:8080"
        apiKey: "${OPENCLAW_API_KEY}"
        selfHosted: true              # 自托管标识
        version: "2.1.0"              # 版本追踪（升级兼容检查）

    # ADP Claw 模式适配器
    - id: "adp-adapter-1"
      type: "adp-claw"
      agent:
        id: "adp-claw-001"
        name: "ADP 代码助手"
        endpoint: "https://adp.tencent.com/api/v1"
        workspaceId: "ws_abc123"

    # 通用 HTTP 适配器（兼容旧版）
    - id: "generic-1"
      type: "generic"
      agent:
        id: "custom-agent"
        name: "自建 Agent"
        endpoint: "http://10.0.1.5:3001/health"
```

---

## 五、L2 — 核心引擎模块设计

### 5.1 模块关系图

```
                        ┌─────────────────┐
                        │   EventBus      │ ← 统一事件总线
                        │   (Node.js      │
                        │    EventEmitter) │
                        └────┬───┬───┬────┘
              ┌──────────────┤   │   ├──────────────┐
              ▼              ▼   ▼   ▼              ▼
     ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐
     │agent-      │  │task-       │  │resource-   │  │audit-      │
     │monitor.js  │  │tracker.js  │  │collector.js│  │logger.js   │
     │(已有,增强) │  │(NEW)       │  │(NEW)       │  │(NEW)       │
     └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
           │               │               │               │
           └───────────────┴───────┬───────┴───────────────┘
                                   ▼
                          ┌────────────────┐
                          │  state-store   │ ← 统一持久化
                          │  (已有,增强)   │
                          └────────┬───────┘
                                   ▼
                          ┌────────────────┐
                          │ notify-engine  │ ← 通知路由
                          │ (已有,增强)    │
                          └────────┬───────┘
                                   ▼
                          ┌────────────────┐
                          │ dashboard-api  │ ← 查询API
                          │ (已有,增强)    │
                          └────────────────┘
```

### 5.2 新增模块详设

#### task-tracker.js — 任务生命周期追踪引擎

```javascript
/**
 * 职责：
 * 1. 接收适配器 / Agent HTTP POST 的任务事件
 * 2. 维护任务状态机：pending → running → step_progress → completed/failed
 * 3. 按任务类型聚合统计（耗时/成功率）
 * 4. 超时检测：任务超过预期时长未更新 → 发射 task:stuck 事件
 * 5. 失败关联：连续失败同类型任务 → 发射 task:type_degraded 事件
 *
 * API:
 *   POST /api/tasks/start     → 创建任务
 *   POST /api/tasks/progress  → 更新步骤
 *   POST /api/tasks/complete  → 标记完成
 *   POST /api/tasks/fail      → 标记失败
 *   GET  /api/tasks/active    → 当前活跃任务
 *   GET  /api/tasks/:id       → 任务详情
 */
```

#### resource-collector.js — 资源指标采集引擎

```javascript
/**
 * 职责：
 * 1. 接收适配器推送的资源快照
 * 2. 存储时序资源数据（CPU/内存/队列）
 * 3. 阈值告警：CPU > 80% / 队列 > 10 → 发射 resource:threshold 事件
 * 4. 趋势分析：持续上升/下降 → 发射 resource:trend 事件
 *
 * API:
 *   POST /api/resources/report  → 上报资源快照
 *   GET  /api/resources/:agentId → 查资源历史
 */
```

#### audit-logger.js — 审计日志模块

```javascript
/**
 * 职责：
 * 1. 接收任务完成/失败事件，保存完整审计记录
 * 2. 决策点结构化记录
 * 3. 支持按时间段/Agent/任务类型检索
 * 4. 提供审计报告生成（输入→决策→输出 的完整链路）
 *
 * API:
 *   POST /api/audit/log         → 写入审计记录
 *   GET  /api/audit/search?...   → 多条件搜索
 *   GET  /api/audit/:taskId      → 查某任务的审计轨迹
 */
```

#### link-tracker.js — 多 Agent 协作链路追踪

```javascript
/**
 * 职责：
 * 1. 接收带 traceId 的多 Agent 任务事件
 * 2. 聚合为 CollaborationLink 模型
 * 3. 计算端到端延迟 + 各段占比
 * 4. 识别瓶颈 Agent
 * 5. 拓扑数据供仪表板可视化
 *
 * API:
 *   POST /api/links/trace       → 上报链路步骤
 *   GET  /api/links/:traceId    → 查完整链路
 *   GET  /api/links/active      → 活跃链路列表
 */
```

### 5.3 已有模块增强点

| 模块 | 增强内容 |
|------|---------|
| **state-store.js** | 新增 `tasks` / `audit` / `links` 三张 Map，复用已有持久化管线 |
| **notify-engine.js** | 新增 4 种卡片类型：`taskProgressCard` / `taskResultCard` / `resourceAlertCard` / `topologyCard` |
| **dashboard-api.js** | 新增 12+ REST 端点：任务查询/资源查询/审计查询/链路查询/全局搜索 |
| **agent-monitor.js** | 支持适配器模式：不再直接 HTTP GET，改为委托给适配器的 `collectHealth()` |
| **agent-bridge.js** | 支持回调任务事件：Agent 回复中包含 `task_event` 字段时，转发到 task-tracker |

---

## 六、L3 — 企微集成层差异化设计

### 6.1 五种卡片模板

```
cards/
├── health-card.js        # 已有：Agent 健康报告（agent-monitor 驱动）
├── alert-card.js         # 已有：Agent 异常告警（agent-monitor 驱动）
├── task-progress-card.js # NEW：任务进度直播（task-tracker 驱动）
├── task-result-card.js   # NEW：任务完成/失败结果播报（task-tracker 驱动）
├── resource-card.js      # NEW：资源阈值告警（resource-collector 驱动）
├── audit-summary-card.js # NEW：执行摘要报告（audit-logger 驱动）
└── topology-card.js      # NEW：多 Agent 链路甘特图（link-tracker 驱动）
```

### 6.2 按 Agent 类型的呈现策略

| Agent 类型 | 任务进度卡片 | 资源告警 | 审计摘要 | 拓扑卡片 |
|-----------|-----------|---------|---------|---------|
| WorkBuddy | ✅ 高频（每个关键任务推送） | ✅ CPU/内存/队列 | ✅ 完整决策点 | ✅ SubAgent 调度链 |
| OpenClaw | ✅ 高频（自托管稳定性关键） | ✅ CPU/内存/磁盘（自托管重点） | ✅ 版本兼容+升级记录 | ✅ 社区多实例协作 |
| ADP Claw 模式 | ✅ 长耗时任务（防止僵死） | ✅ 工作空间资源+代码错误率 | ✅ 代码执行+Skill调用 | ❌ |
| ADP Multi-Agent | ✅ 协作链路关键节点 | ✅ 子Agent状态同步 | ✅ 跨Agent传递记录 | ✅ 甘特图卡片 |
| ClawPro | ✅ 关键业务流程 | ✅ 集群容量预警 | ✅ 合规审计 | ✅ 分布式拓扑 |
| Generic | ❌ 不推送（避免骚扰） | ❌ | ❌ | ❌ |

### 6.3 仪表板差异化视图

dashboard.html 增强为**类型感知**：
- 顶部：类型切换 Tab（全部 | WorkBuddy | ADP | 自建）
- 左侧：Agent 列表（按类型分组，带状态色标）
- 中部：主面板（根据选中 Tab 显示不同视图）
  - WorkBuddy Tab：资源面板 + 任务统计 + 会话记录
  - ADP Multi Tab：协作拓扑图 + 链路耗时分解
  - 通用 Tab：心跳历史 + 基础状态

---

## 七、四大场景 → 架构映射

| 场景 | 数据来源（L0） | 核心处理（L2） | 企微呈现（L3） |
|------|-------------|-------------|-------------|
| **场景一：状态直播+异常告警** | workbuddy-adapter / adp-claw-adapter → task events | task-tracker 维护状态机 + 超时检测 | task-progress-card（分节点更新同一张卡片） |
| **场景二：资源看板+性能优化** | workbuddy-adapter / adp-claw-adapter → resource snapshots | resource-collector 阈值告警 + 趋势分析 | resource-card（@负责人） + dashboard 资源面板 |
| **场景三：交接记录+审计追溯** | task-tracker → task complete events | audit-logger 决策点记录 + 摘要生成 | audit-summary-card（附详细链接） + 审计查询 API |
| **场景四：数字团队统一指挥** | workbuddy-adapter + adp-multi-adapter → trace events | link-tracker 拓扑聚合 + 瓶颈识别 | topology-card（甘特图） + dashboard 拓扑视图 |

---

## 八、分阶段实施路线

### v2.1 — 场景一（任务生命周期追踪）
**目标**：WorkBuddy 执行任务时，企微群收到实时进度卡片

| 模块 | 动作 | 估时 |
|------|------|------|
| `task-tracker.js` | 新建：任务状态机 + HTTP API | 核心 |
| `notify-engine.js` | 增强：新增 task-progress-card / task-result-card | 依赖 |
| `agent-bridge.js` | 增强：支持 task_event 回调转发 | 小改动 |
| `dashboard-api.js` | 增强：新增任务查询端点 | 小改动 |
| `config.yaml` | 增强：新增 tasks 配置段 | 小改动 |

### v2.2 — 场景二（资源监控） + WorkBuddy 适配器 + OpenClaw 适配器 ✅ 已完成
**目标**：WorkBuddy + OpenClaw 资源指标可视化 + 阈值告警

| 模块 | 动作 |
|------|------|
| `adapters/workbuddy-adapter.js` | 新建：Claw API 适配器 |
| `adapters/openclaw-adapter.js` | 新建：OpenClaw 自托管适配器（重点：自托管稳定性监控） |
| `resource-collector.js` | 新建：资源采集 + 阈值告警 |
| `dashboard.html` | 增强：新增资源面板 + 任务统计面板 |

### v2.3 — 场景三（审计追溯）✅ 已完成
**目标**：每个任务完成后生成可审计的执行摘要

| 模块 | 动作 |
|------|------|
| `audit-logger.js` | 新建：审计记录 + 摘要生成 + 决策点结构化存储 |
| `state-store.js` | 增强：新增 audit Map + searchAudit/getTaskAudit + 持久化 |
| `notify-engine.js` | 增强：新增 audit-summary-card（企业微信富卡片） |
| `dashboard-api.js` | 增强：新增 GET /api/audit/search + /api/audit/:taskId + /api/audit/stats |
| `dashboard.html` | 增强：新增审计查询面板（搜索框 + 类型筛选 + 详情展开） |
| `connector.js` | 增强：集成 AuditLogger + POST /api/audit/log + 审计事件→企微推送 |
| `config.yaml` | 增强：新增 audit 配置段 |

### v3.0 — 场景四（多 Agent 拓扑）+ ADP 适配器
**目标**：多 Agent 协作链路可视化 + 瓶颈定位

| 模块 | 动作 |
|------|------|
| `link-tracker.js` | 新建：链路追踪 + 拓扑聚合 |
| `adapters/adp-multi-adapter.js` | 新建：ADP Multi-Agent 适配器 |
| `adapters/adp-claw-adapter.js` | 新建：ADP 单实例适配器 |
| `notify-engine.js` | 增强：新增 topology-card（甘特图） |
| `dashboard.html` | 增强：新增拓扑视图 |

---

## 九、向后兼容策略

1. **config.yaml 格式**：旧版 `monitor.agents` 列表自动映射为 `generic-adapter` 类型，无需手动迁移
2. **HTTP API 路径**：现有 `/api/monitor/*` 端点保持不变，新增 `/api/tasks/*` `/api/resources/*` `/api/audit/*` `/api/links/*`
3. **数据持久化文件**：`state_file` 新增 `tasks`/`audit`/`links` 键，旧 `agents`/`history` 格式不变
4. **notify-engine.js 输出格式**：已有 `healthReportCard`/`alertCard`/`dailySummaryCard` 接口不变，新增卡片为独立方法
5. **CLI 命令**：`pair`/`join`/`status`/`peers` 不变

---

## 十、目录结构（v3.0 目标态）

```
wecom-connector/
├── ARCHITECTURE.md              # 本文档
├── SKILL.md                     # ClawHub 上架描述
├── config.yaml                  # 配置文件 v3.0
├── config.js                    # 配置加载器
├── connector.js                 # 主入口（保持简洁）
├── package.json
│
├── adapters/                    # L0 — 数据源适配层
│   ├── base-adapter.js          # 抽象基类
│   ├── generic-adapter.js       # 通用 HTTP 心跳（兼容旧版）
│   ├── workbuddy-adapter.js     # WorkBuddy Claw API
│   ├── openclaw-adapter.js      # OpenClaw 自托管实例（ClawHub 核心）
│   ├── adp-claw-adapter.js      # ADP 标准/Claw 模式
│   ├── adp-multi-adapter.js     # ADP Multi-Agent 模式
│   ├── clawpro-adapter.js       # ClawPro 企业平台
│   └── a2a-adapter.js           # A2A 协议 Agent
│
├── core/                        # L2 — 核心监控引擎
│   ├── state-store.js           # 统一状态持久化（已有）
│   ├── agent-monitor.js         # Agent 健康监控（已有，增强）
│   ├── task-tracker.js          # 任务生命周期追踪（NEW）
│   ├── resource-collector.js    # 资源指标采集（NEW）
│   ├── audit-logger.js          # 审计日志（v2.3）
│   ├── link-tracker.js          # 多 Agent 链路追踪（NEW）
│   └── notify-engine.js         # 通知引擎（已有，增强）
│
├── integration/                 # L3 — 企微集成层
│   ├── ws-client.js             # 企微 WebSocket 客户端（已有）
│   ├── msg-converter.js         # 消息格式转换（已有）
│   ├── agent-bridge.js          # Agent 通信桥接（已有，增强）
│   ├── dashboard-api.js         # 仪表板 API（已有，增强）
│   └── cards/                   # 企微卡片模板
│       ├── health-card.js       # Agent 健康报告
│       ├── alert-card.js        # Agent 异常告警
│       ├── task-progress-card.js # 任务进度直播（NEW）
│       ├── task-result-card.js  # 任务结果播报（NEW）
│       ├── resource-card.js     # 资源告警（NEW）
│       ├── audit-summary-card.js # 审计摘要（NEW）
│       └── topology-card.js     # 链路甘特图（NEW）
│
├── dashboard/
│   └── dashboard.html           # 仪表板 UI（增强）
│
├── p2p/                         # P2P 子系统（独立）
│   ├── p2p-router.js
│   └── pairing-server.js
│
└── data/                        # 运行时数据
    └── agent_states.json        # 持久化状态文件
```
