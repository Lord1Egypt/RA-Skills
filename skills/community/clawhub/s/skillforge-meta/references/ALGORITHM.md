# SkillForge — Algorithm Deep Dive

> 本文档是 SkillForge 的算法实现细节，供开发者/高级用户参考。
> 普通用户无需阅读此文档，SKILL.md 已包含完整使用指南。

---

## Module 1: Scout（模式侦察引擎）

### 1.1 数据源

Scout 扫描以下数据：

| 数据源 | 路径 | 用途 |
|--------|------|------|
| Daily Log | `{workspace}/.workbuddy/memory/YYYY-MM-DD.md` | 每日工作记录，发现重复行为 |
| Long-term Memory | `{workspace}/.workbuddy/memory/MEMORY.md` | 长期偏好和惯例 |
| 已有 Skill | `~/.workbuddy/skills/*/SKILL.md` | 已沉淀的能力，避免重复 |
| 对话历史摘要 | 当前会话的 cb_summary | 本次对话中的模式 |

### 1.2 模式识别算法

Scout 的模式识别分三步：**提取 → 聚类 → 过滤**。

#### Step 1: 操作序列提取

从每条 daily log 条目中提取结构化的**操作指纹（Action Fingerprint）**：

```yaml
fingerprint:
  intent: string          # 意图摘要（LLM 提取，≤ 20 字）
  domain: enum            # 领域标签：code | data | doc | ops | research | other
  tool_chain: string[]    # 使用的工具序列
  step_count: int         # 步骤数
  output_type: enum       # 产物类型：file | report | config | command | conversation
  keywords: string[]      # 关键词（LLM 提取，≤ 5 个）
```

**提取参数**：
- `MAX_FINGERPRINTS_PER_DAY`: 20
- `MIN_STEP_COUNT`: 2
- `LOOKBACK_DAYS`: 14

#### Step 2: 相似度计算与聚类

```
similarity(A, B) = w_intent × sim_intent(A, B)
                 + w_domain × sim_domain(A, B)
                 + w_tools  × sim_tools(A, B)
                 + w_keywords × sim_keywords(A, B)
```

| 维度 | 权重 | 计算方法 |
|------|------|---------|
| `sim_intent` | **0.40** | LLM 判断两个 intent 是否描述同一类任务，输出 0/0.5/1 三档 |
| `sim_domain` | **0.15** | 相同 domain = 1.0，不同 = 0.0 |
| `sim_tools` | **0.25** | Jaccard 系数：`|tools_A ∩ tools_B| / |tools_A ∪ tools_B|` |
| `sim_keywords` | **0.20** | Jaccard 系数：`|kw_A ∩ kw_B| / |kw_A ∪ kw_B|` |

**聚类参数**：
- `SIMILARITY_THRESHOLD`: 0.65
- `MIN_CLUSTER_SIZE`: 3
- `CLUSTER_METHOD`: 贪心聚合

#### Step 3: 信号分级过滤

**强信号（任一命中即通过初筛）**：
- `STRONG_1`: 簇内指纹数 ≥ 3 且时间跨度 ≤ 7 天
- `STRONG_2`: 用户在 daily log 中使用过重复意图关键词："每次都"、"又要"、"老流程"等
- `STRONG_3`: 同一 tool_chain 出现 ≥ 2 次且 step_count ≥ 3

**弱信号（累积 ≥ 3 个才通过初筛）**：
- `WEAK_1`: 同一 domain 下簇内指纹 ≥ 2
- `WEAK_2`: tool_chain Jaccard ≥ 0.8 但 intent 不完全匹配
- `WEAK_3`: 相似 output_type + 相似 keywords（≥ 2 个重叠）
- `WEAK_4`: 跨 workspace 出现相似指纹

### 1.3 FTRVO 评估模型

对每个发现的模式，Scout 用 FTRVO 模型自动打分（满分 25 分）。

**F（Frequency）— 时间分布**：

| 14 天内出现次数 | 分数 |
|------|------|
| ≥ 7 次 | 5（几乎每天）|
| ≥ 4 次 | 4（每周多次）|
| ≥ 3 次 | 3（每周一次）|
| 2 次 | 2（偶尔）|
| 1 次 | 1（罕见）|

**T（Trigger）— 触发上下文一致性**：

LLM 分析每个指纹在 daily log 中的前文上下文，判断触发场景一致性，输出 1-5 分。

**R（Reproducibility）— 工具链和步骤一致性**：

```
R_score = round(avg_pairwise_tool_similarity × 3 + step_count_variance_penalty + 2)
```

简化判定：
- 工具序列完全相同 + 步骤数差 ≤ 1 → **5**
- Jaccard ≥ 0.8 + 步骤数差 ≤ 2 → **4**
- Jaccard ≥ 0.5 → **3**
- Jaccard ≥ 0.3 → **2**
- 其余 → **1**

**V（Value）— 操作复杂度 × 产出重要性**：

| 条件 | 分数 |
|------|------|
| step_count ≥ 5 且 output_type ∈ {file, config} | 5 |
| step_count ≥ 3 且 output_type ∈ {file, report, config} | 4 |
| step_count ≥ 3 或 output_type ∈ {file, report} | 3 |
| step_count = 2 且 output_type = command | 2 |
| 仅对话，无实质产物 | 1 |

**O（Output）— 产物类型映射**：

| output_type | 分数 |
|-------------|------|
| file / config | 5 |
| report | 4 |
| command | 3 |
| conversation | 1 |

**沉淀决策**：

| 总分 | 决策 |
|------|------|
| 20-25 | 🟢 强烈建议沉淀，自动进入 Smith |
| 15-19 | 🟡 建议沉淀，展示报告由用户决定 |
| 10-14 | 🔵 继续观察 |
| 5-9 | ⚪ 不沉淀 |

---

## Module 2: Smith（Skill 锻造引擎）

### 2.1 重叠检测算法

```
relevance(pattern, skill) = 0.35 × keyword_overlap
                          + 0.15 × domain_match
                          + 0.25 × trigger_overlap
                          + 0.25 × tool_overlap
```

| relevance | 决策 |
|-----------|------|
| ≥ 0.70 | 合并到已有 Skill |
| 0.40 - 0.69 | 交由用户判断 |
| < 0.40 | 新建 Skill |

### 2.2 生成约束

```yaml
SKILL_NAME_MAX_LENGTH: 30
DESCRIPTION_MAX_LENGTH: 200
MIN_TRIGGER_KEYWORDS: 3
MAX_TRIGGER_KEYWORDS: 10
MIN_WORKFLOW_STEPS: 3
MAX_WORKFLOW_STEPS: 15
MIN_EXAMPLES: 1
MAX_EXAMPLES: 3
MAX_REGEN_ATTEMPTS: 2
READABILITY_THRESHOLD: 0.70
```

### 2.3 质量门禁

| 检查项 | 规则 |
|--------|------|
| 章节完整性 | 所有必须章节都存在 |
| 触发词数量 | 3 ≤ count ≤ 10 |
| 工作流步骤 | 3 ≤ count ≤ 15 |
| 名称冲突 | 不与已有 Skill 重名 |
| frontmatter | YAML 合法、必填字段齐全 |
| 可读性 | LLM 自评 ≥ 0.7 |

---

## Module 3: Sensei（进化导师引擎）

### 3.1 健康度四维模型

#### 使用频率（Usage Frequency）

```
usage_freq = count(skill_mentions_in_daily_logs, last_30_days)
```

| 30 天使用次数 | 分数 |
|------|------|
| ≥ 12 | 5（高频）|
| 8-11 | 4（活跃）|
| 4-7 | 3（正常）|
| 1-3 | 2（低频）|
| 0 | 1（零使用）|

#### 覆盖率（Coverage）

```
coverage = capabilities_used / capabilities_defined
```

| coverage | 分数 |
|----------|------|
| ≥ 0.80 | 5 |
| 0.60-0.79 | 4 |
| 0.40-0.59 | 3 |
| 0.20-0.39 | 2 |
| < 0.20 | 1 |

#### 漂移度（Drift）

```
drift = 1 - (1 - levenshtein(actual, defined) / max(len(actual), len(defined)))
```

| drift | 分数 |
|-------|------|
| ≤ 0.10 | 5 |
| 0.11-0.20 | 4 |
| 0.21-0.35 | 3 |
| 0.36-0.50 | 2 |
| > 0.50 | 1 |

#### 满意度（Satisfaction）

```
satisfaction = clamp(3 + positive_signals - negative_signals, 1, 5)
```

#### 综合健康度

```
health = 0.30 × usage + 0.20 × coverage + 0.25 × drift + 0.25 × satisfaction
```

| health | 等级 |
|--------|------|
| ≥ 4.0 | 🟢 健康 |
| 3.0-3.9 | 🟡 需关注 |
| 2.0-2.9 | 🟠 需优化 |
| < 2.0 | 🔴 僵尸 |

### 3.2 进化决策树

```
health ≥ 4.0 → 🟢 保持（但如果有新模式可合并 → 建议扩展）
health ≥ 3.0 → 🟡 分析最低维度，给出具体建议
health ≥ 2.0 → 🟠 输出 Evolution Proposal（具体修改方案）
health < 2.0 → 🔴 建议归档
```

### 3.3 版本管理

每次修改追踪在 frontmatter changelog 中：

```yaml
changelog:
  - version: 1.2.0
    date: 2026-03-23
    changes: "新增 XXX 能力，来自 SkillForge 模式发现"
```

---

## Data Storage

### 工作目录结构

```
{workspace}/.workbuddy/skillforge/
├── patterns/                    # 模式存档
├── reports/                     # 周度报告
└── skill-health.json            # 健康档案
```

### skill-health.json 示例

```json
{
  "last_scan": "2026-03-23T17:00:00+08:00",
  "scan_count": 4,
  "skills": {
    "project-manager": {
      "version": "1.2.0",
      "last_used": "2026-03-23",
      "metrics": {
        "usage_freq": { "count_30d": 12, "score": 5 },
        "coverage": { "defined": 6, "used": 5, "rate": 0.83, "score": 5 },
        "drift": { "avg_drift": 0.12, "sample_size": 5, "score": 4 },
        "satisfaction": { "positive": 3, "negative": 0, "score": 5 }
      },
      "health_score": 4.75,
      "health_level": "green"
    }
  },
  "pending_patterns": []
}
```
