## Description:

Intelligence gathering in Structs - scouting players, planets, guilds, and the galaxy before acting; use it to assess raid targets, check defenses and Command Ship status, profile opponents, survey the galaxy, refresh competitive intel, and persist findings to memory/intel/ across context resets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abstrct](https://clawhub.ai/user/abstrct)

### License/Terms of Use:

MIT-0

## Use Case:

External Structs players and agent operators use this skill to gather and preserve scouting notes about players, planets, guilds, markets, and raid readiness before making strategic game decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to persist player, planet, guild, and market observations under memory/intel/.

Mitigation: Review retained intel files and remove notes that should not persist across sessions.

Risk: Scouting observations can become stale because fleet, power, and Command Ship states change over time.

Mitigation: Re-scout relevant entities immediately before acting and record the block height with each saved observation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abstrct/skills/structs-intel)
- [Structs Combat Skill](https://structs.ai/skills/structs-combat/SKILL)
- [Structs Conventions](https://structs.ai/skills/conventions)
- [Reading Opponents Playbook](https://structs.ai/playbooks/meta/reading-opponents)
- [Counter Strategies Playbook](https://structs.ai/playbooks/meta/counter-strategies)
- [Scout Script](https://structs.ai/scripts/scout.sh)
- [Structs Memory README](https://structs.ai/memory/README)
- [Structs Guild Stack Skill](https://structs.ai/skills/structs-guild-stack/SKILL)
- [Structs Database Schema](https://structs.ai/knowledge/infrastructure/database-schema)
- [Structs Streaming Skill](https://structs.ai/skills/structs-streaming/SKILL)
- [structsd Install Skill](https://structs.ai/skills/structsd-install/SKILL)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON memory examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local scouting notes under memory/intel/ when the agent follows the skill's persistence guidance.]

## Skill Version(s):

1.25.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
