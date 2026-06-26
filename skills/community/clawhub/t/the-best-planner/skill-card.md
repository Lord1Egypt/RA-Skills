## Description: <br>
规范 AI 公司任务流程，要求代理按计划书、用户确认、执行和汇报四个阶段完成工作。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xxxzhuo](https://clawhub.ai/user/xxxzhuo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers use this skill to make an agent slow down, produce a task plan, wait for explicit confirmation, execute the approved plan, and report results transparently. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The confirmation workflow can add extra planning prompts to ordinary tasks. <br>
Mitigation: Use the skill when explicit approval is desired, and review each plan before replying with the confirmation phrase. <br>
Risk: Approved plans may still include high-impact actions such as Git, deployment, API, or file-changing work. <br>
Mitigation: Check those steps carefully before approval and ask the agent to revise the plan when scope or risk is unclear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xxxzhuo/the-best-planner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown plans, confirmation prompts, execution logs, and completion reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes structured tables, checklists, and role-based workflow guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
