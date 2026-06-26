## Description: <br>
For data pipelines, aggregators, or indexers, real-time account state streaming on Solana with light account hot/cold lifecycle tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tilo-14](https://clawhub.ai/user/tilo-14) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers building Solana data pipelines, aggregators, market makers, or indexers use this skill to design continuous Laserstream gRPC account-state streaming for Light token accounts, mint accounts, and compressible PDAs. It is intended for real-time state change notifications rather than simple point lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example streaming code may require RPC provider keys such as HELIUS_API_KEY. <br>
Mitigation: Keep RPC provider keys in environment variables or a secrets manager and avoid committing them to project files. <br>
Risk: Rust examples depend on external crates and provider endpoints. <br>
Mitigation: Review and pin Rust dependencies before production use. <br>
Risk: Repository search by helper agents can inspect files outside the intended task area. <br>
Mitigation: Limit any subagent or MCP file search to the intended project directory. <br>


## Reference(s): <br>
- [Light Protocol documentation](https://www.zkcompression.com) <br>
- [Shared Streaming Architecture](references/shared.md) <br>
- [Streaming Token Accounts](references/token-accounts.md) <br>
- [Streaming Mint Accounts](references/mint-accounts.md) <br>
- [Streaming Compressible PDAs](references/pdas.md) <br>
- [Streaming tokens toolkit](https://www.zkcompression.com/light-token/toolkits/for-streaming-tokens) <br>
- [Streaming mints toolkit](https://www.zkcompression.com/light-token/toolkits/for-streaming-mints) <br>
- [@lightprotocol/stateless.js API docs](https://lightprotocol.github.io/light-protocol/stateless.js/index.html) <br>
- [light-client docs](https://docs.rs/light-client/latest/light_client/) <br>
- [Photon indexer](https://github.com/helius-labs/photon) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Rust and TOML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires cargo to build referenced Rust examples; examples use user-supplied RPC provider keys.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
