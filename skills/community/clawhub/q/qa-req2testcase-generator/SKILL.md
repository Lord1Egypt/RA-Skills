---
name: qa-req2testcase-generator
description: "AI驱动的需求→测试用例生成能力。V4.12.6架构:总控路由+逐条P6生成+渐进式披露+P6质量引导+反脚本防护+批量修复"
version: "4.12.6"
metadata:
  author: "shaozhe"
  architecture: "orchestrator-driven + segmented-rules + auto-fix"
---

# qa-req2testcase-generator V4.12.6

> 版本:4.12.6 | 架构:总控路由+逐条P6生成+渐进式披露+P6质量引导+反脚本防护+批量修复
> V4.12.6关键变更: ⚖️ p6_merge比率自动调平+🔧 p7_batch_fix批量修复+📤 评审推送默认开启 | V4.12.5: 🛡️ 反脚本三段式拦截

---

## ⚠️ 元规则（最高优先级，违反即终止）

**Agent必须100%执行skill规定的流程，不得自行判断"优化"或"改进"。**

1. **执行优先**：按skill规定流程执行每一步，不得跳过、绕道
2. **规则即硬约束**：「禁止」「必须」「🔴」是代码级硬约束，违反即报错
3. **发现问题先执行后反馈**：完成当前流程后反馈，不在执行中自行修改
4. **禁止伪造结果**：orchestrator返回error时必须修复重试，不得伪造gate pass
5. **禁止自我决策**：不允许Agent自行判断"规则不合理/太慢/可优化"并绕过
6. **禁止抛选择题**：任何步骤失败后自动修复重试，禁止停下来向用户要选择
7. **⛔ 禁止脚本批量生成**（V4.12.5）：禁止编写 Python/Shell/JavaScript 脚本循环调用 `p6_generate_one`。这不是效率，是偷懒。脚本批量生成的内容必然空洞，质量门禁会拦截，拦截后再重来反而更慢。必须由 LLM 逐条阅读 prompt 后手写生成每个 TP 的用例。orchestrator 会检测调用频率，违规将被拒绝。

---

## ⛔ 入口强制检查：需求载荷是否存在（最高优先级）

**此检查在技能触发后第一个动作执行。不通过→立即终止。**

✅ 允许继续：用户消息含需求正文 / 含需求附件(.docx/.txt/.pdf) / 明确引用近期需求
❌ 必须停止："我等会发"、"分析这个需求"(无附件)、仅提及技能名、模糊引用

不通过回复：`📋 请先发送需求正文或需求文档，收到后立即开始分析。`
通过回复：`✅ 需求载荷已收到 | 格式:X | 大小:Y | 📋 即将进入初始化...`

---

## 🔴 运行协议

**核心原则:orchestrator.py控制流程,Agent只负责执行prompt返回JSON。**

**6段确认模式:每次「继续」只前进一个段落（绝对禁止连段执行）:**
- 用户回复1次「继续」→ Agent**只执行下一个段落**，执行完立即⏸️停止
- ⛔ 禁止: 用户说1次「继续」Agent连跑多段
- ⛔ 禁止: 看到下一段gate已存在就"继续跑完"
- 每段结束后检查: 是否已输出⏸️？是否已等待「继续」？

**📌 `__must_emit__` 字段**：p2_code_generate / step7_export的stdout包含此字段。Agent必须将MEDIA行复制到回复，同时用 `exec cat` 展示文件内容。

---

## 🔴 段落边界规则（最高优先级，违反视为流程无效）

| 规则 | 说明 |
|------|------|
| ⛔ 禁止连段 | 每段结束→⏸️停止→等「继续」→才读下一段规则文件 |
| ⛔ 禁止预读 | 执行段落N时，禁止读取 rules/paragraph_N+1.md |
| ⛔ 禁止跨段 | 即使下一段gate已存在，也必须等用户「继续」 |
| 🔴 停止锚点 | 每段规则文件末尾有终止锚点，Agent读到必须停止 |

---

## 🔴 操作约束矩阵

| Step | Agent角色 | 唯一正确命令 |
|------|----------|------------|
| P0 | 执行者 | prep_prompt → 生成JSON → step_run |
| P1 | 执行者(分批) | 骨架→循环feature→p1_code_merge |
| P2 | 观察者 | `python3 "$ORCH" --action p2_code_generate` |
| P3 | 执行者 | prep_prompt → 生成JSON → step_run |
| P4 | 执行者 | prep_prompt → 生成JSON → step_run |
| P5 | 观察者 | `python3 "$ORCH" --action p5_code_merge` |
| P6 | **LLM生成者**(⛔禁子Agent) | p6_tp_list→逐条循环(p6_generate_one→完整阅读prompt生成JSON→p6_generate_one --save)→p6_merge<br>🔴 **V4.11.0逐条生成**：一次一个测试点，prompt极简(~400B)。Agent完整阅读prompt后生成JSON，字段由代码自动补全 |
| P7 | 观察者 | `python3 "$ORCH" --action p7_code_check` |

Agent只做3类事: ①exec orchestrator命令 ②read prompt并生成JSON write到文件 ③read图片并描述

---

## 🔴🔴🔴 V3.5.2 绝对禁止行为（代码层硬控）

1. **禁止直接写gate文件** — gates/*.pass.json 只能由orchestrator创建
2. **禁止直接写output文件** — p{N}_output.json 只能通过step_run等action写入
3. **禁止直接修改state文件** — orchestrator_state.json 内部修改
4. **禁止import orchestrator** — 不允许任何形式导入
5. **禁止跳过orchestrator** — 所有步骤必须通过 `python3 "$ORCH" --action XXX`
6. **禁止伪造执行结果** — error时必须修复重试，不得手动替代
7. **Onboarding必须逐步交互** — 3步逐步展示，禁止合并

违反以上任何规则，step7_export会审计拒绝。

---

## 📋 6段执行流程

| 段落 | 内容 | 规则文件 | 前置Gate | 确认点 |
|:--:|------|------|------|:--:|
| 1 | init + onboarding | `read rules/paragraph_1.md` | — | ⏸️ |
| 2 | step0 + 图片理解 | `read rules/paragraph_2.md` | P0 gate | ⏸️ |
| 3 | P0+P1 + 自动P2 | `read rules/paragraph_3.md` | step0 gate | ⏸️ |
| 4 | P3+P4 + 自动P5 | `read rules/paragraph_4.md` | P2 gate | ⏸️ |
| 5 | P6 用例生成 | `read rules/paragraph_5.md` | P5 gate | ⏸️ |
| 6 | P7 + Excel导出 | `read rules/paragraph_6.md` | P6 gate | 🏁 |

**🔴 执行流程（每段通用，严格执行）:**

1. 收到用户「继续」→ 查上表找到下一段N
2. `read rules/paragraph_N.md` → 完整阅读该段规则
3. 严格按规则文件中的指令逐步执行
4. 执行到规则文件末尾的终止锚点 → ⏸️停止
5. 输出「段落N完成，请回复「继续」」
6. 🔴 绝对禁止：读完paragraph_N.md后继续读取paragraph_N+1.md

---

## 🔄 断点续跑

```
exec: python3 "$ORCH" --action status
```
→ 查看已完成的gate pass，从下一个未执行的步骤开始。
→ 如果当前段落已有部分gate pass → 阅读该段规则文件，跳过已完成步骤。

---

## ❌ 错误处理

| 错误类型 | 处理 |
|---------|------|
| gate_blocked | 检查缺失的前置步骤，从该步骤重新执行 |
| guard_failed | 检查truncation，修复JSON后重试 |
| quality_rejected | 按issues和fix_example修复，最多重试2次 |
| timeout | 检查文件是否已生成新内容，有则继续，无则重试 |

---

## 📁 文件结构

```
skill_v4/
├── SKILL.md                     ← 本文件（总控路由）
├── rules/
│   ├── paragraph_1.md           ← 段落1规则
│   ├── paragraph_2.md           ← 段落2规则
│   ├── paragraph_3.md           ← 段落3规则
│   ├── paragraph_4.md           ← 段落4规则
│   ├── paragraph_5.md           ← 段落5规则
│   └── paragraph_6.md           ← 段落6规则
├── prompts/                     ← LLM prompt模板
├── tools/                       ← orchestrator.py等工具
├── config/                      ← 配置
└── references/                  ← 参考文档
```

## 触发条件

「ai用例生成」「ai需求分析」「req2testcase」「生成测试用例」「分析需求」「拆解功能点」「输出测试点」「需求评审」「PRD转测试用例」

## 已知限制

- 仅支持中文需求文档（.docx/.txt/粘贴文本）
- 不支持视频/音频需求输入
- PX图片理解依赖腾讯云API（未配置则降级为caption_only）
- LOW模型（MiniMax等）V4.10.0起走窄聚焦模式，用例质量可达可用水平
