## Description:

Choose-your-own-adventure interactive fiction through your agent. Pre-built stories and a framework for building your own.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to play choice-driven interactive fiction through an agent and to build custom story scenarios with reusable templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Story progress and scenarios may be stored in a local JSON save file, and a configurable save path could overwrite files if pointed at an important path.

Mitigation: Use a dedicated save file path for story progress, avoid pointing it at important files, and keep independent backups of important local data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/story-time)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, code, configuration]

**Output Format:** [Plain text interactive story turns with optional JavaScript scenario code and local JSON save data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent output may include scene text, choices, inventory, and save or load state.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
