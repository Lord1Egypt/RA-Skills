## Description:

Provides developer guidance and code examples for using Solana Light Token client SDKs to create mints and token accounts, transfer tokens, approve and revoke delegates, burn, wrap, unwrap, freeze, thaw, close, and load accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tilo-14](https://clawhub.ai/user/tilo-14)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build Solana Light Token client workflows in TypeScript and Rust. It supports common token operations including mint creation, associated token accounts, transfers, approvals, burns, wrapping, unwrapping, freezing, thawing, closing, and account loading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples may sign Solana transactions that approve, burn, freeze, wrap, unwrap, transfer, or close token accounts.

Mitigation: Use devnet or a dedicated test wallet first, avoid production keypairs and funded mainnet accounts, and review each operation before execution.

Risk: Devnet and mainnet workflows require RPC endpoints, API keys, and wallet keypair configuration supplied by the user.

Mitigation: Verify RPC endpoints and API keys, store secrets outside source code, and load production credentials from a secrets manager.

Risk: Installing or running the skill from an unverified source could expose users to modified transaction examples.

Mitigation: Install only from a trusted source and pin or verify the repository version before use.

## Reference(s):

- [ZK Compression documentation](https://www.zkcompression.com)
- [Light Token cookbook](https://zkcompression.com/light-token/cookbook/)
- [Create mint](references/create-mint.md)
- [Create interface PDA](references/create-interface-pda.md)
- [Create associated token account](references/create-associated-token-account.md)
- [Create token account](references/create-token-account.md)
- [Mint to](references/mint-to.md)
- [Transfer interface](references/transfer-interface.md)
- [Transfer checked](references/transfer-checked.md)
- [Approve](references/approve.md)
- [Revoke](references/revoke.md)
- [Wrap](references/wrap.md)
- [Unwrap](references/unwrap.md)
- [Load associated token account](references/load-associated-token-account.md)
- [Burn](references/burn.md)
- [Burn checked](references/burn-checked.md)
- [Freeze](references/freeze.md)
- [Thaw](references/thaw.md)
- [Close token account](references/close-token-account.md)
- [Mint SPL, wrap, and transfer](references/spl-mint-wrap-transfer.md)
- [TypeScript Light Token examples](https://github.com/Lightprotocol/examples-light-token/tree/main/typescript-client)
- [Rust Light Token examples](https://github.com/Lightprotocol/examples-light-token/tree/main/rust-client)
- [@lightprotocol/stateless.js API docs](https://lightprotocol.github.io/light-protocol/stateless.js/index.html)
- [@lightprotocol/compressed-token API docs](https://lightprotocol.github.io/light-protocol/compressed-token/index.html)
- [light-token-client crate documentation](https://docs.rs/light-token-client/latest/light_token_client/)
- [Light Protocol audits](https://github.com/Lightprotocol/light-protocol/tree/main/audits)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript, Rust, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples may reference RPC endpoints, API keys, and local Solana keypair configuration supplied by the user.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
