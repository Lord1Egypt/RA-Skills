# AGENTS.md - AI 技能说明书

本文件面向使用或扩展本技能的 AI 编码代理（以及接手的人类维护者）。人类读者请优先读 `README.md`。

技能：`symbiosis-expert-team`
一句话定位：This skill should be used when invoking the expert symbiosis-expert-team (共生专家团) — see the package agents for the full persona. 五人AI共生专家团：内嵌XCGS治理属性，支持AI社交、硬件接入、状态可视与知识灌注，与人类长期共事。 当需要调用专家「共生专家团」（symbiosis-expert-team）时使用。

---

## 一、用途（Purpose）

本技能是 LGD/UIBC 治理理论技能体系的一员（SynomosAI 出品）。调用入口为 `SKILL.md`；AI 代理应先读 `SKILL.md`，按 frontmatter 的 `name`/`description` 判断是否适用，再按正文步骤执行。

## 二、文件约定（Directory conventions）

| 路径 | 用途 |
|---|---|
| `SKILL.md` | 主说明书：frontmatter + 触发条件 + 执行步骤（AI 调用入口） |
| `agents/` | 五位能力位人设文件（expert-social / expert-hardware / expert-visual / expert-knowledge / expert-human-copilot；能力位命名、非真人，标注推导来源供校准） |
| `scripts/route.py` | 路由入口：路由表 / `--check` 在位性校验 / `--selftest` 自检 |
| `AGENTS.md` | 本文件：面向 AI 代理的说明书 |
| `README.md` | 面向人类的总览 |
| `llms.txt` | AI 索引：给 Agent 的快速引导 |

## 三、调用方式

1. 读取 `SKILL.md` 全文，确认触发条件与输出格式。
2. 按步骤执行；涉及路由/校验的环节使用技能自带脚本（`scripts/route.py`）。
3. 输出遵循 SKILL.md 规定的结构与质量门（身份透明/边界守恒/单点叙事）。

## 四、生态位

本技能与其他 SynomosAI 技能可组合使用（LGD 治理系列 / UIBC 赛事系列 / [REDACTED] 医械法规系列）。版本 1.1.0。
