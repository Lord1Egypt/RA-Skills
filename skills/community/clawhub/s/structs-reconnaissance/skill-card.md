## Description:

Gathers intelligence on Structs players, guilds, planets, fleets, and galaxy state for scouting, defense checks, fleet monitoring, guild assessment, and competitive intelligence, with findings persisted to local intel notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abstrct](https://clawhub.ai/user/abstrct)

### License/Terms of Use:

MIT-0

## Use Case:

Structs players and guild operators use this skill to run reconnaissance queries, assess vulnerabilities, and update local dossiers before combat, raids, or strategic planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps local Structs intelligence notes under memory/intel, which may include sensitive strategy or opponent assessments.

Mitigation: Review or delete those local intel files when retained scouting records are no longer needed, especially if they include sensitive assessments.

Risk: Reconnaissance findings can become stale as Structs chain state changes.

Mitigation: Re-query relevant entities and check block height before relying on saved intelligence for time-sensitive decisions.

## Reference(s):

- [Structs Intel Memory](https://structs.ai/memory/intel)
- [Intel Memory README](https://structs.ai/memory/intel/README)
- [Threat Detection](https://structs.ai/awareness/threat-detection)
- [Opportunity Identification](https://structs.ai/awareness/opportunity-identification)
- [Combat Mechanics](https://structs.ai/knowledge/mechanics/combat)
- [Reading Opponents](https://structs.ai/playbooks/meta/reading-opponents)
- [Structs Guild Stack Skill](https://structs.ai/skills/structs-guild-stack/SKILL)
- [Database Schema](https://structs.ai/knowledge/infrastructure/database-schema)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with CLI commands, SQL examples, and local intel file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local memory/intel markdown files.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
