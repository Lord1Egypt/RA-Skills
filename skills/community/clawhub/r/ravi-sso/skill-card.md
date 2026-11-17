## Description:

Gets short-lived identity verification tokens to prove a Ravi identity to third-party services that support Login with Ravi.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raunaksingwi](https://clawhub.ai/user/raunaksingwi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to obtain a fresh Ravi SSO token and pass it to a trusted third-party service for Login with Ravi flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SSO tokens are short-lived bearer credentials that can prove identity if exposed before expiry.

Mitigation: Send tokens only to trusted services over secure channels, preferably in HTTPS POST bodies or Authorization headers; do not log, cache, or share them.

Risk: Passing tokens through service-specific channels can lead to accidental exposure if a service asks for URL query parameters.

Mitigation: Prefer body or header transmission when the service supports it, and use query parameters only when required by the trusted service.

Risk: The verification endpoint is intended for third-party backends rather than the user or agent obtaining the token.

Mitigation: Use this skill only to request a fresh token and pass it to the target service; leave token verification to the service backend.

## Reference(s):

- [SSO Token API Reference](https://ravi.id/docs/schema/sso.json)

## Skill Output:

**Output Type(s):** [shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a short-lived bearer token with a documented 5-minute TTL; tokens should not be cached, logged, or shared outside the intended trusted service.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
