## Description:

Provides domain-aware translation between Chinese and English and other requested language pairs, with formatting preservation and terminology handling for finance, legal, technology, and medical content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to translate documents, Markdown, tables, code comments, and structured content while preserving formatting and domain terminology.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: When a user provides a file path, the agent may read the file contents and create a translated copy.

Mitigation: Provide only files that may be processed in the agent environment, and review the translated copy before sharing it.

Risk: Legal, financial, medical, or technical translations can have downstream impact if terminology is wrong or context is ambiguous.

Mitigation: Use bilingual or format-preserving output for sensitive content and have a qualified reviewer check terminology, numbers, dates, and omissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaocaixia888/skills/zcx-translation-assistant)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Plain text or Markdown translations, with optional bilingual side-by-side or interlinear output and translated file copies.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves user-provided formatting where requested and may write translated file copies with a language or translated suffix when given a file path.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
