## Description:

当用户提供客户需求、研究对象（词条/主题词）、业务意图、政府/企业研究需求、市场进入问题、可行性研究需求、排名/背书目标或政策/咨询报告需求时，用于 Wiki 研究项目的任务与决策场景界定。解析客户自由表述，内部调用 wiki-normalize，识别研究对象、管理问题、研究意图、研究口径、风险和待确认项，并输出聊天摘要、人类可读的 scope.md 与机器可读的 scope.json。

This skill is ready for commercial/non-commercial use.

## Publisher:

[leadleo](https://clawhub.ai/user/leadleo)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, consultants, and Wiki workflow agents use this skill to turn Chinese-language client requests into structured research task definitions, research intents, scope assumptions, risk notes, and confirmation questions before downstream framework building.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated scope files may be used downstream for public claims, rankings, endorsements, or government-facing work before evidence has been collected.

Mitigation: Review scope.md and scope.json before downstream use, confirm research assumptions and publication context, and collect evidence before making strong public claims.

Risk: The skill frames research tasks and risks but does not perform formal research, evidence collection, report framework building, or report drafting.

Mitigation: Use the outputs as task-scoping artifacts and route them to the appropriate downstream research workflow before relying on conclusions.

## Reference(s):

- [Intent Taxonomy](references/intent_taxonomy.md)
- [Output Contract](references/output_contract.md)
- [ClawHub Skill Page](https://clawhub.ai/leadleo/skills/wiki-intent-scope)
- [Publisher Profile](https://clawhub.ai/user/leadleo)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Chinese-language chat summary plus scope.md and scope.json files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The JSON handoff includes client_request, normalize, boundary_precheck, problem_transform, research_intent, scope_caliber, conclusion_risk, framework_depth, and handoff_record.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
