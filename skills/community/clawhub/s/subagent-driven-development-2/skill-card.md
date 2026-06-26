## Description: <br>
Execute implementation plans by dispatching a fresh subagent per task with two-stage review for spec compliance and code quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to execute a prewritten implementation plan by assigning each discrete task to a fresh subagent and requiring review before moving on. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Subagents may produce changes that do not fully match the plan or project conventions. <br>
Mitigation: Keep tasks well scoped, enforce the spec and code-quality review gates, and review resulting commits before merging or deploying. <br>
Risk: Sensitive information can be exposed if secrets are included in task context. <br>
Mitigation: Avoid including secrets or credentials in plans, prompts, or subagent context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/subagent-driven-development-2) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only workflow; no API keys or external services are required by the evidence.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
