## Description:

AI-powered crypto trading agent and LLM gateway for natural-language portfolio checks, market research, swaps, transfers, NFTs, leverage trading, Polymarket betting, token deployment, automation, transaction signing and submission, and LLM access across Base, Ethereum, Polygon, Solana, and Unichain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riskiagung-prog](https://clawhub.ai/user/riskiagung-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to Bankr for crypto portfolio queries, trading workflows, wallet actions, token launches, prediction-market actions, and LLM gateway setup. It is intended for users who deliberately want an agent to operate through a dedicated, limited-funds Bankr wallet and API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through irreversible wallet actions including trades, transfers, signatures, automation, and raw transaction submission.

Mitigation: Require explicit human review before any trade, transfer, signature, automation, or raw transaction submission, and use read-only keys unless write access is required.

Risk: Bankr API and LLM gateway keys can grant powerful account access when stored or reused insecurely.

Mitigation: Use a dedicated, limited-funds agent wallet, separate Agent and LLM keys where possible, IP allowlisting, and avoid storing secrets in shell or IDE configuration.

Risk: The Bankr CLI is an external dependency required by the skill.

Mitigation: Pin or verify the CLI package before global installation and install it only in environments where Bankr access is intended.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/riskiagung-prog/skills/riskagent)
- [Publisher Profile](https://clawhub.ai/user/riskiagung-prog)
- [Bankr Homepage](https://bankr.bot)
- [Bankr API Portal](https://bankr.bot/api)
- [Bankr LLM Gateway](https://docs.bankr.bot/llm-gateway/overview)
- [Bankr API Workflow Reference](references/api-workflow.md)
- [Safety and Access Control Reference](references/safety.md)
- [Sign and Submit API Reference](references/sign-submit-api.md)
- [Arbitrary Transaction Reference](references/arbitrary-transaction.md)
- [Leverage Trading Reference](references/leverage-trading.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and REST API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include natural-language prompts, CLI commands, HTTP request examples, configuration guidance, and operational cautions.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
