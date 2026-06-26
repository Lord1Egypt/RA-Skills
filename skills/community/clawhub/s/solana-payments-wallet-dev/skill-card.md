## Description: <br>
Guides developers building stablecoin payment flows and wallet integrations on Solana using light-token, Privy, Solana wallet adapters, and optional nullifier-based duplicate action prevention. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tilo-14](https://clawhub.ai/user/tilo-14) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to plan and implement Solana payment and wallet flows, including receiving and sending tokens, displaying balances and history, signing transactions, and preventing duplicate payment execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment or wallet guidance can affect real Solana funds if token, amount, recipient, network, or signing details are wrong. <br>
Mitigation: Start on devnet and review every token, amount, recipient, network, and signing request before using real funds. <br>
Risk: Privy signing examples involve sensitive treasury credentials and external signing requests. <br>
Mitigation: Keep Privy treasury credentials server-side in a secrets manager, send them only to official Privy signing endpoints, and avoid exposing them to frontends or agent-wide environments. <br>


## Reference(s): <br>
- [zkCompression documentation](https://www.zkcompression.com) <br>
- [Payments docs](https://zkcompression.com/light-token/toolkits/for-payments) <br>
- [Wallets docs](https://zkcompression.com/light-token/toolkits/for-wallets) <br>
- [Payments and wallets examples](https://github.com/Lightprotocol/examples-light-token/tree/main/toolkits/payments-and-wallets) <br>
- [Nullifier program](https://github.com/Lightprotocol/nullifier-program/) <br>
- [stateless.js API docs](https://lightprotocol.github.io/light-protocol/stateless.js/index.html) <br>
- [compressed-token API docs](https://lightprotocol.github.io/light-protocol/compressed-token/index.html) <br>
- [payments.md](references/payments.md) <br>
- [wallets.md](references/wallets.md) <br>
- [sign-with-adapter.md](references/sign-with-adapter.md) <br>
- [sign-with-privy.md](references/sign-with-privy.md) <br>
- [nullifiers.md](references/nullifiers.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript, Rust, shell, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Solana transaction construction guidance, environment setup notes, and wallet signing review steps.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
