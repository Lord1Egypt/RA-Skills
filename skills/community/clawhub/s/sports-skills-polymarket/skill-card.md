## Description:

Polymarket sports prediction markets skill provides live odds, prices, order books, events, series, and market search across major sports with read-only commands that require no authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonelli182](https://clawhub.ai/user/antonelli182)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer sports prediction-market questions by finding Polymarket events, prices, order books, and price history. It can also guide wallet-backed trading commands when the user intentionally enables trading access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet-backed trading commands can place or cancel orders and require a private key.

Mitigation: Prefer read-only market-data commands without a wallet; only configure a limited-purpose wallet/private key when trading is intentional.

Risk: The security summary says wallet-backed trading and private-key setup are documented without enough upfront disclosure or safety controls.

Mitigation: Review the skill carefully before installation, isolate dependency and key handling, and do not provide a real private key unless trading is intentional.

Risk: Using a market_id where a CLOB token_id is required, or omitting the sport parameter for single-game searches, can produce incorrect or empty market data.

Mitigation: Fetch market details before price, order-book, or history calls to obtain token IDs, and pass the relevant sport code when searching single-game markets.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/antonelli182/skills/sports-skills-polymarket)
- [Polymarket API Reference](references/api-reference.md)
- [Polymarket APIs](references/api.md)
- [Valid Commands & Common Mistakes](references/commands.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline command examples and parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only market-data commands need no authentication; trading commands require py_clob_client and an explicitly configured wallet private key.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact frontmatter reports 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
