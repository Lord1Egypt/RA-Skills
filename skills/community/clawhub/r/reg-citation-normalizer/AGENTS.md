# AGENTS.md - AI 技能说明书

本文件面向使用或扩展本技能的 AI 编码代理（以及接手的人类维护者）。人类读者请优先读 `README.md`。

技能：`reg-citation-normalizer`
一句话定位：医疗器械法规引用编号的识别、解析与规范化。将 21 CFR、ISO/IEC、中国国标行标（GB/YY/T）、NMPA 部令公告等各种写法解析为规范结构并给出标准书写建议。零依赖，可离线运行。适用于注册文档审校、IFU/技术文件编写、法规翻译一致性检查。

---

## 一、用途（Purpose）

本技能是 LGD/UIBC 治理理论技能体系的一员（SynomosAI 出品）。调用入口为 `SKILL.md`；AI 代理应先读 `SKILL.md`，按 frontmatter 的 `name`/`description` 判断是否适用，再按正文步骤执行。

## 二、文件约定（Directory conventions）

| 路径 | 用途 |
|---|---|
| `SKILL.md` | 主说明书：frontmatter + 触发条件 + 执行步骤（AI 调用入口） |
| `AGENTS.md` | 本文件：面向 AI 代理的说明书 |
| `README.md` | 面向人类的总览（如存在） |
| `llms.txt` | AI 索引：给 Agent 的快速引导 |

## 三、调用方式

1. 读取 `SKILL.md` 全文，确认触发条件与输出格式。
2. 按步骤执行；涉及评分/验证的环节使用技能自带脚本。
3. 输出遵循 SKILL.md 规定的结构与质量门。

## 四、生态位

本技能与其他 SynomosAI 技能可组合使用（LGD 治理系列 / UIBC 赛事系列 / [REDACTED] 医械法规系列）。版本 1.0.0。
