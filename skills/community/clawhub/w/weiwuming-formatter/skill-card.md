## Description:

Converts Word documents or pasted article text into editor-ready WeChat markdown using the Weiwuming publication syntax.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roloyty](https://clawhub.ai/user/roloyty)

### License/Terms of Use:

MIT-0

## Use Case:

Editors and agents use this skill to format source articles, uploaded .doc/.docx files, and pasted text into WeChat article markdown that follows the Weiwuming syntax, including editorial notes, source notes, bios, reading sections, staff credits, and follow blocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform web lookups and rehost images to a public image service.

Mitigation: Use it only with content and images that are appropriate for public lookup and public hosting; avoid confidential drafts, private image links, or unpublished media.

Risk: The skill injects fixed Weiwuming publication branding and reviewer text into each output.

Mitigation: Review the generated footer, staff credits, and attribution before publication, especially when branding or reviewer conventions are not appropriate.

## Reference(s):

- [Weiwuming Formatter ClawHub release](https://clawhub.ai/roloyty/skills/weiwuming-formatter)
- [Publisher profile](https://clawhub.ai/user/roloyty)
- [WeChat Article Editor Syntax Rules](artifact/references/syntax_rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown article output with image-processing notes and proofreading reminders]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include downloaded image handling, public image-host URLs when uploads succeed, and separate reminders for unresolved formatting or content issues.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
