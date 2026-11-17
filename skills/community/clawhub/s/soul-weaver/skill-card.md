## Description:

Soul Weaver generates OpenClaw agent configuration files from curated celebrity-style templates or custom user inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[addogiavara-tech](https://clawhub.ai/user/addogiavara-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to create persona-oriented agent configurations, either by selecting a local template or answering prompts for a custom configuration. The generated files are intended to be reviewed and installed into an OpenClaw workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated configuration files can persistently steer future agent behavior.

Mitigation: Review every generated file before installing it, especially SOUL.md, AGENTS.md, MEMORY.md, TOOLS.md, and HEARTBEAT.md.

Risk: Full replacement of an existing OpenClaw configuration can overwrite useful user settings or introduce behavior changes.

Mitigation: Create a backup first and prefer incremental installation or fusion mode unless full replacement is intentional.

Risk: API-key and custom prompt handling may expose sensitive data or introduce untrusted content.

Mitigation: Do not provide an API key for local template use, avoid untrusted custom prompt fields, and avoid running audit scripts where logs may capture secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/addogiavara-tech/skills/soul-weaver)
- [Publisher profile](https://clawhub.ai/user/addogiavara-tech)
- [Soul Maker](references/soul-maker.md)
- [Celebrity Template Reference](references/templates.md)
- [Tool Configuration Reference](references/tools.md)
- [Heartbeat Automation Guide](references/heartbeat-automation.md)
- [Never Forget Protocol](references/never-forget-protocol.md)
- [Proactive Playbook](references/proactive-playbook.md)
- [Security Patterns](references/security-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [JSON object containing guidance messages, template metadata, required tools, and generated Markdown configuration file contents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated configurations commonly include SOUL.md, IDENTITY.md, MEMORY.md, USER.md, TOOLS.md, AGENTS.md, HEARTBEAT.md, KNOWLEDGE.md, SECURITY.md, and WORKFLOWS.md.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
