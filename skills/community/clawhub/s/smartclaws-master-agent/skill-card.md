## Description:

Run one SmartClaws master control cycle: read device telemetry on-chain, decide under the owner's guidelines, command a device only when allowed, and log the decision on-chain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eduv09](https://clawhub.ai/user/eduv09)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to run a single SmartClaws control cycle that reads configured device telemetry, applies the owner's goal and authority rules, optionally commands one allowed device, and writes an on-chain decision log.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can command configured SmartClaws devices and create blockchain records.

Mitigation: Install it only for agents intended to operate those devices, and review SMARTCLAWS.md and AGENTS.md for commandable devices, authorized callers, owner goals, and decision-log expectations before use.

Risk: An incomplete setup or missing owner goal could cause an agent to act without enough operational context.

Mitigation: Require a configured SMARTCLAWS.md goal, device/channel wiring, matching device contract skills, and AGENTS.md authority rules; if these are absent, the skill should stop and ask the owner or run onboarding.

Risk: Encrypted channel reads, disclosures, publishes, or notifications may fail or remain scheduled because of permissions, missing viewing keys, unfunded wallets, or chain status.

Mitigation: Use the SmartClaws plugin status as authoritative, do not retry scheduled encrypted writes as new publishes, and report failures or setup gaps instead of claiming state changes.

## Reference(s):

- [SmartClaws project homepage](https://github.com/skalenetwork/smartclaws)
- [ClawHub skill page](https://clawhub.ai/eduv09/skills/smartclaws-master-agent)
- [Publisher profile](https://clawhub.ai/user/eduv09)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with plain-language decisions, tool-call guidance, and transaction status details when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SmartClaws publish or disclose status, transaction hashes, decision labels, device names, and setup guidance; never claims device or log success unless the plugin reports published status.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
