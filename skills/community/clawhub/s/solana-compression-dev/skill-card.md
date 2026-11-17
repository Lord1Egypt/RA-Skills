## Description:

Helps developers build Solana clients and programs that use Light Protocol compressed accounts for lower-cost, rent-free per-user state, DePIN registrations, nullifier PDAs, and custom compressed account operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tilo-14](https://clawhub.ai/user/tilo-14)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to implement and debug Solana compression workflows, including compressed PDA programs, client proof fetching, account packing, nullifier PDAs, and related error handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compressed-account examples may be unsafe if copied directly into production user-owned account flows.

Mitigation: Review update, reinitialize, close, burn, and batch-create flows before production use; add explicit owner or delegation checks and derive addresses from signer- or tenant-bound seeds where appropriate.

Risk: Devnet and mainnet workflows can rely on wallet keypairs and RPC API keys.

Mitigation: Prefer localnet and disposable wallets during development, avoid funded mainnet keypairs, and load API keys and payer keypairs from a secrets manager in production.

Risk: Mutable installation or tooling steps can change behavior across runs.

Mitigation: Pin installed tooling and skill source to reviewed versions before using generated guidance in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tilo-14/skills/solana-compression-dev)
- [ZK Compression documentation](https://www.zkcompression.com)
- [Compressed PDAs](references/compressed-pdas.md)
- [Client guide](references/client.md)
- [Nullifier PDAs](references/nullifier-pdas.md)
- [Error Codes Reference](references/error-codes.md)
- [Light Protocol skills source](https://github.com/Lightprotocol/skills)
- [Light Protocol program examples](https://github.com/Lightprotocol/program-examples)
- [light-sdk API documentation](https://docs.rs/light-sdk/latest/light_sdk/)
- [light-client API documentation](https://docs.rs/light-client/latest/light_client/)
- [stateless.js API documentation](https://lightprotocol.github.io/light-protocol/stateless.js/index.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Rust, TypeScript, TOML, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include localnet, devnet, and mainnet workflows; devnet and mainnet examples can require an API_KEY and Solana keypair configuration.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
