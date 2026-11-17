## Description:

Generates structured Chinese-language anime character sheets with persona, personality, catchphrases, clothing, relationship networks, and a consistency self-check.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyuming0823](https://clawhub.ai/user/liuyuming0823)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, writers, tabletop roleplaying users, and art commissioners use this skill to turn minimal or partial character ideas into complete Markdown character profiles. It is intended for text-only character design support, not image generation or full novel writing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated character sheets may include weak story structure if contradictory traits, ability costs, or tension relationships are omitted.

Mitigation: Use the bundled design checklist and require the final self-check to confirm those three elements before accepting the output.

Risk: The skill may create a character name that resembles a well-known character.

Mitigation: Use the artifact's name-collision checklist item and revise the name when it is too close in pronunciation, writing, or theme.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/liuyuming0823/ym-anime-character-sheet)
- [ClawHub skill page](https://clawhub.ai/liuyuming0823/skills/ym-anime-character-sheet)
- [Internal consistency checklist](references/design-checklist.md)
- [Character card template](templates/character-card.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Structured Markdown character sheet with a checklist-style self-check section]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only output; the skill states that it does not generate images, drawing prompts, scripts, online lookup, local file access, or persistent character storage unless the user explicitly requests export.]

## Skill Version(s):

0.1.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
