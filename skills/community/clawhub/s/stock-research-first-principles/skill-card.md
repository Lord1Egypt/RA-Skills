## Description:

Conduct evidence-first stock research with dated sources, data-quality gates, valuation, scenario analysis, falsifiable theses, and research-only recommendations for single-stock analysis, peer comparisons, sector or theme baskets, thesis reviews, and buy/hold/watch/pass questions without trade execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lee-agi](https://clawhub.ai/user/lee-agi)

### License/Terms of Use:

Apache-2.0 OR MIT-0

## Use Case:

External users and agents use this skill to produce auditable stock research for individual securities, peer comparisons, sector or theme baskets, and thesis reviews. It supports bounded research stances with dated evidence, valuation assumptions, explicit risks, and no trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be mistaken for a trading tool or personalized investment advice.

Mitigation: Use it only as a research assistant; reject outputs that request credentials, account details, portfolio values, broker payloads, order types, exact quantities, limit prices, or executable allocations.

Risk: Stock research can be misleading when sources are stale, incomplete, conflicting, or missing valuation support.

Mitigation: Require dated sources, retrieval times, source-quality labels, conflict handling, valuation assumptions, downside cases, invalidation conditions, and a clear research-only disclaimer before treating the work as complete.

Risk: The skill may activate implicitly for stock-research-like prompts and produce bilingual output.

Mitigation: Deploy where implicit stock-research assistance and bilingual English/Chinese responses are acceptable for the target users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lee-agi/skills/stock-research-first-principles)
- [Data Quality and Provenance](references/data-quality.md)
- [Safety and Communication](references/safety.md)
- [Valuation Standard](references/valuation.md)
- [Research Workflows](references/workflows.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Concise Markdown research packet, with optional JSON validation workflow and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual English and Chinese output by design; completed research must include dated sources, valuation, risk review, bounded stance, and a research-only disclaimer.]

## Skill Version(s):

0.1.1 (source: metadata.version, release.version, and SKILL.md version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
