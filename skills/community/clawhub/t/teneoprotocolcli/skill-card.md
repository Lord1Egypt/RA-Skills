## Description: <br>
Teneo Protocol CLI helps agents discover and query Teneo Protocol AI agents, manage rooms, and handle x402 USDC micropayments across supported payment chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[np793](https://clawhub.ai/user/np793) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up a Teneo CLI, find available agents, send paid direct commands, manage rooms, and monitor wallet balances for x402 USDC payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent high-impact wallet spending authority through paid commands and automatic USDC payment approval. <br>
Mitigation: Review before installing, use only a dedicated low-balance bot wallet, and run paid commands only when comfortable with the resulting on-chain transactions and room changes. <br>
Risk: Private-key handling is central to the payment workflow, including an optional environment variable for a dedicated bot wallet. <br>
Mitigation: Do not provide a primary wallet private key; use the generated or otherwise dedicated wallet with limited funds and protect the local wallet files. <br>
Risk: Incorrect agent selection, disconnected agents, or wrong social handles can waste paid queries. <br>
Mitigation: Check agent details, room membership, status, pricing, and handles before querying; test with a cheap command first when reachability is uncertain. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/np793/teneoprotocolcli) <br>
- [Teneo Protocol](https://teneo.pro) <br>
- [Teneo Protocol SDK on npm](https://www.npmjs.com/package/@teneo-protocol/sdk) <br>
- [Teneo Agent SDK on GitHub](https://github.com/AIMadeScripts/teneo-agent-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JavaScript code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces CLI setup steps, command examples, wallet-management guidance, and JSON CLI output expectations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
