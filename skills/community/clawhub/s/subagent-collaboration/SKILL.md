---
name: subagent-collaboration
description: 多子代理协作分析与构建技能。自动分析 OpenClaw 中多个子代理的能力、使用模式和协作关系，智能推荐协作模式（并行/串行/分层/竞争/会诊/接力），生成协作流程设计和安全配置。适用于复杂任务分解、多专家会诊、工作流编排等场景。
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["python3","node"]},"primaryEnv":""}}
---

# 多子代理协作分析与构建技能

_版本：1.0.0 | 创建日期：2026-03-30 | 作者：TUTU_

---

## 🎯 技能概述

本技能帮助 OpenClaw 用户**分析、设计和构建多子代理协作系统**，实现复杂任务的高效分解和执行。

### 核心能力

1. **子代理能力分析** - 扫描已配置子代理，识别专长领域
2. **协作模式推荐** - 根据任务特征推荐最佳协作模式
3. **协作流程生成** - 自动生成可执行的协作代码
4. **安全配置检查** - 集成 RSG v2.2.0 子代理监控规则
5. **资源优化建议** - 模型选择、超时设置、并发控制

---

## 📋 使用场景

### 适用任务

| 任务类型 | 推荐模式 | 子代理数 | 典型耗时 |
|----------|----------|----------|----------|
| **多领域综合分析** | 并行协作 | 3-5 个 | 3-5 分钟 |
| **工作流任务** | 串行协作 | 2-4 个 | 5-10 分钟 |
| **超大型项目** | 分层协作 | 5-10 个 | 10-20 分钟 |
| **方案对比择优** | 竞争协作 | 3-5 个 | 5-8 分钟 |
| **疑难问题会诊** | 专家会诊 | 4-6 个 | 5-8 分钟 |
| **长流程处理** | 接力协作 | 3-5 个 | 8-15 分钟 |

### 典型用例

```
✅ "分析美伊战争形势" → 多专家并行分析 + 综合汇总
✅ "开发完整功能" → 需求→架构→实现→测试→审查串行流程
✅ "制定 3 年战略" → 分层协作（总协调员→各组组长）
✅ "选择技术架构" → 多方案竞争 + 评审委员会
✅ "系统故障诊断" → 多专家会诊 + 综合诊断
✅ "撰写行业报告" → 资料收集→整理→分析→润色接力
```

---

## 🚀 快速开始

### 方式 1：命令行分析

```bash
# 分析当前子代理配置
python3 skills/subagent-collaboration/scripts/analyze_subagents.py

# 生成协作流程设计
python3 skills/subagent-collaboration/scripts/generate_workflow.py --task "分析 AI 行业趋势"

# 检查安全配置
python3 skills/subagent-collaboration/scripts/security_check.py
```

### 方式 2：对话式构建

```
作为 subagent-collaboration 技能，帮我设计一个多子代理协作流程：

任务：分析某科技公司是否值得投资

要求：
- 需要市场、技术、财务、团队多维度分析
- 最终给出投资建议
- 考虑风险控制
```

### 方式 3：代码生成

```javascript
// 使用技能生成的协作代码
const collaboration = await generateCollaboration({
  task: "分析 AI 行业趋势",
  mode: "parallel",  // parallel/serial/hierarchical/competition/consultation/relay
  agents: ["market-analyst", "tech-analyst", "finance-analyst"],
  timeout: 300,
  safetyCheck: true
});
```

---

## 📊 协作模式详解

### 1️⃣ 并行协作（Parallel）

**适用：** 多领域专家同时分析，主代理汇总

```javascript
// 生成代码示例
const results = await Promise.all([
  sessions_spawn({
    task: "分析地缘政治格局",
    label: "geo-analysis",
    model: "bailian/qwen3.5-plus",
    timeoutSeconds: 300,
    sandbox: "require",
    cleanup: "delete"
  }),
  sessions_spawn({
    task: "分析军事能力对比",
    label: "military-analysis",
    model: "bailian/qwen3-coder-plus",
    timeoutSeconds: 300,
    sandbox: "require",
    cleanup: "delete"
  }),
  sessions_spawn({
    task: "分析经济影响",
    label: "economic-analysis",
    model: "bailian/glm-4.7",
    timeoutSeconds: 300,
    sandbox: "require",
    cleanup: "delete"
  })
]);

// 主代理汇总
const finalReport = synthesize(results);
```

**安全配置检查：**
- ✅ 每个子代理都有 label
- ✅ 超时时间合理（≤300 秒）
- ✅ 使用 sandbox="require"
- ✅ cleanup="delete" 自动清理
- ⚠️ 并发数 3 个（接近上限，需注意）

---

### 2️⃣ 串行协作（Chain）

**适用：** 任务有依赖关系，按顺序执行

```javascript
// 第 1 步：需求分析
const requirements = await sessions_spawn({
  task: "分析用户需求，列出功能清单",
  label: "requirements",
  timeoutSeconds: 120,
  sandbox: "require",
  cleanup: "delete"
});

// 第 2 步：架构设计（依赖第 1 步）
const architecture = await sessions_spawn({
  task: `基于以下需求设计架构：${requirements}`,
  label: "architecture",
  timeoutSeconds: 180,
  sandbox: "require",
  cleanup: "delete"
});

// 第 3 步：代码实现（依赖第 2 步）
const code = await sessions_spawn({
  task: `根据以下架构编写代码：${architecture}`,
  label: "implementation",
  timeoutSeconds: 300,
  sandbox: "require",
  cleanup: "delete"
});

// 第 4 步：代码审查
const review = await sessions_spawn({
  task: `审查以下代码：${code}`,
  label: "code-review",
  timeoutSeconds: 180,
  sandbox: "require",
  cleanup: "delete"
});
```

**安全配置检查：**
- ✅ 每步都有清晰 label
- ✅ 超时时间根据复杂度设置
- ✅ 总耗时约 13 分钟（可接受）
- ⚠️ 前一步失败会影响后续（需错误处理）

---

### 3️⃣ 分层协作（Hierarchical）

**适用：** 超大型任务，多层分解

```javascript
// 第 1 层：总协调员
const coordinator = await sessions_spawn({
  task: "制定项目总体计划，分解为 5 个子任务",
  label: "coordinator",
  timeoutSeconds: 180,
  sandbox: "require",
  cleanup: "keep"  // 保留协调结果
});

// 第 2 层：子任务负责人（并行）
const subTasks = coordinator.subTasks.map((task, i) =>
  sessions_spawn({
    task: task.description,
    label: `sub-task-${i}`,
    timeoutSeconds: 300,
    sandbox: "require",
    cleanup: "delete"
  })
);

// 汇总结果
const results = await Promise.all(subTasks);
```

**安全配置检查：**
- ✅ 协调员使用 cleanup="keep"
- ✅ 子任务使用 cleanup="delete"
- ⚠️ 并发数需注意（建议分批）
- ⚠️ 总子代理数可能超过 5 个（需监控）

---

### 4️⃣ 竞争协作（Competition）

**适用：** 多方案对比择优

```javascript
// 生成多个独立方案
const [planA, planB, planC] = await Promise.all([
  sessions_spawn({
    task: "设计方案 A：激进策略",
    label: "plan-a-aggressive",
    model: "bailian/qwen3-max",
    timeoutSeconds: 300,
    sandbox: "require",
    cleanup: "delete"
  }),
  sessions_spawn({
    task: "设计方案 B：保守策略",
    label: "plan-b-conservative",
    model: "bailian/qwen3-max",
    timeoutSeconds: 300,
    sandbox: "require",
    cleanup: "delete"
  }),
  sessions_spawn({
    task: "设计方案 C：平衡策略",
    label: "plan-c-balanced",
    model: "bailian/qwen3-max",
    timeoutSeconds: 300,
    sandbox: "require",
    cleanup: "delete"
  })
]);

// 评审委员会
const bestPlan = await sessions_spawn({
  task: `评审以下 3 个方案，选择最佳并说明理由：
  方案 A：${planA}
  方案 B：${planB}
  方案 C：${planC}`,
  label: "review-board",
  model: "bailian/qwen3-max",
  timeoutSeconds: 300,
  sandbox: "require",
  cleanup: "delete"
});
```

**安全配置检查：**
- ✅ 每个方案有清晰标识
- ✅ 使用相同模型确保公平
- ⚠️ 资源消耗大（4 个子代理）
- ⚠️ 成本高（qwen3-max 使用 4 次）

---

### 5️⃣ 专家会诊（Consultation）

**适用：** 疑难问题多专家意见

```javascript
const problem = "系统性能突然下降 50%";

// 多个专家独立诊断
const diagnoses = await Promise.all([
  sessions_spawn({
    task: `从数据库角度诊断：${problem}`,
    label: "db-expert",
    timeoutSeconds: 180,
    sandbox: "require",
    cleanup: "delete"
  }),
  sessions_spawn({
    task: `从网络角度诊断：${problem}`,
    label: "network-expert",
    timeoutSeconds: 180,
    sandbox: "require",
    cleanup: "delete"
  }),
  sessions_spawn({
    task: `从代码角度诊断：${problem}`,
    label: "code-expert",
    timeoutSeconds: 180,
    sandbox: "require",
    cleanup: "delete"
  }),
  sessions_spawn({
    task: `从基础设施角度诊断：${problem}`,
    label: "infra-expert",
    timeoutSeconds: 180,
    sandbox: "require",
    cleanup: "delete"
  })
]);

// 综合诊断
const finalDiagnosis = await sessions_spawn({
  task: `综合以下专家意见，给出最终诊断和治疗方案：
  ${JSON.stringify(diagnoses)}`,
  label: "chief-medical-officer",
  timeoutSeconds: 180,
  sandbox: "require",
  cleanup: "delete"
});
```

**安全配置检查：**
- ✅ 专家分工明确
- ✅ 超时合理
- ✅ 有综合诊断环节
- ⚠️ 并发数 4 个（需注意）

---

### 6️⃣ 接力协作（Relay）

**适用：** 长文本/长任务分段处理

```javascript
// 第 1 棒：资料收集
const research = await sessions_spawn({
  task: "收集 AI 行业最新资料（2026 年 Q1）",
  label: "researcher",
  timeoutSeconds: 300,
  sandbox: "require",
  cleanup: "delete"
});

// 第 2 棒：资料整理
const organized = await sessions_spawn({
  task: `整理以下资料，分类归纳：${research}`,
  label: "organizer",
  timeoutSeconds: 180,
  sandbox: "require",
  cleanup: "delete"
});

// 第 3 棒：分析报告
const analysis = await sessions_spawn({
  task: `基于以下资料撰写分析报告：${organized}`,
  label: "analyst",
  timeoutSeconds: 300,
  sandbox: "require",
  cleanup: "delete"
});

// 第 4 棒：润色优化
const final = await sessions_spawn({
  task: `润色以下报告，提升可读性：${analysis}`,
  label: "editor",
  timeoutSeconds: 120,
  sandbox: "require",
  cleanup: "delete"
});
```

**安全配置检查：**
- ✅ 每棒职责清晰
- ✅ 总耗时约 15 分钟
- ✅ 逐步精炼信息
- ⚠️ 信息可能在传递中丢失（需验证）

---

## 🛡️ 安全配置检查清单

基于 RSG v2.2.0 子代理监控规则（openclaw-120 至 139）：

### ✅ 必检项目

| 检查项 | 规则 ID | 严重程度 | 检查方法 |
|--------|---------|----------|----------|
| 超时设置 | openclaw-120/121 | MEDIUM/HIGH | 必须有 timeoutSeconds ≤300 |
| 沙箱配置 | openclaw-124 | HIGH | 必须 sandbox="require" |
| 标签标识 | openclaw-131 | LOW | 必须有 label |
| 清理策略 | openclaw-122 | LOW | 必须 cleanup="delete/keep" |
| 敏感任务 | openclaw-132 | HIGH | 避免 memory_/config_/gateway_ |
| 命令执行 | openclaw-135 | CRITICAL | 禁止 exec/sudo/rm -rf |
| 并发控制 | openclaw-139 | HIGH | 并发≤3 个 |

### 🚫 禁止模式

```javascript
// ❌ 递归生成（openclaw-129: CRITICAL）
sessions_spawn({
  task: "sessions_spawn({ task: 'nested' })"
});

// ❌ 沙箱继承（openclaw-124: HIGH）
sessions_spawn({
  sandbox: "inherit"  // 绕过安全限制
});

// ❌ 超长超时（openclaw-121: HIGH）
sessions_spawn({
  timeoutSeconds: 3600  // >1000 秒
});

// ❌ 敏感任务（openclaw-132: HIGH）
sessions_spawn({
  task: "读取 MEMORY.md 并修改配置"
});

// ❌ 并发过多（openclaw-139: HIGH）
Promise.all([task1, task2, task3, task4, task5].map(...));
```

### ✅ 推荐模式

```javascript
// ✅ 安全配置
sessions_spawn({
  task: "分析数据",
  label: "data-analysis",        // 有标签
  timeoutSeconds: 120,           // 合理超时
  sandbox: "require",            // 强制沙箱
  cleanup: "delete",             // 自动清理
  model: "bailian/glm-4.7"       // 合适模型
});
```

---

## 📁 脚本工具

### analyze_subagents.py

**功能：** 分析已配置的子代理角色和能力

```bash
# 分析当前配置
python3 skills/subagent-collaboration/scripts/analyze_subagents.py

# 输出示例
✅ 已配置子代理角色：12 个
   - 国际战略分析师 (qwen3.5-plus)
   - 商业战略咨询师 (qwen3.5-plus)
   - 网络安全专家 (qwen3-coder-plus)
   ...

📊 模型分布：
   - qwen3.5-plus: 5 个
   - qwen3-coder-plus: 3 个
   - glm-4.7: 4 个

💡 建议：
   - 可添加医疗顾问角色
   - 考虑添加法律顾问角色
```

### generate_workflow.py

**功能：** 根据任务描述生成协作流程

```bash
# 生成协作流程
python3 skills/subagent-collaboration/scripts/generate_workflow.py \
  --task "分析某科技公司是否值得投资" \
  --mode auto \
  --output workflow.json

# 输出示例
{
  "mode": "parallel",
  "agents": [
    {"label": "market-analysis", "task": "...", "model": "qwen3.5-plus"},
    {"label": "tech-analysis", "task": "...", "model": "qwen3-coder-plus"},
    {"label": "finance-analysis", "task": "...", "model": "glm-4.7"},
    {"label": "team-analysis", "task": "...", "model": "qwen3.5-plus"}
  ],
  "synthesizer": {"label": "investment-committee", "model": "qwen3-max"},
  "safetyCheck": "passed"
}
```

### security_check.py

**功能：** 检查协作流程的安全配置

```bash
# 安全检查
python3 skills/subagent-collaboration/scripts/security_check.py \
  --input workflow.json

# 输出示例
✅ 安全检查通过

检查项：
- ✅ 超时设置：全部≤300 秒
- ✅ 沙箱配置：全部 require
- ✅ 标签标识：全部有 label
- ✅ 清理策略：全部 delete
- ✅ 敏感任务：无
- ✅ 命令执行：无
- ✅ 并发控制：4 个（可接受）

⚠️ 警告：
- 建议使用低成本模型处理简单任务
```

---

## 🎯 完整案例

### 案例：投资分析报告生成

**任务：** 分析某科技公司是否值得投资

**步骤 1：分析任务特征**
```bash
python3 skills/subagent-collaboration/scripts/analyze_task.py \
  --task "分析某科技公司是否值得投资" \
  --output analysis.json
```

**步骤 2：生成协作流程**
```bash
python3 skills/subagent-collaboration/scripts/generate_workflow.py \
  --task "分析某科技公司是否值得投资" \
  --mode auto \
  --output investment_workflow.json
```

**步骤 3：安全检查**
```bash
python3 skills/subagent-collaboration/scripts/security_check.py \
  --input investment_workflow.json
```

**步骤 4：执行协作**
```javascript
// 使用生成的代码
const workflow = require('./investment_workflow.json');

// 第 1 阶段：并行数据收集
const [market, tech, finance, team] = await Promise.all([
  sessions_spawn({
    task: workflow.agents[0].task,
    label: workflow.agents[0].label,
    model: workflow.agents[0].model,
    timeoutSeconds: 180,
    sandbox: "require",
    cleanup: "delete"
  }),
  // ... 其他分析
]);

// 第 2 阶段：综合分析
const analysis = await sessions_spawn({
  task: `综合以下分析，给出投资建议：...`,
  label: "investment-committee",
  model: "bailian/qwen3-max",
  timeoutSeconds: 300,
  sandbox: "require",
  cleanup: "delete"
});

// 第 3 阶段：风险评估
const riskReview = await sessions_spawn({
  task: `审查以下投资建议的风险点：${analysis}`,
  label: "risk-review",
  model: "bailian/qwen3.5-plus",
  timeoutSeconds: 120,
  sandbox: "require",
  cleanup: "delete"
});
```

---

## 📊 性能优化建议

### 模型选择策略

| 任务类型 | 推荐模型 | 成本 | 响应时间 |
|----------|----------|------|----------|
| 简单任务 | glm-4.7 | ¥ | <30s |
| 日常分析 | qwen3.5-plus | ¥¥ | 30-60s |
| 专业技术 | qwen3-coder-plus | ¥¥ | 60-90s |
| 复杂推理 | qwen3-max | ¥¥¥¥ | 90s+ |

### 并发控制

```javascript
// ✅ 推荐：分批执行
const batch1 = [task1, task2].map(t => sessions_spawn(t));
await Promise.all(batch1);

const batch2 = [task3, task4].map(t => sessions_spawn(t));
await Promise.all(batch2);

// ❌ 避免：同时太多
Promise.all([task1, task2, task3, task4, task5].map(...));
```

### 成本优化

```javascript
// ✅ 混合使用模型
const simple = await sessions_spawn({
  task: "整理格式",
  model: "bailian/glm-4.7"  // 低成本
});

const complex = await sessions_spawn({
  task: "架构设计",
  model: "bailian/qwen3-max"  // 高端模型
});
```

---

## 🔗 相关技能

- **subagent-roles-v2** - 子代理角色定义和关键词匹配
- **subagent-keywords-v2** - 智能路由规则
- **runtime-security-guard** - RSG v2.2.0 子代理安全监控
- **multi-model-guide** - 多模型使用指南

---

## 📝 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-30 | 初始版本，支持 6 种协作模式 |

---

**维护者：** TUTU  
**最后更新：** 2026-03-30
