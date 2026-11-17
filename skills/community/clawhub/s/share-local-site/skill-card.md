## Description:

Share a local development server through a public URL for demos, mobile testing, colleague previews, and localhost sharing, with guidance for ngrok, localhost.run, cloudflared, and common host-header issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darwin7381](https://clawhub.ai/user/darwin7381)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to expose local development servers through public tunnel URLs for client demos, colleague review, mobile testing, pair programming, and quick external previews without deploying.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public tunnel URLs can expose a local development server more broadly than intended.

Mitigation: Use only non-sensitive development servers, verify the target port and page before sharing, avoid admin pages or real credentials, and stop the tunnel when the demo is done.

Risk: Host-validation bypass settings can weaken framework protections if left in place.

Mitigation: Apply host-check bypass settings only temporarily when needed for tunneling, do not commit or persist them, and remove them after use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/darwin7381/skills/share-local-site)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public tunnel URLs, local port checks, framework host-validation settings, and troubleshooting guidance.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
