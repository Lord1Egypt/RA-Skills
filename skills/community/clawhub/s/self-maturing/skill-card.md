## Description: <br>
Self-reflection, correction logging, persistent memory, WAL protocol, cold-boot recovery, and automated daily review with self-healing cron. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joelsalespossible](https://clawhub.ai/user/joelsalespossible) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add correction logging, persistent working memory, cold-boot recovery, and recurring review behavior to an OpenClaw-style agent workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs persistent agent instructions and recurring automation that can rewrite core workspace control files. <br>
Mitigation: Install only when that behavior is intended; back up SOUL.md, AGENTS.md, IDENTITY.md, HEARTBEAT.md, SESSION-STATE.md, and ~/self-improving/ before use, and verify how to disable the cron and remove injected hooks. <br>
Risk: Persistent memory can capture sensitive or unwanted information if the agent records inappropriate content. <br>
Mitigation: Follow the documented security boundaries: do not store credentials or sensitive personal data, keep memory visible to the user, and support audit and deletion requests. <br>
Risk: Recurring review behavior may keep applying stale or incorrect lessons after context changes. <br>
Mitigation: Review proposed memory changes, keep self-inferred rules revisable, and remove or demote stale patterns during maintenance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/joelsalespossible/self-maturing) <br>
- [Setup](setup.md) <br>
- [Security Boundaries](references/boundaries.md) <br>
- [Learning Mechanics](references/learning.md) <br>
- [Memory Operations](references/operations.md) <br>
- [Scaling Rules](references/scaling.md) <br>
- [Heartbeat Rules](heartbeat-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local memory files, workspace hook files, and cron setup guidance when initialized.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact manifest reports 3.2.0 and SKILL.md frontmatter reports 3.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
