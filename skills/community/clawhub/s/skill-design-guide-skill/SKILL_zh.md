name: skill-design-guide
display_name: "Skill 设计指南"
description: >
  用经过验证的架构模式设计更好的 AI Skill。帮你判断该用 Workflow 还是 Agent，
  从 5 种工作流模式中选出最合适的，用 25 项检查清单审查质量，避开常见反模式。
  基于 Anthropic、OpenAI、LangChain 的设计原则。中文版，英文版见 SKILL.md。
version: "1.6.0"
agent_created: true
category: "Architecture / Design Patterns"
license: "MIT"
read_when:
  - 设计skill架构
  - workflow还是agent
  - 选工作流模式
  - 审查skill设计
  - skill质量检查
  - brain hands session
  - skill反模式
  - prompt chaining vs routing
  - 什么时候用agent
  - 创建新skill
  - 优化现有skill
---

# Skill 架构设计指南

> **30秒判断**：你正要写 SKILL.md？你的 skill "能跑但架构乱"？加载本指南。

## 定位

| 工具 | 做什么 |
|------|--------|
| **skill-creator** | 怎么写 SKILL.md 文件 |
| **本指南** | 为什么这样设计——Workflow 还是 Agent，选哪个模式 |

本指南回答的是 **WHY（为什么）**。行业研究背景见 `references/agent-design-research.md`。

## 3 种使用方式

| 方式 | 触发 | 输出 |
|------|------|------|
| **新建设计** | "我想做一个 [X] skill" | 架构蓝图（模式 + 结构） |
| **Skill 审查** | "审查这个 skill" / "检查质量" | 通过检查清单出审查报告 |
| **模式选择** | "我该用 X 还是 Y？" | 模式推荐 + 理由 |

---

## 硬性规则

> **以下规则不可违反，优先于所有其他考虑。**

1. **简单优先。** 从单个 SKILL.md 开始。只有简单方案不够用时才增加复杂度。
2. **Brain ≠ Hands。** LLM 决定做什么（SKILL.md），确定性代码执行（scripts/）。绝不混用。
3. **按需加载。** references 只在使用时加载，绝不一次性塞进上下文。
4. **每个 skill 必须包含：** 触发词 / 标注 `[Deterministic]`/`[LLM]` 的步骤 / Hard Rules / Failure Handling / Output Format。

---

## 原则零：简单优先

> **从简单开始。只当简单方案不够用时才增加复杂度。**

实用检查：
- 单个 SKILL.md 能搞定 → 不拆分
- 脚本能做 → 不用 LLM
- 固定工作流够用 → 不用动态 Agent
- 先发 MVP，根据输出质量迭代

---

## 原则一：Brain / Hands / Session 分离

| 层 | 角色 | 文件 |
|----|------|------|
| **Brain** | 决策逻辑、工作流定义 | `SKILL.md` |
| **Hands** | 确定性执行 | `scripts/` |
| **Session** | 知识库、配置、模板 | `references/`、`assets/` |

**你的已有实践：** `data-ai-daily-brief`（scripts 拉数据）、`benjie-model`（为其他 skill 提供 Session 层）。

---

## 第一步：Workflow 还是 Agent？

先回答一个问题：**任务步骤是预先确定的吗？**

| 类型 | 何时选择 |
|------|----------|
| **Workflow** | 步骤清晰可预测 → 选这个（更快、更便宜、可调试） |
| **Agent** | 步骤不确定，需要动态规划 → 选这个（灵活但成本高） |

**大多数场景都是 Workflow。** 别因为 Agent 听起来高级就选它。

---

## 第二步：选择模式

五种工作流模式。详解见 `references/pattern-details.md`。

| 模式 | 最适合 |
|------|--------|
| **提示链** | 顺序步骤 + 检查点 |
| **路由** | 输入类型明确 → 不同路径 |
| **并行化** | 子任务互相独立 |
| **协调者-执行者** | 子任务不可预测（谨慎！） |
| **评估器-优化器** | 生成→评估→迭代直到达标 |

---

## 第三步：Skill 结构

### 必需

| 组件 | 内容 |
|------|------|
| **SKILL.md** | YAML 元数据（`name`、`description`、`read_when`）+ 工作流 + Hard Rules + Failure Handling + Output Format |

### 可选

| 组件 | 何时需要 |
|------|---------|
| `references/` | 领域知识（按需加载） |
| `scripts/` | 确定性步骤 |
| `assets/` | 模板、配置 |
| `hooks/` | 宿主会话钩子——opt-in 门控、fail-open（见「行为面」） |
| `evals/` | skill 自身的可运行输出质量检查 |

### SKILL.md 模板

```yaml
---
name: my-skill
description: 一句话描述。触发词：a, b, c。
version: 1.0.0
read_when:
  - "触发短语 1"
  - "触发短语 2"
---

# Skill 名称

概述段落。

## 工作流

### 步骤 1：[Deterministic] 确认输入
- 验证输入存在
- 如果缺失，停止并报告

### 步骤 2：[Deterministic] 加载材料
- 读取 `references/xxx.md`（仅需要的文件）

### 步骤 3：[LLM] 核心执行
- 基于以上材料生成输出，遵循以下规则：
  - 规则 1
  - 规则 2

### 步骤 4：[LLM] 自检
- 验证输出是否达标 → 修正 → 重新输出

### 步骤 5：[Deterministic] 保存输出

## 硬性规则

> 以下规则不可违反。

1. 规则 1
2. 规则 2

## 失败处理

| 场景 | 动作 |
|------|------|
| 源文件未找到 | 停止生成，报告缺失文件 |
| 输出超出字数上限 50% | 压缩重写 |

## 输出格式

[定义具体输出格式和字段]
```

---

## 第四步：质量检查清单

完成后加载 `references/quality-checklist.md` 运行完整的 25 项检查。

结构 ✓ | 原则 ✓ | 工具 ✓ | 护栏 ✓ | 可观测性 ✓

---

## 反模式

| 反模式 | 修正 |
|--------|------|
| **过度工程** | 从单个 SKILL.md 开始 |
| **全量预加载** | references 按需加载 |
| **上帝 Skill** | 拆分——一个 skill 做一件事 |
| **全 LLM** | 确定性步骤用脚本 |
| **无护栏** | 加 Hard Rules + Failure Handling |
| **模糊输出** | 明确定义格式和字段 |
| **未声明副作用** | 脚本的每个网络/凭据行为都写进 frontmatter（见「行为面」） |

---

## 行为面：最小、可选加入、如实声明

约束 skill 里 prose 之外的附属物——hooks、脚本、平台适配器。提炼自线上扫描结论与一个 48k 星社区 skill（2026-09）。

| 规则 | 含义 |
|------|------|
| **只做 opt-in** | 任何自动运行的东西（hooks、会话启动注入）必须由用户创建的 flag 文件门控；flag 不存在 → 什么都不做 |
| **宿主边界 fail-open** | hook 或辅助脚本出错绝不能阻塞宿主会话：捕获一切，exit 0 |
| **路径从脚本自身位置解析** | 永远不要用环境变量定位随包文件——从脚本自身路径推导 |
| **单一规则源** | 只有一份权威规则文件；各平台适配器只做注入，绝不复制——副本必然漂移并自相矛盾 |
| **声明与行为一致** | 脚本实施的每个网络端点、凭据来源、文件读取都必须写进 frontmatter（`permissions` + capability token）。扫描器会标记未声明行为（LP1）；「从不读文件」这类绝对化表述在另一个组件确实读文件时必须加限定 |
| **自带 override 条款** | 写明 skill 自身规则何时让位——安全 > 任务 > 宿主 > 风格。没有逃生门的全套规则会被整体丢弃 |

行为面越小越好：最好的辅助物在被显式调用前什么都不做，失败时也不造成任何伤害。

---

## 失败处理（本指南自身）

| 场景 | 动作 |
|------|------|
| 用户问的是代码怎么写，不是设计 | 重定向到 `skill-creator` |
| 模式对比不够精确 | 加载 `references/pattern-details.md` |
| 审查请求缺少 skill 详情 | 询问："给我看你的 SKILL.md 或描述 skill 功能" |

---

## 参考文件（按需加载）

| 需要 | 加载 |
|------|------|
| **完整设计与实践指南**（全生命周期：设计/编写/审计/发布/安全对抗/维护） | `GUIDE_zh.md` |
| 25 项检查清单 | `references/quality-checklist.md` |
| 模式详解 | `references/pattern-details.md` |
| 平台配置 | `references/platform-compatibility.md` |
| 行业研究背景 | `references/agent-design-research.md` |
| Anthropic 工具设计 | `references/anthropic-tool-design.md` |

---

*v1.4.3 | Based on Anthropic/OpenAI/LangChain design principles | 2026-06-23*

**更新日志：**
- v1.7.1：新增「行为面」一节（opt-in 门控、fail-open hooks、路径自解析、单一规则源、声明与行为一致、override 条款）+ `hooks/`、`evals/` 可选组件 + 未声明副作用反模式。提炼自 i-have-adhd 审计与 LP1 扫描结论。（v1.5.0-v1.7.0 的更新日志未记录，以 frontmatter 版本号为准。）
- v1.4.3：恢复显示名称 "Skill Design Guide"
- v1.4.2：合并 `reference/` 与 `references/` 为单一 `references/` 目录；修正所有引用路径
- v1.4.1：修正显示名称
- v1.4.0：重构为渐进式加载——检查清单/模式/平台表拆分到 `references/`；新增 Hard Rules + Failure Handling；SKILL_zh.md 从 9.3K 精简到 ~4.5K
- v1.3.0：添加使用场景，中英文双版本
- v1.2.0：平台无关化重写，添加 Credits
