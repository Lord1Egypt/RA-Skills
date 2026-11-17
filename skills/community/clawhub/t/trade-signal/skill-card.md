## Description:

Provides real-time Buy/Sell/Hold trade signals and stock analysis for public securities across U.S. and global markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kslee9572](https://clawhub.ai/user/kslee9572)

### License/Terms of Use:


## Use Case:

External users and agent developers use this skill to request market research, trade signals, price targets, technical analysis, earnings analysis, analyst coverage, and citation-backed financial summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides broad trading recommendations through a remote API, and its outputs could be mistaken for personalized investment advice.

Mitigation: Review outputs carefully, treat them as informational market analysis, and do not use them as the sole basis for trades or investment decisions.

Risk: Queries may expose sensitive portfolio, account, or proprietary strategy details to a remote service.

Mitigation: Avoid sending confidential financial, account, portfolio, or proprietary strategy information in prompts.

Risk: The bundled search script has a command-execution flaw for crafted query input.

Mitigation: Fix the query encoding path before use and review the script before installation or execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kslee9572/skills/trade-signal)
- [Terminal X homepage](https://terminal-x.ai)
- [Terminal X API base](https://terminal-x.ai/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON responses with citation-backed analysis and optional Markdown-formatted narrative text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tickers, Buy/Sell/Hold trade signals, price targets, technical indicators, related analysis, and source citations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
