## Description:

Turn your agent into an affiliate earner. Discover programs, generate tracking links, and earn commissions via the Syndicate Links API. Supports Stripe + Bitcoin Lightning payouts. Install this skill and your agent automatically becomes an affiliate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cmcgrabby-hue](https://clawhub.ai/user/cmcgrabby-hue)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to register an agent with Syndicate Links, discover affiliate programs, create tracking links, and check affiliate earnings. It is intended for affiliate monetization workflows where recommendations may include commission-tracking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Affiliate tracking can reduce the neutrality and transparency of product recommendations.

Mitigation: Use tracking links only with clear user disclosure and preserve recommendation quality independently of commission potential.

Risk: The skill requires external registration and local storage of an affiliate API key.

Mitigation: Run setup only in trusted environments, restrict credential-file permissions, and rotate or remove credentials when access is no longer needed.

Risk: The setup script is not suitable for shared environments unless credential and temporary-file handling are hardened.

Mitigation: Avoid shared hosts for setup, or harden file permissions and temporary-file handling before use.

## Reference(s):

- [API Examples](references/api-examples.md)
- [Syndicate Links Website](https://syndicatelinks.co)
- [Syndicate Links API Docs](https://syndicatelinks.co/docs)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with bash command examples and API endpoint tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses external Syndicate Links API calls and local affiliate API key configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
