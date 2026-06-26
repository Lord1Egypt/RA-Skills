# 5步串联工作流

## 数据流总览

```
                    ┌─────────────────────────────────┐
                    │     Unified Input (JSON)         │
                    │  primary_task + subject + time   │
                    │  goal_mode + target_variable     │
                    └──────────────┬──────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────┐
│ Step 1: query-planner                                        │
│                                                              │
│ 输入: primary_task, primary_subject, goal_mode               │
│ 处理: 问题拆解 → 维度映射 → 查询生成 → 反证方向              │
│ 输出: planned_queries[], counter_queries[]                   │
└──────────────────────────────┬───────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│ Step 2: source-router                                         │
│                                                              │
│ 输入: planned_queries[], counter_queries[], available_sources │
│ 处理: 查询分类 → 来源匹配 → 优先级排序 → 路由分配            │
│ 输出: routed_queries[{query, source, priority, method}]      │
└──────────────────────────────┬───────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│ Step 3: evidence-cleaner                                      │
│                                                              │
│ 输入: routed_queries[], raw_search_results                   │
│ 处理: 去重 → 信源评级 → 相关性过滤 → 结构化提取              │
│ 输出: cleaned_evidence[], coverage_report                     │
└──────────────────────────────┬───────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│ Step 4: freshness-judge                                       │
│                                                              │
│ 输入: cleaned_evidence[], canonical_time_frame                │
│ 处理: 时间戳解析 → 新鲜度评级 → 过时预警 → 时效冲突检测      │
│ 输出: dated_evidence[], freshness_report, staleness_warnings[]│
└──────────────────────────────┬───────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│ Step 5: counter-evidence-hunter                               │
│                                                              │
│ 输入: dated_evidence[], mainline_synthesis, counter_queries  │
│ 处理: 反证搜索 → 强度评级 → 翻转条件 → 替代路径              │
│ 输出: counter_evidence[], flip_conditions[], alt_supports[]   │
└──────────────────────────────┬───────────────────────────────┘
                               ↓
                    ┌─────────────────────────────────┐
                    │  Enhanced Evidence Base (JSON)   │
                    │  包含全部5步的产出                │
                    └─────────────────────────────────┘
```

---

## 各步详细逻辑

### Step 1: query-planner

**输入**: primary_task, primary_subject, goal_mode

**处理逻辑**:
1. **问题拆解**: 将 primary_task 分解为 3-7 个独立的子问题维度
2. **维度映射**: 每个子问题映射到搜索空间中的可查询实体
3. **查询生成**: 为每个维度生成 1-3 条精确搜索查询（复合关键词）
4. **反证方向**: 为每个核心维度设计至少 1 条反向查询
5. **输出格式化**: 结构化为 planned_queries[] 和 counter_queries[]

**输出传递给 Step 2**: 全部查询列表（含正反方向）

---

### Step 2: source-router

**输入**: planned_queries[], counter_queries[], available_sources

**处理逻辑**:
1. **查询分类**: 根据查询主题标签（科技/金融/政策/学术/舆论等）
2. **来源匹配**: 每类查询匹配最合适的来源
3. **优先级排序**: 一手权威源 > 深度分析 > 快讯 > 社区讨论
4. **路由分配**: 为每条查询分配具体来源和搜索方法

**输出传递给 Step 3**: routed_queries[]（每条含query + source + priority + method）

---

### Step 3: evidence-cleaner

**输入**: routed_queries[]，执行搜索后获得 raw_search_results

**处理逻辑**:
1. **去重**: 基于内容相似度（非URL）去除重复条目
2. **信源评级**: S(一手权威) / A(深度分析) / B(快讯) / C(农场号)
3. **相关性过滤**: 与 primary_subject 的相关性评分，低于阈值的标记为弱相关
4. **结构化提取**: 从每条结果中提取核心信息、来源URL、时间戳
5. **覆盖率报告**: 统计各维度查询的命中情况

**输出传递给 Step 4**: cleaned_evidence[]（含信源评级 + 相关性评分） + coverage_report

---

### Step 4: freshness-judge

**输入**: cleaned_evidence[], canonical_time_frame

**处理逻辑**:
1. **时间戳解析**: 提取每条证据的发布/更新时间
2. **新鲜度评级**:
   - 🟢 Fresh: 在 canonical_time_frame 内
   - 🟡 Aging: 在时间窗之外但仍在合理范围内（1-3个月）
   - 🔴 Stale: 显著过时（>3个月），结论可能已变化
3. **过时预警**: 对 🔴 Stale 证据生成具体警告
4. **时效冲突检测**: 同一维度的证据时间戳冲突时，标注矛盾并建议优先采信方向

**输出传递给 Step 5**: dated_evidence[]（含新鲜度标签） + freshness_report + staleness_warnings[]

---

### Step 5: counter-evidence-hunter

**输入**: dated_evidence[], 从 Step 1 传入的 counter_queries[], 以及基于全部证据提取的 mainline_synthesis（主线叙事摘要）

**处理逻辑**:
1. **主线提取**: 从全部证据中归纳出当前证据集支持的主线叙事
2. **反证搜索**: 对 counter_queries 执行搜索
3. **强度评级**: hard / soft / noise
4. **翻转条件提炼**: 从有效反证中提取结构化翻转条件
5. **替代路径识别**: 找出能解释同一现象的替代解释

**最终输出**: counter_evidence[], flip_conditions[], alternative_supports[], confidence_assessment

---

## 异常处理：降级策略

| 异常场景 | 降级策略 |
|---------|---------|
| Step 1 某维度无查询可生成 | 标注为"维度盲区"，不阻塞后续步骤 |
| Step 2 无可用来源匹配 | 降级到通用搜索源（tavily/web_search），标注"来源未优化" |
| Step 3 搜索返回空结果 | 标注为"维度零命中"，建议扩大搜索范围或调整关键词 |
| Step 4 证据全部无时间戳 | 标注"新鲜度无法评估"，整体降级为"Aging"处理 |
| Step 5 未发现任何反证 | 明确声明"未发现有效反证" + 搜索范围评估，不编造反证 |
| 任一步骤崩溃/超时 | 记录错误，使用已有产出继续流水线，最终输出标注"步骤X降级执行" |

---

## 动态反馈传播

### 反馈信号格式

每步输出可包含 `feedback_signals[]`：

```json
{
  "feedback_signals": [
    {
      "signal_type": "gap_detected",
      "target_step": "query-planner",
      "action": "append_queries",
      "payload": {
        "description": "market_capitalization维度零命中",
        "suggested_queries": ["AI芯片 市值 估值 2025 2026"],
        "affected_dimensions": ["market_capitalization"]
      }
    }
  ]
}
```

### 反馈传播示例

**场景：evidence-cleaner发现维度盲区**

```
Step 3 (evidence-cleaner) 清洗完成
    ↓
发现 coverage_report 中 market_capitalization 维度命中数 = 0
    ↓
生成 feedback_signal: {
  signal_type: "gap_detected",
  target_step: "query-planner",
  action: "append_queries",
  payload: { suggested_queries: [...] }
}
    ↓
编排器检测到信号 → 检查 feedback_loops_executed < max (0 < 1) ✓
    ↓
feedback_loops_executed = 1
    ↓
回溯到 Step 1: query-planner 追加 2-3 条补充查询
    ↓
Step 2: source-router 仅路由新增查询
    ↓
Step 3: evidence-cleaner 合并新搜索结果（不重跑已有）
    ↓
继续 Step 4 → Step 5（不再触发回溯）
```

### 回溯次数保护

```python
# 伪代码
if feedback_signal_detected:
    if pipeline_metadata.feedback_loops_executed < pipeline_metadata.max_feedback_loops:
        execute_backtrack(feedback_signal)
        pipeline_metadata.feedback_loops_executed += 1
    else:
        log("回溯已达上限，忽略反馈信号")
        continue_pipeline()
```

### 信号降级为待办（Deferred Action）

当反馈信号被检测但因外部约束无法执行回溯时（如搜索配额耗尽、时间预算耗尽），信号不丢弃，而是降级为待办项写入最终输出。

**触发条件**：
- feedback_signal 已检测（signal_type 有效）
- 但 `feedback_loops_executed >= max_feedback_loops`（回溯次数已满）
- 或搜索预算 `total_search_calls >= budget_limit`（预算耗尽）

**降级逻辑**：
```
if signal_detected AND cannot_execute_backtrack:
    add to pending_actions[]:
    {
      "signal_type": "gap_detected",
      "target_step": "query-planner",
      "action": "append_queries",
      "priority": "recommended",
      "reason_deferred": "搜索配额耗尽，回溯预算不足",
      "suggested_queries": ["...", "..."]
    }
```

**pending_actions 输出位置**：pipeline_metadata.pending_actions[]

**下游消费**：
- 编排器/人类操作者可在后续批次中按优先级逐项执行 pending_actions
- 当 confidence_assessment.overall_score < 60 时，强制建议优先执行所有 required 级 pending_actions
