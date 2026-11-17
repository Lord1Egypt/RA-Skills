## Description:

Real-time financial data API for AI agents. Stocks, crypto, forex, ETFs. 120+ endpoints. Alternative to Alpha Vantage, CoinGecko. Works with Claude, Cursor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextfrontierbuilds](https://clawhub.ai/user/nextfrontierbuilds)

### License/Terms of Use:


## Use Case:

Developers and AI-agent users use this skill to resolve financial asset identifiers, retrieve real-time market data, scan tokens, inspect wallets, and summarize cross-market signals from the PRISM API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finance queries, asset symbols, contract identifiers, and wallet addresses may be sent to the configured PRISM API host.

Mitigation: Avoid confidential trading strategy, private portfolio details, or wallet addresses that should not be associated with the provider.

Risk: Broad finance-related prompts could trigger external PRISM API calls unintentionally.

Mitigation: Use explicit PRISM-related prompts and review generated requests before sharing sensitive identifiers.

## Reference(s):

- [Strykr PRISM API base URL](https://strykr-prism.up.railway.app)
- [Strykr Prism ClawHub release](https://clawhub.ai/nextfrontierbuilds/skills/strykr-prism)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and formatted financial summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses PRISM_API_KEY and an optional PRISM_URL override for API calls.]

## Skill Version(s):

1.1.2 (source: server release evidence; artifact frontmatter says 1.1.1 and skill.json says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
