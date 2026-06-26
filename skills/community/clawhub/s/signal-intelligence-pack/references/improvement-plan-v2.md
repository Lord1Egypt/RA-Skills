# Signal Intelligence Pack V2 改进方案

**日期**: 2026-03-26
**基于**: 首次实战测试（AI芯片竞争格局分析）反馈
**核心目标**: 增强步骤间动态反馈能力 + 提升搜索降级韧性

---

## 问题总览

| # | 问题 | 影响等级 | 改进优先级 |
|---|------|---------|-----------|
| P1 | 搜索降级缺乏内建机制 | 高 | P0 |
| P2 | 反证搜索缺乏动态调整 | 中高 | P1 |
| P3 | 时间窗偏差未自动补偿 | 中 | P1 |
| P4 | 步骤间反馈链路断裂 | 中高 | P0 |
| P5 | 置信度缺乏量化评分 | 中低 | P2 |

---

## 改进1: 搜索降级韧性 (P0)

### 现状问题
测试中 Tavily 配额耗尽 → source-router 没有内置降级逻辑 → 完全依赖外部协议手动降级。

### 改进方案: source-router 增加 `fallback_chain` 字段

**修改文件**: `source-router/SKILL.md` + `references/source-selection-rules.md`

#### 新增输出字段

```json
{
  "fallback_chain": [
    {
      "level": 1,
      "source": "tavily_search",
      "trigger_fallback": "quota_exhausted | timeout > 30s | empty_results",
      "fallback_to": 2
    },
    {
      "level": 2,
      "source": "bailian_web_search",
      "trigger_fallback": "api_error | timeout > 30s",
      "fallback_to": 3
    },
    {
      "level": 3,
      "source": "web_search",
      "trigger_fallback": "empty_results",
      "fallback_to": 4
    },
    {
      "level": 4,
      "source": "web_fetch_direct",
      "trigger_fallback": null,
      "fallback_to": null
    }
  ],
  "degradation_log": []
}
```

#### 新增字段说明

| 字段 | 说明 |
|------|------|
| `fallback_chain` | 有序降级链，每级定义触发降级的条件和下一级目标 |
| `trigger_fallback` | 触发条件，用 `|` 分隔多个条件 |
| `degradation_log` | 运行时记录实际降级事件，供审计 |

#### 默认降级链（硬编码参考）

```
P1: tavily_search (原生工具，配额1000/月)
  ↓ quota_exhausted / timeout / empty
P2: bailian_web_search (百炼Qwen+，国内零延迟)
  ↓ api_error / timeout
P3: web_search (Brave，GFW风险)
  ↓ empty / GFW
P4: web_fetch_direct (搜索引擎URL模板)
  ↓ 全部失败
P5: 本地缓存 (memory/*_cache.md)
```

#### source-router 输出规格变更

在现有输出 JSON 中新增 `fallback_chain` 字段。当 `available_sources` 未显式提供时，使用默认降级链。

---

## 改进2: 步骤间动态反馈链路 (P0)

### 现状问题
5步流水线是单向线性：Step 1→2→3→4→5。后置步骤发现的问题无法回传给前置步骤触发补充动作。

### 改进方案: 引入 `feedback_signal` 机制

**修改文件**: `signal-intelligence-pack/SKILL.md` + `references/workflow.md` + `references/stop-rules.md`

#### 核心设计

在每步输出中新增 `feedback_signals[]` 字段，后置步骤可向前置步骤发送反馈信号，触发**单轮回溯**。

```json
{
  "feedback_signals": [
    {
      "signal_type": "gap_detected | stale_found | contradiction_found | coverage_insufficient",
      "target_step": "query-planner | source-router | evidence-cleaner | freshness-judge",
      "action": "append_queries | re_route | re_search | reclassify",
      "payload": {
        "description": "...",
        "suggested_queries": ["...", "..."],
        "affected_dimensions": ["market_share", "geopolitics"]
      }
    }
  ]
}
```

#### 6种反馈信号定义

| 信号 | 触发步骤 | 目标步骤 | 动作 | 示例 |
|------|---------|---------|------|------|
| `gap_detected` | evidence-cleaner | query-planner | 追加查询 | 某维度零命中 → 补充查询重搜 |
| `stale_found` | freshness-judge | source-router | 切换来源 | 核心证据全部 stale → 换高时效来源重搜 |
| `contradiction_found` | evidence-cleaner | counter-evidence-hunter | 提前激活 | 发现强矛盾 → 跳过 freshness 直进反证 |
| `coverage_insufficient` | evidence-cleaner | query-planner | 追加维度 | 覆盖率<50% → 补盲区维度 |
| `new_lead` | evidence-cleaner | source-router | 深挖 | 搜索发现意外高价值方向 → 单独深挖 |
| `counter_gap` | counter-evidence-hunter | query-planner | 追加反证查询 | 反证方向不足 → 追加 counter_queries |

#### 反馈传播流程

```
Step 3 (evidence-cleaner) 发现 gap_detected
    ↓
生成 feedback_signal: {target: "query-planner", action: "append_queries"}
    ↓
编排器收到信号 → 单轮回溯到 Step 1
    ↓
Step 1 追加 2-3 条补充查询
    ↓
Step 2 重新路由补充查询
    ↓
Step 3 重新搜索并清洗（仅补充部分，不重跑已有）
    ↓
继续 Step 4 → Step 5
```

#### 回溯次数限制

**硬性约束**: 整条流水线最多允许 **1次回溯**，防止无限循环。回溯后禁止再次回溯。

```json
{
  "pipeline_metadata": {
    "feedback_loops_executed": 0,
    "max_feedback_loops": 1
  }
}
```

---

## 改进3: 时间窗偏差自动补偿 (P1)

### 现状问题
freshness-judge 识别了"12/15证据集中在3月"的风险，但只标注风险，未触发补偿动作。

### 改进方案: freshness-judge 增加 `compensation_queries`

**修改文件**: `freshness-judge/SKILL.md` + `references/freshness-rules.md`

#### 新增输出字段

```json
{
  "freshness_profile": {
    // ... 现有字段 ...
    "risk_flags": [
      "证据时间分布过于集中（12/15在2026年3月）"
    ],
    "compensation_queries": [
      {
        "query": "AI芯片 2025年Q3 Q4 市场格局变化 NVIDIA AMD",
        "rationale": "补充2025年H2背景数据，平衡时间分布偏差",
        "target_period": "2025-07 至 2025-12",
        "priority": "recommended"
      },
      {
        "query": "AI芯片 产业政策 2025年全年 回顾",
        "rationale": "补充政策时间线背景",
        "target_period": "2025-01 至 2025-12",
        "priority": "optional"
      }
    ]
  }
}
```

#### 自动补偿触发条件

| 条件 | 补偿级别 | 说明 |
|------|---------|------|
| current_ratio > 0.8 且 time_span < 时间窗50% | `recommended` | 证据过度集中在近期，建议补充历史背景 |
| 某维度证据全部为 stale/undated | `required` | 关键维度无新鲜证据，必须补充 |
| background_ratio = 0 且 goal_mode = strategic | `recommended` | 战略分析缺乏背景深度 |
| undated_ratio > 0.3 | `required` | 大量无日期证据，必须尝试补充日期信息 |

---

## 改进4: 反证搜索动态调整 (P1)

### 现状问题
counter-evidence-hunter 的搜索方向完全依赖 query-planner 预设的 counter_queries。如果主线搜索发现意外信息（如某个假设被实际数据直接推翻），无法动态调整反证方向。

### 改进方案: counter-evidence-hunter 支持 `dynamic_queries`

**修改文件**: `counter-evidence-hunter/SKILL.md` + `references/counter-patterns.md`

#### 动态查询生成规则

```
主线搜索结果分析 → 识别"意外发现"(unexpected_findings)
    ↓
意外发现分类:
  A. 主线假设被直接支持（强度异常高）→ 动态生成"极端反面测试查询"
  B. 主线假设出现裂缝（矛盾证据）→ 动态生成"裂缝深挖查询"
  C. 发现全新维度（未预设方向）→ 动态生成"新维度探索查询"
    ↓
动态查询与预设 counter_queries 合并 → 去重 → 执行搜索
```

#### 新增输入字段

```json
{
  "unexpected_findings": [
    {
      "finding": "搜索发现NVIDIA Blackwell延迟交付比例高达30%",
      "finding_type": "assumption_crack",
      "suggested_counter_query": "NVIDIA Blackwell 交付延迟 客户流失 竞争对手替代"
    }
  ]
}
```

#### 新增输出字段

```json
{
  "dynamic_queries": [
    {
      "query": "...",
      "trigger": "assumption_crack | overconfident_signal | new_dimension",
      "origin": "dynamic (unexpected finding)"
    }
  ],
  "all_counter_queries": [
    // 合并后的完整列表（预设 + 动态）
  ]
}
```

---

## 改进5: 量化置信度评分 (P2)

### 现状问题
confidence_assessment 只有 high/medium/low 三级标签，不便于下游模块做阈值判断。

### 改进方案: 引入 0-100 数值化评分

**修改文件**: `counter-evidence-hunter/SKILL.md` + `signal-intelligence-pack/references/input-output.md`

#### 新增评分维度

```json
{
  "confidence_assessment": {
    "overall_score": 72,
    "dimensions": {
      "source_quality": {
        "score": 80,
        "rationale": "S+A级信源占比60%，高于30%门禁"
      },
      "coverage_completeness": {
        "score": 85,
        "rationale": "6/6维度有命中，100%覆盖"
      },
      "freshness_adequacy": {
        "score": 87,
        "rationale": "87%证据为current，但时间分布集中"
      },
      "counter_evidence_sufficiency": {
        "score": 60,
        "rationale": "4条反证中2条hard，但缺初创公司维度"
      },
      "consistency": {
        "score": 70,
        "rationale": "主线证据内部一致，但存在2处需注意的矛盾"
      }
    },
    "mainline_robustness": "medium",
    "blind_spots": ["...", "..."],
    "search_coverage": "adequate"
  }
}
```

#### 评分公式（参考）

```
overall_score = source_quality * 0.25
              + coverage_completeness * 0.20
              + freshness_adequacy * 0.20
              + counter_evidence_sufficiency * 0.20
              + consistency * 0.15
```

#### 阈值参考

| 分段 | 含义 | 建议动作 |
|------|------|---------|
| 80-100 | 高置信度 | 可直接进入下游分析 |
| 60-79 | 中等置信度 | 建议关注扣分维度，选择性补搜 |
| 40-59 | 低置信度 | 强烈建议回溯补充后重跑 |
| 0-39 | 不可用 | 放弃当前证据底座，重新规划搜索 |

---

## 实施计划

### Phase 1: 核心改动（P0，立即执行）

| 文件 | 改动内容 | 工作量 |
|------|---------|--------|
| `source-router/SKILL.md` | 新增 `fallback_chain` 字段和默认降级链 | 中 |
| `source-router/references/source-selection-rules.md` | 新增降级链规则章节 | 小 |
| `signal-intelligence-pack/SKILL.md` | 新增 feedback_signal 机制说明 | 中 |
| `signal-intelligence-pack/references/workflow.md` | 新增反馈传播流程图 | 中 |
| `signal-intelligence-pack/references/stop-rules.md` | 新增回溯次数限制规则 | 小 |

### Phase 2: 增强改动（P1，72小时内）

| 文件 | 改动内容 | 工作量 |
|------|---------|--------|
| `freshness-judge/SKILL.md` | 新增 `compensation_queries` 输出 | 中 |
| `freshness-judge/references/freshness-rules.md` | 新增补偿触发条件表 | 小 |
| `counter-evidence-hunter/SKILL.md` | 新增 `dynamic_queries` + `unexpected_findings` | 中 |
| `counter-evidence-hunter/references/counter-patterns.md` | 新增动态查询生成规则 | 小 |

### Phase 3: 完善改动（P2，本周内）

| 文件 | 改动内容 | 工作量 |
|------|---------|--------|
| `counter-evidence-hunter/SKILL.md` | 置信度从三级改数值化 | 小 |
| `signal-intelligence-pack/references/input-output.md` | 新增 confidence_assessment 完整schema | 小 |

---

## 改进后预期效果

| 改进项 | 改进前 | 改进后 |
|--------|--------|--------|
| 搜索降级 | 手动感知 + 外部协议 | source-router 内建 fallback_chain，自动降级 |
| 步骤反馈 | 单向线性，无回传 | feedback_signal 单轮回溯机制 |
| 时间偏差 | 仅标注风险 | 自动生成补偿查询建议 |
| 反证动态性 | 仅依赖预设查询 | 支持基于意外发现的动态查询 |
| 置信度 | high/medium/low | 5维度 0-100 数值化评分 |
| **预期整体评分** | **7.5/10** | **8.5-9.0/10** |

---

## V2 数据流全景图

```
                    ┌─────────────────────────────────┐
                    │     Unified Input (JSON)         │
                    └──────────────┬──────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────┐
│ Step 1: query-planner                                        │
│ → 4类查询生成 + counter_queries ≥ 2                          │
│ ← feedback: gap_detected → 追加查询                          │
└──────────────────────────────┬───────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│ Step 2: source-router                                         │
│ → 来源选择 + fallback_chain (自动降级)                        │
│ ← feedback: stale_found → 切换来源                           │
└──────────────────────────────┬───────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│ Step 3: evidence-cleaner                                      │
│ → 清洗 + 信源评级 + 覆盖率报告                                │
│ → 发出 feedback_signals (gap/contradiction/new_lead)          │
└──────────────────────────────┬───────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│ Step 4: freshness-judge                                       │
│ → 5级分类 + compensation_queries (自动补偿建议)                │
│ → 发出 feedback_signals (stale_found)                         │
└──────────────────────────────┬───────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│ Step 5: counter-evidence-hunter                               │
│ → 反证搜索 + dynamic_queries (基于意外发现)                    │
│ → flip_conditions + 量化置信度评分 (0-100)                     │
└──────────────────────────────┬───────────────────────────────┘
                               ↓
                    ┌─────────────────────────────────┐
                    │  Enhanced Evidence Base V2       │
                    │  + feedback_log                  │
                    │  + degradation_log               │
                    │  + confidence_score (0-100)      │
                    └─────────────────────────────────┘
```
