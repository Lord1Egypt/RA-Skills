# 多智能体协作系统 (Multi-Agent Collaboration System)

## 📖 概述

多智能体协作系统是一个基于 JavaScript 的智能体协作框架，灵感来源于 AutoGen Teams、CrewAI Crews 和 OpenAI Swarm 等主流多智能体框架。

### 核心设计理念

本系统提取了主流多智能体框架的核心设计模式：

#### 1. **角色分工模式 (Role-Based Specialization)**
- 每个智能体承担特定职责（研究员、程序员、审核员等）
- 角色预定义专业能力和工具访问权限
- 支持自定义角色扩展

#### 2. **任务分解模式 (Task Decomposition)**
- 复杂任务自动分解为可执行的子任务
- 识别任务间的依赖关系
- 智能分配最优执行者

#### 3. **编排执行模式 (Orchestration Patterns)**
- **并行执行**: 独立任务同时执行，提高效率
- **串行执行**: 依赖任务按顺序执行，保证正确性
- **混合编排**: 复杂工作流的 DAG 执行

#### 4. **结果聚合模式 (Result Aggregation)**
- 收集各智能体的执行结果
- 处理结果冲突和异常
- 生成最终综合输出

#### 5. **协作沟通模式 (Inter-Agent Communication)**
- 智能体间消息传递
- 上下文共享机制
- 请求 - 响应协作

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                    Orchestrator                         │
│              (编排器 - 协调全局流程)                      │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   Task Planner                          │
│            (任务规划器 - 分解和分配任务)                   │
└─────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │  Researcher  │ │  Developer   │ │   Reviewer   │
    │   (研究员)    │ │   (程序员)    │ │   (审核员)    │
    └──────────────┘ └──────────────┘ └──────────────┘
            │               │               │
            └───────────────┼───────────────┘
                            ▼
┌─────────────────────────────────────────────────────────┐
│                 Result Aggregator                       │
│              (结果聚合器 - 汇总输出)                      │
└─────────────────────────────────────────────────────────┘
```

## 📁 目录结构

```
skills/multi-agent/
├── src/
│   ├── agent-team.js      # 智能体团队管理类
│   ├── roles.js           # 预定义角色
│   ├── task-planner.js    # 任务分解和分发
│   └── orchestrator.js    # 编排和结果聚合
├── test/
│   └── team.test.js       # 测试用例
├── SKILL.md               # 使用文档
└── README.md              # 详细说明（本文件）
```

## 🚀 快速开始

### 基础使用

```javascript
const { AgentTeam, roles } = require('./src/agent-team');

// 创建团队
const team = new AgentTeam('research-team');

// 添加角色
team.addRole('researcher', roles.Researcher);
team.addRole('writer', roles.Writer);

// 分配任务
team.assignTask('调研 AI 智能体发展趋势', 'researcher');
team.assignTask('撰写调研报告', 'writer');

// 执行并收集结果
const results = await team.orchestrate();
console.log(results);
```

### 高级编排

```javascript
const { Orchestrator } = require('./src/orchestrator');

const orchestrator = new Orchestrator();

// 定义工作流
const workflow = {
  parallel: [
    { agent: 'researcher', task: '搜索技术文档' },
    { agent: 'developer', task: '编写代码示例' }
  ],
  serial: [
    { agent: 'reviewer', task: '审核所有内容', dependsOn: ['parallel'] }
  ]
};

const result = await orchestrator.execute(workflow);
```

## 🎭 预定义角色

| 角色 | 职责 | 工具 |
|------|------|------|
| **Researcher** | 信息搜索和整理 | Tavily Search, Web Fetch |
| **Developer** | 代码编写和执行 | Code Sandbox, Exec |
| **Reviewer** | 质量审核和反馈 | 代码审查，内容验证 |
| **Planner** | 任务分解和规划 | 任务分析，依赖识别 |
| **Writer** | 文档撰写和总结 | 文档生成，内容整合 |

## 📊 测试覆盖

系统包含 4 个核心测试场景：

1. ✅ **单智能体任务** - 验证基础功能
2. ✅ **双智能体协作** - 验证简单协作
3. ✅ **多智能体协作** - 验证复杂协作
4. ✅ **复杂任务分解** - 验证任务规划器

测试覆盖率目标：>80%

## 🔧 配置选项

### 角色配置

```javascript
const config = {
  name: 'custom-researcher',
  capabilities: ['search', 'analyze'],
  tools: ['tavily', 'web-fetch'],
  maxConcurrency: 3,
  timeout: 30000
};
```

### 编排模式

- `parallel`: 并行执行独立任务
- `serial`: 串行执行依赖任务
- `hybrid`: 混合编排（默认）

## 📝 最佳实践

### 1. 合理分工
根据任务特性选择合适的角色，避免角色重叠。

### 2. 明确依赖
清晰定义任务间的依赖关系，确保执行顺序正确。

### 3. 错误处理
为每个角色配置超时和重试策略，处理异常情况。

### 4. 结果验证
使用 Reviewer 角色对输出进行质量审核。

### 5. 性能优化
- 并行执行独立任务
- 合理设置并发限制
- 缓存重复查询结果

## 📚 参考框架

本系统设计参考了以下主流框架：

- **AutoGen Teams** (Microsoft) - 对话式多智能体协作
- **CrewAI Crews** - 角色驱动的自动化工作流
- **OpenAI Swarm** - 轻量级智能体编排

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
