# Pass 2: Extract — 能力/知识/角色抽取

**加载时机：** 📍 执行到 Pass 2 时加载。

---

## 三合一抽取

原 16-phase 设计把 Capability Extraction、Knowledge Extraction、Role Extraction 拆成三步。但它们本质都是"分析 Prompt 的组成要素"，强关联且无独立决策门。合并为一次扫描，产出三个 IR 字段。

---

## Step 2.1 — Capability Graph 构建

### 能力识别

从 Pass 1 的 `capability_hints` 出发，构建能力依赖图：

```
Primary Capability（核心能力，1-3 个）
  ├── Sub-capability（子能力）
  └── Supporting Capability（支撑能力）
```

### 能力分类参考

| 类别 | 能力 |
|------|------|
| 认知 | Decision Making, Reasoning, Analysis, Prediction |
| 创造 | Writing, Brainstorming, Coding, Mapping |
| 评估 | Review, Evaluation, Scoring, Ranking, Classification |
| 执行 | Planning, Workflow, Research, Knowledge Retrieval |
| 交互 | Role Playing, Simulation |

### Graph 构建规则

1. **Primary** = Prompt 的核心功能对应的能力（1-3 个）
2. **Secondary** = 支撑核心能力的能力
3. **Graph edges** = 能力间的依赖关系（A 需要 B 先完成）

---

## Step 2.2 — Knowledge Inventory 提取

扫描 Prompt，逐句分类：

| 知识类型 | 识别信号 | 去向 |
|---------|---------|------|
| **Rules** | "必须"、"禁止"、"不要"、"always"、"never" | `references/rules.md` |
| **Templates** | 有结构化输出格式、固定 section | `templates/*.md` |
| **Domain Knowledge** | 行业术语、专业概念、法规 | `references/domain-*.md` |
| **Examples** | "例如"、"示例"、"case" | `examples/*.md` |
| **Standards** | 评分标准、质量标准、验收标准 | `rubrics/*.md` |
| **Roles** | "你是..."、"作为..."、persona 定义 | Pass 2.3 处理 |
| **Processes** | 步骤、流程、phase | Pass 3 Design 处理 |
| **Experience** | 经验法则、最佳实践、教训 | `references/best-practices.md` |

### 提取规则

- **去重：** 相同规则出现多次，只保留一次
- **去噪：** Prompt 中的过渡句、寒暄语不提取
- **标注来源：** 每条知识标注 `[from source prompt]` 或 `[inferred by compiler]`

---

## Step 2.3 — Role Matrix 构建

### 识别现有角色

扫描 Prompt 中的 persona 定义：

| 信号 | 示例 |
|------|------|
| 显式角色声明 | "你是世界级 AI Skill Architect" |
| 隐式角色 | "审查代码质量"（隐含 Reviewer 角色） |
| 多角色切换 | Prompt 中有多个"你是..." |

### 角色分析

对每个识别到的角色：

| 字段 | 说明 |
|------|------|
| name | 角色名 |
| responsibility | 职责描述 |
| capabilities | 需要的能力（关联 Capability Graph） |
| should_split | 是否应该拆分为独立 agent |
| split_reason | 拆分理由（如果 should_split=true） |

### 拆分判断

| 条件 | should_split |
|------|-------------|
| 单一角色，职责清晰 | false |
| 角色有 3+ 不相关职责 | true |
| 角色同时负责"产出"和"验证" | true（干验分离原则） |
| 角色需要不同的知识域 | true |

### 建议新增角色

分析 Prompt 缺失但 Skill 需要的角色：
- 缺少 Verifier？（产出后需要独立验证）
- 缺少 Router？（多种输入类型需要路由）
- 缺少 Formatter？（需要统一输出格式）

---

## Output Schema

```json
{
  "capability_graph": {
    "primary": ["能力1", "能力2"],
    "secondary": ["能力3"],
    "graph": {
      "能力1": ["子能力A", "子能力B"],
      "能力2": ["子能力C"]
    }
  },
  "knowledge_inventory": {
    "rules": [
      { "content": "规则内容", "source": "from source prompt | inferred", "target_file": "references/rules.md" }
    ],
    "templates": [
      { "name": "模板名", "structure": "结构描述", "target_file": "templates/xxx.md" }
    ],
    "domain_knowledge": [
      { "content": "知识内容", "domain": "领域", "target_file": "references/domain-xxx.md" }
    ],
    "examples": [
      { "type": "minimal | normal | complex", "content": "示例内容", "target_file": "examples/xxx.md" }
    ],
    "standards": [
      { "type": "scoring | quality | acceptance", "content": "标准内容", "target_file": "rubrics/xxx.md" }
    ],
    "best_practices": [
      { "content": "实践内容", "target_file": "references/best-practices.md" }
    ]
  },
  "role_matrix": {
    "existing": [
      {
        "name": "角色名",
        "responsibility": "职责",
        "capabilities": ["关联能力"],
        "should_split": false,
        "split_reason": ""
      }
    ],
    "to_add": [
      {
        "name": "建议角色名",
        "reason": "为什么需要这个角色",
        "responsibility": "职责"
      }
    ]
  }
}
```

## Decision Gate

| 条件 | 动作 |
|------|------|
| capability_graph.primary 非空 | → Pass 3 |
| capability_graph 为空 | REJECT — Prompt 没有可提取的能力，不适合做 Skill |
