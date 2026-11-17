## Description:

Chinese-language SMS RPG text-adventure engine that lets an agent generate wuxia story turns, manage JSON save slots, and present player choices without an external API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayshna](https://clawhub.ai/user/jayshna)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to run a Chinese-language wuxia text adventure, create or continue local saves, generate turn-by-turn narrative, and maintain goals, crises, NPC relationships, and world state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill manages local game saves and can create, read, update, or delete files under ./sms-rpg-saves/.

Mitigation: Use it in a dedicated game workspace and keep backups of saves that should not be overwritten or deleted.

Risk: The bundled test_save_system.py scripts can overwrite and delete slot 1 if run manually.

Mitigation: Do not run the test scripts in a directory containing real saves, or back up ./sms-rpg-saves/save_001.json first.

## Reference(s):

- [Drive Engine reference](artifact/references/drive-engine.md)
- [ClawHub skill page](https://clawhub.ai/jayshna/skills/sms-rpg)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown/text responses with JSON save structures and occasional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates, reads, updates, and deletes local save files under ./sms-rpg-saves/.]

## Skill Version(s):

3.0.1 (source: server release evidence and artifact version notes, released 2026-04-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
