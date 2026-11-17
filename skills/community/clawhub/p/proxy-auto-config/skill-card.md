## Description:

Automatically detects local proxy settings and configures OpenClaw Gateway environment variables, proxy files, startup scripts, and scheduled checks for proxy-based network environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rutianze](https://clawhub.ai/user/rutianze)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to detect available local proxies and configure OpenClaw Gateway to run through those proxies in restricted network environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent network and security changes may affect existing Gateway traffic, proxy credentials, or scheduled tasks.

Mitigation: Review scripts before installation, remove TLS-disable settings, preserve existing crontab entries, and make persistence explicitly opt-in.

Risk: Proxy settings may route sensitive traffic through an unintended or untrusted proxy.

Mitigation: Confirm the selected proxy endpoint and credentials before applying generated environment variables or Gateway configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rutianze/skills/proxy-auto-config)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and generated configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose scripts and persistent proxy or Gateway configuration changes.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
