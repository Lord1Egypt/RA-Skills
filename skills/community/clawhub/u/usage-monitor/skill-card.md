## Description:

Monitor any service usage dashboard and alert when threshold is reached. User-configurable URL and threshold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[strongking666](https://clawhub.ai/user/strongking666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure an agent-assisted check for service usage or quota dashboards and generate alerts when a configured usage threshold is reached.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured dashboard URLs may include sensitive account, session, token, signature, or query-string data.

Mitigation: Use stable HTTPS dashboard URLs that do not contain secrets, and avoid sharing alert messages with the full URL unless every recipient is authorized to see it.

Risk: The generated usage log can store the configured panel URL and usage details locally.

Mitigation: Keep config.json and usage-log.md out of source control and add repository-specific .gitignore entries before running the skill in a project.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/strongking666/skills/usage-monitor)
- [README](artifact/README.md)
- [Installation guide](artifact/INSTALL.md)
- [User guide](artifact/USER-GUIDE.md)
- [Configuration schema](artifact/config.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JavaScript helper output, alert text, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or update a local usage-log.md file with service name, threshold, usage percentage, remaining days, and the configured panel URL.]

## Skill Version(s):

2.0.0 (source: release metadata, README.md, USER-GUIDE.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
