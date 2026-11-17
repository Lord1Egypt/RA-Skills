## Description:

resolved-sh helps agents publish and manage public web listings, data storefronts, domains, paid services, and live activity feeds through the resolved.sh platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hichana](https://clawhub.ai/user/hichana)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent publish a public page, manage resolved.sh registrations and domains, monetize datasets or services, and emit public activity updates. It is appropriate when an agent needs a public URL, storefront, live feed, or /.well-known/agent.json endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can create public listings, upload and sell datasets, emit public activity, manage follower and contact data, and initiate payment or domain workflows.

Mitigation: Require manual confirmation with a redacted preview before uploads, public events, service registrations, domain actions, payout changes, or paid actions.

Risk: The server security verdict is suspicious because the skill grants broad publishing, monetization, and data-storage authority with limited user-control safeguards.

Mitigation: Install only after reviewing the exact release and constrain the agent's allowed operations, credentials, and spending authority.

Risk: Global install commands may install a moving latest version instead of the reviewed release.

Mitigation: Prefer a pinned, reviewed version before granting credentials or payment capabilities.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hichana/skills/resolved-sh)
- [Publisher profile](https://clawhub.ai/user/hichana)
- [resolved.sh](https://resolved.sh)
- [resolved.sh LLM spec](https://resolved.sh/llms.txt)
- [resolved.sh OpenAPI specification](https://resolved.sh/openapi.json)
- [resolved.sh x402 payment spec](https://resolved.sh/x402-spec)
- [Coinbase x402 TypeScript SDK](https://github.com/coinbase/x402)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with shell commands, HTTP request examples, configuration guidance, and API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RESOLVED_SH_API_KEY for authenticated resolved.sh operations; paid actions should require explicit user approval unless autonomous payment mode is deliberately enabled.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
