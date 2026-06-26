---
name: source-router
description: LLM通用来源路由技能。根据任务类型、时间要求和信息缺口，决定优先去哪些来源找信息并给出搜索顺序。支持的来源类型：web/local_file/vector/graph/counter。在已知需要搜索但不知道先搜什么时使用。触发条件：多源搜索决策、搜索成本控制、需要决定是否开启反证搜索。
---

# Source Router — 来源路由技能

## 核心职责

根据任务特征、时间要求和信息缺口，**决定去哪找、先找什么、是否开反证搜索、何时停止**。

**边界（绝对禁止）**：
- ❌ 不执行搜索
- ❌ 不生成最终判断或结论
- ❌ 不自行 invent 新的来源类型

**唯一产出**：搜索路由计划。

---

## 输入规格（最小集）

| 字段 | 必填 | 说明 |
|------|------|------|
| `task_type` | ✅ | 任务类型：`breaking_news` / `deep_research` / `entity_analysis` / `internal_knowledge` / `tech_evaluation` |
| `primary_subject` | ✅ | 核心实体/对象 |
| `goal_mode` | ✅ | 目标模式：`analyze` / `evaluate` / `compare` / `investigate` |
| `freshness_required` | ✅ | 时效性要求：`high`（≤24h）/ `medium`（≤30天）/ `low`（不限） |
| `available_sources` | ✅ | 当前环境可用的来源列表，从 `[web, local_file, vector, graph, counter]` 中选 |
| `need_counter_evidence` | ✅ | 是否需要反面证据搜索：`true` / `false` |

**可选输入**：
| 字段 | 说明 |
|------|------|
| `information_gaps` | 已知信息缺口列表 |
| `budget_limit` | 搜索次数预算上限 |
| `preferred_domains` | 优先域名列表 |

---

## 输出规格（固定结构）

```json
{
  "task_id": "SR-<uuid前8位>",
  "task_type": "...",
  "primary_subject": "...",
  "selected_sources": [
    {
      "source": "web",
      "priority": 1,
      "rationale": "...",
      "search_hints": ["...", "..."]
    }
  ],
  "search_order": ["web", "counter", "graph"],
  "counter_search_enabled": true,
  "counter_trigger": "...",
  "stop_rule": {
    "condition": "...",
    "max_rounds": 3
  },
  "budget_allocation": {
    "total_budget": 10,
    "web": 5,
    "counter": 2,
    "graph": 2,
    "local_file": 1
  },
  "fallback_chain": [
    {
      "level": 1,
      "source": "tavily_search",
      "trigger_fallback": "quota_exhausted | timeout_30s | empty_results",
      "fallback_to": 2
    },
    {
      "level": 2,
      "source": "bailian_web_search",
      "trigger_fallback": "api_error | timeout_30s",
      "fallback_to": 3
    },
    {
      "level": 3,
      "source": "web_search",
      "trigger_fallback": "empty_results | gfw_blocked",
      "fallback_to": 4
    },
    {
      "level": 4,
      "source": "web_fetch_direct",
      "trigger_fallback": null,
      "fallback_to": 5
    },
    {
      "level": 5,
      "source": "local_cache",
      "trigger_fallback": null,
      "fallback_to": null
    }
  ],
  "degradation_log": []
}
```

---

## 5 种来源类型

| 来源 | 说明 | 核心优势 | 局限 |
|------|------|----------|------|
| `web` | 互联网搜索（Tavily/搜索引擎） | 实时性最强，覆盖面最广 | 信源质量参差，有噪音 |
| `local_file` | 本地文件系统（记忆/缓存/文档） | 零成本，已知内容可靠 | 可能过时，覆盖有限 |
| `vector` | 向量数据库/知识库 | 语义检索，历史知识密集 | 需预先索引，不含实时 |
| `graph` | 知识图谱/关系数据库 | 实体关系挖掘，结构化推理 | 建设成本高，覆盖有限 |
| `counter` | 反证搜索（对立观点/质疑信源） | 纠偏，防止确认偏误 | 消耗额外预算 |

---

## 核心路由规则

### 规则 1：时效性 → 来源优先级

```
freshness_required = high  →  web 优先（≥70% 预算）
freshness_required = medium →  web + vector/local_file 混合
freshness_required = low   →  vector/local_file 优先，web 补充
```

### 规则 2：任务类型 → 来源组合

| task_type | 推荐组合 | 说明 |
|-----------|----------|------|
| `breaking_news` | web + counter | 实时性最高，必须反证 |
| `deep_research` | vector + web + graph + counter | 全源深度研究 |
| `entity_analysis` | graph + web + vector | 实体关系为核心 |
| `internal_knowledge` | vector + local_file | 内部知识优先 |
| `tech_evaluation` | web + vector + counter | 技术评估需外部验证 |

### 规则 3：已有材料 → 优先本地

若 `available_sources` 包含 `local_file` 或 `vector`，且任务 subject 在本地有已知相关材料：
- 优先检索本地 → 识别信息缺口 → 仅缺口部分走 web
- 节省预算，减少噪音

### 规则 4：反证搜索触发

**必须开启 counter_search**：
- `need_counter_evidence = true`（显式要求）
- `task_type = evaluate` 或 `investigate`（隐式需要）
- `goal_mode = compare`（对比场景天然需要反面证据）

**可以跳过 counter**：
- `task_type = internal_knowledge` 且目标是纯检索
- `need_counter_evidence = false` 且 budget_limit 极低（≤3）

### 规则 5：stop_rule 自动生成

| 场景 | stop_rule |
|------|-----------|
| 高时效新闻 | "找到3个独立权威信源确认同一事实后停止" |
| 深度研究 | "每类来源至少覆盖2次，或找到10条高质量结果" |
| 实体分析 | "主实体的关系网络 ≥ 5 个节点后停止 graph 搜索" |
| 内部知识 | "本地命中 ≥ 5 条相关文档后停止" |
| 默认 | "总搜索轮数 ≤ 3 轮，或找到3条以上高置信度结果" |

### 规则 6：搜索降级链（Fallback Chain）

当首选搜索源不可用时，按预设降级链自动切换：

```
P1: tavily_search (原生工具，配额1000/月)
  ↓ quota_exhausted / timeout > 30s / empty_results
P2: bailian_web_search (百炼Qwen+，国内零延迟)
  ↓ api_error / timeout > 30s
P3: web_search (Brave API)
  ↓ empty_results / GFW封堵
P4: web_fetch_direct (搜索引擎URL模板直采)
  ↓ 全部失败
P5: local_cache (memory/*_cache.md 本地缓存)
```

**降级执行规则**：
- 每级失败后自动切换至下一级，不需要人工干预
- 每次降级事件记录到 `degradation_log[]`
- 如果 `available_sources` 显式提供，则基于可用源构建降级链（排除不可用源）
- 降级链中最高可用级别作为实际 `selected_sources[0]`

---

## 执行流程

```
输入解析 → 提取 task_type / freshness / available_sources
    → 按规则1-4 确定来源组合和优先级
    → 按 need_counter_evidence 和规则4 决定是否开 counter
    → 按规则5 生成 stop_rule
    → 按 budget_limit 分配预算（默认总预算10次）
    → 输出 JSON
```

---

## 参考文档

- **来源选择详细规则**：[references/source-selection-rules.md](references/source-selection-rules.md)
- **完整输入输出用例**：[references/examples.md](references/examples.md)
