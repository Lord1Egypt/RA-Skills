## Description:

Use this skill when the user wants to install, configure, or troubleshoot the Shlink CLI from GitHub and manage short URLs, tags, visits, domains, and health checks through Shlink REST API v3.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parinll](https://clawhub.ai/user/parinll)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install, configure, and troubleshoot the Shlink CLI for managing short URLs, tags, visits, domains, and service health through the Shlink REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary identifies avoidable risk from installing unverified code.

Mitigation: Prefer a pinned, verified release or commit and review the skill carefully before installing.

Risk: The security guidance warns that SHLINK_API_KEY exposure can compromise access to the Shlink instance.

Mitigation: Never print or paste the full API key; use a least-privilege key and revoke it if it may have been shared.

Risk: The installation instructions include optional global installation with sudo.

Mitigation: Avoid sudo or global installation until provenance has been checked.

## Reference(s):

- [Shlink CLI GitHub repository](https://github.com/ParinLL/shlink-cli)
- [ClawHub skill page](https://clawhub.ai/parinll/skills/shlink-cli)
- [Publisher profile](https://clawhub.ai/user/parinll)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command examples, environment variable guidance, troubleshooting steps, and security cautions for Shlink API credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
