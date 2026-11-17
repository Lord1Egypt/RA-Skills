## Description:

Toc Trading helps users analyze Chinese A-share market signals, manage watchlists, simulate holdings and trades, and run challenge-style stock practice from natural-language commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuritu](https://clawhub.ai/user/wuritu)

### License/Terms of Use:

MIT-0

## Use Case:

Users following Chinese A-share markets can use this skill to review public market data, maintain a stock pool, simulate buy and sell decisions, track hypothetical performance, and practice challenge-based trading without executing real trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat simulated stock recommendations or challenge results as investment advice.

Mitigation: Treat outputs as informational practice only and verify any investment decision independently before acting.

Risk: Local JSON records may expose watchlists, simulated holdings, trades, recommendations, or challenge state on a shared machine.

Mitigation: Review local file permissions and clear stored records when using a shared or untrusted environment.

Risk: The skill contacts AKShare and Tushare for market data, and some Tushare-backed features can use a TUSHARE_TOKEN.

Mitigation: Install only if those market-data calls are acceptable, keep tokens in environment variables, and rotate or remove tokens after shared use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuritu/skills/toc-trading)
- [Skill manifest](artifact/SKILL.md)
- [Product design](artifact/docs/product-design.md)
- [Full product design](artifact/docs/product-design-full.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown and plain text responses, often with tables and short status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local JSON records for stock pools, simulated positions, trades, recommendations, and challenge state.]

## Skill Version(s):

1.0.0 (source: server release evidence, target metadata, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
