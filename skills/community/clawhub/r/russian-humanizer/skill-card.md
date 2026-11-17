## Description:

Russian Humanizer analyzes and rewrites Russian-language text to remove AI-slop markers, bureaucratic phrasing, artificial structure, and unnatural constructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horosheff](https://clawhub.ai/user/horosheff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, editors, and agents use this skill to audit Russian drafts for AI-generated cliches and to produce cleaner, more natural Russian rewrites. It also provides optional Glavred scoring for teams that accept sending text to glvrd.ru.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Glavred check sends user-provided text to glvrd.ru.

Mitigation: Do not use the Glavred tool with confidential drafts, personal data, customer text, or proprietary material unless that external submission is acceptable.

Risk: Automatic cleanup can change tone or meaning while removing stylistic markers.

Mitigation: Review rewritten or auto-fixed output before publishing or sending it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horosheff/skills/russian-humanizer)
- [README](README.md)
- [Transformation examples](references/examples.md)
- [Phrases to remove](references/phrases.md)
- [Structures to avoid](references/structures.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text or Markdown reports with rewrite guidance and optional cleaned Russian text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally send submitted text to glvrd.ru for style scoring when the Glavred tool is used.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
