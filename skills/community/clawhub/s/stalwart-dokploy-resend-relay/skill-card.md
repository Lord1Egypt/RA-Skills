## Description:

Set up Stalwart Mail Server on a new VPS via Dokploy, with default outbound delivery through Resend SMTP relay for environments where direct SMTP port 25 egress is blocked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to deploy a self-hosted Stalwart mail server on a Dokploy-managed VPS and route outbound mail through Resend when direct SMTP port 25 egress is blocked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production deployment guidance may expose the Stalwart admin service if port 8080 is reachable from the public internet.

Mitigation: Restrict port 8080 to localhost or the reverse proxy and confirm public access is only through the intended HTTPS route.

Risk: The Resend API key could be spread to mail clients or other unintended locations.

Mitigation: Keep the Resend API key server-side in Stalwart and do not configure it directly in end-user mail clients except as a temporary reviewed fallback.

Risk: Using the unpinned Stalwart container tag can change deployed behavior across installs.

Mitigation: Pin the Stalwart image to a reviewed version or digest before production deployment.

Risk: Shell commands using sudo and production paths can modify the wrong VPS or volume if copied without review.

Mitigation: Run commands only on the intended VPS after confirming domains, mapped ports, and volume paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clarezoe/skills/stalwart-dokploy-resend-relay)
- [ClawHub publisher profile](https://clawhub.ai/user/clarezoe)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied domain, mail host, VPS SSH access, Dokploy access, and Resend API key.]

## Skill Version(s):

1.1.2 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
