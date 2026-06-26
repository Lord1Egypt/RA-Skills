## Description: <br>
当有规格说明或需要多步骤任务的需求时，在编写代码之前使用。根据 spec-design.md 生成可执行的 spec-plan.md。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mahingbun-dev](https://clawhub.ai/user/mahingbun-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn an existing spec-design.md into a concise, executable spec-plan.md with task steps and automated verification checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated plan can include implementation steps or verification commands based on project specs and nearby source context. <br>
Mitigation: Review the final Markdown tables, generated spec-plan.md, and verification commands before confirming or using the plan for later automation. <br>
Risk: The workflow reads project specifications and surrounding source context to produce the plan. <br>
Mitigation: Use it only in workspaces where that project context is appropriate to expose to the agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mahingbun-dev/sdd-writing-plans) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown file with task checklists and inline CLI, curl, or script verification commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes spec-plan.md beside the selected spec-design.md only after user review and confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
