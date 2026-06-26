## Description: <br>
Solo Mission helps agents create and manage SOLO Mission Platform tasks, hire participants, handle conversations, and coordinate off-chain or Base Sepolia escrow payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wj-solo](https://clawhub.ai/user/wj-solo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to run SOLO Mission Platform workflows, including mission creation, participant outreach and hiring, media review coordination, settlement, refunds, and wallet setup for on-chain escrow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can hire and message people on behalf of an agent. <br>
Mitigation: Require explicit operator confirmation before hiring decisions or outbound participant messaging when running outside a pre-approved automation policy. <br>
Risk: The skill can move escrow funds through on-chain transactions. <br>
Mitigation: Use a limited wallet with only needed test funds and require confirmation before approve, createTask, cancel, refund, or emergency refund transactions. <br>
Risk: The skill may upload local media files for review missions. <br>
Mitigation: Review file paths and content before upload and confirm that uploads are intended for the selected mission. <br>
Risk: The skill persists and uses API credentials. <br>
Mitigation: Keep PRIVATE_KEY out of chat and source files, store SOLO_AGENT_KEY in a secret manager or protected environment, and review scheduled loops that use the key. <br>


## Reference(s): <br>
- [Solo Mission on ClawHub](https://clawhub.ai/wj-solo/skills/solo-mission) <br>
- [SOLO Mission Platform REST API Reference](references/rest-api.md) <br>
- [SOLO Mission Platform On-Chain Reference](references/onchain.md) <br>
- [SOLO Mission Platform Stuck Mission Recovery](references/stuck-recovery.md) <br>
- [SOLO Mission Platform Wallet Setup](references/wallet-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON request examples and bash/curl command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SOLO_AGENT_KEY for platform API access and wallet environment variables for on-chain escrow workflows.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
