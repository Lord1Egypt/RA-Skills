## Description: <br>
SysClaw Ops guides a SysClaw operator agent through processing cross-agent requests, reviewing issues, setting verdicts, notifying agents, and managing the system_comm database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MBojer](https://clawhub.ai/user/MBojer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
SysClaw operators use this skill to triage pending agent requests, assess operational risk, update request status, execute approved infrastructure actions, and notify requesting agents. It is intended for an OpenClaw agent with scoped database and SSH access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill can guide an agent that changes databases and runs SSH actions on infrastructure. <br>
Mitigation: Install only on the intended SysClaw operator agent, restrict database and SSH roles to exact required grants, and define allowed hosts and commands before enabling it. <br>
Risk: Recurring notification processing can approve and execute low-risk requests automatically. <br>
Mitigation: Monitor the recurring job, verify request identity, require human confirmation for state-changing actions that exceed the allowed scope, and keep a worklog for executed actions. <br>
Risk: High-risk requests such as access grants, firewall changes, or production restarts can affect shared infrastructure. <br>
Mitigation: Escalate high-risk or urgent requests to the human operator and require explicit approval before changing shared infrastructure. <br>


## Reference(s): <br>
- [Database Schema Reference](references/db-schema.md) <br>
- [ClawHub release page](https://clawhub.ai/MBojer/sysclaw-ops) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with SQL examples, JSON configuration, and shell-command patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include verdict recommendations, notification text, worklog updates, database queries, and operator escalation guidance.] <br>

## Skill Version(s): <br>
1.6.2 (source: server release metadata; artifact _meta.json and CHANGELOG show 1.6.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
