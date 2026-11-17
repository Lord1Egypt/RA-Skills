## Description:

Systematic multi-step pipeline for sourcing, analyzing, verifying, and adapting Western product-market-fit startups to the Russian market with competitor and market filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reactlab23](https://clawhub.ai/user/reactlab23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, and startup operators use this skill to research Western startups with product-market fit, test whether analogous opportunities may work in Russia, and produce a practical MVP adaptation plan.

### Deployment Geography for Use:

Global; analysis and adaptation guidance are focused on the Russian market.

## Known Risks and Mitigations:

Risk: Startup idea details may be submitted to a third-party API during the red-team check.

Mitigation: Ask the user before external submission and send only a redacted summary when consent is given.

Risk: Candidate research notes may be retained in agent memory without clear limits.

Mitigation: Store only user-approved, sourced notes and define an expiration or deletion path.

Risk: Market, legal, and competitive guidance may become stale or regionally incomplete.

Mitigation: Verify payment, hosting, regulatory, and competitor claims against current authoritative sources before acting.

## Reference(s):

- [Startup Pipeline on ClawHub](https://clawhub.ai/reactlab23/skills/startup-pipeline)
- [Bundled skill workflow](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with structured tables and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-candidate strategy analysis, API-check summary, verifier table, GitHub library notes, and copy-paste MVP plan.]

## Skill Version(s):

3.2.0 (source: server release evidence; changelog: v3.2 fixed pipeline order)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
