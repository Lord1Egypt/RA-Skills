## Description: <br>
Session Bridge helps agents preserve short task context across surface switches and handoffs using lightweight topic capsules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeinonenight](https://clawhub.ai/user/codeinonenight) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create, refresh, hydrate, hand off, list, and expire compact session capsules when work moves across surfaces or between agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Capsules are local files that may contain sensitive project or personal context if users add it. <br>
Mitigation: Do not put secrets, credentials, or highly sensitive personal details in capsules, and delete or expire capsules when a topic is finished. <br>
Risk: Handoff text can carry incorrect, stale, or over-broad context to another agent or surface. <br>
Mitigation: Review handoff text before sending it and refresh capsules with current status, decisions, open questions, and next actions. <br>


## Reference(s): <br>
- [Session Bridge on ClawHub](https://clawhub.ai/codeinonenight/session-bridge) <br>
- [Publisher profile](https://clawhub.ai/user/codeinonenight) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON capsule files, Markdown capsule views, and compact text briefings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Hydrate and handoff outputs are designed as compact briefings of about 150-350 tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
