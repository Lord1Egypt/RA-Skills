## Description: <br>
A general employee-role agent skill that helps an agent receive tasks from a CEO coordinator, clarify requirements, execute work, report results, and handle follow-up within a five-turn limit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Moistenxx](https://clawhub.ai/user/Moistenxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Solo operators and agent-workflow builders use this skill to make an agent act as an employee that accepts assigned work from a CEO-style coordinator, asks concise clarification questions, produces structured deliverables, and responds to follow-up requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CEO/coordinator prompt and workspace SOUL.md role file determine the task and role the agent follows. <br>
Mitigation: Keep those inputs trusted and review assigned tasks before relying on the agent's output. <br>
Risk: A five-turn conversation limit can force a partial result when requirements remain unclear or external dependencies block completion. <br>
Mitigation: Require the agent to state blockers, open questions, and partial-completion status before the limit is reached. <br>


## Reference(s): <br>
- [Employee SOUL.md Template](references/employee_soul_template.md) <br>
- [Solo Employee ClawHub Release](https://clawhub.ai/Moistenxx/solo-employee) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Structured Markdown responses with task status, deliverables, clarifying questions, and optional code blocks or tables when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Limits employee-coordinator exchanges to five turns and expects the workspace SOUL.md role file to define the employee's specialization and communication style.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
