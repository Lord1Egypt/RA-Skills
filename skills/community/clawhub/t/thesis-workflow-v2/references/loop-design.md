# Loop 设计说明（v1.7）

> 本文档解释 MBA Thesis Workflow v1.7 引入的 **Loop Agent 架构思想**——为什么要在传统多阶段状态机上"加 Loop 元素"，以及如何落地。

---

## 一、为什么引入 Loop 思想？

### 1.1 传统多阶段工作流的问题

MBA 论文写作（v1.6 及之前）是一个**线性多阶段流程**：
```
Phase 1 → Phase 2 → Phase 2.5 → Phase 3 → Phase 3.5 → Phase 4 → Phase 5 → Phase 5.1 → Phase 5.2
```

**痛点**：
- ❌ 每个 Phase 之间需要**用户手动 trigger**（体验差、效率低）
- ❌ 审核是**单向线性**（写→审→改→过），没有"重审直到通过"的闭环
- ❌ 规范是写在 SKILL.md 里**靠 Agent 自觉**，没有自动化校验
- ❌ 失败恢复是**手动打回**（"返回 Phase 2 重写"），没有自动重试

### 1.2 Loop Agent 思想的核心价值

**AI Agent Loop**（ReAct / OpenAI Agents SDK）的核心是 **"感知 → 思考 → 行动 → 观察"** 的循环，并具备：
- 自我纠正（self-correction）
- 自动化工具调用
- 明确终止条件
- Human-in-the-loop（关键决策点确认）
- Guardrails（输入输出校验）

**应用到 MBA 论文工作流**：
- 现状已经是"半 Loop 化"（状态文件、人工门槛、审核机制）
- 但**缺乏显式的 Loop 编排**和**自动化校验**
- v1.7 在保留主流程的前提下，**显式声明 5 个 Loop 元素**

### 1.3 不是"完全 Loop 化"的理由

**为什么不做"全自动 Loop Agent"？**

| 因素 | 说明 |
|------|------|
| **高 stakes** | MBA 论文关系到用户年底毕业，错版交付给导师代价极大 |
| **学术质量不可妥协** | LLM 可能幻觉、跑偏，学术逻辑链需要人工把关 |
| **决策需要人** | 题目选择、研究方向、整合方案、最终交付——都是用户决策 |
| **监管/审计** | 导师可能问"这章怎么来的"，需要明确的人工审查节点 |

**结论**：采用**多阶段状态机 + 内部 Loop 元素**的混合架构，而非纯 Loop Agent。

---

## 二、5 个 Loop 元素详解

### 2.1 Orchestrator Loop（自动推进）

**目标**：取代"每步手动 trigger"。

**实现**：
- 每 Phase 完成后，Orchestrator 读取 `*_任务状态.json`
- 根据状态文件 + Guardrails 校验结果，**自动判断下一步**：
  - 通过 → 进入下一 Phase
  - 缺条件 → 提示用户补
  - 出错 → 自动打回当前 Phase 重做

**终止条件**：全部 7 个 Phase 状态都是 `completed`。

**最大重试**：3 次，超过则强制 Human-in-the-loop。

**伪代码**（详见 SKILL.md）：
```python
def decide_next_action(state):
    if state["phase"] == "Phase 3.5 完成" and has_p0_issues(state):
        return "Phase 4 修订（修订后自动重审，最多 3 轮）"
    ...
```

### 2.2 Phase 内部自检 Loop（Observe → Think → Act → Verify）

**目标**：每个 Phase 内部遵循四步循环，确保输出符合规范。

**通用模板**：
```
1. Observe  ——  读取上一阶段产出 + 状态文件
                ↓
2. Think    ——  判断本 Phase 任务清单
                ↓
3. Act      ——  执行 spawn / exec / 文件写入
                ↓
4. Verify   ——  运行 Guardrails 脚本校验
                ↓
              通过？→ 退出 Phase，更新状态
              不通过？→ 回到 Step 2 修订（最多 3 次）
```

**为什么不直接用 OpenClaw 的 Agent Loop？**

- OpenClaw 的 Agent Loop 适合**单次任务**（写一篇文章、调一个 API）
- MBA 论文是**多阶段长任务**，需要**持久状态**（状态文件）+ **跨 Phase 协调**（状态机）
- Loop 元素是在每个 Phase 内部"借用" Agent Loop 的思想，不破坏主流程的状态边界

### 2.3 审核 Loop（多轮闭环）

**目标**：把审核做成"审→改→重审→...→通过"的闭环。

**状态机**：
```
[Phase 3 快速审核] → 输出报告
        ↓
[Phase 3.5 深度评审] → P0/P1/P2 分级
        ↓
   有 P0？── 是 → [Phase 4 修订] → 重审（仅审 P0）→ ...
                          ↑                              │
                          └──── 连续 2 轮无新 P0 ─────────┘
                                                        │
   无 P0（仅 P1/P2）──→ [Phase 4 整合] → [Phase 5 终审] → 退出
```

**关键设计**：
- **仅重审 P0**：避免 LLM 上下文爆炸（不重复扫描全文）
- **连续 2 轮无新 P0**：视为通过（容忍小波动）
- **超过 3 轮强制人工决策**：防止死循环

**重审报告命名**：`审核报告_Phase3.5_v{轮次}.md`，归档保留。

### 2.4 Guardrails 校验（自动化规范检查）

**目标**：把"应该遵守的规范"做成自动化脚本，Agent 不再靠自觉。

**脚本**：`scripts/loop_self_check.py`（v1.7 新增）

**10 项校验**：
1. 章节完整性（7 章齐全）
2. 字数门槛（每章 ≥ 100 行）
3. 参考文献存在
4. 无 `## 第X章` 混合格式
5. 无 `**正文加粗**` 残留
6. 引用完整性（作者，年份）模式
7. 三线表无竖线
8. 表格标题在表上方
9. 无合并残留（`===END===`）
10. 核心章节关键词（第5章战略/第6章实施）

**使用方式**：
```bash
# 单文件校验
python3 scripts/loop_self_check.py --file 论文_xxx.md

# Phase 级别校验
python3 scripts/loop_self_check.py --phase 2 --workspace ~/.openclaw/workspace/

# JSON 报告（用于自动化）
python3 scripts/loop_self_check.py --file 论文_xxx.md --json
```

**失败处理**：
- 软错误（可自动修复）→ 自动修复并重试
- 硬错误（需 Agent 决策）→ 打回当前 Phase
- 累计 3 次失败 → 强制 Human-in-the-loop

### 2.5 Verification Loop（Word 输出校验）

**目标**：Word 输出后自动校验格式，避免错版交付。

**实现**：
```bash
python3 scripts/loop_self_check.py --file 论文_xxx_v4.0_终稿.docx --verify-docx
```

**校验项**：
- 分页符（每章后）
- 表格数量
- 段落数量（≥ 500 段）
- 标题层级（字体/字号）
- 行距 20 磅
- 三线表样式

**失败处理**：
- 软错误（脚本可修复）→ 自动修复并重新生成
- 硬错误（数据问题）→ 提示用户并打回 Phase 4

---

## 三、终止条件与边界保护

### 3.1 最大重试机制

每个 Loop 都有**最大重试次数**，防止"无限循环"：

| Loop 类型 | 最大重试 | 超过后行为 |
|----------|---------|-----------|
| Orchestrator Loop | 3 次 | 强制 Human-in-the-loop |
| Phase 内部自检 Loop | 3 次 | 强制 Human-in-the-loop |
| 审核 Loop | 3 轮 | 强制 Human-in-the-loop |
| Verification Loop | 2 次 | 强制 Human-in-the-loop |

**为什么不设更多？**
- 超过 3 次仍未通过 → 说明问题超出 Loop 自动化能力
- 必须让用户决策（继续 / 调整方向 / 接受当前版本）

### 3.2 Human-in-the-loop 检查点

以下节点**必须**用户确认，不能由 Loop 自动跳：

| 检查点 | 确认内容 | 不确认的后果 |
|-------|---------|------------|
| **Phase 1 末尾** | 写作任务书（题目/公司映射/大纲） | 方向错了全白做 |
| **Phase 2.5 末尾** | 章节内容是否符合预期 | 跑偏了审完也白审 |
| **Phase 4 末尾** | 整合方案是否接受 | 整合错了质量更差 |
| **Phase 5.2 末尾** | Word 文档是否符合预期 | 错版交付给导师 |

**设计哲学**：
- 流程性、规则性、可自动化的 → Loop 处理
- 战略性、决策性、需要人类判断的 → 人工处理

### 3.3 状态文件机制（持久化）

`论文_{题目}_任务状态.json` 是 Loop 之间的"记忆"：

```json
{
  "paper": "A公司互联网分发业务竞争战略研究",
  "version": "v1.0",
  "phase": "Phase 3.5",
  "started_at": "2026-06-12 07:00",
  "last_updated": "2026-06-12 08:30",
  "review_loop": {
    "current_round": 2,
    "p0_fixed": ["P0-1", "P0-2"],
    "p0_pending": ["P0-3"],
    "max_rounds": 3
  },
  "chapters": {
    "chapter1_2_7": {"status": "completed", "file": "...", "lines": 850},
    "chapter3_4": {"status": "completed", "file": "...", "lines": 1200},
    "chapter5_6": {"status": "completed", "file": "...", "lines": 1100}
  }
}
```

**作用**：
- Orchestrator Loop 读取状态判断下一步
- Review Loop 读取 `current_round` 决定是否重审
- 中断后恢复（session 重启后从状态文件继续）

---

## 四、与 OpenClaw Agent Loop 的对应

| OpenClaw / Loop Agent 概念 | MBA Skill v1.7 实现 |
|--------------------------|---------------------|
| **Agent loop**（自动推进） | Orchestrator Loop |
| **Tool invocation** | sessions_spawn / exec / hermes chat |
| **Self-correction** | 审核 Loop（Phase 3 + 3.5 + 修订） |
| **Guardrails** | loop_self_check.py 脚本（10 项校验） |
| **Human-in-the-loop** | Phase 1/2.5/4 强制用户确认 |
| **Sessions**（持久状态） | `*_任务状态.json` |
| **Tracing**（追踪） | 各 Phase 输出文件 + 状态文件 |
| **Verification** | Verification Loop（Word 格式校验） |
| **MCP tools** | multi-search-engine / academic-research / arxiv-search-collector |
| **Sandbox** | sessions_spawn 子 agent 隔离执行 |

**关键差异**：
- **OpenClaw Agent Loop**：单次任务内循环（适合写一篇文章、调一个 API）
- **MBA Skill v1.7**：**多阶段状态机 + 每阶段内部 Loop**（适合长任务、有明确状态边界的复杂工作）

---

## 五、未来扩展方向

### 5.1 短期（v1.8 - v1.9）

- [ ] **Orchestrator Loop 完整实现**：把伪代码变成可执行的 `orchestrator.py`
- [ ] **状态文件自动生成**：每 Phase 启动时自动创建/更新 `*_任务状态.json`
- [ ] **Guardrails 软错误自动修复**：例如 `**正文加粗**` 自动去除、`## 第X章` 自动纠正
- [ ] **审核 Loop 报告对比工具**：自动 diff 两轮审核报告，识别"新增 P0"

### 5.2 中期（v2.0）

- [ ] **多论文并行支持**：用状态文件隔离，同时跑多篇论文
- [ ] **审核报告自动归档**：所有 Phase 3.5 报告统一管理，支持历史回溯
- [ ] **导师反馈 Loop**：接入导师的批注，自动生成"导师反馈 → 修订 → 复审"闭环
- [ ] **Word 模板自定义**：支持不同学校（南大、复旦、交大等）的论文模板

### 5.3 长期（v3.0+）

- [ ] **AI 辅助选题**：Phase 1 前置 Loop，根据用户方向自动推荐题目 + 大纲
- [ ] **文献自动追踪**：论文写作过程中自动追踪相关领域新论文
- [ ] **答辩 PPT 自动生成**：基于终稿自动生成答辩 PPT
- [ ] **跨论文知识库**：所有论文的素材、参考文献、模板沉淀为可复用知识库

---

## 六、参考资料

- **ReAct 论文**（arXiv:2210.03629）：https://arxiv.org/abs/2210.03629
- **OpenAI Agents SDK Agent Loop 概念**：https://openai.github.io/openai-agents-python/
- **OpenAI Operator / CUA 介绍**：https://openai.com/index/introducing-operator/
- **Anthropic Computer Use 文档**：（抓取失败，可参考 OpenAI Operator 的设计思路）

---

> **维护者**：MBA Skill v1.7 引入，最后更新 2026-06-12。
> **反馈**：发现 Loop 元素设计问题，提交 issue 或直接修订本文档。
