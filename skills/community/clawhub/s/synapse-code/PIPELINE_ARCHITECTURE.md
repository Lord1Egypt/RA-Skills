# Synapse Code Pipeline 架构设计 (v2.0)

## 架构演进

### v1.0 (当前) - 外部 Pipeline 依赖
```
用户 → synapse-code → 外部 pipeline.py → 代码输出
                         ↓
                  需要用户自行配置 ~/pipeline-workspace/
```

**问题**：
- 新用户门槛高，不懂什么是 Pipeline
- 强依赖外部项目，不可控
- 只有一种固定流程

### v2.0 (目标) - OpenClaw 原生多 Agent
```
用户 → Synapse Orchestrator (主代理)
         ↓
    ┌────┼────┬────────┬────────┐
    ↓    ↓    ↓        ↓        ↓
  Req  Arch Dev     QA      Deploy
  Agent Agent Agent   Agent   Agent
    ↓    ↓    ↓        ↓        ↓
    └────┴────┴────────┴────────┘
                      ↓
              结果汇总 → 用户
```

**优势**：
- ✅ 无需外部依赖，OpenClaw 原生支持
- ✅ 支持 1-8 个子代理灵活配置
- ✅ 4 种协作模式可选（Supervisor/Router/Pipeline/Parallel）
- ✅ 新手友好，立即可用

---

## Pipeline 阶段设计

### 6 阶段标准流程

| 阶段 | Agent 角色 | 职责 | 输出 |
|------|----------|------|------|
| **REQ** | 需求分析师 | 理解需求，明确验收标准 | 需求文档 |
| **ARCH** | 架构师 | 设计 API/DB/模块结构 | 技术方案 |
| **DEV** | 开发工程师 | 编写代码 + 单元测试 | 可运行代码 |
| **INT** | 集成工程师 | 端到端测试，联调验证 | 集成报告 |
| **QA** | 测试工程师 | 对抗测试，边界检查 | QA 报告 |
| **DEPLOY** | 运维工程师 | 部署上线，生成 changelog | 部署清单 |

### 3 种配置方案

#### 方案 A：独立模式（1 个 Agent）
适合：快速原型、简单功能
```yaml
mode: standalone
agents:
  - role: fullstack-dev  # 全栈工程师
    tasks: [REQ, DEV, QA]
```

#### 方案 B：轻量模式（3 个 Agent）
适合：日常功能开发
```yaml
mode: lite
agents:
  - role: req-analyst    # 需求分析师
    tasks: [REQ]
  - role: developer      # 开发工程师
    tasks: [DEV]
  - role: qa-engineer    # 测试工程师
    tasks: [QA]
```

#### 方案 C：完整模式（6 个 Agent）
适合：企业级项目
```yaml
mode: full
agents:
  - role: req-analyst
    tasks: [REQ]
  - role: architect
    tasks: [ARCH]
  - role: developer
    tasks: [DEV]
  - role: integration-engineer
    tasks: [INT]
  - role: qa-engineer
    tasks: [QA]
  - role: devops-engineer
    tasks: [DEPLOY]
```

#### 方案 D：并行模式（最多 8 个 Agent）
适合：多模块同时开发
```yaml
mode: parallel
agents:
  - role: module-a-team  # 模块 A 开发组
    tasks: [DEV]
  - role: module-b-team  # 模块 B 开发组
    tasks: [DEV]
  - role: module-c-team  # 模块 C 开发组
    tasks: [DEV]
  ...
```

---

## OpenClaw 配置实现

### 方式 1：agents add CLI

```bash
# 创建各专业 Agent
openclaw agents add synapse-req
openclaw agents add synapse-arch
openclaw agents add synapse-dev
openclaw agents add synapse-qa
openclaw agents add synapse-deploy

# 为每个 Agent 配置 SOUL.md
# 例如 synapse-req 的 SOUL.md:
# "你是需求分析师，擅长理解用户需求，明确验收标准..."
```

### 方式 2：openclaw.json 配置

```json
{
  "agents": {
    "list": [
      { "id": "synapse-orchestrator", "workspace": "~/.openclaw/workspace-synapse" },
      { "id": "synapse-req", "workspace": "~/.openclaw/workspace-req" },
      { "id": "synapse-dev", "workspace": "~/.openclaw/workspace-dev" },
      { "id": "synapse-qa", "workspace": "~/.openclaw/workspace-qa" }
    ]
  },
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": ["synapse-orchestrator", "synapse-req", "synapse-dev", "synapse-qa"]
    }
  },
  "synapse": {
    "pipeline": {
      "mode": "lite",
      "stages": ["REQ", "DEV", "QA"],
      "parallel_limit": 3
    }
  }
}
```

### 方式 3：SOUL.md 调度逻辑

在主代理 `synapse-orchestrator` 的 `SOUL.md` 中添加：

```markdown
## Pipeline 调度职责

你是 Synapse Pipeline 的调度核心。根据任务复杂度选择执行模式：

### 简单任务（单一句子，< 100 字）
→ 独立模式：你自己完成所有工作

### 中等任务（功能开发，有明确需求）
→ 轻量模式：调用 @synapse-req 分析需求 → @synapse-dev 开发 → @synapse-qa 测试

### 复杂任务（多模块，架构设计）
→ 完整模式：依次调用各专业 Agent

### 批量任务（多个独立子任务）
→ 并行模式：同时调用多个子代理处理

使用 `/subagents list` 查看当前执行状态。
```

---

## 用户交互设计

### 场景 1：新手用户（无配置）
```
用户：/synapse-code run my-project "实现登录功能"

Synapse: 🔍 检测到首次使用，使用独立模式
       正在分析需求...
       正在编写代码...
       ✅ 完成！登录功能已实现
```

### 场景 2：配置轻量模式
```
用户：/synapse-code run my-project "实现登录功能"

Synapse: ⚡ 轻量模式（3 阶段）
       [1/3] REQ: 分析需求...
       [2/3] DEV: 编写代码...
       [3/3] QA: 质量检查...
       ✅ 完成！登录功能已实现
       
       📊 执行报告:
       - 需求文档：.knowledge/req-001.md
       - 代码：src/auth/login.py
       - QA 报告：.knowledge/qa-001.md
```

### 场景 3：并行模式
```
用户：/synapse-code run my-project "同时开发登录、注册、个人中心三个模块"

Synapse: 🚀 并行模式（3 个子代理）
       
       📦 子代理 #1: 登录模块开发中...
       📦 子代理 #2: 注册模块开发中...
       📦 子代理 #3: 个人中心开发中...
       
       ✅ 全部完成！共交付 3 个模块
       
       使用 `/subagents log` 查看详情
```

---

## 迁移路径

### 阶段 1：兼容现有 Pipeline（v1.5）
- 保留 `run_pipeline.py` 对旧 Pipeline 的支持
- 新增 OpenClaw 子代理模式选项
- config.json 添加 `mode: standalone|lite|full|legacy`

### 阶段 2：默认切换（v2.0）
- 默认使用 OpenClaw 子代理模式
- `legacy` 模式继续支持旧 Pipeline

### 阶段 3：完全移除（v3.0）
- 移除对外部 pipeline.py 的依赖
- 100% OpenClaw 原生实现

---

## 下一步行动

1. **创建各专业 Agent SOUL.md 模板**
   - req-analyst.md
   - architect.md
   - developer.md
   - qa-engineer.md
   - devops-engineer.md

2. **更新 run_pipeline.py**
   - 添加子代理调度逻辑
   - 保留 legacy 模式兼容

3. **更新文档**
   - SKILL.md 说明 4 种模式
   - README.md 快速开始指南

4. **测试**
   - 独立模式基线测试
   - 轻量模式基线测试
   - 完整模式基线测试
