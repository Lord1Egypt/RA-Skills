---
name: skill-sub
version: 1.27.1
author: wUwproject
license: MIT
description: 调用链编排技能 — 既是调用链编辑器，也是粗粒度规划器。理解用户意图 → 规划 Skill 参与顺序 → 更新/保存/推荐调用链 → 拼接为调用链（支持循环/分支编排、子步骤拓扑排序、准确步骤计数）。
sensitive_access: false
critical_write: false
permission_weight: LOW
data_dir: ../.standardization/skill-sub/data/
tags: ['chain', 'orchestration', 'usable', 'skill-builder', 'progressive-loading', 'planner', 'editor']
external_data_dir: true
trigger: ['规划类: 帮我规划一下/步骤是什么', '顺序类: 依次执行/先...再...', '链管理: 创建/查看/更新/删除调用链']
trigger_negative: ['不使用调用链', '手动逐步执行']
meta_field_sync: true
h1_position: true
---
# skill-sub




## 触发场景

**当用户提出以下意图时触发本技能：**
- 规划类：「帮我规划一下...」、「...的步骤是什么」
- 顺序类：「依次执行 A、B、C」、「先...再...」
- 链管理：「创建/查看/更新/删除调用链」

**否定条件**：仅当用户明确要求「不使用调用链」或「手动逐步执行」时，不自动触发。



## 核心能力

> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。

| # | 功能 | 说明 |
|---|------|------|
| 1 | **调用链管理** | 创建、查询、更新、删除调用链 |
| 2 | **执行计划生成** | 生成结构化执行计划，含并行/串行标记 |
| 3 | **条件执行** | 支持条件步骤，按条件判断是否执行 |
| 4 | **循环与分支编排** | 支持 for-each/while 循环和 if-else 分支 |
| 5 | **Dry-Run 模式** | 模拟执行，不实际调用技能 |
| 6 | **链备份与版本管理** | 自动备份，支持版本恢复 |
| 7 | **粘连点（Adhesion Point）** | 标记 skill 无法自动化的缺口，提供三种解决方案保证链不断；支持自愈 —— 每次执行自动扫描是否有新 skill 可填补 |

---

---





### 渐进式文件索引

| 文件名 | 位置 | 说明 |
|--------|------|------|
| `references/antipatterns.md` | skill-sub 反模式 | > 本文档收录 skill-sub 使用中的常见错误和正确做法。完整反模式示例见 `references/faq.md` |
| `references/adhesion.md` | 粘连点机制（v1.25.0） | > 粘连点定义、三种解决方案（manual/auto/hybrid）、自愈流程 |
| `references/chain_schema.md` | skill-sub 调用链数据结构 | > 本文档定义 Chain / Step / retry_policy / failure_mode 的完整结构。 |
| `references/changelog.md` | skill-sub 更新日志 | - **循环步骤（Loop Step）** — `type: "loop"` 支持 `for_each` / `whil |
| `references/examples.md` | skill-sub 使用示例 | > 本文档是 SKILL.md 的渐进式补充，提供完整使用示例。 |
| `references/faq.md` | skill-sub 常见问题 | > 本文档是 SKILL.md 的渐进式补充，收录常见问题与使用技巧。 |
| `references/permissions.md` | 权限说明 | 权限扫描风险等级：**MEDIUM** |
| `references/reference.md` | skill-sub 参考手册 | > 本文档是 SKILL.md 的渐进式补充，包含完整 CLI 速查、脚本 API、存储格式。 |
| `references/workflow.md` | skill-sub 详细工作流程 | > 本文档是 SKILL.md 的渐进式补充，详细描述执行流程、里程碑判断规则、三层回退策略。 |
## 快速开始

### 三步上手：创建一个最小调用链

```bash
# 第一步：初始化
python {SKILL_DIR}/scripts/chain_manager.py init

# 第二步：创建调用链（两个 skill + 一个粘连点连接）
python {SKILL_DIR}/scripts/chain_manager.py create --name "代码发布" \
  --description "从代码分析到发布的完整流程" \
  --steps '[
    {"index":1,"type":"skill","step_name":"代码审查","skill_name":"code-review","action":"审查PR"},
    {"index":2,"type":"adhesion","step_name":"审批发布","adhesion":{"reason":"发布审批需要人工决策","solutions":[{"mode":"manual","description":"人工审批发布申请"}]}},
    {"index":3,"type":"skill","step_name":"部署","skill_name":"deploy","action":"部署到生产环境"}
  ]'

# 第三步：生成执行计划
python {SKILL_DIR}/scripts/chain_executor.py plan --name "代码发布" --verbose
```

> 💡 **小贴士**：创建时如果步骤有 ERROR，会提示具体原因（如"连续缺口应合并为一个粘连点"），按提示修正后重试即可。

### 更多命令

```bash
# Dry-Run 模拟执行（不实际调用技能）
python {SKILL_DIR}/scripts/chain_executor.py plan --name "代码发布" --dry-run

# 查看调用链详情
python {SKILL_DIR}/scripts/chain_manager.py show --name "代码发布"

# 列出所有调用链
python {SKILL_DIR}/scripts/chain_manager.py list

# 删除（自动备份）
python {SKILL_DIR}/scripts/chain_manager.py delete --name "代码发布" --force
```

---



## 工作流程

1. **理解意图** → 分析用户输入，判断是否需要调用链
2. **规划技能顺序** → 推荐参与的 Skill 及其顺序
3. **流程缺口分析** → 检查技能衔接处是否存在语义/流程/决策缺口，在天然断裂处打粘连点（**禁止随意添加**）
4. **生成调用链** → 创建 JSON 格式的调用链定义（含 skill 步骤和 adhesion 步骤）。如有定时/自动化意图，**必须** 附带 `--schedule` 参数
5. **立即注册调度** → 链创建成功且带 `schedule` 时，AI **必须当场**完成注册。定时任务不等手动执行，不存在"等下次执行时再注册"的可能
6. **生成执行计划** → 输出 AI 可直接执行的指令序列
7. **（可选）实际执行** → 按执行计划逐步调用技能

---


### 循环与分支编排

### for-each 循环

在调用链 JSON 中，将某步骤的 `type` 设为 `"loop"`，并定义 `loop` 对象：

```json
{
  "type": "loop",
  "step_name": "批量处理文件",
  "loop": {
    "mode": "for_each",
    "items": "{{file_list}}",
    "loop_variable": "f",
    "max_iterations": 10,
    "steps": [
      {"type": "skill", "skill_name": "file-ops", "step_name": "处理单个文件", "action": "处理 {{f}}"}
    ]
  }
}
```text

### while 循环

```json
{
  "type": "loop",
  "step_name": "重试直到成功",
  "loop": {
    "mode": "while",
    "while_condition": "{{retry_count}} < 3 and {{last_result}} != 'success'",
    "max_iterations": 3,
    "steps": [
      {"type": "skill", "skill_name": "api-call", "step_name": "调用接口", "action": "重试第 {{retry_count}} 次"}
    ]
  }
}
```text

### if-else 分支

```json
{
  "type": "branch",
  "step_name": "按环境部署",
  "branch": {
    "condition": "{{env}} == 'prod'",
    "if_steps": [
      {"type": "skill", "skill_name": "deploy", "step_name": "生产部署", "action": "部署到生产环境"}
    ],
    "else_steps": [
      {"type": "skill", "skill_name": "deploy", "step_name": "预发部署", "action": "部署到预发环境"}
    ]
  }
}
```

> 📚 完整 schema 详见 `references/chain_schema.md`

---



## 能力边界与限制

### 适宜场景 ✅

| 场景 | 说明 |
|------|------|
| 多 skill 编排 | 涉及 2 个及以上 skill，步骤间有明确依赖关系 |
| 可固化流程 | 流程稳定、可复现，不是一次性操作 |
| 跨步骤衔接 | skill 之间需要数据转换、人工审批、流程补全 |

### 不适宜场景 ❌

| 场景 | 原因 |
|------|------|
| 单 skill 任务 | 直接调 skill 本身即可，不需要调用链 |
| 一次性操作 | 调用链的价值在于复用，一次性工作不值得建链 |
| 无依赖的并行任务 | 多个独立任务应并行执行，不需要编排 |
| 高度动态的流程 | 每次执行步骤都不一样，粘连点也解决不了，直接 AI 手动处理 |

### 硬限制

| 限制项 | 值 | 说明 |
|--------|-----|------|
| 最大步骤数 | 30 层（含嵌套） | 超过后校验器会告警，但不阻断执行 |
| 粘连点占比 | 30% | 超过告警，建议合并或补充 skill |
| 粘连点连续 | **禁止** | 连续缺口合并为一个粘连点 |
| 依赖深度 | 10 层 | 过深依赖链难以维护和排查 |
| 循环最大迭代 | 默认 10，可配置 | 超过按 on_max_iteration 处理 |

### 常见创建错误速查

| 报错信息 | 原因 | 解决方法 |
|---------|------|---------|
| 连续缺口应合并为一个粘连点 | 两个 adhesion 步骤相邻 | 合并为一个 adhesion，用 hybrid 方案覆盖全部缺口 |
| 粘连点占比超过 30% | adhesion 步骤太多 | 检查是否有 skill 可以替代 |
| 缺少 solutions | adhesion 步骤没有提供方案 | 至少加一个 manual 方案 |
| 依赖不存在的步骤 | depends_on 引用了无效索引 | 检查依赖步骤的 index 是否正确 |
| 引用的 skill 不存在 | skill_name 对应的 skill 未安装 | 检查 skill 名称是否正确 |
| 检测到定时/自动化意图，但未提供 --schedule | 描述中含"每天/每周/定时"等词但没给调度配置 | 添加 --schedule 参数，或移除描述中的时间相关词 |

> **强制规则**：用户描述中包含定时/自动化意图（如"每天"、"每周"、"自动执行"等）时，**必须**提供 `--schedule` 参数配置调度信息，否则链创建被拦截。不依赖 AI 自觉判断。

## 配置

配置界面：`python {SKILL_DIR}/scripts/settings.py`

| 配置项 | 选项 | 说明 |
|--------|------|------|
| **记忆参考** | 是 / 否 | 创建/执行调用链时，是否读取用户记忆文件增强步骤描述 |
| **命名方式** | 自动 / 人工 | 创建调用链时，由 AI 自动命名还是询问用户 |
| **默认重试次数** | 1-10（默认3） | 所有步骤的默认最大重试次数 |

---

