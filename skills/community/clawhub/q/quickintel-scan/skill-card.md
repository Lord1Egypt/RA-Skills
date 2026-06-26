## Description: <br>
Scans token contracts across supported chains for honeypots, scam signals, ownership risks, permissions, taxes, and liquidity indicators using Quick Intel's contract analysis API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[azep-ninja](https://clawhub.ai/user/azep-ninja) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and trading agents use this skill to scan token contracts before trading and interpret Quick Intel risk signals such as honeypots, scam flags, owner permissions, taxes, and liquidity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scans may send token contract identifiers and chain names to Quick Intel and may involve x402 payment. <br>
Mitigation: Confirm each scan target and paid request before it runs, and avoid sending wallet secrets or unrelated sensitive data. <br>
Risk: Programmatic x402 signing can expose funds if a main wallet or raw private key is used. <br>
Mitigation: Use a managed wallet service or a dedicated low-balance hot wallet, and keep main wallet private keys and seed phrases out of prompts and skill configuration. <br>
Risk: Token scan results are point-in-time signals and are not financial advice. <br>
Mitigation: Treat results as one input, re-scan before acting, and cross-check high-value trades with independent block explorer and DEX or liquidity data. <br>


## Reference(s): <br>
- [Quick Intel x402 Payment Reference](Reference.md) <br>
- [Quick Intel Docs](https://docs.quickintel.io) <br>
- [x402 Protocol](https://www.x402.org) <br>
- [Quick Intel Accepted Payments](https://x402.quickintel.io/accepted) <br>
- [ClawHub Release Page](https://clawhub.ai/azep-ninja/quickintel-scan) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with JSON, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate paid Quick Intel scan requests when an x402-compatible wallet is configured.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
