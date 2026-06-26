---
name: true-seeing
description: 审核 AI 生成文章中的可验证事实，通过 web search 逐条校验，输出差异报告并支持用户审批替换。当用户需要事实核查、验证文章准确性、检查数据日期金额是否正确、去除 AI 幻觉内容、或 fact-check 一篇文章时使用。触发于"事实核查"、"验一下这些数据"、"检查事实"、"去幻觉"、"fact check"、"核实文章"、"核实这段话"、"帮我对一下数据"、"这篇文章里的数字对不对"。不适用于语法纠错、翻译校对、纯观点验证、文风调整。
---

# True Seeing — AI 文章去幻觉校验

## 目的

识别文章中的可验证事实性陈述，通过 web search 逐条校验，输出差异报告供用户审批后替换。适用于 AI 生成内容的去幻觉化处理。

## Pipeline 架构

```
[article] → Stage 1: extract → fact_list → Stage 2: verify → report → 🛑 用户审批 → Stage 3: replace → corrected article
```

三个阶段支持独立调用（`stage` 参数）或全流程顺序执行（默认）。

**`stage=full` 模式的执行流程：**
1. 执行 Stage 1 → 输出 fact_list
2. 执行 Stage 2 → 输出 verification_report
3. **暂停。向用户呈现差异报告，等待用户回复 user_selections。**
4. 收到 user_selections 后执行 Stage 3 → 输出修正文章

Stage 2 完成后必须暂停等待用户审批，不得自动进入 Stage 3。

## 输入参数

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| article | string | 是 | 待核查的文章全文或文件路径 |
| stage | enum | 否 | `extract` / `verify` / `replace` / `full`（默认 `full`） |
| fact_list | JSON | 条件必需 | `stage=verify` 时必需；Stage 1 的输出 |
| verification_report | JSON | 条件必需 | `stage=replace` 时必需；Stage 2 的输出 |
| user_selections | list[int] | 条件必需 | `stage=replace` 时必需；用户选择替换的有分歧事实编号 |

## 数据契约

### fact_list（Stage 1 输出 → Stage 2 输入）

```json
{
  "article_summary": "文章主题一句话概括",
  "total_facts": 5,
  "facts": [
    {
      "id": 1,
      "category": "funding",
      "original_text": "XXX公司于2025年3月完成B轮融资5亿元",
      "position": "第2段第3句",
      "search_query": "XXX公司 B轮融资 2025年3月 金额"
    }
  ]
}
```

### verification_report（Stage 2 输出 → Stage 3 输入）

```json
{
  "summary": { "total": 5, "verified": 3, "corrected": 1, "remain": 1 },
  "verified": [
    {
      "id": 1,
      "original_text": "原文描述",
      "source_url": "https://...",
      "source_snippet": "网页上的对应描述"
    }
  ],
  "corrected": [
    {
      "id": 2,
      "original_text": "原文描述",
      "actual_fact": "实际查找到的信息",
      "source_url": "https://...",
      "source_snippet": "网页上的对应描述",
      "divergence_type": "number_mismatch | date_mismatch | event_nonexistent | entity_mismatch"
    }
  ],
  "remain": [
    {
      "id": 3,
      "original_text": "原文描述",
      "search_queries_tried": ["query1", "query2"],
      "note": "未找到可验证的搜索结果"
    }
  ]
}
```

---

## Stage 1: Extract（事实抽取）

### 输入
- `article`：文章全文

### 执行步骤

1. **通读全文**，逐段扫描。

2. **按 `references/fact-extraction-rules.md` 中的分类规则**，标记每一条可验证的事实性陈述。
   - 跳过：观点、推测、评价、定性描述（如"市场前景广阔"）。
   - 标记：包含具体数字、日期、金额、事件名称、人物+动作的陈述。

3. **对每条标记事实**，记录：
   - `id`：自增编号，从 1 开始
   - `category`：分类标签（funding / pricing / date / event / statistic / personnel / product / other）
   - `original_text`：原文中的完整句子或分句
   - `position`：段落+句子位置描述
   - `search_query`：转化为适合 web search 的关键词查询（去掉虚词，保留实体+关键信息）

4. **批量上限检查**：如果标记事实数量超过 30 条，仅保留前 30 条，在输出中附注"发现 N 条事实，已截取前 30 条。如需继续，请将剩余部分作为新输入。"。

5. **输出 `fact_list` JSON**。

6. **质量自检**：
   - 每条事实都有 id、category、original_text、position、search_query。
   - search_query 不包含虚词和上下文依赖词。
   - 总数 ≤ 30。

### 停止条件
- 文章为空或不含可验证事实 → 输出空 fact_list，附注"未发现可验证事实"。
- 事实数量超过 30 条 → 截取前 30 条，附注截取说明。

### search_query 构造规则
- 提取核心实体（公司名、人名、产品名）
- 保留关键数值和日期
- 去掉修饰词和上下文依赖词
- 如有歧义，生成 2 个备选查询（用 `|` 分隔）

---

## Stage 2: Verify（事实校验）

### 输入
- `fact_list`：Stage 1 输出的 JSON

### 事实状态机

每条事实在处理过程中有以下状态：

| 状态 | 含义 |
|------|------|
| `Unverified` | 初始状态，待处理 |
| `keywords-generated` | 已生成检索词，待搜索 |
| `fact-fetch` | 已获取搜索结果，待比对 |
| `Verified` | 终态：内容无误 |
| `Corrected` | 终态：内容已修正 |
| `Remain` | 终态：保持不变（无法验证或用户选择保留） |

状态转换规则：

```
Unverified ──(生成检索词成功)──→ keywords-generated
Unverified ──(生成检索词失败)──→ 留在 Unverified，回到大池子

keywords-generated ──(搜索成功)──→ fact-fetch
keywords-generated ──(搜索失败)──→ 留在 keywords-generated，等当前批次步骤 5 重试

fact-fetch ──(比对：内容无误)──→ Verified
fact-fetch ──(比对：内容有差异)──→ Corrected
fact-fetch ──(比对：结果模糊/无法判定)──→ Remain
```

### 执行步骤

1. **前置检查**：执行一次 `web_search`，查询 `"test"`，确认 Brave Search 可用。
   - 成功 → 继续。
   - 失败 → **abort**，向用户输出错误信息："web_search (Brave) 当前不可用，无法执行事实校验。建议过一段时间再试。"，流程终止。

2. **初始化**：将 fact_list 中所有事实放入 `unverified_pool`（大池子），创建空的 `done_pool`（已完成池）。

3. **进入循环**（最多 5 轮）：

   **3a.** 从 `unverified_pool` 中捞出最多 5 条 Unverified 事实，形成当前批次的 `batch_pool`（小池子）。如果 `unverified_pool` 为空，跳到步骤 4。

   **3b.** 对 `batch_pool` 中的每条事实，按 `references/search-query-templates.md` 生成检索词：
   - 成功 → 状态变为 `keywords-generated`。
   - 失败 → 状态保持 `Unverified`，移出 `batch_pool`，放回 `unverified_pool`（大池子）。

   **3c.** 对 `batch_pool` 中所有 `keywords-generated` 的事实，使用 `sessions_spawn` 启动 sub-agent 并行搜索：
   - 每个 sub-agent 执行 `web_search`，取前 3 条结果用 `web_fetch` 抓取内容。
   - 搜索返回 ≥1 条包含原文实体的结果 → 状态变为 `fact-fetch`。
   - 搜索返回 0 条包含原文实体的结果，或工具返回错误 → 状态保持 `keywords-generated`，留在 `batch_pool`。

   **3d.** 对 `batch_pool` 中所有 `fact-fetch` 的事实，按 `references/verification-criteria.md` 逐要素比对：
   - 所有要素一致 → 状态变为 `Verified`。
   - 有关键要素不一致 → 状态变为 `Corrected`，记录 actual_fact + source_url + divergence_type。
   - 搜索结果与原文的实体/数值/日期无直接对应关系 → 状态变为 `Remain`，附注原因。

   **3e.** 对 `batch_pool` 中仍然停留在 `keywords-generated` 的事实（搜索失败的），换策略重搜一次：
   - 换策略规则：换用英文查询 / 去掉数值只搜实体+事件 / 扩大时间范围（按 `references/search-query-templates.md` 重试策略）。
   - 成功 → 回到步骤 3d 处理。
   - 失败 → 状态变为 `Remain`，附注"搜索重试失败"。

   **3f.** 当前批次处理完毕：
   - `batch_pool` 中已达终态（Verified / Corrected / Remain）的事实 → 移入 `done_pool`。
   - `batch_pool` 中仍有未达终态的事实 → 放回 `unverified_pool`。

   **3g.** 检查 `unverified_pool` 是否为空。空 → 跳到步骤 4。非空 → 回到 3a 开始下一轮。

4. **循环结束**：
   - 循环 5 轮后 `unverified_pool` 中仍有 Unverified 事实 → 全部标记为 `Remain`，附注"超过最大轮次（5轮）仍未验证"，移入 `done_pool`。
   - 合并 `done_pool` 中所有事实，输出 `verification_report` JSON。

5. **质量自检**：
   - Verified 事实都有 source_url。
   - Corrected 事实都有 actual_fact + source_url + divergence_type。
   - Remain 事实都有 search_queries_tried + note。
   - 无事实停留在中间状态（Unverified / keywords-generated / fact-fetch）。

### 并行处理规则
- 步骤 3c 中，当前批次内所有 `keywords-generated` 的事实同时启动 sub-agent 搜索，不逐条等待。
- 每个 sub-agent 内部保持搜索节流（间隔 ≥ 2 秒）。
- 单个 sub-agent 最多使用 2 个搜索查询 + 3 次 web_fetch。
- 如果 sub-agent 执行失败，该条事实状态保持 `keywords-generated`，等步骤 3e 重试。

### 停止条件
- 前置检查 web_search 不可用 → abort，向用户报错。
- 搜索结果全部为 429 → 当前批次暂停，已完成的批次结果保留，未完成的标记为 Remain 附注"因 rate limit 中断"。
- 循环 5 轮结束 → 兜底，剩余 Unverified 标记 Remain。

---

## Stage 3: Replace（审批 + 替换）

### 输入
- `article`：原文
- `verification_report`：Stage 2 输出的 JSON
- `user_selections`：用户选择替换的有分歧事实编号列表

### 执行步骤

1. **呈现差异报告**，格式如下：

```markdown
# 事实核查报告

## 有分歧的事实（Corrected）

| 编号 | 原文事实 | 实际查找到的事实 | 出处 |
|------|---------|----------------|------|
| {id} | "{original_text}" | "{actual_fact}" | [来源]({source_url}) |

## 无分歧的事实（Verified）

| 编号 | 原文事实 | 佐证出处 |
|------|---------|----------|
| {id} | "{original_text}" | [来源]({source_url}) |

## 未能验证的事实（Remain）

| 编号 | 原文事实 | 备注 |
|------|---------|------|
| {id} | "{original_text}" | {note} |
```

2. **等待用户回复**，格式为：用户给出「有分歧的事实」表格中的编号（如 `2, 5`）。空回复或不修改 → 输出原文不变，流程结束。

3. **根据 user_selections 执行替换**：
   - 在原文中定位对应编号的 `original_text`
   - 替换为 `actual_fact`
   - 在替换处追加 citation 标记 `[^fc-{id}]`（如 `[^fc-2]`），使用 `fc-` 前缀避免与原文已有脚注编号冲突
   - 在文末追加参考来源列表

4. **输出修正后的文章**，文末附：

```markdown
---

## 参考来源

- [^fc-1] {source_url} — {source_snippet 摘要}
- [^fc-2] {source_url} — {source_snippet 摘要}
...
```

5. **质量自检**：
   - 替换后的文章保持原文结构，仅修改事实部分。
   - citation 编号 `[^fc-{id}]` 与参考来源一一对应。
   - 用户未选择的事实保持原样未修改。

### 替换规则
- 替换时保持原文句式结构，只替换有差异的事实部分，不重写整句。
- 如果用户选择的编号包含 Remain 状态的事实，提示用户该事实无法验证，确认是否仍要保留原文。

---

## 故障处理

| 故障场景 | 行为 |
|---------|------|
| 文章为空 | 输出错误信息："文章内容为空，无法执行事实核查" |
| fact_list 为空 | 输出："未发现可验证事实"，流程结束 |
| web_search 不可用 | abort，输出错误信息：“web_search (Brave) 当前不可用，无法执行事实校验。建议过一段时间再试。” |
| 搜索结果全部 429 | 输出已完成部分，标记中断位置 |
| 原文找不到对应位置 | 跳过该条替换，在输出中标注"原文未找到匹配位置" |
| 用户选择的编号不存在 | 提示"编号 X 不在差异列表中"，忽略无效编号 |

## 质量门槛

执行完成后自检：

- [ ] 每条事实都有明确的分类和编号
- [ ] Verified 事实都有 source_url
- [ ] Corrected 事实都有 actual_fact + source_url + divergence_type
- [ ] Remain 事实都有 search_queries_tried + note
- [ ] 替换后的文章保持原文结构，仅修改事实部分
- [ ] citation 编号与参考来源一一对应
- [ ] 用户未选择的事实保持原样未修改

## 范围边界

**做：** 校验文章中的可验证事实性陈述（数据、日期、金额、事件等）。
**不做：** 语法纠错、观点验证、逻辑推理验证、翻译质量检查。
**移交：** 如果文章需要专业领域事实核查（法律条文、医学数据），提示用户建议由领域专家复核。
