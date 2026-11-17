## Description:

Guilds in Structs - choosing and joining one, ranks and rank-permissions, membership flows, settings, UGC moderation, charter vs entitlement founding, and the Central Bank (mint/redeem/convert).

This skill is ready for commercial/non-commercial use.

## Publisher:

[abstrct](https://clawhub.ai/user/abstrct)

### License/Terms of Use:

MIT-0

## Use Case:

External Structs players and operators use this skill to choose or join a guild, create and administer guilds, manage ranks and memberships, moderate member identity, and run guild token operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact guild administration or token commands can change membership, ownership, moderation state, or guild-token balances.

Mitigation: Review proposed rank changes, kicks, ownership transfers, UGC moderation, mint/redeem operations, and confiscate-and-burn commands before signing or broadcasting any transaction.

Risk: The skill provides command guidance but does not execute transactions automatically.

Mitigation: Use it only with an operator-controlled structsd setup and require explicit human approval for any generated transaction command.

## Reference(s):

- [Structs conventions](https://structs.ai/skills/conventions)
- [Guild Charter hashing mechanics](https://structs.ai/knowledge/mechanics/hashing#guild-charter)
- [Structs permissions](https://structs.ai/knowledge/mechanics/permissions)
- [UGC moderation mechanics](https://structs.ai/knowledge/mechanics/ugc-moderation)
- [Guild banking economy](https://structs.ai/knowledge/economy/guild-banking)
- [Structs factions lore](https://structs.ai/knowledge/lore/factions)
- [Guild war playbook](https://structs.ai/playbooks/situations/guild-war)
- [structs-permissions skill](https://structs.ai/skills/structs-permissions/SKILL)
- [structsd install skill](https://structs.ai/skills/structsd-install/SKILL)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory output for Structs guild operations; transaction commands require a local structsd client, a signing key, and human review before signing or broadcasting.]

## Skill Version(s):

1.25.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
