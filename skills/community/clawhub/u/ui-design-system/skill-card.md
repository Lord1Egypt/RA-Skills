## Description:

Provides UI design guidance for selecting color themes, generating custom palettes, applying soft, minimalist, or brutalist aesthetics, and combining those choices into coherent frontend outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and frontend agents use this skill to choose UI color themes, aesthetic variants, typography, motion, and component rules before producing interface guidance or frontend code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad triggers may activate the skill more often than intended.

Mitigation: Confirm the user is asking for UI theme, aesthetic, or design-system guidance before applying the skill.

Risk: The artifact references a placeholder image URL for cases where real assets are unavailable, which may be unsuitable for privacy-sensitive or offline work.

Mitigation: Use approved local or project-provided assets, or remove placeholder-image usage when network access or external media sources are not acceptable.

Risk: Design guidance can produce visually polished but contextually incorrect UI decisions if applied without review.

Mitigation: Review generated palettes, typography, accessibility contrast, and component choices against the target product requirements before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/ui-design-system)
- [Soft aesthetic reference](artifact/references/soft.md)
- [Minimalist aesthetic reference](artifact/references/minimalist.md)
- [Brutalist aesthetic reference](artifact/references/brutalist.md)
- [Preset theme definitions](artifact/themes/)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with CSS variables, frontend code patterns, and design-system recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include theme palettes, typography choices, aesthetic rules, component guidance, and frontend implementation snippets.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
