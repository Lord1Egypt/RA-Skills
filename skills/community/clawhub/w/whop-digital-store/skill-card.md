## Description:

Build and manage a Whop store for digital products, SaaS licenses, memberships, and subscriptions, with guidance for product setup, API connection, license delivery, and affiliate payouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, developers, and store operators use this skill to plan and automate Whop product listings, license or access-link delivery, earnings checks, and affiliate payouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Whop API keys could be exposed through prompts, logs, or generated files.

Mitigation: Use a least-privilege WHOP_API_KEY where possible, store it only in approved secret settings, and keep it out of prompts, logs, and files.

Risk: Product creation, customer delivery, and affiliate payout actions can affect customers or funds.

Mitigation: Require manual review before creating products, sending access links, delivering license keys, or paying affiliates.

Risk: The artifact includes commercial earning claims and platform comparisons that may be outdated or unverifiable.

Mitigation: Verify current Whop terms, fees, and performance claims before relying on them for business decisions.

## Reference(s):

- [Whop API Documentation](https://whop.com/api)
- [Whop](https://whop.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python, shell, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API setup steps, product configuration examples, and implementation guidance for Whop store operations.]

## Skill Version(s):

1.0.14 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
