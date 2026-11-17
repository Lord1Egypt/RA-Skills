## Description:

Write and typeset richly illustrated books with Typst, including text, CeTZ vector art, AI-generated images, and full layout control to PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bezkom](https://clawhub.ai/user/bezkom)

### License/Terms of Use:

MIT-0

## Use Case:

External authors, designers, and developers use this skill to create and typeset illustrated books in Typst, combining prose, CeTZ vector art, generated images, reusable layouts, and PDF or PNG compilation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install guidance downloads a mutable native Typst executable without checksum or signature verification.

Mitigation: Review and pin the Typst release before use; prefer an OS package manager or verify the downloaded binary before adding it to PATH.

Risk: The suggested install path can place a newly downloaded binary in a persistent user PATH location.

Mitigation: Only copy binaries into persistent PATH locations when intentionally approved for the environment.

Risk: Typst and CeTZ package use can require network access during setup or first compilation.

Mitigation: Use controlled package caches or review dependencies before compiling in restricted environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bezkom/skills/typst-book)
- [Typst Project](https://github.com/typst/typst)
- [CeTZ Reference for Book Illustrations](references/cetz-reference.md)
- [Typst Syntax Quick Reference](references/typst-syntax.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Typst code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce project structure, Typst source files, generated image prompts, PDF/PNG compilation commands, and visual review guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
