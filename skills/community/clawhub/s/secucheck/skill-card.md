## Description: <br>
Secucheck performs read-only OpenClaw security audits across runtime, channels, agents, cron, skills, sessions, and network posture with localized reports, context-aware guidance, and an optional dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jooneyp](https://clawhub.ai/user/jooneyp) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use Secucheck to audit OpenClaw deployments for configuration, permission, runtime, session, skill, channel, cron, and network risks. It produces localized findings, context-aware recommendations, and a visual dashboard without automatically modifying configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect sensitive local details about OpenClaw configuration, agents, skills, runtime state, and network posture. <br>
Mitigation: Treat generated reports as sensitive and review them before sharing or storing them outside the audited environment. <br>
Risk: The dashboard may publish the generated security report on the local network. <br>
Mitigation: Use the dashboard only on trusted networks, or change it to bind to localhost before serving reports in shared or untrusted environments. <br>
Risk: Remediation advice may involve gateway, cron, or configuration changes that affect system behavior. <br>
Mitigation: Review each requested change and approve it explicitly only after considering functional impact. <br>


## Reference(s): <br>
- [Secucheck ClawHub listing](https://clawhub.ai/jooneyp/secucheck) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Runtime security checks](artifact/checks/runtime.md) <br>
- [Network security checks](artifact/checks/network.md) <br>
- [Agent security checks](artifact/checks/agents.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with JSON audit data, shell command suggestions, and optional HTML dashboard output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final reports are localized to the user's language and adjust explanation depth for beginner, intermediate, or expert audiences.] <br>

## Skill Version(s): <br>
2.8.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
