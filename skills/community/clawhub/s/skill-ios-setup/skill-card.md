## Description:

Sets up the OpenClaw iOS app by deploying the stats server, configuring access through domain/nginx, Tailscale, LAN, or manual setup, and returning connection details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parham-dev](https://clawhub.ai/user/parham-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect the OpenClaw iOS app to an OpenClaw installation. It checks the environment, starts the stats server when needed, guides the user through an exposure method, and summarizes the URL and token needed by the app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes a reusable gateway token in agent output.

Mitigation: Treat the token as a secret, avoid including it in shared chat logs or summaries, and rotate it if it is exposed.

Risk: The skill configures network access to OpenClaw for an iPhone.

Mitigation: Prefer a private network such as Tailscale or a properly secured reverse proxy, and avoid broad exposure unless the operator has reviewed the access path.

Risk: The skill can add an auto-restart cron entry for direct installs.

Mitigation: Add the reboot cron entry only after reviewing the resolved workspace path and accepting that a workspace script will run automatically after reboot.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/parham-dev/skills/skill-ios-setup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup choices, command snippets, connection details, status summaries, and error guidance.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
