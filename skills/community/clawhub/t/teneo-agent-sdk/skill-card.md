## Description: <br>
Teneo Agent SDK/CLI helps agents discover and query Teneo Protocol agents, manage rooms, and handle x402 USDC payments and encrypted wallet setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teneoprotocoldev](https://clawhub.ai/user/teneoprotocoldev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install and operate a Teneo CLI for discovering agents, querying specialized data agents, managing rooms, and handling USDC-based payments when required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage a Teneo payment wallet, automatically approve paid agent queries, and sign requested on-chain transactions. <br>
Mitigation: Use a fresh low-balance wallet, review prices before paid commands, and do not connect a wallet holding funds you cannot afford to spend. <br>
Risk: The wallet-export-key command can print a live private key. <br>
Mitigation: Treat exported keys as secrets, keep them out of logs and transcripts, and rotate or drain the wallet if a key is exposed. <br>
Risk: Supplying TENEO_PRIVATE_KEY can give the CLI authority over an existing wallet. <br>
Mitigation: Avoid TENEO_PRIVATE_KEY for valuable wallets and prefer an isolated wallet dedicated to this skill. <br>


## Reference(s): <br>
- [Teneo Protocol homepage](https://teneo-protocol.ai) <br>
- [@teneo-protocol/sdk npm package](https://www.npmjs.com/package/@teneo-protocol/sdk) <br>
- [ClawHub skill page](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk) <br>
- [x402 protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce JSON output from the Teneo CLI when commands are run with machine-readable options.] <br>

## Skill Version(s): <br>
1.0.21 (source: server release metadata; artifact frontmatter version 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
