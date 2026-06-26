## Description: <br>
Onchain security scanner on Base that scans token approvals, detects honeypots, analyzes contracts for rugpull indicators, and scores contract safety through keyless read-only VIGIL API calls; revoke actions require separate Bankr authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vigilcodes](https://clawhub.ai/user/vigilcodes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External DeFi users, developers, and wallet operators use this skill to inspect Base wallet approvals and token contracts before trading or interacting with contracts. It surfaces VIGIL risk signals such as honeypot behavior, rugpull indicators, deployer reputation, liquidity context, scam reports, and safety scores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet and token addresses are sent to the hosted VIGIL service. <br>
Mitigation: Use the skill only when sharing those addresses with the VIGIL service is acceptable. <br>
Risk: The artifact bundles revoke and batch-revoke scripts that can initiate wallet-changing onchain actions even though normal scanning is framed as read-only. <br>
Mitigation: Run revoke scripts only after explicit user intent is confirmed and Bankr read-write authentication is deliberately enabled. <br>
Risk: The artifact includes reputation-reporting scripts that can submit external scam reports. <br>
Mitigation: Run reporting scripts only when the user intends to submit a report and has verified the address and supporting evidence. <br>


## Reference(s): <br>
- [VIGIL API Reference](artifact/references/api-reference.md) <br>
- [VIGIL Bankr Integration Guide](artifact/references/bankr-integration.md) <br>
- [VIGIL Contract Addresses](artifact/references/contracts.md) <br>
- [VIGIL MCP Service](https://mcp.vigil.codes) <br>
- [ClawHub Skill Page](https://clawhub.ai/vigilcodes/vigil-security-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a single wallet or token contract address as input; read-only scans call the hosted VIGIL service, while bundled revoke and reporting scripts require intentional separate actions.] <br>

## Skill Version(s): <br>
1.0.3 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
