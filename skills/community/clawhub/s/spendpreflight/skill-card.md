## Description:

Screen public payees or preflight x402 payments with SpendPreflight. Offline hold by default; opt-in free OFAC and Lint, or human-approved paid checks through an existing x402 payment tool. Never requests keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wisted-1](https://clawhub.ai/user/wisted-1)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and agents use this skill to apply local spend policy and screen public payees or x402 payment challenges. It returns holds or blocks by default and can perform opt-in free checks or human-approved paid checks through an already connected x402 payment tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marked the release suspicious with medium confidence; two components were only partially inspected, and online checks send public inputs to an external service or may request paid checks.

Mitigation: Review the partially inspected components and decide whether external screening is appropriate. Keep offline mode unless online use is requested, and require fresh approval of the exact fee and service payee for each paid check.

## Reference(s):

- [Usage and payment-tool integration](references/usage.md)
- [SpendPreflight documentation](https://docs.spendpreflight.com/mcp/)
- [SpendPreflight ClawHub release](https://clawhub.ai/wisted-1/skills/spendpreflight)
- [SpendPreflight SDK 0.4.0](https://www.npmjs.com/package/spendpreflight/v/0.4.0)
- [Coinbase Wallet MCP x402 payments](https://docs.cdp.coinbase.com/ai-agents/coinbase-for-agents/wallet-mcp#make-x402-payments)
- [OpenClaw skill format](https://docs.openclaw.ai/clawhub/skill-format)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON screening or preflight result with decision and reasons, plus usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline hold or block by default; remote checks are opt-in and paid checks require fresh human approval.]

## Skill Version(s):

1.1.0 (source: package.json, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
