## Description:

AI Translator Pro is a prompt-only translation and localization skill that detects language pairs and domains, preserves document formatting, maintains terminology consistency, and can produce glossaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yqghlx](https://clawhub.ai/user/yqghlx)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to translate, localize, batch-convert, or review multilingual text while preserving Markdown, code blocks, tables, links, frontmatter, and terminology consistency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Translated content may be written to a file or Feishu document when the user asks for that output.

Mitigation: Only request file or Feishu document output when the content is intended to be saved there and the destination is approved for the text's sensitivity.

Risk: Domain-sensitive translations can still contain terminology, legal, medical, or localization errors.

Mitigation: Review high-impact translations with a qualified domain reviewer before external publication or operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yqghlx/skills/yqg-ai-translator-pro)
- [Publisher profile](https://clawhub.ai/user/yqghlx)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Plain text or Markdown, with optional file or Feishu document output when requested by the user.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May preserve source formatting, retain code and links unchanged, emit bilingual alignment, and append a glossary for terminology-heavy documents.]

## Skill Version(s):

3.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
