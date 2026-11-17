## Description:

A quant-trading assistant that helps agents use the XG Quant Platform for historical market data, factor extraction, financial data analysis, strategy backtesting, simulated trading, and strategy management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li152](https://clawhub.ai/user/li152)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and quant-trading users use this skill to generate API-oriented guidance and Python examples for XG Quant Platform workflows, including market data retrieval, factor and financial analysis, backtesting, simulated trading, and strategy management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles account credentials and authorization tokens in API examples.

Mitigation: Use only trusted XG Quant servers, avoid real or reused passwords in examples, and prefer HTTPS and safer token handling where the service supports them.

Risk: The skill includes strategy deletion and clearing workflows that may be irreversible.

Mitigation: Run destructive strategy-management actions only after confirming the target account, strategy scope, and explicit user intent.

Risk: The server security verdict is suspicious because insecure HTTP examples appear in the skill evidence.

Mitigation: Review endpoint configuration before installation and avoid sending credentials to untrusted or plaintext endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/li152/skills/xg-quant-pt)
- [xg_quant_backtrader_data usage tutorial](https://gitcode.com/qq_50882340/xg_quant_backtrader_data)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python code examples and API usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account, authorization, server, and strategy-management parameters supplied by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
