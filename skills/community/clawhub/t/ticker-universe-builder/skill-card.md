## Description:

Build and maintain auditable, evidence-gated ticker universes for fourteen markets at four depths, with TradingView watchlist exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitpunklabs](https://clawhub.ai/user/bitpunklabs)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, researchers and developers use this skill to assemble and maintain sourced market-observation watchlists and review their coverage. Its output is not investment advice or trade instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public market-data sources may be incomplete or stale, producing misleading watchlists.

Mitigation: Review cited sources, dates and validation results; do not treat watchlists as investment advice or trade instructions.

Risk: Running the bundled CLI writes watchlist and report bundles into the project.

Mitigation: Use a fresh output directory and pin a reviewed release or commit for reproducibility.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/bitpunklabs/skills/ticker-universe-builder)
- [Project homepage](https://github.com/bitpunklabs/ticker-universe-builder)
- [Coverage plan](references/coverage-plan.md)
- [Source policy](references/source-policy.md)
- [Output artifacts](references/output-artifacts.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Files]

**Output Format:** [TradingView TXT watchlists, JSON universes and validation results, and Markdown and offline HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dated sources, validation findings and partial-delivery status accompany outputs.]

## Skill Version(s):

0.9.1 (source: ClawHub release and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
