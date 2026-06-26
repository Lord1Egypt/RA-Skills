## Description: <br>
SolanaProx MCP lets agents send prompts to supported AI models through SolanaProx, using a Solana wallet and deposited balance instead of API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure an MCP-compatible assistant to check SolanaProx balances, estimate costs, list models, and make paid AI requests through SolanaProx. It is intended for workflows where wallet-based micropayments replace traditional API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, code snippets, model settings, and the configured wallet address are sent to SolanaProx and may be processed by upstream AI providers. <br>
Mitigation: Do not submit secrets, private keys, regulated data, or proprietary code unless the provider terms and controls have been reviewed. <br>
Risk: Calls to ask_ai can deduct from the user's deposited SolanaProx balance. <br>
Mitigation: Check balance and estimate cost before large or automated tasks, and require user confirmation before retrying failed or payment-related requests. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/unixlamadev-spec/solanaprox-mcp) <br>
- [SolanaProx homepage](https://solanaprox.com) <br>
- [SolanaProx API docs](https://solanaprox.com/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, configuration] <br>
**Output Format:** [Plain text MCP tool responses and Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool responses can include model output, balance details, cost estimates, available model lists, and error guidance.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
