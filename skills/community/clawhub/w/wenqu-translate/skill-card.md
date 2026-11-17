## Description:

文曲·翻译 translates English README files, papers, code comments, documentation, and articles into natural Chinese for reading and content creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gogoingai](https://clawhub.ai/user/gogoingai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content creators use this skill to translate single-article English materials into natural Chinese while preserving technical accuracy, terminology consistency, and Markdown structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a companion wenqu-review R2 review step for translation-tone quality control.

Mitigation: Before use, confirm that the companion review skill is installed and trusted, or perform the documented R2 review inline.

Risk: The skill may write persistent per-article translation preferences into project files.

Mitigation: Review any preferences.md changes as normal repository edits before committing or reusing them.

## Reference(s):

- [Translation guide](references/translation-guide.md)
- [Project source](https://github.com/gogoingai/wenqu-skills/tree/master/wenqu-translate)
- [ClawHub skill page](https://clawhub.ai/gogoingai/skills/wenqu-translate)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Natural Chinese prose, usually preserving the source Markdown structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for reader background before translation and may record per-article translation preferences as project changes.]

## Skill Version(s):

0.1.19 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
