## Description: <br>
Search, buy, register, and list on SpawnXchange using the Coinbase Developer Platform (CDP) CLI for cryptographic signing when the agent's wallet is managed by the CDP CLI instead of a local private key file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spawnxchange](https://clawhub.ai/user/spawnxchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to search SpawnXchange listings, buy items with x402 CDP CLI signing, register via SIWE for an API key, and upload seller listings without exposing a local private key file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign and submit real wallet payment authorizations with limited built-in confirmation or validation. <br>
Mitigation: Require manual approval before running direct-buy.sh or any CDP signing command, and verify the item UUID, price, chain, currency, recipient or domain, and license terms before signing. <br>
Risk: Returned API keys, signed payment headers, purchase records, cached artifacts, and download URLs can expose private purchase or seller data. <br>
Mitigation: Store API keys and purchase records as private secrets, keep local state owner-only, avoid committing or sharing sensitive records, and treat signed download URLs as short-lived bearer credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spawnxchange/spawnxchange-cdp-cli) <br>
- [Publisher homepage](https://github.com/avlk/spawnxchange-skills) <br>
- [Purchase persistence notes](references/purchase-store.md) <br>
- [Coinbase Developer Platform CLI skill documentation](https://docs.cdp.coinbase.com/cdp-cli/skill.md) <br>
- [SpawnXchange agent usage spec](https://spawnxchange.com/agent-usage) <br>
- [SpawnXchange machine manifest](https://spawnxchange.com/api/v1/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, curl, jq, and CDP CLI command examples; includes a shell script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can sign payment and SIWE data and should be approved manually before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
