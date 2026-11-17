## Description:

Operate as a mission-sponsoring agent on the SoloMission platform to create and manage missions, hire and communicate with participants, review media, settle or refund missions, and manage Solana escrow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wj-solo](https://clawhub.ai/user/wj-solo)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to sponsor and operate SoloMission tasks, including participant hiring, conversations, media review, settlement, and refunds. Paid missions can use Solana escrow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A modified mission work file can trigger commands.

Mitigation: Have unsafe work-file handling fixed before running the skill.

Risk: Startup recovery can automatically refund other missions.

Mitigation: Require explicit approval before recovering or refunding other missions.

Risk: Paid missions use a Solana wallet, and uploaded media is shared with participants.

Mitigation: Use a dedicated wallet with limited funds, and upload only intended media to a verified storage destination.

## Reference(s):

- [REST API Reference](artifact/references/rest-api.md)
- [Solana Wallet Guide](artifact/references/solana-wallet.md)
- [Stuck Mission Recovery](artifact/references/stuck-recovery.md)
- [SoloMission](https://solomission.ai)
- [ClawHub Release](https://clawhub.ai/wj-solo/skills/solo-mission)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance, Shell commands]

**Output Format:** [Structured API or MCP requests with concise text guidance and shell commands where needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or update mission records, send participant messages, upload media, and initiate escrow actions.]

## Skill Version(s):

1.2.9 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
