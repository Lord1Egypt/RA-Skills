## Description:

Generates, edits, and reads PowerPoint presentations using PptxGenJS for new decks, XML workflows for existing PPTX templates, and MarkItDown for text extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fusuvae-art](https://clawhub.ai/user/fusuvae-art)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to create polished PPTX decks, adapt existing PowerPoint templates, or extract presentation text for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned global dependency installation can affect the host environment more broadly than the skill requires.

Mitigation: Install the skill in an isolated or disposable project and prefer local, pinned dependencies for PptxGenJS, MarkItDown, and optional icon tooling.

Risk: Presentation generation and template editing can overwrite existing slide modules, unpacked XML, images, or PPTX outputs when paths are reused.

Mitigation: Review output paths before generation or template edits, preserve original templates, and stage repacked PPTX files in /tmp before copying final outputs.

Risk: Generated presentations can contain placeholder text, missing content, or corrupted PPTX formatting if PptxGenJS and XML constraints are missed.

Mitigation: Run the documented MarkItDown extraction checks, placeholder scans, and preview or final deck verification before using the generated presentation.

## Reference(s):

- [PptxGenJS Documentation](https://gitbrent.github.io/PptxGenJS/)
- [MarkItDown](https://github.com/microsoft/markitdown)
- [Slide Page Types](references/slide-types.md)
- [Design System](references/design-system.md)
- [Editing Existing Presentations](references/editing.md)
- [QA Process and Common Pitfalls](references/pitfalls.md)
- [PptxGenJS Tutorial](references/pptxgenjs.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JavaScript slide modules, extracted text, and PPTX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate slide source files, image assets, unpacked PPTX XML trees, and final or preview PowerPoint decks.]

## Skill Version(s):

1.0.0 (source: server evidence, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
