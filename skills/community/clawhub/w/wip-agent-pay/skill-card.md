## Description:

Give your agent a wallet. Fund with Apple Pay. Pay for paywalled content. x402 native.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent request funding, pay for x402-gated content, and mint one-time payment links with human approval and wallet controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may receive broad spending or wallet authority.

Mitigation: Use an isolated, low-balance wallet, require explicit user approval for every payment, and configure hard spend caps.

Risk: Untrusted worker responses or payment URLs may lead to unsafe execution or unintended spending before validation issues are fixed.

Mitigation: Avoid running the CLI against untrusted worker responses; validate URLs and require user confirmation before payment or shell execution.

Risk: Shared worker secrets and broad signing scopes can increase blast radius.

Mitigation: Scope worker secrets and signing permissions narrowly, avoid broad shared credentials, and rotate secrets if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/parkertoddbrooks/skills/wip-agent-pay)
- [x402 Protocol](https://www.x402.org/)
- [Coinbase Developer Platform](https://portal.cdp.coinbase.com)
- [Package README](README.md)
- [Technical Specification](SPEC.md)
- [Setup Guide](SETUP.md)
- [Technical Reference](REFERENCE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include payment URLs, wallet setup steps, budget settings, and approval prompts.]

## Skill Version(s):

1.0.2 (source: server release evidence, frontmatter, package.json, CHANGELOG released 2026-07-21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
