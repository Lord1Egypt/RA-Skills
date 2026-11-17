# Pass 6: Validate — 三层评估

**加载时机：** 📍 执行到 Pass 6 时加载。

---

## 设计哲学

**IR 是 spec，产出是 implementation，拿 spec 验 implementation。**

Pass 1-3 产出的 Skill IR 已经包含评估所需的全部信号：边界、能力、标准、失败用例。Pass 6 的职责是回头拿 IR 验证 Pass 4 生成的文件——这是编译器的语义闭环，和编译器做类型检查同理。

四层评估全部静态，零运行时依赖：

| Layer | 检查对象 | Oracle | 产出 |
|-------|---------|--------|------|
| **A 结构完整性** | 文件结构、模块边界 | 五角色审查清单 | issues 列表 |
| **B IR 一致性** | 生成文件 vs IR 契约 | Skill IR（Pass 1-3） | 契约违反项 |
| **C 触发质量** | description 触发准确性 | `self_test_cases`（Pass 3 派生） | 触发精度分数 |
| **D 平台合规** | 生成文件 vs 平台 profile | `profiles/{platform}.md` | 合规违反项 |

---

## Layer A — 结构完整性（五角色审查）

### Role 1 — Skill Architect（模块边界）

| 检查项 | 问题信号 | 严重度 |
|--------|---------|--------|
| 模块边界清晰 | 一个模块的修改不影响其他模块 | 🟠 High |
| 耦合度 | 模块间是否有不必要的依赖 | 🟠 High |
| 扩展风险 | 新增功能是否需要改动核心架构 | 🟡 Medium |
| 单一职责 | 每个模块只做一件事 | 🟠 High |

### Role 2 — Knowledge Engineer（知识管理）

| 检查项 | 问题信号 | 严重度 |
|--------|---------|--------|
| 知识污染 | 不同来源的知识混在同一文件 | 🟠 High |
| 知识重复 | 同一规则出现在多处 | 🟡 Medium |
| 可维护性 | 知识更新是否只改一处 | 🟠 High |
| 信任域 | 产出者和验证者是否读同一文件 | 🟠 High |
| 边界声明存在（v2.0） | 是否有 honest-boundaries / limitations 章节 | 🟠 High |
| 推断标注（v2.0） | inferred 知识是否标注为"推断/可能"而非确定性事实 | 🟠 High |
| 失败模式诚实（v2.0） | 是否声明至少 1 个已知失败模式（非空壳） | 🟡 Medium |

### Role 3 — Workflow Designer（流程设计）

| 检查项 | 问题信号 | 严重度 |
|--------|---------|--------|
| 流程合理 | 步骤顺序是否最优 | 🟡 Medium |
| 可恢复 | 步骤失败后是否能恢复 | 🟠 High |
| 死步骤 | 是否有从不执行的步骤 | 🟡 Medium |
| 循环上限 | 迭代步骤是否有 max_iterations | 🟠 High |

### Role 4 — Prompt Engineer（Prompt 质量）

| 检查项 | 问题信号 | 严重度 |
|--------|---------|--------|
| Prompt 膨胀 | SKILL.md > 300 行 | 🟠 High |
| 触发词 | description 是否含 3+ 触发词 | 🔴 Critical |
| 懒加载 | 是否有 📍 标记 | 🟡 Medium |
| frontmatter 卫生 | 是否只有 name + description | 🟠 High |

### Role 5 — Software Architect（架构债务）

| 检查项 | 问题信号 | 严重度 |
|--------|---------|--------|
| 技术债务 | 是否有明显的短期 hack | 🟡 Medium |
| 版本演进 | 是否支持未来扩展 | 🟡 Medium |
| 过度设计 | 是否有不必要的抽象 | 🟡 Medium |
| 文件组织 | 目录结构是否合理 | 🟡 Medium |

### Role 6 — Compaction Resilience（截断韧性，v2.0 新增）

**问题：** Harness 的 compaction 机制会截断 SKILL.md body（只保留前 N 行），导致 routing 信息丢失。

**方法：** 读取 `meta.target_platform` 对应的 `compaction_limit_lines`，模拟截断，检查 routing 完整性。

| 检查项 | 问题信号 | 严重度 |
|--------|---------|--------|
| 路由信息前置 | 截断后 routing table（或等效锚点）是否仍完整 | 🔴 Critical |
| 关键引用可达 | 截断后 "Always Read" 等关键引用声明是否保留 | 🟠 High |
| 无长依赖链 | 是否存在"需读完整个 body 才能理解"的隐式依赖 | 🟡 Medium |

**PASS 标准：** 截断后 routing 信息完整度 ≥ 80%（按 routing table 可执行行数比例计算）。

**FAIL 处理：** 要求将 routing table 移至 SKILL.md 前 N 行内，或在前 N 行添加显式锚点链接。

---

## Layer B — IR 一致性（契约验证）

**问题：** 生成的文件未必忠实于 IR。比如 IR 说 `out_of_scope: ["纯翻译"]`，但生成的 SKILL.md description 宽到会触发翻译请求。

**方法：** 逐字段比对 IR 与生成文件。IR 是 Pass 1-3 产出的 spec，生成文件是 Pass 4 的 implementation。

### B 组检查项

| # | IR 字段 | 验证目标 | PASS 标准 | 严重度 |
|---|---------|---------|-----------|--------|
| B1 | `capability_graph.primary` | SKILL.md description | description 含每个 primary capability 的同义词或近义表述 | 🔴 Critical |
| B2 | `boundary.out_of_scope` | SKILL.md / Pass 0 拒绝逻辑 | 每个 out_of_scope 项在 SKILL.md 有对应排斥声明或 Pass 0 拒绝规则 | 🟠 High |
| B3 | `knowledge_inventory.standards[].target_file` | 文件存在 + 被引用 | target_file 存在且被 SKILL.md 或 workflow 引用（不是孤儿） | 🟠 High |
| B4 | `knowledge_inventory.examples[type=failure]` | examples 被消费 | failure 类型 example 至少被 Gotchas 或审查逻辑引用一次 | 🟡 Medium |
| B5 | `role_matrix.existing[should_split=true]` | 拆分已执行 | should_split=true 的角色在生成的 agents/ 下确实被拆成独立文件 | 🟠 High |
| B6 | `module_decomposition.references[]` | 无知识重复 | 任意两个 reference 文件内容重叠 < 40% | 🟡 Medium |
| B7 | `workflow_steps[].exit_criteria` | 门控可执行 | 每个 workflow step 的 exit_criteria 在生成文件中有对应检查点 | 🟠 High |
| B8 | `self_test_cases.negative` | description 不含排斥词 | description 不包含任何 negative case 的核心词 | 🔴 Critical |
| B9 | `knowledge_inventory[*].evidence`（v2.0） | evidence 字段完整性 | 所有知识条目都有 evidence 字段（primary/secondary/inferred） | 🟠 High |
| B10 | `knowledge_inventory[evidence=inferred]`（v2.0） | 推断条目有标注 | evidence=inferred 的条目在生成文件中明确标注为"推断/可能" | 🟡 Medium |
| B11 | `conflicts`（v2.0） | 冲突未被静默丢弃 | IR 中 conflicts 数组的每个条目在生成文件中都有对应呈现 | 🟠 High |
| B12 | `conflicts.status`（v2.0） | 冲突健康度 | status=open 占比 < 30%；不存在"连续 3 次编译仍为 open"的冲突 | 🟡 Medium |

### B 组执行规则

1. **读取完整 IR** — Pass 1-3 的 IR 是唯一 oracle，不重新推断
2. **逐字段比对** — B1-B8 逐项检查，不跳过
3. **同义词容忍** — B1 允许同义词匹配（如 "审查" ↔ "review" ↔ "检查"），不要求字面一致
4. **FAIL 记录差异** — 记录 IR 期望值与文件实际值的差异，供修复

---

## Layer C — 触发质量（静态触发评测）

**问题：** description 写得再好，实际触发准不准？不跑 LLM 也能回答。

**方法：** 用 Pass 3 派生的 `self_test_cases` 当测试集，静态匹配 description。

### C 组检查项

| # | 检查项 | 方法 | PASS 标准 | 严重度 |
|---|--------|------|-----------|--------|
| C1 | positive 召回 | 对每个 `self_test_cases.positive`，检查 description 是否含能匹配的词（含同义词） | 召回率 = 100% | 🔴 Critical |
| C2 | negative 排斥 | 对每个 `self_test_cases.negative`，检查 description 是否**不**含匹配词 | 误触发率 = 0% | 🟠 High |
| C3 | near_miss 边界 | 对每个 `self_test_cases.near_miss`，检查 description 是否有明确排斥声明 | 有排斥声明 或 near_miss 为空 | 🟡 Medium |
| C4 | 压力测试 / 诱饵题（v2.0） | 构造"看似在 scope 内但实际应拒绝"的诱饵输入，检查 description 是否会被误导触发 | 诱饵题误触发率 = 0% | 🟠 High |

### C4 压力测试（诱饵题）说明

从 `boundary.out_of_scope` 与 `capability_graph.primary` 的**语义交叉区**构造诱饵题——那些表面上像是 skill 职责、但实际超出边界或需要拒绝的输入。

**构造方法：**
- 取一个 out_of_scope 项，用 in_scope 的措辞方式重新表述
- 例：out_of_scope 是"翻译任务"，in_scope 是"代码审查"，诱饵题 = "审查这段代码的英文翻译是否准确"
- 诱饵题应在字面上命中 description 的触发词，但实际不应由本 skill 处理

**PASS 标准：** description 中的排斥声明或 Pass 0 拒绝逻辑能正确识别诱饵题并拒绝。若诱饵题会误触发，说明 description 边界不够锐利，需补充排斥声明。

### 触发精度计算

```
trigger_precision = matched_positive / (matched_positive + matched_negative + 0.5 × matched_near_miss)
```

| trigger_precision | 含义 |
|-------------------|------|
| 1.0 | 完美 — 所有 positive 命中，无 negative/near_miss 误触发 |
| 0.7-0.99 | 良好 — 少量 near_miss 模糊 |
| < 0.7 | 不合格 — 存在 negative 误触发或 positive 漏召回 |

### 匹配方法

- **词级匹配：** description 含 case 中的核心动词/名词
- **同义词扩展：** "审查" 含 "review/check/检查"，"生成" 含 "create/write/写"
- **不跑 LLM：** 纯字符串/词级匹配，零成本可重复

---

## Layer D — 平台合规（Profile 验证）

**问题：** 生成的 Skill 符合 IR 规范，但在目标平台上可能无法正常运行。比如 TRAE 平台不支持多行 description、agents/ 目录等。

**方法：** 读取 `meta.target_platform` 并加载对应平台 profile，逐项验证生成文件是否满足 profile 约束。profile 作为 oracle。

### D 组检查项

| # | 检查项 | 方法 | PASS 标准 | 严重度 |
|---|--------|------|-----------|--------|
| D1 | frontmatter 字段合规 | 比对 profile.frontmatter 允许字段 | 生成文件的 frontmatter 字段是 profile 允许的超集 | 🔴 Critical |
| D2 | description 格式合规 | 检查 description 是否为 profile 要求的格式（单行/多行） | 格式匹配 profile 约束 | 🔴 Critical |
| D3 | description 长度合规 | 检查 description 字符数 | ≤ profile 规定的上限 | 🟠 High |
| D4 | 触发词格式合规 | 检查触发词格式是否遵循 profile 规范 | 格式匹配（逗号分隔 / 列表格式） | 🟠 High |
| D5 | 目录合规 | 检查所有生成的目录是否在 profile 白名单中 | 无不在白名单的目录 | 🟠 High |
| D6 | platform_profile_applied 标记 | 检查 IR 中此标记 | `meta.platform_profile_applied === true` | 🟡 Medium |
| D7 | agents/ 目录约束（TRAE） | 若 target=trae，检查是否误生成了 agents/ | 无 agents/ 目录 | 🟠 High |
| D8 | 额外字段约束 | 检查 frontmatter 是否包含 profile 不允许的额外字段 | 无 profile 不允许的字段 | 🟡 Medium |

### D 组执行规则

1. **无 profile 时跳过** — 若 `meta.target_platform` 对应的 profile 文件不存在，跳过此层并标注 warning
2. **默认值回退** — 若 profile 中某字段未定义，回退到 `generic` profile 的对应值
3. **Critical 优先** — D1/D2 失败直接标记为 Critical，必须修复

### 平台合规率计算

```
platform_compliance_rate = D 组通过项数 / D 组总检查项数
```

---

## 综合评分

### 评分公式

```
skill_quality_score =
    structural_pass_rate       × 0.2    (Layer A)
  + ir_consistency_rate        × 0.3    (Layer B — 权重最高，契约验证)
  + trigger_precision          × 0.25   (Layer C)
  + platform_compliance_rate   × 0.25   (Layer D)
```

- `structural_pass_rate` = Layer A 通过项数 / 总项数
- `ir_consistency_rate` = Layer B 通过项数 / 总项数
- `trigger_precision` = Layer C 计算值

### Verdict 判定

| 条件 | Verdict |
|------|---------|
| `skill_quality_score ≥ 85` 且 0 个 Critical issue | `pass` |
| `skill_quality_score 60-84` 或有 Critical 但有明确修复方案 | `conditional-pass` |
| `skill_quality_score < 60` 或有 Critical 且无法本轮修复 | `fail` |

### 严重度处理优先级

| 严重度 | 处理 |
|--------|------|
| 🔴 Critical | 必须修复才能 pass |
| 🟠 High | 应该修复 |
| 🟡 Medium | 建议修复 |
| 🟢 Low | 记录即可 |

---

## 审查流程

### Step 6.0 — Meta-Reflection Pre-Check（v2.1）

在启动四层评估前，用以下 3 个维度做最终的编译自省。Quick 模式跳过此步。

📍 完整框架见 [meta-reflection.md](meta-reflection.md)

| 维度 | 自检问题 |
|------|---------|
| D4 证据 | inferred 条目占比是否 > 30%？是否存在"公认事实"其实只是推断的知识？ |
| D7 目标 | 为了"通过所有 Pass"是否做了不必要的过度设计？最终产出对用户而言真的可用吗？ |
| D8 不确定性 | skill 中哪些部分是我们猜测的而非确定的？如果只能修正一件事来提高可信度，是什么？ |

**输出：** 自省结果写入 Evaluation Report 的 `meta_reflection_notes` 字段。不阻塞 verdict 判定。

### Step 6.1 — Layer A 扫描

五角色独立审查，输出 issues 列表。

### Step 6.2 — Layer B 契约验证

读取完整 IR，逐字段（B1-B8）比对生成文件。

### Step 6.3 — Layer C 触发评测

读取 `self_test_cases`，对 description 做静态匹配，计算 trigger_precision。

### Step 6.4 — Layer D 平台合规

读取 `meta.target_platform`，加载对应平台 profile，逐项检查 D1-D8。

### Step 6.5 — 去重合并

四层可能发现相同问题（如 Layer A Role 4 和 Layer C C1 都发现触发词不足）。合并为单条 issue，标注发现层。

### Step 6.6 — 计算综合评分

按含 Layer D 的公式计算 `skill_quality_score`，结合 Critical issue 数判定 verdict。

---

## Optimization Opportunities

审查中发现的非问题但可改进的点：

| 类型 | 示例 |
|------|------|
| 未来扩展 | "当前是 single-prompt，未来可演进为 workflow" |
| 性能 | "reference 文件可进一步拆分以减少加载" |
| 用户体验 | "可添加更多触发词变体" |

---

## Output Schema

```json
{
  "review_summary": "整体评价（2-3 句）",
  "layer_a_structural": {
    "issues": [
      {
        "id": "A-ISS-001",
        "severity": "critical | high | medium | low",
        "role": "Skill Architect | Knowledge Engineer | Workflow Designer | Prompt Engineer | Software Architect",
        "title": "问题标题",
        "detail": "具体描述",
        "fix": "修复方案",
        "fix_difficulty": "easy | medium | hard"
      }
    ],
    "pass_rate": 0.85
  },
  "layer_b_ir_consistency": {
    "issues": [
      {
        "id": "B-ISS-001",
        "check": "B1 | B2 | ... | B8",
        "severity": "critical | high | medium | low",
        "ir_field": "capability_graph.primary",
        "expected": "IR 期望值",
        "actual": "文件实际值",
        "fix": "修复方案"
      }
    ],
    "pass_rate": 0.75
  },
  "layer_c_trigger_quality": {
    "positive_recall": 1.0,
    "negative_precision": 0.0,
    "near_miss_boundary": 0.5,
    "trigger_precision": 0.83,
    "details": [
      {
        "case": "审查这段 Python 代码",
        "expected": "positive",
        "matched": true,
        "matched_token": "审查"
      }
    ]
  },
  "layer_d_platform_compliance": {
    "issues": [
      {
        "id": "D-ISS-001",
        "check": "D1 | D2 | ... | D8",
        "severity": "critical | high | medium | low",
        "title": "问题标题",
        "detail": "具体描述",
        "fix": "修复方案"
      }
    ],
    "pass_rate": 0.875,
    "platform": "trae"
  },
  "cost_summary": {
    "total_tokens": 12500,
    "total_passes_executed": 5,
    "total_passes_skipped": 2,
    "budget_consumption_pct": 62.5
  },
  "skill_quality_score": 81,
  "issues": [
    {
      "id": "ISS-001",
      "layer": "A | B | C | D",
      "severity": "critical | high | medium | low",
      "title": "问题标题",
      "detail": "具体描述",
      "fix": "修复方案",
      "fix_difficulty": "easy | medium | hard"
    }
  ],
  "optimization_opportunities": [
    {
      "type": "future-expansion | performance | ux",
      "description": "建议描述",
      "priority": "low | medium | high"
    }
  ],
  "verdict": "pass | conditional-pass | fail",
  "verdict_reason": "判定理由（含分数构成）",
  "meta_reflection_notes": "v2.1: Step 6.0 元反思自省记录（D4/D7/D8 维度发现）"
}
```
