## Description: <br>
For client development with tokens on Solana, Light Token is 200x cheaper than SPL and has minimal changes. Skill includes guides for create mints, associated token accounts, transfer, approve, burn, wrap, and more. @lightprotocol/compressed-token (TypeScript) and light_token_client (Rust). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tilo-14](https://clawhub.ai/user/tilo-14) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill as a Solana Light Token cookbook for creating mints and token accounts, minting, transferring, approving, revoking, burning, wrapping, unwrapping, freezing, thawing, closing, and loading token accounts with TypeScript and Rust SDKs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples may sign and broadcast real Solana transactions, including transfer, mint, burn, freeze, close, wrap, and unwrap actions. <br>
Mitigation: Prefer localnet or devnet, use a dedicated low-value test wallet, and require explicit confirmation before any mainnet action. <br>
Risk: Devnet and mainnet examples may use RPC API keys and a local Solana keypair. <br>
Mitigation: Keep RPC keys and wallet material out of logs and commits, and load production credentials from a secrets manager. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tilo-14/solana-light-token-client) <br>
- [Light Token documentation](https://www.zkcompression.com) <br>
- [Light Token cookbook](https://zkcompression.com/light-token/cookbook/) <br>
- [Create mint](references/create-mint.md) <br>
- [Create associated token account](references/create-associated-token-account.md) <br>
- [Transfer interface](references/transfer-interface.md) <br>
- [Approve delegate](references/approve.md) <br>
- [Wrap SPL to Light](references/wrap.md) <br>
- [Unwrap Light to SPL](references/unwrap.md) <br>
- [TypeScript examples](https://github.com/Lightprotocol/examples-light-token/tree/main/typescript-client) <br>
- [Rust examples](https://github.com/Lightprotocol/examples-light-token/tree/main/rust-client) <br>
- [@lightprotocol/compressed-token API docs](https://lightprotocol.github.io/light-protocol/compressed-token/index.html) <br>
- [light-token-client Rust docs](https://docs.rs/light-token-client/latest/light_token_client/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript, Rust, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires caller review before executing examples that can sign or broadcast Solana transactions.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
