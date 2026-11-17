## Description:

Translates and localizes text, software strings, documents, subtitles, web content, and marketing copy across language pairs while preserving locale, terminology, formatting, and regulated-content constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, localization teams, and content owners use this skill to translate, review, and localize source material for products, documents, subtitles, websites, and regulated workflows. It is intended for translation and localization work, not for original single-language copywriting or audio caption generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may maintain persistent local translation records and shared contacts, project, and finance notes.

Mitigation: Install only when persistent local translation memory is desired, review declared storage paths first, and require confirmation before writes, deletions, migrations, or updates to shared records.

Risk: Confidential, client, legal, medical, or business material can be retained in notes if workflows are not tightly controlled.

Mitigation: Avoid storing full source documents unless explicitly requested, limit saved notes to necessary terms and decisions, and use local-only workflows for confidential or regulated material.

Risk: Machine translation or CAT workflows can involve external services and credential pointers.

Mitigation: Confirm what content would leave the machine before any machine-translation step, store only credential pointers, and keep secret values in environment variables or a password manager.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/translate)
- [Clawic Translate skill page](https://clawic.com/skills/translate)
- [Software strings guidance](artifact/software-strings.md)
- [Machine translation and post-editing guidance](artifact/machine-translation.md)
- [Regulated work guidance](artifact/legal-medical.md)
- [Quality review guidance](artifact/quality.md)
- [Translation memory guidance](artifact/translation-memory.md)
- [Working file templates](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown or plain text, with code or configuration snippets when translating structured files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce localized copy, translation reviews, glossary entries, locale decisions, LQA notes, subtitle edits, or implementation guidance.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
