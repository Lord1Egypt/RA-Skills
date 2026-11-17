## Description:

For data pipelines, aggregators, or indexers, real-time account state streaming on Solana with light account hot/cold lifecycle tracking. Stream Light token accounts, mint accounts, and PDAs via Laserstream gRPC.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tilo-14](https://clawhub.ai/user/tilo-14)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build continuous Solana data pipelines, aggregators, market-making infrastructure, or indexers that need real-time Light Protocol token account, mint account, and PDA state changes instead of point lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command is not pinned to a source commit or installer version.

Mitigation: Verify the repository before installing and pin the installer version and source commit when possible.

Risk: Project environments may contain wallet keys, API credentials, or other secrets unrelated to the skill.

Mitigation: Run installation and example work from a restricted project environment without unnecessary wallet keys or API credentials present.

Risk: Rust examples copied into production may panic or mishandle network-supplied account data if used without hardening.

Mitigation: Add length checks and avoid unwrap() on network-supplied account data before using the examples in production.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tilo-14/skills/solana-stream-light)
- [ZK Compression Documentation](https://www.zkcompression.com)
- [Shared Streaming Architecture](references/shared.md)
- [Streaming Token Accounts](references/token-accounts.md)
- [Streaming Mint Accounts](references/mint-accounts.md)
- [Streaming Compressible PDAs](references/pdas.md)
- [Photon Indexer](https://github.com/helius-labs/photon)
- [Streaming Tokens Toolkit](https://www.zkcompression.com/light-token/toolkits/for-streaming-tokens)
- [Streaming Mints Toolkit](https://www.zkcompression.com/light-token/toolkits/for-streaming-mints)
- [@lightprotocol/stateless.js API Docs](https://lightprotocol.github.io/light-protocol/stateless.js/index.html)
- [light-client Documentation](https://docs.rs/light-client/latest/light_client/)
- [Light Protocol Audits](https://github.com/Lightprotocol/light-protocol/tree/main/audits)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with Rust code examples, shell commands, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires cargo for building referenced Rust streaming examples; no environment variables are required by the skill itself.]

## Skill Version(s):

1.0.2 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
