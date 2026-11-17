## Description:

Builds and publishes web apps from an idea, or upgrades existing apps to Shipyard's standards for security, data handling, testing, deployment, and launch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philipposk](https://clawhub.ai/user/philipposk)

### License/Terms of Use:

MIT-0

## Use Case:

People with an app idea and developers maintaining an existing app use this skill to build, publish, test, or upgrade a Shipyard app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing setup can make an app publicly reachable or remove its login wall.

Mitigation: Confirm which deployments should be public and verify access controls before publishing; hiding a site from search engines does not restrict access.

Risk: AI features can send app content to external AI providers without clear privacy notices.

Mitigation: Disclose which content is sent to AI providers and review the full Shipyard plugin before enabling AI processing.

## Reference(s):

- [Shipyard new-app on ClawHub](https://clawhub.ai/philipposk/skills/shipyard-new-app)
- [Build rules](artifact/references/build-rules.md)
- [AI features and service keys](artifact/references/ai-and-keys.md)
- [API and MCP guidance](artifact/references/api-and-mcp.md)
- [Verification guidance](artifact/references/verify.md)
- [Shipyard plugin installation guide](https://github.com/philipposk/shipyard/blob/main/INSTALL.md)

## Skill Output:

**Output Type(s):** [Code, Files, Configuration instructions, Shell commands, Guidance]

**Output Format:** [Application source and configuration files, with concise Markdown guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create, test, and publish an app through Shipyard workflows; publishing requires the user's approval.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
