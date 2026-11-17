# 常见问题 / FAQ

> 审计方法论、边界与产物行为的集中解答。每条尽量短，避免和主文档重复。
> Central FAQ for the audit method, boundaries, and artifact behavior. Kept short to avoid duplicating the main doc.

## 1. 能帮我改代码吗？
不能。本 skill **只读审计**，产出报告与修复优先级建议，但不在被审计代码上改任何一个字。若要落地修复，另开一轮，按报告「结论」的优先级逐个 PR（见《修复优先级：增量清理》）。
No. This skill **audits read-only** and emits a report with fix-priority advice, but changes not a single character of the code under review. To apply fixes, open a separate pass, one PR at a time per the report's conclusion priority.

## 2. 和 code-review-assistant / clean-code / project-code-standard 区别？
- `code-review-assistant` / `critical-code-reviewer`：通用 PR/MR 审查，会逐 diff 给建议、可批注。本 skill 不做 diff 审查。
- `clean-code`：写代码的规范手册（SRP/DRY/KISS 那套现成规则）。本 skill 不抄规则，而是从「代码是写给人看的」**推导**判据。
- `project-code-standard`：lint/格式化执行（ruff/eslint/prettier）。本 skill 不执行格式化。
Difference: those do PR review / style handbook / lint execution. This skill only does first-principles readability-maintainability audit and derives its own criteria.

## 3. 报告写到哪？
当前 agent 会话的**工作区根目录**，文件名 `clean_code_audit_<target>.md`；**不覆盖**已有同名报告（避免静默丢失你之前的审计）。
Workspace root of the current session, as `clean_code_audit_<target>.md`; never overwrites an existing same-name report.

## 4. 大文件 / 整目录怎么审？
- 超大文件（>500 行）：若用户要整文件审，按 **~500 行一段**分段审——每段独立打红黄绿，最后给「跨段汇总」，避免一次性扫全文件导致严重度失真或上下文溢出。**不**为凑分段而硬拆一个逻辑函数（函数跨段时整体判）。
- 整 Skill 目录：逐个脚本审，优先挑最常被修改的那几个（修改风险本就高）。
Large file (>500 lines): audit in ~500-line segments, score each independently, then give a cross-segment summary; don't hard-split one logical function. Whole skill dir: script by script, prioritize the most-frequently-changed ones.

## 5. 指标命中就代表脏吗？
不。5 项轻量指标只是「值得多看一眼」的探针，**判据永远是 A/B 两轴**。若能用「注释说清 + 范围可控」解释且真降成本，仍是干净的。
No. The 5 lightweight metric signals are only probes for "worth a closer look"; the criteria remain the A/B axes. If explained by comment + scoped and it truly lowers cost, it stays clean.

### 五项信号的完整定义与 A/B 轴归属

| 信号 | 阈值 | 轴 | 判读要点 |
|---|---|---|---|
| 函数行数 | > 40 行 | **A** | 看是否仍内聚；若内聚难拆，归**黄**而非红 |
| 参数数 | ≥ 4 | **A** | 调用处难读懂意图；优先抽 options 对象 |
| 嵌套深度 | ≥ 4 层（if/for/try 套） | **A** | 读者需脑内维护多个上下文 |
| 布尔旗参数 | `def f(..., dry_run=False)` | **A** | 函数实际做两件相反的事，违反单一职责 |
| 同类逻辑重复 | ≥ 3 次（单文件/单函数内） | **B** | DRY 违反，改一处忘一处 |

| Signal | Threshold | Axis | How to read it |
|---|---|---|---|
| Function length | > 40 lines | **A** | Check cohesion; if hard to split, **amber** not red |
| Param count | ≥ 4 | **A** | Call site hard to read; prefer an options object |
| Nesting depth | ≥ 4 levels | **A** | Reader must hold multiple contexts in head |
| Boolean flag | `def f(..., dry_run=False)` | **A** | The function does two opposite things (SRP violation) |
| Duplicated logic | ≥ 3× in one file/function | **B** | DRY violation, fix-one-forget-another |

> 指标命中 ≠ 脏。若它能用「注释说清 + 范围可控」解释，且真降低了理解/修改成本，仍是干净的。指标只为节省你逐行扫的时间。
> Metric hit ≠ dirty. If explained by "comment + scoped" and it truly lowers cost, it stays clean. Metrics only save you line-by-line scanning time.

可跑 `scripts/metric_probe.py --src <file>` 自动探测这 5 项并输出 `file:line` 清单；脚本**只提示不判级**，最终仍由你按 A/B 两轴判断。
Run `scripts/metric_probe.py --src <file>` to auto-detect all 5 with `file:line` output; the script *hints only, never grades*.

## 6. 支持哪些语言？
Python（.py）为主；WorkBuddy Skill 脚本常含 .py / .js / .ts；以及任何**人类可读的源代码文本**。不接受二进制 / 图片 / 数据文件 / 加密或混淆代码。
Python (.py) primarily; skill scripts often .py / .js / .ts; any human-readable source text. Not binaries / images / data / obfuscated code.

## 7. 需要联网 / API key 吗？
不需要。纯本地只读审计，零网络、零凭据、零运行时依赖。可选 `scripts/metric_probe.py` 也是纯 Python 标准库、零网络、零凭据、只读。
No. Pure local read-only audit — zero network, zero credentials, zero runtime dependencies. The optional `scripts/metric_probe.py` is also pure Python stdlib, offline, no credentials, read-only.

## 8. 每种语言该用哪个产物文件？（产物映射表）
按《语言选择》定下 `zh` / `en` / `auto` 后，从下表取对应文件：

| 产物 | `zh` | `en` |
|---|---|---|
| 交互清单 | `assets/clean_code_checklist.html` | `assets/clean_code_checklist.en.html` |
| 审计样例（函数式） | `references/clean_code_audit_sample.md` | `references/clean_code_audit_sample.en.md` |
| 审计样例（复杂场景） | `references/clean_code_audit_sample_complex.md` | `references/clean_code_audit_sample_complex.en.md` |
| FAQ（本文件） | `references/faq.md` | `references/faq.en.md` |

缺失某英文版时 fallback 到中文并在报告中注明「该范例暂无英文版」，**不静默给错语言**。
Artifact mapping per language mode. If an English version is missing, fall back to Chinese and note "no English version yet" — never silently give the wrong language.

## 9. 这个 skill 是「工具」还是「方法论」？为什么没有端到端脚本？
**方法论型（methodology）**，不是工具型。审计的核心动作是**判断**——「这段代码偏 A 还是偏 B、是红还是有意黄的债」本质是人的推理，无法预先写成确定性的自动流程。所以本 skill 交付的是「判据 + 流程 + 可勾选清单」，由你（Agent）逐项判断并给出 `文件:行号` 证据。

**因此没有端到端自动化脚本是设计决策，不是缺失。** 本 skill 提供的 `scripts/metric_probe.py` 是**可选加速器**：它只探测 5 类指标信号、输出 `file:line` 清单帮你快速定位疑点，**只提示不判级**——严重度仍由你按 A/B 两轴判断。用不用它，审计结果的质量标准不变。
Methodology-type, not tool-type. The core action is *judgment*, which cannot be pre-encoded into a deterministic pipeline. The absence of an end-to-end script is a design decision, not a gap; `metric_probe.py` is an optional accelerator only.
