## Description:

Configure Nginx as a reverse proxy with SSL/TLS via Let's Encrypt, security headers, HTTP/2, and gzip compression for any application on any VPS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[llcsamih](https://clawhub.ai/user/llcsamih)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure a VPS-hosted application behind Nginx with HTTPS, reverse proxying, certificate renewal, and production-oriented security headers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe live-server defaults or unreviewed commands could disrupt a production Nginx deployment.

Mitigation: Review the skill before installing or using it on a production server, and back up existing Nginx configs before changes.

Risk: Removing the default Nginx site, enabling HSTS includeSubDomains/preload, or adding renewal hooks can have lasting operational effects.

Mitigation: Require explicit approval before those actions, and test Nginx configuration before reloads.

Risk: DNS API tokens for automated wildcard certificates can expose domain control if over-scoped or mishandled.

Mitigation: Use narrowly scoped DNS tokens, store credential files with restrictive permissions, and review token handling before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with bash and Nginx configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses placeholders for domain, app port, VPS IP, email, certificate mode, and extra domains.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
