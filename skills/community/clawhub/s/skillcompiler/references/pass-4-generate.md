# Pass 4: Generate — 生成 Skill 包

**加载时机：** 📍 执行到 Pass 4 时加载。

---

## 生成原则

1. **IR 驱动** — 所有文件内容来自 Pass 1-3 的 IR，不凭空创造
2. **三层加载** — L1 frontmatter / L2 SKILL.md 路由 / L3 references 懒加载
3. **平台感知渲染** — frontmatter、description、文件结构按 `target_platform` 对应的 profile 规范渲染
4. **frontmatter 卫生** — 只含目标平台要求的字段（generic/trae 仅 name + description）
5. **无占位符** — 不留 TODO/TBD/placeholder
6. **文件最小化** — 只生成 IR 要求的文件，不多创建

---

## Step 4.1 — SKILL.md 生成

### Step 4.0 — 加载目标平台 Profile

读取 `meta.target_platform` 并加载对应 profile：

| target_platform | Profile 文件 |
|----------------|-------------|
| `trae`         | 📍 [profiles/trae.md](../profiles/trae.md) |
| `claude`       | 📍 [profiles/claude.md](../profiles/claude.md) |
| `generic`      | 📍 [profiles/generic.md](../profiles/generic.md) |

后续渲染步骤全部参考 profile 中定义的约束（description 格式、触发词策略、文件结构支持列表）。

### Frontmatter — 按平台渲染

#### TRAE 平台

```yaml
---
name: {kebab-case-name}
description: "Use when {触发场景}. Triggers on: {触发词1}, {触发词2}, {触发词3}. {核心功能一句话}"
---
```

**约束：**
- description 必须为**严格单行 YAML 字符串**，不支持多行 block scalar
- ≤ 500 字符
- 触发词用「逗号 + 空格」分隔
- 不包含 `version` 等额外 frontmatter 字段

#### Claude 平台

```yaml
---
name: {kebab-case-name}
description: >
  Use when {触发场景}.

  Triggers on:
  - {触发词1}
  - {触发词2}
  - {触发词3}

  {核心功能一句话描述}
version: 1.0.0
---
```

**约束：**
- description 支持多行 block scalar（`>` 或 `|`）
- ≤ 500 字符
- 触发词支持列表格式（每行一个）
- 可包含 `version` 等额外字段

#### Generic 平台（默认）

```yaml
---
name: {kebab-case-name}
description: "Use when {触发场景}. Triggers on: {触发词1}, {触发词2}, {触发词3}. {核心功能一句话}"
---
```

**约束：**
- description 严格单行（兼容所有 YAML 解析器）
- ≤ 300 字符（最严格限制）
- frontmatter 只保留 name + description

---

**description 通用规则（所有平台）：**
- 以 "Use when" / "Use for" 开头
- 包含 3+ 用户可能输入的触发词
- 聚焦用户意图，不描述内部机制

### Body 结构

```markdown
# {Skill Name}

{一句话定位}

## 核心流程
{3-5 步流程概览，每步一句话}

## 执行步骤
### Step 1 — {名称}
📍 加载文件: references/xxx.md
{简要说明 + 输入输出}

### Step 2 — {名称}
...

## 输出格式
{输出 schema 或模板引用}

## Gotchas
{常见陷阱，首次留骨架}
```

### 行数控制

- **< 150 行：** 理想
- **150-300 行：** 可接受
- **> 300 行：** 必须拆分（AP-02 Prompt Black Hole）

### 平台感知的文件结构约束

生成 `references/` 和可能的工作流/agent 目录时，参考目标平台的 profile：

| 目录 | generic | trae | claude |
|------|---------|------|--------|
| `references/` | ✅ | ✅ | ✅ |
| `templates/` | ✅ | ✅ (放 references/ 更安全) | ✅ |
| `workflows/` | ❌ | ❌ | ✅ |
| `agents/` | ❌ | ❌ | ✅ |
| `rubrics/` | ❌ | 放 references/ 内 | ✅ |
| `checklists/` | ❌ | 放 references/ 内 | ✅ |

**规则：** 不生成目标平台不支持的目录。必须生成的 reference 文件全部放在 `references/` 或模板所在平台允许的位置。

---

## Step 4.2 — References 生成

对 Pass 3 的 `reference_tree` 中每个文件：

### rules.md 模板

```markdown
# Rules

{从 knowledge_inventory.rules 逐条列出}

## 规则列表

| # | 规则 | 来源 |
|---|------|------|
| 1 | {规则内容} | source / inferred |
```

### domain-xxx.md 模板

```markdown
# {Domain} Knowledge

## {Topic 1}
{知识内容}

## {Topic 2}
{知识内容}
```

### best-practices.md 模板

```markdown
# Best Practices

## {Practice 1}
{内容 + 为什么}

## {Practice 2}
{内容 + 为什么}
```

### gotchas.md 模板（首次骨架）

```markdown
# Gotchas / Footguns

> 上线后根据实际 failure case 填充。

## 常见失败点
- TODO: {占位 — 替换为实际失败模式}

## 字段/命名歧义
- TODO: {占位}

## 边界条件
- TODO: {占位}
```

---

## Step 4.3 — Workflows 生成（workflow/multi-agent only）

对 Pass 3 的 `workflow_steps` 生成 YAML：

```yaml
name: {skill-name}-{workflow-name}
description: {工作流描述}

input:
  type: object
  required: [{必需字段}]
  properties:
    {field}: { type: string }

steps:
  - id: {step-id}
    agent: {agent-name}
    description: {步骤描述}
    input:
      {field}: "{{input.xxx}}"
    output: {output-var}
    when: [{条件表达式，可选}]
```

---

## Step 4.4 — Templates 生成

对 Pass 3 的 `module_decomposition.templates`：

```markdown
# {Template Name}

## 变量
| 变量 | 说明 | 必填 |
|------|------|------|
| {var} | {描述} | yes/no |

## 模板
---
{模板内容，用 {{var}} 标记变量}
---
```

---

## Step 4.5 — Checklists 生成

```markdown
# {Checklist Name}

## 检查项

| # | 检查项 | 如何检查 | PASS 标准 |
|---|--------|---------|-----------|
| 1 | {检查内容} | {方法} | {标准} |
```

---

## Step 4.6 — Rubrics 生成（当有 standards 时）

```markdown
# {Rubric Name}

## 评分维度

| 维度 | 权重 | 评分标准 |
|------|------|---------|
| {维度} | {X}% | {1-5 分的描述} |

## 风险矩阵
| 风险 | 概率 | 影响 | 等级 |
|------|------|------|------|

## 成熟度模型
| 级别 | 特征 |
|------|------|
| L1 | {描述} |
| L2 | {描述} |
| L3 | {描述} |
```

---

## Step 4.7 — Config 生成（当有参数化时）

```yaml
# config/settings.yaml
skill_name: {name}
version: 1.0.0
{参数}: {默认值}
```

---

## Step 4.8 — Schemas 生成（当有结构化输出时）

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "{Skill} Output",
  "type": "object",
  "required": ["field1"],
  "properties": {
    "field1": { "type": "string", "description": "..." }
  }
}
```

---

## Step 4.9 — Self-Check（生成后立即执行）

| # | 检查项 | FAIL 处理 |
|---|--------|----------|
| 1 | frontmatter 符合目标平台 profile 规范 | 按 profile 重写 |
| 2 | description 触发导向（Use when + 3+ 触发词） | 重写 description |
| 3 | SKILL.md < 300 行 | 拆分到 references |
| 4 | 所有 📍 标记的文件存在 | 创建缺失文件 |
| 5 | 无 TODO/TBD/placeholder（gotchas.md 骨架除外） | 填充或移除 |
| 6 | 每个文件被至少一个其他文件引用 | 移除孤立文件或添加引用 |
| 7 | 未生成目标平台不支持的目录 | 移入 references/ |
| 8 | 已设置 `meta.platform_profile_applied = true` | 设置标记 |

任一 FAIL → 修复后重新检查，全部 PASS → 进入 Pass 5/6。
