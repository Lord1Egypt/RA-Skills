## Description:

Search, list, resolve, and trade xStocks tokenized stocks on Solana using a hardcoded token catalog and optional Jupiter and wallet tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manu-xmint](https://clawhub.ai/user/manu-xmint)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill to identify xStocks by name, symbol, or Solana mint address and to prepare buy flows with standard Jupiter swaps and wallet signing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A simple amount or yes may be treated as permission to sign and broadcast a financial swap.

Mitigation: Require explicit final confirmation of the exact token, mint address, payment token, amount, quoted terms, and wallet before any signing or broadcast.

Risk: Partial mint-address lookups can select the wrong token.

Mitigation: Validate the full mint address and displayed token details before using the result in any transaction.

Risk: The hardcoded token catalog can become stale as xStocks listings change.

Mitigation: Check the referenced xStocks token API when a token is missing or before high-value trading decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/manu-xmint/skills/xstocks-beta)
- [Jupiter agent skills](https://github.com/jup-ag/agent-skills)
- [xStocks token API](https://api.xstocks.fi/api/v1/token)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, JSON, and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May output token names, symbols, Solana mint addresses, lookup errors, transaction guidance, and transaction status details.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
