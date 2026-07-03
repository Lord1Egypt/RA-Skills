## Description: <br>
SmartClaws guides OpenClaw agents and owners through onboarding for SKALE-based IoT telemetry, including plugin installation, wallet setup, role selection, and deployment configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eduv09](https://clawhub.ai/user/eduv09) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent owners use this skill to set up SmartClaws agents for blockchain-backed IoT telemetry and command workflows. It helps them configure plugins, wallets, roles, deployment facts, and owner-controlled operating contracts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup can involve wallet creation or import, sFUEL funding, role grants, and backups. <br>
Mitigation: Keep those steps owner-controlled, confirm intent before proceeding, and do not place private keys or secrets in SMARTCLAWS.md or AGENTS.md. <br>
Risk: Publishing and notifying are write actions that sign transactions. <br>
Mitigation: Allowlist write tools explicitly and rely on tool or CLI success responses before reporting balances, registrations, transactions, or published data. <br>


## Reference(s): <br>
- [SmartClaws ClawHub page](https://clawhub.ai/eduv09/skills/smartclaws) <br>
- [SmartClaws homepage](https://github.com/skalenetwork/smartclaws) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Owner decisions are required for wallet creation or import, sFUEL funding, role grants, backups, AGENTS.md adoption, and write-tool allowlisting.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
