## Description:

Call any API without leaking credentials. Keychains proxies requests and injects real tokens server-side; your agent never sees them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smarcombes](https://clawhub.ai/user/smarcombes)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to make API requests through Keychains using credential placeholders instead of exposing real API keys or OAuth tokens to the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API requests and connected credentials are routed through a third-party credential proxy and vault.

Mitigation: Install only after accepting that trust boundary, use narrowly scoped credentials, and review approval pages before authorizing access.

Risk: The CLI creates a persistent local machine identity in ~/.keychains/ for authentication.

Mitigation: Verify machine revocation and local key rotation procedures before relying on the skill.

Risk: The skill can support high-impact write-capable or financial/account APIs.

Mitigation: Avoid broad or write-capable credentials unless necessary, and prefer least-privilege provider scopes.

## Reference(s):

- [Keychains homepage](https://keychains.dev)
- [Keychains dashboard](https://keychains.dev/dashboard)
- [Keychains security whitepaper](https://keychains.dev/api/whitepaper)
- [Python SDK](https://pypi.org/project/keychains/)
- [Client SDK](https://www.npmjs.com/package/@keychains/client-sdk)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline shell and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include placeholder credential variables and approval URLs for user authorization.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
