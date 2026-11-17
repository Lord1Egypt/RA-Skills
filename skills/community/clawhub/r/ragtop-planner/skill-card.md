## Description:

面向外部 OpenClaw 的达人推广方案制定 Skill。基于 RAGTOP 三个工具接口（list_kb/list_doc/retrieval）执行四阶段工作流：规则提炼、案例总结、达人筛选、方案生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qbs784](https://clawhub.ai/user/qbs784)

### License/Terms of Use:


## Use Case:

External OpenClaw users use this skill to produce influencer marketing plans from RAGTOP knowledge bases for rules, cases, and pricing. It guides agents through knowledge-base discovery, retrieval, candidate influencer selection, budget compliance checks, and final plan generation with source traceability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default RAGTOP endpoint uses plaintext HTTP while requests include an API token and business knowledge-base data.

Mitigation: Use only a trusted, approved RAGTOP endpoint, override the default with HTTPS, and use a scoped, rotatable token.

Risk: Retrieved knowledge-base text can influence generated marketing plans and may lead to incorrect, unsupported, or misleading recommendations.

Mitigation: Review generated plans against trusted source records and require traceability for key claims, influencer details, pricing, and budget calculations.

Risk: Invalid tokens, unauthorized knowledge bases, or missing required knowledge bases can stop or misdirect the workflow.

Mitigation: Validate `RAGTOP_API_TOKEN`, resolve the required `方案`, `案例`, and `价格` knowledge bases with `list_kb`, and stop with a clear remediation message when access or required data is missing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qbs784/skills/ragtop-planner)
- [FH Agentic Workflow](references/workflow.md)
- [FH Prompts for External Skill](references/prompts.md)
- [FH Skill Error Handling](references/error_handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional HTML table output and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final plans should include budget compliance checks and cite retrieved source records where available.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
