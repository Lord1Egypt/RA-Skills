## Description: <br>
Generates alternative task plans for complex multi-step work, coordinates available tools or skills, and records concise task reports for later optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[louisding9527](https://clawhub.ai/user/louisding9527) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to break complex requests into short, medium, or long plans, compare execution strategies, ask focused clarification questions, and archive compact task reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local task reports may retain sensitive task details in shared or synced workspaces. <br>
Mitigation: Use the skill only where local task_reports retention is acceptable, and review or remove reports for sensitive work. <br>
Risk: The skill may read planning resource files from the workspace, parent directory, or home resource path and rely on stale resource records. <br>
Mitigation: Review plan_source.md contents and stale entries before relying on generated resource choices. <br>
Risk: Generated plans and success-rate estimates are advisory and may choose unsuitable tools or underestimate execution risk. <br>
Mitigation: Review proposed plans, resource choices, and clarification questions before execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/louisding9527/task-plan-generator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/louisding9527) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown task plans, clarification prompts, and compact task-report summaries with structured DATA blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local task report content intended for task_reports/YYYYMM and may reference plan_source.md lookup paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
