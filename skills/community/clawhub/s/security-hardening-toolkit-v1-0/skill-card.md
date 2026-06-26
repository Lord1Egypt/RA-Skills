## Description: <br>
Provides manual audit checklists and configuration guidance to harden OpenClaw/Aegis deployments against instance exposure, credential leakage, malicious skill installation, unauthorized gateway access, and post-compromise recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thebrierfox](https://clawhub.ai/user/thebrierfox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to review OpenClaw/Aegis deployments, audit exposed gateways and credential storage, verify skills before installation, and follow incident response checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hardening and incident response commands may interrupt services or require elevated privileges. <br>
Mitigation: Review each command before running it, back up configuration files, and plan for service interruption where applicable. <br>
Risk: Credential rotation workflows involve sensitive tokens and secrets. <br>
Mitigation: Rotate credentials through provider dashboards and avoid exposing secret values to the agent or workspace files. <br>
Risk: Checklist guidance can be misapplied if deployment paths, ports, or service names differ. <br>
Mitigation: Treat the skill as manual guidance and adapt commands to the verified local environment before execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/thebrierfox/security-hardening-toolkit-v1-0) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Manual checklist; review commands before execution and apply environment-specific judgment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
