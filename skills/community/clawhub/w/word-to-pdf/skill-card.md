## Description:

Convert Word documents (.docx) to PDF using Python's reportlab library, with support for Chinese characters, emojis, and basic formatting preservation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lirenweim](https://clawhub.ai/user/lirenweim)

### License/Terms of Use:

MIT

## Use Case:

Developers and document automation users use this skill to convert .docx files into PDF files from a command-line workflow, especially for documents that need Chinese text and emoji handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency versions are not pinned, which can make conversion behavior vary across environments.

Mitigation: Install in a virtual environment and use pinned versions for reportlab and python-docx.

Risk: Complex Word layouts, images, tables, numbering, and some emoji rendering may not be preserved accurately.

Mitigation: Use this for trusted or low-risk documents and manually review generated PDFs before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lirenweim/skills/word-to-pdf)
- [Publisher profile](https://clawhub.ai/user/lirenweim)
- [OpenClaw homepage listed by artifact metadata](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance, files]

**Output Format:** [Markdown guidance with command-line examples; runtime output is a PDF file and console status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The command accepts a required .docx input path and an optional PDF output path.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter, skill.json, _meta.json, and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
