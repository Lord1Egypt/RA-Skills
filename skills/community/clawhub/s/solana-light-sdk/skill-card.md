## Description: <br>
Guides Solana developers through using Light SDK to build rent-free PDAs, token accounts, mints, DeFi routers, and Anchor or Pinocchio integrations with minimal program logic changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tilo-14](https://clawhub.ai/user/tilo-14) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to plan and implement Solana programs that use Light SDK for lower-rent PDAs, token accounts, mints, and DeFi router integrations across Anchor and Pinocchio patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Solana transaction examples can affect wallets, payer keys, tips, fees, and network endpoints if copied into a live environment without review. <br>
Mitigation: Review transaction examples before running them, use devnet or localnet first, and avoid funded wallets or mainnet payer keys until endpoints, payer identity, tip amounts, and fees are checked. <br>
Risk: The skill may inspect project files and use subagents to search the local repository during implementation planning. <br>
Mitigation: Install and run it only in a scoped project workspace, not from a home directory or a folder containing unrelated secrets. <br>
Risk: Guidance for blockchain programs may be incomplete or mismatched to the user's protocol, framework versions, or account model. <br>
Mitigation: Review generated plans and code against the target Solana program, run tests on localnet or devnet, and verify Anchor, Pinocchio, and Light SDK dependency versions before deployment. <br>


## Reference(s): <br>
- [ZK Compression Documentation](https://www.zkcompression.com) <br>
- [Anchor Pattern](references/anchor.md) <br>
- [Pinocchio Pattern](references/pinocchio.md) <br>
- [Client SDK](references/client-sdk.md) <br>
- [CPI Pattern](references/instructions.md) <br>
- [Router Integration](references/router.md) <br>
- [Testing](references/testing.md) <br>
- [FAQ](references/faq.md) <br>
- [light-sdk API Reference](https://docs.rs/light-sdk/latest/light_sdk/) <br>
- [light-token API Reference](https://docs.rs/light-token/latest/light_token/) <br>
- [Light Protocol Audits](https://github.com/Lightprotocol/light-protocol/tree/main/audits) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Rust, TypeScript, TOML, and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, cargo, and anchor for examples that build or test Solana programs; no environment variables are declared.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
