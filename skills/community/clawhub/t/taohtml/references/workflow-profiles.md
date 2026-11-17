# Workflow Profiles

This lightweight catalog is used only when the primary business outcome remains
ambiguous. TaoHtml remains one installed Skill. Show the nine customer-facing names
and primary outcomes in one round; do not show internal ids or file paths. After the
user chooses, read only that row's `definition_ref`.

## Complete Ambiguous-Routing Catalog

| profile_id | 精确客户名称 | 主目标 | definition_ref |
|---|---|---|---|
| `formal-submission-writing` | 规范报送与正式写作 | 形成可正式报送、流转或归档，且章节、措辞与责任边界经得起审查的成品。 | `references/workflow-profile-formal-submission-writing.md` |
| `research-analysis-argumentation` | 研究分析与专业论证 | 以透明的方法、证据和推理回答专业问题，并给出有边界的结论。 | `references/workflow-profile-research-analysis-argumentation.md` |
| `periodic-operations-reporting` | 周期经营与数据汇报 | 基于受控数据说明周期业绩、差异、驱动因素、风险与管理动作。 | `references/workflow-profile-periodic-operations-reporting.md` |
| `proposal-planning-decision` | 方案策划与决策提案 | 通过选项、标准、取舍、建议和实施风险支持一项明确决策。 | `references/workflow-profile-proposal-planning-decision.md` |
| `live-presentation-persuasion` | 现场演讲与说服表达 | 通过口头节奏与可见证据，帮助演讲者推动现场受众形成认知、决策或行动。 | `references/workflow-profile-live-presentation-persuasion.md` |
| `teaching-training-knowledge-transfer` | 教学培训与知识传递 | 通过解释、示范、练习与回顾，让学习者获得可使用的知识或方法。 | `references/workflow-profile-teaching-training-knowledge-transfer.md` |
| `project-lifecycle-reporting` | 项目全过程汇报 | 让项目相关方围绕目标、范围、阶段、进度、变更、风险、决策与收尾保持一致。 | `references/workflow-profile-project-lifecycle-reporting.md` |
| `brand-communication-editorial-publishing` | 品牌传播与编辑出版 | 在保护身份、主张、素材和行动路径的前提下，形成可信且可记忆的对外叙事。 | `references/workflow-profile-brand-communication-editorial-publishing.md` |
| `rule-response-application-defense` | 规则响应、申报与答辩 | 以完整响应、可追溯证据和可答辩表达满足权威规则或评分标准。 | `references/workflow-profile-rule-response-application-defense.md` |

Ask exactly one question: “这份成品最主要要完成上述哪一种业务目标？”
Record the catalog as the latest active option set. After the answer, select exactly
one primary Profile, read only its unique `definition_ref`, and apply any other
Profile capability only as a bounded overlay. Do not run multiple complete workflows.
