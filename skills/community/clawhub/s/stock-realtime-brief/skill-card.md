## Description:

Stock Realtime Brief helps agents produce A-share market briefs, single-stock analysis, multi-stock comparisons, valuation checks, alerts, and portfolio risk summaries from public market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelliugh](https://clawhub.ai/user/michaelliugh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate A-share portfolio, single-stock, and multi-stock analysis briefs with explicit trigger levels, stop-loss lines, and risk checks. It supports watchlists, announcement checks, alerts, valuation checks, and trading-discipline reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Push and watch modes may send private stock alerts or reports to a packaged QQ account instead of a recipient selected by the user.

Mitigation: Change recipient handling to an account the user controls before enabling QQ push or watch mode.

Risk: Packaged fixed paths or shared secrets can expose portfolio data or TinyFish credentials across skill contexts.

Mitigation: Use explicit portfolio paths and private secret configuration; rotate any shared TinyFish API key if untrusted skills may have accessed it.

Risk: Financial outputs can be mistaken for investment advice or relied on despite stale or inaccurate third-party market data.

Mitigation: Treat outputs as analysis aids, verify data freshness and accuracy, and consult qualified financial professionals before making trading decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/michaelliugh/skills/stock-realtime-brief)
- [Methodology](docs/methodology.md)
- [Data Freshness Principle](docs/principles/data-freshness.md)
- [Trading Discipline](docs/principles/trading-discipline.md)
- [Disclaimer](DISCLAIMER.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown briefs with tables, JSON or configuration examples, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public A-share market data and optional portfolio or watchlist configuration; outputs are analysis aids and not investment advice.]

## Skill Version(s):

5.5.0 (source: frontmatter, pyproject.toml, CHANGELOG, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
