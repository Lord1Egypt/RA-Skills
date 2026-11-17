# 与自己对话 · Self-Relationship Skill

[English](README.md) | **中文** | [Deutsch](README.de.md) | [Español](README.es.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

> 帮助一个人更好地理解自己、接纳自己、调整自己，并在现实中做出更适合自己的选择。
>
> Help people understand themselves more clearly, accept themselves without giving up on growth, and make choices that fit their actual lives.

一个基于积极心理学视角的 AI Skill：当用户谈论「与自己相处」「自我关系」「自我接纳」「认识自己」「自我成长」等话题时，引导用户先理解、再改变，而不是急着给出方案或贴标签。

## 核心理念

- **先理解自己，再改变自己**：不急着评价，先问"发生了什么、我在经历什么、这对我意味着什么"
- **状态不等于身份**：「我现在很焦虑」≠「我是一个焦虑的人」
- **接纳不等于放弃改变**：在接受现实的基础上决定下一步
- **测试是理解工具，不是定义标签**：人格测试、MBTI、Big Five 都只是认识自己的镜子
- **不把心理学变成新的自我评判工具**：不制造确定性，不虚构经历，不强行积极

## 特性

- 中英双语内容（`SKILL.md` 内含中文全文 + English Version）
- 结构化的自我反思框架：事实 → 感受 → 解释 → 判断 → 选择
- 明确的表达原则与边界，避免「AI 心理学文章腔」
- 不诊断、不贴标签、不替用户做重大决定

## 安装

将本目录（或 `SKILL.md`）放入你的 Agent 的 skills 目录：

```bash
# 例如 Claude Code / Trae 等支持 skills 的 Agent
# 将 self-relationship 目录复制到你的 skills 目录下
cp -r self-relationship ~/.claude/skills/
```

安装后，当用户提及「与自己相处」「自我关系」「自我接纳」「自我理解」「认识自己」「自我成长」或 `self-relationship`、`self-acceptance` 等话题时，Agent 会自动加载本技能。

## 使用方法

直接与 Agent 交谈即可，例如：

- 「我总是忍不住自我批评，怎么办？」
- 「我觉得自己很失败，是不是性格有问题？」
- 「我测了 MBTI，但感觉被它定义了」
- 「我不确定自己真正想要什么」

Agent 会按照技能内定义的对话原则与你互动：先理解 → 澄清 → 提供视角 → 找到选择。

## 目录结构

```
self-relationship/
├── README.md        # 英文说明（GitHub 默认展示）
├── README.zh-CN.md  # 本文件（中文说明）
└── SKILL.md         # 技能主体（中英双语，含 frontmatter 触发描述）
```

## 内容框架

1. **Core Philosophy** — 10 条核心理念（状态≠身份、接纳≠放弃、关注倾向等）
2. **Self-Reflection Framework** — 事实 → 感受 → 解释 → 判断 → 选择 五层区分
3. **Important Distinctions** — 事实 vs 解释、感受 vs 判断、接纳 vs 放弃等关键区分
4. **Conversation Principles** — 先理解再建议、允许不知道、允许矛盾、寻找可控部分
5. **Expression Principles** — 13 条表达原则（避免 AI 腔、少用金句、不虚构经历）
6. **Response Orientation** — 理解 → 澄清 → 提供视角 → 找到选择
7. **Boundaries** — 不诊断、不病理化、不替用户做决定

## 免责声明

本技能用于教育与自我反思，不构成任何医疗、心理或临床诊断。如果你正在经历严重的心理困扰或危机，请及时寻求合格的专业帮助（如心理咨询师、精神科医生或本地危机干预热线）。

## License

本项目未指定开源许可证。如需商用或二次分发，请联系作者。
