## Description:

Control Sony Bravia TVs on a local network through IP Control by sending IRCC remote commands, opening URLs in the TV browser, terminating apps, and running diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yardfarmer](https://clawhub.ai/user/yardfarmer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to generate guidance, shell commands, and helper code for controlling a Sony Bravia TV they own or administer on a trusted local network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a hardcoded TV pre-shared key and local TV address.

Mitigation: Replace hardcoded credentials with environment-specific values, rotate the exposed PSK before relying on it, and avoid committing real TV credentials.

Risk: The optional web server can expose TV-control endpoints on the local network without authentication.

Mitigation: Bind the server to localhost or add authentication, and run it only on a trusted network.

Risk: Diagnostic pages can send TV browser and device details back to the local server.

Mitigation: Run diagnostics only on TVs and networks you control, and review collected diagnostic data before sharing it.

Risk: Generated commands can power off the TV, switch inputs, open URLs, or terminate running apps.

Mitigation: Confirm the target TV address and intended command before execution, especially in shared or production environments.

## Reference(s):

- [ClawHub Sony Tv skill page](https://clawhub.ai/yardfarmer/skills/sony-tv)
- [Sony TV browser diagnostic report](artifact/docs/diag-report.md)
- [Sony TV browser diagnostic results](artifact/docs/diag-results.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, JavaScript, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local-network TV IP and pre-shared-key placeholders that must be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 2.0.0 local-development)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
