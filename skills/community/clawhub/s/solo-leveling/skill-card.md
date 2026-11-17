## Description:

Solo Leveling is a life RPG skill that turns real-world habits into configurable quests, stats, ranks, dungeons, titles, and proof-based accountability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolmoses](https://clawhub.ai/user/anmolmoses)

### License/Terms of Use:


## Use Case:

External users use this skill to turn personal habits and goals into daily quests, status checks, XP, ranks, and weekly challenges. It supports configurable routines for fitness, coding, studying, creative work, sleep, and other recurring goals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Under-disclosed phone-call automation and persistent scheduled jobs could contact users or continue reminders without clear consent.

Mitigation: Remove or clearly disable call scripts and cron setup by default, and require explicit opt-in before enabling phone calls or scheduled jobs.

Risk: Audio, proof material, or habit-tracking data may be sent to external services or temporary public hosting.

Mitigation: Document each external service used and require explicit opt-in before public uploads, proof collection, or sending data to Twilio, ElevenLabs, transfer.sh, or messaging platforms.

Risk: Packaged runtime data can expose prior player state or quest history.

Mitigation: Delete packaged personal runtime data such as solo-leveling-data/player.json and solo-leveling-data/quest-log.json before release or installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anmolmoses/skills/solo-leveling)
- [Game Mechanics Reference](references/game-mechanics.md)
- [Configuration Template](references/config-template.json)
- [Balanced Preset](references/presets/balanced.json)
- [Developer Preset](references/presets/developer.json)
- [Fitness Preset](references/presets/fitness.json)
- [Student Preset](references/presets/student.json)
- [Creative Preset](references/presets/creative.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and text responses with JSON configuration files and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local JSON player state and quest logs; call, upload, proof-collection, and scheduled-job behavior should require explicit user opt-in.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
