## Description: <br>
YES.md is a workflow-governance skill that guides agents to verify claims, investigate before asking, use available tools, and check changes before reporting completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sstklen](https://clawhub.ai/user/sstklen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical agents use this skill during implementation, debugging, configuration, deployment, API integration, and data processing tasks to maintain evidence-based investigation, safety gates, and verification before handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can activate frequently as a broad workflow guardrail, and its guidance may lead an agent to propose shell commands, deployments, database changes, or edits involving sensitive configuration. <br>
Mitigation: Keep approval prompts enabled for shell commands, deployments, database changes, and edits involving sensitive configuration or credentials; review proposed changes before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sstklen/yes-md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code] <br>
**Output Format:** [Markdown text with inline commands and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include verification evidence, safety checklist items, and structured handoff notes.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
