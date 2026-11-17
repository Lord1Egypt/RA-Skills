# Honest Boundaries — 诚实边界规范

**加载时机：** 📍 Pass 3 Design 规划模块时加载；Pass 6 Layer A 结构审查时加载。

---

## 设计哲学

一个不告诉你"它做不到什么"的 skill，不值得信任。

大多数 skill 只描述自己的能力，却不声明局限。这导致用户在边界外使用时得到错误结果，却以为是 skill 质量问题。诚实边界的核心是：**每个 skill 必须显式声明自己的能力边界、失败模式、和适用前提**，让用户在使用前就知道风险。

这不是"谦虚"，是工程契约——类似 API 文档里的 `throws` 声明。

---

## 三类边界声明

每个生成的 skill 必须包含以下三类边界声明：

### 1. 能力边界（Cannot Do）

明确列出 skill **做不到**的事。来源：

- Pass 1 的 `boundary.out_of_scope`
- Pass I 的 `extraction_warnings`（如内容不完整）
- 领域知识中隐含的适用限制

**示例：**

```markdown
## 局限性

本 skill **不能**：
- 处理实时数据流（设计为批处理模式）
- 识别 0-day 漏洞（规则库更新周期为周级）
- 保证 100% 准确率（基于启发式规则，误报率约 5%）
```

### 2. 失败模式（Failure Modes）

描述 skill 在什么情况下会**给出低质量或错误结果**：

```markdown
## 已知失败模式

- 输入代码超过 2000 行时，审查质量下降（注意力分散）
- 混合语言的代码块（如 SQL 内嵌在 Python）可能漏报
- 高度抽象的设计模式代码，规则匹配可能误报
```

来源：Pass 6 审查中发现的弱点、Pass 2 的 `inferred` 知识、领域经验。

### 3. 适用前提（Prerequisites）

使用 skill 前必须满足的条件：

```markdown
## 适用前提

- 输入必须是可编译的源码（不支持伪代码）
- 项目需有基本的测试覆盖（否则"未覆盖"警告无意义）
- 单次审查文件数 ≤ 50（超过需分批）
```

---

## 在 Pass 3 中的应用

### 模块规划

Pass 3 Design 必须在 `module_decomposition` 中规划边界声明模块：

```json
{
  "module_decomposition": {
    "references": [
      "references/honest-boundaries.md — 局限性、失败模式、适用前提"
    ]
  }
}
```

### 边界声明来源映射

| 边界类型 | 数据来源 | IR 字段 |
|---------|---------|---------|
| Cannot Do | 显式排除项 | `pass_1.boundary.out_of_scope` |
| Cannot Do | 提取警告 | `pass_ingestion.extraction_warnings` |
| Failure Modes | 推断性知识的弱点 | `pass_2` 中 evidence=inferred 的条目 |
| Failure Modes | 架构固有限制 | `pass_3.architecture_type` 的已知弱点 |
| Prerequisites | 输入要求 | `pass_1.input_spec` |

### 生成模板（Pass 4 使用）

```markdown
# Honest Boundaries

## 局限性（Cannot Do）
{从 boundary.out_of_scope 逐条生成}

## 已知失败模式
{从 inferred 知识 + 架构弱点生成}

## 适用前提
{从 input_spec + 架构约束生成}

## 证据强度提示
{当 skill 包含 secondary/inferred 知识时，声明"部分结论基于转述/推断，建议核对原文"}
```

---

## 在 Pass 6 中的应用

### Layer A 结构审查新增角色检查

**Role 2 — Knowledge Engineer** 新增检查项：

| 检查项 | 问题信号 | 严重度 |
|--------|---------|--------|
| 边界声明存在 | 生成的 skill 是否有 honest-boundaries / gotchas / limitations 章节 | 🟠 High |
| 边界完整性 | out_of_scope 项是否都在生成文件中有对应声明 | 🔴 Critical |
| 推断标注 | inferred 知识是否被标注为"推断/可能"而非"事实" | 🟠 High |
| 失败模式诚实 | 是否声明了至少 1 个已知失败模式（非空壳） | 🟡 Medium |

### 空壳检测

若生成的 `references/honest-boundaries.md` 只有骨架无实质内容（全是 TODO/占位符），标记为：

> 🟡 Medium — 边界声明为空壳。建议基于 Pass 6 审查发现补充实际失败模式。

### 评分影响

- 缺失边界声明章节：Layer A pass_rate 扣减
- out_of_scope 项未在生成文件中体现：Layer B B2 直接 FAIL（Critical）
- inferred 知识未标注：Layer B B10 FAIL（Medium）

---

## 与 Gotchas 的区别

| 文档 | 职责 | 时态 |
|------|------|------|
| `honest-boundaries.md` | 系统性的能力边界声明 | 设计时已知 |
| `gotchas.md` | 上线后发现的踩坑记录 | 运行时发现 |

两者互补：honest-boundaries 是"出生时就知道的局限"，gotchas 是"踩坑后补的"。新生成的 skill 优先填充 honest-boundaries，gotchas 留骨架待运行时填充。

---

## 反模式

| 反模式 | 说明 | 检测 |
|--------|------|------|
| **全能声明** | description 声称能做所有事，无任何局限 | Layer C 触发质量检查：negative case 未被排斥 |
| **空壳边界** | 有 honest-boundaries 章节但全是占位符 | Pass 6 空壳检测 |
| **隐藏推断** | inferred 知识用确定性语气陈述 | Layer B B10 检查 |
| **静默丢弃冲突** | 多源矛盾信息只保留一方 | evidence-grading.md 冲突保留规则 + Layer B B11 |
