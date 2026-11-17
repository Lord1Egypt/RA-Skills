## Description:

Translates legacy smart-home scene triggers into six-element spatial intents for S2-style orchestration, including manual override and avatar habit roaming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and smart-space integrators use this skill to inspect or demonstrate how rigid physical scene buttons can be translated into richer semantic intents for downstream home, timeline, and agent orchestration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes persistent local orchestration and memory records, including JSON files and a SQLite database.

Mitigation: Run it in a contained test directory and review generated folders and records before using the output in any real environment.

Risk: Unvalidated profile text can be forwarded into agent-like mandates for downstream systems.

Mitigation: Treat rendered_tracks.json and s2_chronos.db records as untrusted data and revalidate them before any downstream agent or device controller acts on them.

Risk: Smart-home scene intents may imply physical device, privacy, security, or wellness actions.

Mitigation: Require human review and environment-specific safety checks before connecting the translated intents to live smart-home or agent-orchestration systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-classic-scene-parser)
- [Space2 homepage](https://space2.world)
- [S2-SP-OS Classic Scene Semantic Parser whitepaper](artifact/S2-SP-OS-Ultimate-Whitepaper.md)
- [S2-SP-OS Chinese classic scene parser whitepaper](artifact/S2-SP-OS经典场景语义降维解析白皮书.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and Python-generated local JSON and SQLite records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces interactive console output and may create local S2 data folders, rendered_tracks.json, avatar_habits.json, house_topology.json, and s2_chronos.db when executed.]

## Skill Version(s):

1.1.0 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
