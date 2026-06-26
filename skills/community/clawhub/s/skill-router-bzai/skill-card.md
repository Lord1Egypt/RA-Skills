## Description: <br>
Cost-effective skill selector for maximizing ROI on AI operations that searches local skills and ClawHub, scores candidates by quality, token cost, security/reliability, and speed, and presents top recommendations for confirmation before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binziai7996](https://clawhub.ai/user/binziai7996) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to compare local and ClawHub skills for a task, estimate cost and speed, review security signals, and choose a recommended skill before installation or execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can search ClawHub with task details, which may expose sensitive task context. <br>
Mitigation: Require explicit approval before any ClawHub search that includes sensitive details, and summarize or redact sensitive inputs before searching. <br>
Risk: The skill may install and execute another selected skill, expanding the agent's effective behavior beyond the router itself. <br>
Mitigation: Require explicit user confirmation before any install or execution step, and review the selected skill's scan results and permissions first. <br>
Risk: Automated scoring may recommend a skill based on incomplete security or quality signals. <br>
Mitigation: Treat recommendations as decision support, manually review the top candidate, and reject skills with unclear permissions, suspicious behavior, or weak provenance. <br>


## Reference(s): <br>
- [Evaluation Rubric](references/evaluation-rubric.md) <br>
- [Security Checklist](references/security-checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/binziai7996/skill-router-bzai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown recommendations with ranked scores, security notes, estimates, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Top-3 ranked skill recommendations and require user confirmation before install or execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
