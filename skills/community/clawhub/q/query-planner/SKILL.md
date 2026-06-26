---
name: query-planner
description: LLM通用查询规划技能。将复杂任务拆解为4类标准查询(identity/event/action/counter)。在需要联网搜索、多步分析、反证检索前使用。触发条件：任务依赖外部信息、需要拆解复杂问题、需要统一query结构供下游消费。
---

# Query Planner — 查询规划技能

## 核心职责

将任意复杂任务拆解为 **4 类标准查询**，交付给下游搜索/分析模块消费。

**边界（绝对禁止）**：
- ❌ 不执行搜索
- ❌ 不判断真假
- ❌ 不输出结论或建议
- ❌ 不发明第 5 类 query 分类
- ❌ 不遗漏 counter_queries

**唯一产出**：结构化查询计划。

---

## 输入规格（最小集）

| 字段 | 必填 | 说明 |
|------|------|------|
| `primary_task` | ✅ | 用户原始任务的一句话描述 |
| `primary_subject` | ✅ | 核心实体/对象（人/组织/技术/事件） |
| `canonical_time_frame` | ❌ | 时间范围，如 `2024-2025`、`过去30天`、`null` |
| `goal_mode` | ✅ | 目标模式：`analyze`（分析）\|`evaluate`（评估）\|`compare`（对比）\|`investigate`（调查） |
| `target_variable` | ❌ | 需要量化/测量的变量，如 "市场份额"、"出口额"、"准确率" |

---

## 输出规格（固定结构）

```json
{
  "task_id": "QP-<uuid前8位>",
  "primary_subject": "...",
  "time_frame": "...或null",
  "goal_mode": "...",
  "target_variable": "...或null",
  "identity_queries": [...],
  "event_queries": [...],
  "action_queries": [...],
  "counter_queries": [...]
}
```

每条 query 为字符串，可直接作为搜索关键词使用。

---

## 4 类查询生成规则

### 1. identity_queries — "谁/什么"

定义主对象的身份、背景、属性、分类。

- **核心问题**：主对象是什么？它的关键属性和定位是什么？
- **模板**：`"{subject} 是什么"`, `"{subject} 背景 历史"`, `"{subject} 核心特征 属性"`
- **数量**：2–5 条
- **约束**：围绕主对象生成，不发散到无关实体

### 2. event_queries — "发生了什么"

定义与主对象相关的关键事件、时间线、数据点、因果关系。

- **核心问题**：发生了什么？什么时候？有什么数据和趋势？
- **模板**：`"{subject} {time_frame} 重大事件 里程碑"`, `"{subject} {time_frame} 数据 统计 趋势"`, `"{subject} {time_frame} 因果关系 影响"`
- **数量**：3–8 条
- **约束**：有 `time_frame` 则必须绑定；有 `target_variable` 则必须纳入至少 1 条

### 3. action_queries — "做了什么/该做什么"

定义决策、政策、干预措施、战略动作。

- **核心问题**：相关方采取了什么行动？有哪些政策和策略？
- **模板**：`"{subject} 政策 战略 决策"`, `"{subject} 干预措施 行动计划"`, `"{subject} 行业对标 竞争对手策略"`
- **数量**：2–6 条
- **约束**：有 `target_variable` 则纳入至少 1 条测量维度

### 4. counter_queries — "反面证据"

质疑主线叙事，寻找冲突数据、替代解释、被忽略的视角。

- **核心问题**：有没有反面证据？主流观点可能错在哪里？有没有被忽略的因素？
- **模板**：`"{subject} 反面证据 批评 争议"`, `"{subject} 替代解释 不同观点"`, `"{subject} 失败案例 负面数据"`, `"{subject} 数据造假 质疑"`
- **数量**：**2–5 条，绝对不为空**
- **约束**：即使主任务是正面评估，也必须生成反面查询

---

## 强制规则

1. **counter_queries 零容忍**：输出中 `counter_queries` 数组长度必须 ≥ 2。违反即视为输出失败。
2. **分类锁定**：只有 identity / event / action / counter 四类。禁止自定义新分类。
3. **主对象聚焦**：默认所有 query 围绕 `primary_subject` 生成。只有 action_queries 可合理扩展到相关方。
4. **时间绑定**：若 `canonical_time_frame` 非 null，event_queries 和 action_queries 中 ≥ 50% 的 query 必须包含时间关键词。
5. **变量渗透**：若 `target_variable` 非 null，它必须出现在 event_queries 和 action_queries 中（至少各 1 条）。
6. **query 可搜索性**：每条 query 必须是可直接复制到搜索引擎的关键词短语，非自然语言长句。
7. **去重**：同一输出内不允许语义重复的 query。

---

## 执行流程

```
输入解析 → 提取 primary_subject/time_frame/target_variable
    → 按 4 类规则分别生成 query
    → 检查强制约束（counter≥2, 分类锁定, 时间绑定, 变量渗透）
    → 输出 JSON
```

---

## 参考文档

- **查询模式详细规则与模板**：[references/query-patterns.md](references/query-patterns.md)
- **完整输入输出用例**：[references/examples.md](references/examples.md)
