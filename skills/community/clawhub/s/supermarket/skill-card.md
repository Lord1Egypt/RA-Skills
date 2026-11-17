## Description:

Searches Kroger-family grocery products, finds store locations, adds items to a Kroger cart, and views profile information through the Kroger API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niemesrw](https://clawhub.ai/user/niemesrw)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search Kroger-family grocery products and stores, check local product details when location data is available, and manage a Kroger cart or profile after OAuth login.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hosted OAuth proxy handles Kroger OAuth tokens for account-linked cart and profile flows.

Mitigation: Review the proxy trust model before installation; use the skill only if the hosted proxy is acceptable, or self-host with fixed OAuth scopes and rate limits.

Risk: The skill may lead an agent to retain a Kroger refresh token across sessions.

Mitigation: Prefer secure keychain storage or avoid saving refresh tokens in agent memory; provide a clear logout or revocation path.

Risk: Token polling returns user access and refresh tokens to the agent after browser login.

Mitigation: Use short-lived login sessions, hard-to-guess session IDs, atomic token claiming, denied direct database access, and no token logging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/niemesrw/skills/supermarket)
- [Kroger Developer API](https://developer.kroger.com/)
- [Kroger Products OpenAPI](artifact/openapi/products-openapi.json)
- [Kroger Locations OpenAPI](artifact/openapi/locations-openapi.json)
- [Kroger Cart OpenAPI](artifact/openapi/cart-openapi.json)
- [Kroger Identity OpenAPI](artifact/openapi/identity-openapi.json)
- [Kroger Authorization OpenAPI](artifact/openapi/authorization-openapi.json)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON request or response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require OAuth login for cart and profile actions; product and location queries use short-lived client tokens.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
