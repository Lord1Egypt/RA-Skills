## Description: <br>
Helps developers build and maintain SecondMe platform apps, OAuth integrations, MCP integrations, open API usage, app scaffolds, and release workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daihaochen-mv](https://clawhub.ai/user/daihaochen-mv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to create and maintain SecondMe third-party apps and integrations, including OAuth setup, API guidance, control-plane changes, validation, and release submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local commands, call SecondMe APIs, and change app or integration records after confirmation. <br>
Mitigation: Review each proposed create, update, delete, secret regeneration, listing, validation, or release action before approving it. <br>
Risk: The skill stores access tokens, client secrets, telemetry settings, and analytics under ~/.secondme. <br>
Mitigation: Protect local credential files, keep file permissions restrictive, rotate exposed credentials, and keep telemetry off if local analytics logs are not desired. <br>
Risk: The skill includes an automatic update check and update command. <br>
Mitigation: Disable or remove the automatic update block unless self-updating behavior is explicitly desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/daihaochen-mv/secondme-dev-assistant) <br>
- [App Bootstrap](references/app-bootstrap.md) <br>
- [Control Plane Operations](references/control-plane.md) <br>
- [Feedback Preference Flow](references/feedback-prompt.md) <br>
- [Implementation Guidance & SecondMe Standards](references/implementation-guidance.md) <br>
- [MCP & Integration Implementation Guidance](references/mcp-integration.md) <br>
- [Open APIs for Third-Party Developers](references/open-apis.md) <br>
- [Release & Maintenance](references/release-maintenance.md) <br>
- [Requirements & Scaffold Plan](references/requirements-scaffold.md) <br>
- [SecondMe Develop](https://develop.second.me) <br>
- [SecondMe API Base](https://api.mindverse.com/gate/lab) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline code, shell commands, JSON payloads, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform confirmed SecondMe control-plane actions and write local credential, telemetry, or planning files when the workflow requires it.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
