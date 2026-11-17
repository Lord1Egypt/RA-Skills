# Pass 1: Analyze — 理解 Prompt

**加载时机：** 📍 执行到 Pass 1 时加载。
**输入来源：** 若 Pass I Ingestion 执行过，本 Pass 的输入是其产出的 `structured_content`（标准化文本），需额外关注来源溯源与证据等级。若未执行 Ingestion，输入为用户原始 Prompt。

---

## 执行步骤

### Step 1.1 — Prompt Summary

用一句话概括 Prompt 的核心功能。不照搬原文，用自己的话重述。

### Step 1.2 — Goal Extraction

区分 Prompt"说的"和"真正需要的"：
- **说的：** Prompt 字面要求做什么
- **真正需要的：** 这个能力长期来看应该解决什么问题

### Step 1.3 — Input/Output Spec

| 字段 | 如何确定 |
|------|---------|
| input | Prompt 接收什么？用户输入？文件？API 响应？结构化内容？ |
| output | Prompt 产出什么？文本？JSON？文件？结构化报告？ |

如果 Prompt 没有明确说明，从上下文推断并标注为 `inferred`。

**多源输入识别（v2.0）：** 若 Pass I 执行过（IR 含 `pass_ingestion` 字段），`input_spec.type` 设为 `structured_content`，并在 description 中注明原始来源类型（如"来自 PDF 规范文档的结构化内容"）。同时检查 `pass_ingestion.extraction_warnings`，若存在 critical 警告，在 `hidden_assumptions` 中记录"输入内容可能不完整"。

### Step 1.4 — Capability Hints

快速扫描 Prompt 中暗示的能力关键词：

```
决策类：decision, choose, recommend, 判断, 推荐, 决策
规划类：plan, strategy, roadmap, 规划, 策略, 路线图
写作类：write, draft, compose, 写, 起草, 撰写
审查类：review, audit, check, 审查, 检查, 审核
研究类：research, investigate, search, 调研, 搜索, 调查
分析类：analyze, assess, evaluate, 分析, 评估
编码类：code, implement, debug, 编码, 实现, 调试
推理类：reason, infer, deduce, 推理, 推断
模拟类：simulate, model, predict, 模拟, 建模, 预测
评估类：score, rate, benchmark, 评分, 打分, 基准
分类类：classify, categorize, sort, 分类, 归类
排名类：rank, prioritize, 排序, 优先级
```

记录命中的关键词，传给 Pass 2 做深度抽取。

### Step 1.5 — Boundary Definition

明确 Skill 的边界——**不处理什么**：

1. Prompt 中暗示但不应包含的场景
2. 与其他 Skill 的职责划分
3. 用户可能误用的方向

### Step 1.6 — Hidden Assumptions

Prompt 中隐含但未明说的前提：

- 隐含的角色假设（"你是专家" → 需要领域知识）
- 隐含的格式假设（"输出报告" → 需要模板）
- 隐含的质量假设（"高质量" → 需要评分标准）

### Step 1.7 — Unknowns

需要向用户澄清的问题。**最多问 3 个**，只问能改变架构设计的：

- 不确定的核心目标？
- 不确定的使用频率（影响 archetype）？
- 不确定的输出消费者（影响输出格式）？

### Step 1.8 — Meta-Reflection Checkpoint（v2.1）

在进入 Pass 2 之前，用以下 4 个维度二次审视刚才的分析结论。Quick 模式跳过此步。

📍 完整框架见 [meta-reflection.md](meta-reflection.md)

| 维度 | 自检问题 | 触发条件 |
|------|---------|---------|
| D1 问题定义 | `prompt_goal.actual` 是否比 `stated` 更深一层？有没有更好的问题表述？ | 总是 |
| D2 假设 | `hidden_assumptions` 中是否有"假设用户会正确使用"？最脆弱的假设如果错了，哪些结论崩塌？ | hidden_assumptions 非空 |
| D7 目标 | 是否为了降低 token 消耗而在牺牲 skill 的准确度？最终产出对用户真的可用吗？ | 总是 |
| D8 不确定性 | `unknowns` 之外是否还有未记录的不确定点？如果只能向用户确认一件事，是什么？ | 总是 |

**输出：** 将自省结果追加到 `unknowns`（如有新发现的不确定点）或写入 trace。不阻塞 Decision Gate。

---

## Output Schema

```json
{
  "prompt_summary": "一句话，不照搬原文",
  "prompt_goal": {
    "stated": "字面目标",
    "actual": "真正需要的能力"
  },
  "input_spec": {
    "type": "string | structured_content | file | api | mixed",
    "description": "输入描述",
    "inferred": false
  },
  "output_spec": {
    "type": "string | json | file | report",
    "description": "输出描述",
    "inferred": false
  },
  "capability_hints": ["命中的能力关键词"],
  "boundary": {
    "in_scope": ["处理的场景"],
    "out_of_scope": ["不处理的场景"]
  },
  "hidden_assumptions": ["隐含前提"],
  "unknowns": ["需要澄清的问题（<= 3 个）"]
}
```

## Decision Gate

| 条件 | 动作 |
|------|------|
| unknowns 为空 | → Pass 2 |
| unknowns 非空 | 向用户提问，收到回答后更新 IR → Pass 2 |
