## Description:

武侠X is a Chinese-language wuxia text adventure skill powered by Drive Engine v3 for goals, challenges, crises, progress tracking, five local save slots, and direct story generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayshna](https://clawhub.ai/user/jayshna)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run a Chinese wuxia text adventure, create or continue local save slots, and generate turn-by-turn narrative with goals, challenges, crisis events, state tracking, and action choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, and delete local save files under ./sms-rpg-saves/.

Mitigation: Confirm overwrite and deletion requests before changing save files, and keep file operations scoped to ./sms-rpg-saves/.

Risk: Generated game state can become inconsistent across long play sessions or damaged save files.

Mitigation: Use the skill's stated consistency rules, state-change records, and damaged-save handling before continuing a session.

## Reference(s):

- [Drive Engine 驱动引擎](references/drive-engine.md)
- [ClawHub skill page](https://clawhub.ai/jayshna/skills/wuxia-x)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Chinese Markdown-style game turns with structured JSON save-state data and local shell commands for save discovery.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses up to five local JSON save files under ./sms-rpg-saves/ and requires each turn to end with three to four action choices.]

## Skill Version(s):

3.0.1 (source: server release evidence and SKILL.md version history, released 2026-04-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
