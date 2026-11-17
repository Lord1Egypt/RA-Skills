## Description:

Analyzes China A-share watchlists and holdings with deterministic sector-routed value scoring, separate trading-environment scoring, scenario valuation, data-gap reporting, constrained allocation references, and offline HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[holauv](https://clawhub.ai/user/holauv)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to review China A-share watchlists or holdings, produce transparent value scores and scenario valuations, identify data gaps, and generate allocation references constrained by user risk policy. It is intended for research-style portfolio review and reporting, not investment advice or automatic trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can invoke an npm data client with automatic npx execution.

Mitigation: Use a dedicated workspace and review or preinstall the data client before allowing automatic execution.

Risk: Portfolio screenshots, holdings, and generated ledgers may be stored as local plaintext files.

Mitigation: Avoid storing real portfolio data unless local plaintext storage is acceptable, and remove sensitive workspace files after review.

Risk: The security scan reports a snapshot write bug that can overwrite JSON files.

Mitigation: Patch and review snapshot date validation before relying on snapshot writes.

Risk: Financial scoring, valuation, and allocation references may be mistaken for investment advice.

Mitigation: Keep the documented disclaimer visible, require human review, and do not treat outputs as orders, return guarantees, or risk-limit guarantees.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/holauv/skills/stock-portfolio-advisor)
- [README](README.md)
- [Scoring model](references/scoring-model.md)
- [Indicator mapping](references/indicator-mapping.md)
- [Data playbook](references/data-playbook.md)
- [Backtesting](references/backtesting.md)
- [Valuation review archive](references/valuation-review-2026-09-05.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, html, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with tables, JSON scoring artifacts, shell command snippets, configuration files, and offline HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are deterministic Python-stdlib calculations when required inputs are supplied; reports include data coverage and gaps, and do not place trades.]

## Skill Version(s):

2.4.0 (source: server release metadata, SKILL.md frontmatter, README, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
