## Description:

Enable Shopify superpowers for OpenClaw. Get a massive boost in knowledge about everything related to Shopify in general and Shopify development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realm1lf](https://clawhub.ai/user/realm1lf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to orient agents for Shopify app, theme, API, extension, webhook, metafield, Hydrogen, headless, and deployment work. It routes the agent to bundled Shopify reference excerpts and reminds users to verify live API versions, scopes, and payload shapes against current Shopify documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled examples and guidance may trigger live Shopify reads or writes when connected to a real store.

Mitigation: Use test stores where possible, confirm shop domain, API version, access scopes, and require explicit human approval before destructive or customer-impacting operations.

Risk: Webhook examples may send live order data to a third-party webhook service.

Mitigation: Replace webhook.site examples with an endpoint controlled by the app developer or merchant before registering webhooks.

Risk: Production credentials could expose broad Shopify Admin API access.

Mitigation: Store tokens only in environment variables or secret storage and grant least-privilege scopes for the intended task.

Risk: Bundled Shopify reference material is a point-in-time snapshot and can become stale.

Mitigation: Verify API versions, payload fields, scopes, rate limits, and compliance-sensitive details against live shopify.dev documentation.

## Reference(s):

- [Shopify Developer Documentation](https://shopify.dev/)
- [ClawHub Skill Listing](https://clawhub.ai/realm1lf/skills/shopify-expert)
- [Overview](references/OVERVIEW.md)
- [Authentication and Secrets](references/AUTH.md)
- [Safety](references/SAFETY.md)
- [Sources and Versions](references/SOURCES_AND_VERSIONS.md)
- [Admin API](references/DOC_ADMIN_API.md)
- [Admin REST API](references/ADMIN_REST_API.md)
- [Tooling](references/TOOLING.md)
- [Connecting OpenClaw to Shopify](references/CONNECTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, API examples, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose live Shopify API calls when credentials, shop domain, API version, scopes, and user confirmation are available.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact frontmatter and bundled docs report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
