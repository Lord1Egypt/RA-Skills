## Description: <br>
YES.md 日本語版 guides agents through evidence gathering, safety gates, verification, and escalation when working on code, configuration, database, deployment, API, and data tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sstklen](https://clawhub.ai/user/sstklen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to keep implementation, debugging, configuration, deployment, API integration, and data work grounded in evidence, backups, impact checks, and post-change verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages proactive file checks, diagnostics, backups, and verification steps that may lead an agent toward shell commands or operational changes. <br>
Mitigation: Keep approval gates enabled for shell commands, deployments, database changes, and any action that could affect real systems. <br>
Risk: Strict workflow guidance may add operational overhead or block premature conclusions when evidence is incomplete. <br>
Mitigation: Use the skill for tasks involving code, configuration, databases, deployment, API integration, and data changes where evidence gathering and verification are appropriate. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sstklen/yes-md-ja) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code; single-file Japanese engineering workflow skill.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
