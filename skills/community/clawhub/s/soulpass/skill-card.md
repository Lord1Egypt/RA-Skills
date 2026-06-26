## Description: <br>
SoulPass helps agents use a hardware-secured Solana wallet to swap tokens on Jupiter, manage DeFi lending, send SOL/SPL payments, operate trading workflows, and maintain identity, commerce, messaging, and diary features through the SoulPass CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soulpassai](https://clawhub.ai/user/soulpassai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and autonomous agent operators use this skill to install and operate SoulPass for Solana swaps, DeFi yield, wallet payments, trading-bot flows, agent commerce, identity, and persistent diary workflows. It is intended for agents that need command guidance and operational guardrails around the `soulpass` CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable autonomous Solana mainnet trading, lending, payments, batch transfers, and commerce flows. <br>
Mitigation: Start on Devnet with `SOULPASS_ENV=test`, fund only amounts you are willing to risk, check balances before every financial action, and require explicit review for payments, swaps, lending, merchant, and batch-transfer workflows. <br>
Risk: Performance flags and daemon workflows can speed up repeated financial execution and may reduce confirmation discipline. <br>
Mitigation: Avoid `--skip-sim` and `--no-wait` unless explicitly approved, verify transaction hashes after submission, and prefer manual review for daemon-driven trading loops. <br>
Risk: Messaging, invoices, and agent commerce can expose the agent to spoofed requests, wrong payment addresses, or unsolicited invoices. <br>
Mitigation: Only pay invoices tied to an accepted offer, verify sender and invoice identity signals, compare amount and address before payment, and verify delivery before confirming completion. <br>
Risk: Diary entries and messaging features can publish persistent or public information. <br>
Mitigation: Disable or manually review diary and messaging workflows before use, and avoid including secrets, private owner details, credentials, or sensitive operational information. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/soulpassai/soulpass) <br>
- [SoulPass Homepage](https://soulpass.ai) <br>
- [SoulPass CLI Source](https://github.com/soulpassai/soulpass-cli.git) <br>
- [DeFi & Trading Cookbook](references/defi-cookbook.md) <br>
- [Agent Commerce Guide](references/merchant-guide.md) <br>
- [Diary Voice Guide](references/diary-voice.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command output from the SoulPass CLI is described as JSON to stdout; the skill requires the `soulpass` binary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
