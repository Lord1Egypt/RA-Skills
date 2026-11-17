## Description:

Track learning across topics like an RPG skill tree. Prerequisites, milestones, suggested next steps. Gamified learning path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to track learning progress, prerequisites, milestones, unlocked topics, and suggested next steps across customizable learning trees.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Progress data is stored locally in a JSON file and could be lost, corrupted, or exposed if the chosen file location is unsuitable.

Mitigation: Use a dedicated data file path, apply normal local file permissions, and maintain backups for important learning records.

Risk: Trading-themed learning paths or suggestions could be mistaken for financial advice.

Mitigation: Treat trading curriculum suggestions as educational organization only, not financial, legal, trading, or professional advice.

## Reference(s):

- [Skill release page](https://clawhub.ai/theshadowrose/skills/skill-tree)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown text with JSON-like progress and suggestion objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write a local JSON progress file configured by dataFile.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
