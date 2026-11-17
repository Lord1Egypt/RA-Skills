## Description:

Scans token contracts across supported chains for honeypots, scam indicators, ownership controls, taxes, liquidity signals, and other security risks using Quick Intel's contract analysis API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azep-ninja](https://clawhub.ai/user/azep-ninja)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to scan token contracts before trading or integrating with a token, interpret Quick Intel risk signals, and choose wallet-safe x402 payment patterns. It is intended to provide security analysis data, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to trigger paid wallet-backed scans.

Mitigation: Require the agent to show the scan cost and ask for approval before each scan.

Risk: Programmatic payment-signing examples may under-validate what the wallet signs.

Mitigation: Prefer a managed wallet or a dedicated low-balance payment wallet, and check expected amount, token contract, recipient, chain, and EIP-712 domain before signing.

Risk: Using the service sends the token address and chain to Quick Intel.

Mitigation: Install and use the skill only when sharing those scan inputs with Quick Intel is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/azep-ninja/skills/quickintel-scan)
- [Quick Intel Docs](https://docs.quickintel.io)
- [Quick Intel](https://quickintel.io)
- [Quick Intel Gateway Discovery](https://x402.quickintel.io/accepted)
- [x402 Protocol](https://www.x402.org)
- [x402 EVM Exact Scheme](https://github.com/coinbase/x402/blob/main/specs/schemes/exact/scheme_exact_evm.md)
- [Quick Intel x402 Payment Reference](artifact/Reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON scan results, code examples, shell commands, and risk interpretation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate a paid read-only API scan through an x402-compatible wallet when the agent is configured to do so.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
