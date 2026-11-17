## Description:

Residential proxy CLI with explicit V2 and legacy credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ultronprime2026](https://clawhub.ai/user/ultronprime2026)

### License/Terms of Use:

MIT

## Use Case:

Developers use ProxyClaw to retrieve HTTP(S) pages through IPLoop residential proxies, with country or state/city selection and optional sticky sessions. The CLI returns raw response text or a basic Markdown conversion for downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable proxy credentials are sent over unencrypted proxy connections.

Mitigation: Use encrypted transport to the proxy and keep proxy credentials private; HTTPS to the destination does not protect proxy authentication.

## Reference(s):

- [ProxyClaw documentation](https://proxyclaw.ai/docs.html)
- [ProxyClaw website](https://proxyclaw.ai)
- [ProxyClaw ClawHub release](https://clawhub.ai/ultronprime2026/skills/proxyclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Raw HTTP response text or basic Markdown-converted text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Markdown conversion strips HTML tags; it does not render JavaScript or extract structured data.]

## Skill Version(s):

3.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
