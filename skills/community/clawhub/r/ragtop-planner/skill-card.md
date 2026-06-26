## Description: <br>
面向外部 OpenClaw 的达人推广方案制定 Skill。基于 RAGTOP 三个工具接口（list_kb/list_doc/retrieval）执行四阶段工作流：规则提炼、案例总结、达人筛选、方案生成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qbs784](https://clawhub.ai/user/qbs784) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External OpenClaw users use this skill to orchestrate RAGTOP knowledge-base retrieval and generate influencer marketing plans with rules, case summaries, candidate selection, budget checks, and source-traceable conclusions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a trusted RAGTOP service endpoint. <br>
Mitigation: Confirm RAGTOP_API_URL points to an approved RAGTOP service, preferably HTTPS unless it is strictly on a trusted internal network. <br>
Risk: A broad or long-lived API token could expose knowledge-base access. <br>
Mitigation: Use a least-privilege, revocable RAGTOP_API_TOKEN and rotate it according to local credential policy. <br>
Risk: Sensitive business requirements or proprietary knowledge-base content may be sent to the configured service. <br>
Mitigation: Avoid sending sensitive content unless the configured RAGTOP service is approved to handle it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qbs784/ragtop-planner) <br>
- [Publisher profile](https://clawhub.ai/user/qbs784) <br>
- [FH Agentic Workflow](references/workflow.md) <br>
- [FH Prompts for External Skill](references/prompts.md) <br>
- [FH Skill Error Handling](references/error_handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown, API calls] <br>
**Output Format:** [Markdown with inline bash code blocks and generated HTML tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RAGTOP_API_TOKEN and optionally RAGTOP_API_URL; final plans should include budget compliance checks and traceable source references.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
