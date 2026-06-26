## Description: <br>
ZKGov helps agents query HashKey Chain testnet governance, manage voter registration, create proposals, cast anonymous zero-knowledge votes, and finalize outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blockchain-oracle](https://clawhub.ai/user/blockchain-oracle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when they want an agent to inspect ZKGov proposals, check voter status, register a wallet, create proposals, vote privately with zero-knowledge proofs, or finalize HashKey Chain testnet governance outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write actions can register wallets, create proposals, cast votes, or finalize governance outcomes on HashKey Chain testnet. <br>
Mitigation: Treat each write action as requiring explicit user approval before execution. <br>
Risk: The skill can use sensitive wallet credentials from ~/.zkgov/config.json or ZKGOV_PRIVATE_KEY. <br>
Mitigation: Use testnet-only keys, protect wallet configuration files and environment variables, and avoid reusing production private keys. <br>
Risk: The skill depends on external @zkgov MCP and CLI packages. <br>
Mitigation: Install and run the packages only when the publisher and package source are trusted for HashKey Chain testnet governance work. <br>


## Reference(s): <br>
- [ZKGov Skill Page](https://clawhub.ai/blockchain-oracle/zkgov) <br>
- [@zkgov/mcp package](https://www.npmjs.com/package/@zkgov/mcp) <br>
- [@zkgov/cli package](https://www.npmjs.com/package/@zkgov/cli) <br>
- [HashKey Chain Testnet RPC](https://testnet.hsk.xyz) <br>
- [HashKey Chain Testnet Explorer](https://testnet-explorer.hsk.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline tool names, CLI commands, and JSON-oriented command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI fallback should use --json for machine-readable command output.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
