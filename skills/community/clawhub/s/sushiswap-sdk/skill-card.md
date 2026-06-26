## Description: <br>
TypeScript SDK integration guidance for the SushiSwap Aggregator, including typed helpers for token amounts, prices, quotes, and swap transaction generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xMasayoshi](https://clawhub.ai/user/0xMasayoshi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers building TypeScript or JavaScript SushiSwap integrations use this skill to install the SDK, request swap quotes, generate swap transaction data, validate inputs, and handle required referrer and fee considerations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated swap examples can sign and broadcast real blockchain transactions when a private key is provided. <br>
Mitigation: Use only developer-controlled integrations, never expose a primary wallet private key to an agent or logs, and require explicit approval before signing or broadcasting. <br>
Risk: Incorrect chain, token, amount, recipient, router, calldata, value, slippage, fees, or expected output could cause financial loss. <br>
Mitigation: Inspect all transaction fields and simulate or review the returned transaction data before any wallet signs it. <br>


## Reference(s): <br>
- [SushiSwap SDK Reference](references/REFERENCE.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/0xMasayoshi/sushiswap-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes integration steps, SDK method selection, required referrer handling, supported-network checks, and transaction review guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
