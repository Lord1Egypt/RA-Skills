## Description:

Detects and rewrites English text to reduce AI-writing signals through calibrated, multi-pass editing while preserving meaning, register, and authorial voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[idcesares](https://clawhub.ai/user/idcesares)

### License/Terms of Use:

MIT-0

## Use Case:

External users, writers, and editors use this skill to identify AI-writing artifacts in English text, rewrite drafts in a more natural human voice, and optionally score AI-likeness. It is intended for editing workflows where meaning, genre, and authorial register need to be preserved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is explicitly designed to make AI-generated English text look less AI-generated and may be used to conceal authorship or AI-use provenance.

Mitigation: Use it only in editing contexts where reducing AI-like style is appropriate, and avoid academic, legal, hiring, moderation, or disclosure-sensitive settings where provenance matters.

Risk: Broad trigger language may activate the skill for ordinary cleanup requests.

Mitigation: Confirm the user's intent and context before applying a full rewrite, and use light-touch editing or no rewrite when the text does not show clear AI-pattern density.

## Reference(s):

- [Genre playbooks](references/genre-playbooks.md)
- [AI vocabulary by era](references/vocabulary-by-era.md)
- [Structural patterns](references/structural-patterns.md)
- [Statistical guide](references/statistical-guide.md)
- [Anti-patterns](references/anti-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, analysis]

**Output Format:** [Plain text or Markdown rewrite with optional change summary and scoring notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [English-only; output detail varies by input length and requested mode.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
