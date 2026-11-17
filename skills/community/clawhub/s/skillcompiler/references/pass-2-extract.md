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

扫描内容，逐句分类：

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

### 并行提取（v2.0）

当输入来自 Pass I 多源摄取，或内容较长（> 3000 字）时，启用并行提取器代替单线程扫描。五个专项提取器（框架/原则/案例/反例/术语）并行扫描，合并后经三重验证筛入知识库。

📍 并行提取器与三重验证详见 [parallel-extractors.md](parallel-extractors.md)

### 提取规则

- **去重：** 相同规则出现多次，只保留一次
- **去噪：** 过渡句、寒暄语不提取
- **标注来源：** 每条知识标注 `[from source prompt]` 或 `[inferred by compiler]`

### 证据分级标注（v2.0）

每条提取的知识**必须携带 `evidence` 字段**，表示其可信度等级：

| 等级 | 含义 | 典型场景 |
|------|------|---------|
| `primary` | 原文直引，可溯源 | PDF 文本层、字幕原文、代码注释 |
| `secondary` | 经过一次模型转述 | OCR 结果、语音转写、视觉理解 |
| `inferred` | 编译器从上下文推断 | 隐含假设、跨段推理 |

默认值继承自 `pass_ingestion.evidence_grade`（若存在），但可逐条覆盖。

📍 完整证据分级体系与 confidence 字段定义见 [evidence-grading.md](evidence-grading.md)

### 冲突保留（v2.0）

当多条知识描述同一事实但内容矛盾时，**不强行统一，保留所有版本**并记录到 IR 的 `conflicts` 字段。冲突处理策略（unresolved / prefer_higher_evidence / prefer_newer / flag_for_user）见 [evidence-grading.md](evidence-grading.md) 的"冲突保留规则"章节。

**禁止：** 静默丢弃任一版本、强行取平均值、随机选择一方。

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

### Step 2.4 — Meta-Reflection Checkpoint（v2.1）

在进入 Pass 3 之前，用证据维度审视知识提取质量。Quick 模式跳过此步。

📍 完整框架见 [meta-reflection.md](meta-reflection.md)

| 维度 | 自检问题 |
|------|---------|
| D4 证据 | 所有知识条目是否都携带 `evidence` 字段？inferred 条目占比是否 > 30%？是否存在"公认事实"其实只是推断的知识？ |

**输出：** 如发现大量 inferred 条目缺少推断依据标注，补充标注后写入 IR。不阻塞 Decision Gate。

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
