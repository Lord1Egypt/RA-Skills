---
name: triphasic-execution
version: 5.19.1
author: wUwproject
license: MIT
description: Execute→Review→Advance 三步循环执行框架。增强步骤规划能力、增强语义理解；明确空转/重试/换思路/求助完整流转规则；最多重试3次、最多空转3次强制约束。
tags: ['framework', 'execution', 'debugging', 'problem-tracking', 'risk-tracking', 'lessons-learned', 'cross-platform', 'configuration', 'config-ui']
category: workflow
trigger: ['三步循环', 'Execute', 'Review', 'Advance', '步骤', 'pre_exec', 'verify_exec', 'retry', 'idle']
trigger_negative: true
sensitive_access: false
critical_write: false
permission_weight: LOW
data_dir: ../.standardization/triphasic-execution/data/
external_data_dir: true
meta_field_sync: true
h1_position: true
---
# Triphasic Execution Framework
执行 → 审查 → 推进。每次交互只做一件事，三者缺一不可。

> → 详见 `references/antipatterns.md`
> → 详见 `references/faq.md`

---

## 触发条件

**正向触发（满足以下任意一条）：**

- 说出"三步执行"、"执行审查推进"、"triphasic"
- 说出"问题记录"、"经验教训"、"problem logger"
- 说出"打开 triphasic 配置"、"triphasic config"
- 需要结构化执行框架防止死循环或跳步
- 复杂多步骤任务，需要强制进度追踪和中断恢复

**否定条件（满足以下任意一条，不触发）：**

- 简单问答、闲聊、问候（不需要结构化执行）
- 单步任务（如"查看文件"、"运行命令"等一步完成的操作）
- 用户明确说"不要使用 triphasic"或"关闭 triphasic"
- 纯信息查询（不需要执行-审查-推进循环）

---

## 核心能力

> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。

| # | 能力 | 说明 |
|---|------|------|
| 1 | **语义理解增强（F-01+）** | 参考 semantic-split 的 5W2H 维度提取与约束强度标注（🔴🟡⚪），增强第一步理解能力；详见 `references/mandatory.md` Phase 0 |
| 2 | **步骤规划增强（F-02+）** | 参考 skill-sub 的规划逻辑（意图理解→步骤排序→执行计划生成），健壮步骤规划能力（非调用链，仅参考逻辑）；详见 `references/mandatory.md` Phase 1 |
| 3 | **三步循环执行** | Execute→Review→Advance，每步必须完整，不可跳过 |
| 4 | **进度文件持久化（F-03/F-07/F-09）** | init→update→complete，中断后可 resume 恢复；**complete 强制校验（v5.12）** |
| 5 | **问题/风险/经验记录** | 任务完成后强制记录（复杂任务 Python 侧校验），积累 PROBLEMS.md / RISKS.md / LESSONS_REGISTER.md |
| 6 | **最多 3 次重试（F-08）** | 同一步骤失败 3 次必须换方案，禁止第 4 次重试 |
| 7 | **最多 3 次空转（F-11）** | 同一步骤空转（未实际执行）3 次必须截断并请求触发词输入，禁止第 4 次空转 |
| 8 | **双模式支持** | 按需调用模式（默认）/ 全局自动模式 |
| 9 | **HTML 配置界面** | `settings.py` 可视化配置技能参数 |

---

## 空转/重试/换思路/求助 流转规则

> 详细规则见 `references/mandatory.md` Phase 2~4。
> **核心原则：无任何三步骤内部直接循环，每一步都是最小单元。**

---

## 快速开始

```bash
# 按需调用（默认）— 任务开头说出关键词即可
"使用 triphasic-execution 执行以下任务：..."

# 全局自动模式 — 所有任务自动套用框架
编辑 data/default_config.json → "mode": "auto"

# 可视化配置
python {SKILL_DIR}/scripts/settings.py
```

---

## ⚡ [LOADING PROTOCOL]

skill 加载后，AI 输出以下状态标识：

```
[triphasic] skill loaded — 执行顺序：语义拆分 → 任务规划 → 执行/审查/推进
```

| 观察结果 | 结论 |
|---------|------|
| 状态输出在任务相关内容之前出现 | ✅ 执行顺序正确 |
| 状态输出在任务执行后才出现 | ❌ 执行顺序错误 |
| 无状态输出 | ❌ skill 未加载 |

---

## 🚨 [MANDATORY] 强制约束总表

> **本节是整个技能的执行宪法。违反任意一条 = 违规，必须立即停止并补救。**

| 序号 | 约束内容 | 触发时机 | Python 强制 |
|------|---------|---------|------------|
| **F-01** | 收到任务后首先执行语义拆分，禁止直接进入规划 | 收到任务第一个响应 | ❌ AI 自觉 |
| **F-02** | 语义拆分完成后必须输出【任务规划】，禁止直接执行 | 语义拆分输出后 | ❌ AI 自觉（需用户确认规划）|
| **F-03** | 任务规划输出后立即调用 `task_progress.py init` | 规划确认后 | ✅ 文件不存在则后续 update/complete 报错 |
| **F-04** | 每步 EXECUTE 开始前重述本步骤任务目的 | 每步执行前 | ❌ AI 自觉 |
| **F-05** | 每步执行后必须紧跟 REVIEW，禁止连续执行两步 | 每步执行后 | ✅ `pre_exec_search` 钩子拦截未 REVIEW 的执行 |
| **F-06** | 每步 REVIEW 后必须紧跟 ADVANCE | 每步 REVIEW 后 | ✅ `block_skip_review` 钩子拦截未 REVIEW 的下一步 |
| **F-07** | 每步 ADVANCE 后调用 `task_progress.py update` | 每步 ADVANCE 后 | ✅ update 校验 init 存在性 |
| **F-08** | 同一步骤失败 3 次后必须换方案，禁止第 4 次重试 | 重试计数达到 3 | ✅ 脚本强制（`retries>=3 → sys.exit(1)`）|
| **F-09** | 任务完成后调用 `task_progress.py complete` | 任务完成时 | ✅ **v5.12 强制**：校验步骤完成率、记录文件、summary.json |
| **F-10** | 任务完成后必须输出【任务完成】总结 | 任务结束时 | ⚠️ 部分（summary.json 自动生成）|
| **F-11** | 同一步骤空转（未实际执行）3 次必须截断并请求触发词输入 | 空转计数达到 3 | ✅ `auto_idle_cutoff` 钩子自动 abort（默认关）|
| **F-12** | 换思路必须经 ADVANCE→EXECUTE→REVIEW→ADVANCE 完整循环，禁止三步骤内部直接循环 | 换思路请求产生时 | ❌ AI 自觉（LLM 决策流程，无法脚本化）|
| **F-13** | 推进阶段成功后，坚决不倒回已画√的步骤 | 推进决策时 | ❌ AI 自觉（LLM 决策流程，无法脚本化）|

### 自检指令

```
[自检] 当前阶段：[阶段名称]
- F-01 语义拆分：[已完成/待执行]
- F-02 任务规划：[已完成/待执行]
- F-03 进度文件创建：[已完成/待执行]
- 当前步骤 N：[待执行/执行中/已完成]
- 重试计数：[0/1/2/3/超次]
- 空转计数：[0/1/2/3/超次]
违规项：[无/F-XX 描述]
```

---

## 工作流程

```
用户任务
  ↓ [F-01 MANDATORY]
语义拆分 → 输出块分析（主语/目的/诉求/动机）[增强：5W2H + 约束标注]
  ↓ [F-02 MANDATORY]
任务规划 → 明确目的/要求/工具/结果/风险 → 确认执行 [增强：参考 skill-sub 规划逻辑]
  ↓ [F-03 MANDATORY]
task_progress.py init → 创建进度文件
  ↓
执行循环（每步骤）：
  🔧 EXECUTE（重述目的 → 执行）[空转计数]
    ↓ [F-05]
  🔍 REVIEW（✅/❌/⚠️ + 证据）[重试计数/空转计数]
    ↓ [F-06]
  📍 ADVANCE（继续/换方案/求助/完成）[截断/触发词重启]
    ↓ [F-07]
  task_progress.py update
  ↓
任务完成
  ↓ [F-09] task_progress.py complete
  ↓ [F-10] 输出【任务完成】总结
  ↓ [MANDATORY] 问题/风险/经验记录
```

### 🔴 任务完成后的强制输出协议（AI 必读）

> **每完成一个任务后，AI 必须执行以下 3 步，不可跳过。**
> 不管任务成败，只要有实际工作产出，就必须记录。

| 步骤 | 命令 | 说明 |
|------|------|------|
| 1 | `task_progress.py complete --task "名称"` | 完成任务，强制校验记录文件 |
| 2 | `problem_logger.py add --scene "场景" --symptom "现象" --cause "原因" --solution "方案" --task "任务"` | 每遇到一个非 trivial 问题都记录 |
| 3 | `problem_logger.py merge-to-lessons` | 任务完全完成后，合并所有待合并条目到 LESSONS_REGISTER.md |

→ 完整用法见下方「快速命令」章节
→ 数据目录：`skills/.standardization/triphasic-execution/`（符合 R-11/R-12 规范）
→ 结构规范：`data/`(进度文件) `output/`(记录文件) `logs/`(日志) `temp/`(临时文件)

→ 详细规则、模板、禁止行为清单见 `references/mandatory.md`
→ 完整示例见 `references/examples.md`
→ CLI 命令、进度文件、数据目录、安装见 `references/reference.md`

---

## 循环规则（摘要）

1. **语义拆分先行** — 收到任务的第一个动作（增强：5W2H + 约束强度标注）
2. **规划先行** — 所有任务必须先输出任务规划（增强：参考 skill-sub 规划逻辑）
3. **临时文件持久化** — init → update（每步）→ complete
4. **最小单元** — 单次工具调用，每步立即审查+推进
5. **最多 3 次重试** — 3 次失败后必须换方案
6. **最多 3 次空转** — 3 次空转后必须截断并请求触发词输入
7. **大任务才拆分** — 3步以上输出步骤列表
8. **中断可恢复** — 进度文件保留，重启后 resume
9. **换思路走完整三步** — 禁止三步骤内部直接循环

---

## 快速命令

```bash
# 进度文件
python {SKILL_DIR}/scripts/task_progress.py init --task "名称" --purpose "目的" --requirements "要求" --risks "风险" --steps '[...]'
python {SKILL_DIR}/scripts/task_progress.py update --task "名称" --step 1 --status success --review "..." --advance "..."
python {SKILL_DIR}/scripts/task_progress.py complete --task "名称"  # --force 跳过步骤检查；--no-enforce 关闭记录校验
python {SKILL_DIR}/scripts/task_progress.py resume --task "名称"

# 问题/风险/经验
python {SKILL_DIR}/scripts/problem_logger.py add --scene "场景" --symptom "症状" --cause "原因" --solution "方案" --task "任务"
python {SKILL_DIR}/scripts/problem_logger.py add-risk --description "风险" --impact "影响" --mitigation "缓解" --task "任务"
python {SKILL_DIR}/scripts/problem_logger.py merge-to-lessons

# 配置界面
python {SKILL_DIR}/scripts/settings.py
```

---

## 渐进式 MD 文件体系

| 本文件（SKILL.md）包含 | 拆分到 references/ |
|---|---|
| ✅ 触发条件、核心能力、强制约束总表 | 📄 `mandatory.md` — Phase 0~4 详细规则、模板、禁止行为、空转/重试/换思路流转 |
| ✅ 工作流程概述、循环规则 | 📄 `examples.md` — 完整执行示例（含空转/重试/换思路场景） |
| ✅ 快速命令 | 📄 `reference.md` — 进度文件机制、问题记录、安装、数据目录 |
| | 📄 `antipatterns.md` — 反模式收录（AP-01~AP-08） |
| | 📄 `faq.md` — 常见问题（Q&A 1~12） |

---
## 版本
当前版本：**5.19.1** — 强制约束总表强制级别标注修正
