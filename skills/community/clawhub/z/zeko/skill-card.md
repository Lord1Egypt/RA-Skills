## Description: <br>
Helps agents use and build on Zeko by selecting docs, endpoints, Bridge CLI or SDK workflows, faucet commands, GraphQL and curl queries, sequencer and archive guidance, and o1js or OCaml development paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hebilicious](https://clawhub.ai/user/hebilicious) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Zeko users, builders, and operators use this skill to bridge assets, request testnet funds, inspect Zeko and Mina endpoints, run terminal or API workflows, and build zkApps or protocol integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes workflows that handle private keys, signing, bridging, and transaction broadcasts. <br>
Mitigation: Use disposable testnet keys, avoid pasting real secrets inline, review commands before execution, and require explicit confirmation before signing, bridging, or broadcasting transactions. <br>
Risk: Generated bridge, faucet, or GraphQL commands can affect funds or network state when executed against live endpoints. <br>
Mitigation: Prefer public testnet routes for validation, start with small amounts, verify endpoints and routes, and inspect generated commands before running them. <br>


## Reference(s): <br>
- [ClawHub Zeko Skill](https://clawhub.ai/hebilicious/zeko) <br>
- [Zeko Agent Skills Docs](https://docs.zeko.io/developers/tools/agent-skills) <br>
- [Zeko Docs](https://docs.zeko.io) <br>
- [Bridge CLI Docs](https://docs.zeko.io/developers/tools/bridge-cli) <br>
- [Bridge SDK Docs](https://docs.zeko.io/developers/guides/bridge-sdk) <br>
- [Faucet CLI Docs](https://docs.zeko.io/developers/guides/faucet-cli) <br>
- [Custom Network Guide](https://docs.zeko.io/developers/guides/custom-network) <br>
- [o1js Docs](https://docs.o1labs.org/o1js/) <br>
- [Zeko Protocol Repository](https://github.com/zeko-labs/zeko) <br>
- [Agent Workflows](references/10-agent-workflows.md) <br>
- [Bridge, Faucet, And Agent Automation](references/30-bridge-and-faucet.md) <br>
- [Endpoints And Curl](references/40-endpoints-and-curl.md) <br>
- [Build On Zeko](references/50-build-on-zeko.md) <br>
- [Sequencer Archive And DA](references/60-sequencer-archive-and-da.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash, JavaScript, and GraphQL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that require local environment variables such as MINA_PRIVATE_KEY, GITHUB_TOKEN, PUBLIC_KEY, or ADDRESS.] <br>

## Skill Version(s): <br>
0.0.1-main.17.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
