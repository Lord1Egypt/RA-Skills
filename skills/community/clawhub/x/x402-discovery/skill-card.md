## Description:

Discover x402-enabled services across multiple catalogs, including Bazaar, Agentic Market, x402-list.com, and .well-known/x402 manifests, to find services for a task by scanning machine-readable discovery surfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marketingkioldenburg](https://clawhub.ai/user/marketingkioldenburg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover x402-enabled HTTP services, inspect catalog and manifest metadata, compare pricing, and identify endpoints that match a task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Discovery commands make network requests to public x402 catalogs and service manifest URLs.

Mitigation: Review queried URLs before use and avoid including secrets, private endpoints, or sensitive task details in discovery requests.

Risk: Discovered services may be paid services with pricing or endpoint details that require review before use.

Mitigation: Inspect discovered pricing, schemas, and service metadata before invoking or paying for any service.

## Reference(s):

- [x402 homepage](https://www.x402.org)
- [x402 Bazaar discovery resources](https://api.cdp.coinbase.com/x402/discovery/resources)
- [x402-list services API](https://x402-list.com/api/services)
- [ClawHub skill page](https://clawhub.ai/marketingkioldenburg/skills/x402-discovery)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for command examples; produces discovery guidance rather than executable code.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
