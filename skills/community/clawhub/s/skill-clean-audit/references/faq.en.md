# FAQ

> Central answers for the audit method, boundaries, and artifact behavior. Kept short to avoid duplicating the main doc.
> 审计方法论、边界与产物行为的集中解答。每条尽量短，避免和主文档重复。

## 1. Will it edit my code for me?
No. This skill **audits read-only** and emits a report with fix-priority advice, but changes not a single character of the code under review. To apply fixes, open a separate pass, one PR at a time per the report's conclusion priority (see "Fix Priority: Incremental Cleanup").
不能。本 skill **只读审计**，产出报告与修复优先级建议，但不在被审计代码上改任何一个字。若要落地修复，另开一轮，按报告「结论」的优先级逐个 PR。

## 2. How is it different from code-review-assistant / clean-code / project-code-standard?
- `code-review-assistant` / `critical-code-reviewer`: generic PR/MR review with per-diff advice and annotations. This skill does not do diff review.
- `clean-code`: a style handbook (off-the-shelf SRP/DRY/KISS rules). This skill does not copy rules; it *derives* criteria from "code is written for humans".
- `project-code-standard`: lint/format execution (ruff/eslint/prettier). This skill does not run formatting.
区别：那些做 PR 审查 / 规范手册 / lint 执行。本 skill 只做第一性原理可读性-可维护性审计，并自行推导判据。

## 3. Where does the report go?
The **workspace root** of the current agent session, as `clean_code_audit_<target>.md`; it **never overwrites** an existing same-name report (avoids silently losing your earlier audit).
当前 agent 会话的**工作区根目录**，文件名 `clean_code_audit_<target>.md`；**不覆盖**已有同名报告。

## 4. How do I audit a huge file / a whole directory?
- Very large file (>500 lines): audit in ~500-line segments, score each independently, then give a cross-segment summary; this avoids severity distortion or context overflow from one huge sweep. Don't hard-split one logical function (judge it whole if it spans).
- Whole skill directory: script by script, prioritizing the most-frequently-changed ones (high change risk by nature).
超大文件（>500 行）：按 ~500 行一段分段审，每段独立打分后给跨段汇总；不为凑分段硬拆逻辑函数。整目录：逐脚本审，优先最常改的。

## 5. Does a metric hit mean it's dirty?
No. The 5 lightweight signals are only probes for "worth a closer look"; the criteria remain the A/B axes. If explained by comment + scoped and it truly lowers cost, it stays clean.
不。5 项轻量指标只是探针，判据永远是 A/B 两轴。能注释说清+范围可控且真降成本，仍干净。

### Full definitions of the five signals and their A/B attribution

| Signal | Threshold | Axis | How to read it |
|---|---|---|---|
| Function length | > 40 lines | **A** | Check cohesion; if hard to split, **amber** not red |
| Param count | ≥ 4 | **A** | Call site hard to read; prefer an options object |
| Nesting depth | ≥ 4 levels | **A** | Reader must hold multiple contexts in head |
| Boolean flag | `def f(..., dry_run=False)` | **A** | The function does two opposite things (SRP violation) |
| Duplicated logic | ≥ 3× in one file/function | **B** | DRY violation, fix-one-forget-another |

| 信号 | 阈值 | 轴 | 判读要点 |
|---|---|---|---|
| 函数行数 | > 40 行 | **A** | 看是否仍内聚；若内聚难拆，归**黄**而非红 |
| 参数数 | ≥ 4 | **A** | 调用处难读懂意图；优先抽 options 对象 |
| 嵌套深度 | ≥ 4 层 | **A** | 读者需脑内维护多个上下文 |
| 布尔旗参数 | `def f(..., dry_run=False)` | **A** | 函数实际做两件相反的事，违反单一职责 |
| 同类逻辑重复 | ≥ 3 次（单文件内） | **B** | DRY 违反，改一处忘一处 |

> Metric hit ≠ dirty. If explained by "comment + scoped" and it truly lowers cost, it stays clean. Metrics only save you line-by-line scanning time.
> 指标命中 ≠ 脏。若能用「注释说清 + 范围可控」解释且真降成本，仍是干净的。

Run `scripts/metric_probe.py --src <file>` to auto-detect all 5 with `file:line` output; the script *hints only, never grades*.
可跑 `scripts/metric_probe.py --src <file>` 自动探测并输出 `file:line` 清单；只提示不判级。

## 6. Which languages are supported?
Python (.py) primarily; skill scripts often .py / .js / .ts; and any **human-readable source text**. Not binaries / images / data files / obfuscated code.
Python（.py）为主；Skill 脚本常含 .py / .js / .ts；及任何人类可读源码文本。不接受二进制/图片/数据/混淆代码。

## 7. Does it need network / an API key?
No. Pure local read-only audit — zero network, zero credentials, zero runtime dependencies. The optional `scripts/metric_probe.py` is also pure Python stdlib, offline, no credentials, read-only.
不需要。纯本地只读，零网络零凭据零依赖。可选 `scripts/metric_probe.py` 也是纯 stdlib、离线、无凭据、只读。

## 8. Which artifact file per language? (artifact mapping)
Once *Language Selection* settles `zh` / `en` / `auto`, pick the file from this table:

| Artifact | `zh` | `en` |
|---|---|---|
| Interactive checklist | `assets/clean_code_checklist.html` | `assets/clean_code_checklist.en.html` |
| Audit sample (functional) | `references/clean_code_audit_sample.md` | `references/clean_code_audit_sample.en.md` |
| Audit sample (complex) | `references/clean_code_audit_sample_complex.md` | `references/clean_code_audit_sample_complex.en.md` |
| FAQ (this file) | `references/faq.md` | `references/faq.en.md` |

If an English version is missing, fall back to Chinese and note "no English version yet" — never silently give the wrong language.
缺失某英文版时 fallback 到中文并在报告中注明「该范例暂无英文版」，**不静默给错语言**。

## 9. Is this skill a "tool" or a "methodology"? Why is there no end-to-end script?
**Methodology-type**, not tool-type. The core action is *judgment* — "does this code lean A or B, is it red or intentionally-amber debt" — which is human reasoning and cannot be pre-encoded into a deterministic pipeline. So what this skill ships is criteria + flow + a tickable checklist, applied by you (the agent) item by item with `file:line` evidence.

**The absence of an end-to-end automation script is a design decision, not a gap.** The `scripts/metric_probe.py` shipped here is an **optional accelerator**: it detects the 5 metric signals and emits a `file:line` list to help you locate suspects fast — *hints only, never grades*. Severity is still yours to judge via the A/B axes. Whether you run it or not, the quality bar for the audit is unchanged.
方法论型，非工具型。审计的核心动作是判断，本质是人的推理，无法预先写成确定性自动流程。因此没有端到端自动化脚本是设计决策而非缺失；`metric_probe.py` 仅为可选加速器。
