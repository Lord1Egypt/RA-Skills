## Description: <br>
Security audit + append-only logging + monitoring for OpenClaw skills (file-level diff, baseline approval, SHA-256 integrity). Requires Python >=3.9 and git. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ucloud-security](https://clawhub.ai/user/ucloud-security) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to statically audit OpenClaw skill directories, record append-only local audit logs, compare file and content diffs, manage approved baselines, and generate monitoring notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitoring notifications or raw diffs may expose sensitive workspace content if sent to an external channel. <br>
Mitigation: Confirm the notification target before enabling scheduled monitoring, send concise summaries by default, and review raw diffs for secrets before sharing them. <br>
Risk: Scheduled monitoring may scan an unintended workspace if cron is configured with the wrong path. <br>
Mitigation: Create cron jobs only after explicit user approval and verify the workspace path before enabling recurring scans. <br>
Risk: Agent-level semantic analysis may handle skill source context according to the hosting Agent deployment rather than the bundled scripts. <br>
Mitigation: Configure the hosting Agent's data handling policy appropriately, especially when audited skills may contain private code or credentials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ucloud-security/skills-auditor) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [scripts/README.md](artifact/scripts/README.md) <br>
- [templates/README.md](artifact/templates/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands plus local JSON and NDJSON audit artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local SHA-256 integrity fields, diff summaries, baseline state, and optional notification text.] <br>

## Skill Version(s): <br>
1.0.3 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
