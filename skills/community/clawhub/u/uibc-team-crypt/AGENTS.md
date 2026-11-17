# AGENTS.md - AI 技能说明书

本文件面向使用或扩展本技能的 AI 编码代理（以及接手的人类维护者）。人类读者请优先读 `README.md`。

技能：`uibc-team-crypt`
一句话定位：UIBC（国际自治之物挑战赛）加密资产域参赛队。以 TH-CRYPT-001 判据为底座，参加「迁移的判定与问责」赛题——给定一次记忆迁移，证明「迁移后仍是同一个 Agent」并为判定负责。三层交付：判定规则（L1 有籍）／证据包（L2 有证）／失败处置与责任归属（L3 有门禁），并须声明判据可形式化等级 L0–L4。触发词：UIBC、加密资产、迁移判定、记忆迁移、证据包、责任归属、参赛队。

---

## 一、用途（Purpose）

本技能是 LGD/UIBC 治理理论技能体系的一员（SynomosAI 出品）。调用入口为 `SKILL.md`；AI 代理应先读 `SKILL.md`，按 frontmatter 的 `name`/`description` 判断是否适用，再按正文步骤执行。

## 二、文件约定（Directory conventions）

| 路径 | 用途 |
|---|---|
| `SKILL.md` | 主说明书：frontmatter + 触发条件 + 执行步骤（AI 调用入口） |
| `判据_CRYPT.md` | 本域 L1 判据摘要（作答真源） |
| `scripts/check_judge_CRYPT.py` | 判据检查器：校验判据 5 节结构，`--selftest` 实跑 PASS/FAIL |
| `AGENTS.md` | 本文件：面向 AI 代理的说明书 |
| `README.md` | 面向人类的总览（如存在） |
| `llms.txt` | AI 索引：给 Agent 的快速引导 |

## 三、调用方式

1. 读取 `SKILL.md` 全文，确认触发条件与输出格式。
2. 按步骤执行；涉及评分/验证的环节使用技能自带脚本（`scripts/check_judge_CRYPT.py`）。
3. 输出遵循 SKILL.md 规定的结构与质量门。

## 四、生态位

本技能与其他 SynomosAI 技能可组合使用（LGD 治理系列 / UIBC 赛事系列 / [REDACTED] 医械法规系列）。版本 1.1.0。
