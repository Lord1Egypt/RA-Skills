## Description:

A comprehensive text analysis tool that counts words, characters, sentences, and paragraphs, and calculates reading time, speaking time, reading level, and keyword density.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, marketers, students, and developers use this skill to measure text length, estimate reading or speaking time, assess approximate readability, and review keyword frequency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The --file option reads a user-selected local file and prints derived statistics and keywords.

Mitigation: Analyze only files the user intentionally provides, especially when the text may contain sensitive or confidential content.

Risk: Readability and keyword-density values are estimates based on simple formulas and filtering.

Mitigation: Treat these metrics as drafting aids, not as definitive editorial, accessibility, compliance, or SEO decisions.

## Reference(s):

- [Text Analysis Formulas Reference](references/formulas.md)
- [ClawHub Word Counter skill page](https://clawhub.ai/openlark/skills/word-counter)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Plain text or JSON analysis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes word, character, sentence, paragraph, reading-time, speaking-time, readability, and keyword-density metrics.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
