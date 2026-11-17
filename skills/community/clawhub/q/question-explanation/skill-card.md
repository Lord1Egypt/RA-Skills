## Description:

Generate a complete HTML tutorial that explains one or more problems with clear reasoning and embedded SVG or Canvas visuals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vaintwyt](https://clawhub.ai/user/vaintwyt)

### License/Terms of Use:

MIT-0

## Use Case:

Students, educators, and agents assisting with problem solving use this skill to turn question images, screenshots, worksheets, exam problems, homework prompts, or pasted problem text into a self-contained HTML tutorial with step-by-step reasoning and visual explanations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can silently create or overwrite local HTML files when the user only expected a chat explanation.

Mitigation: Use it only when the user explicitly wants an HTML tutorial file, and use unique filenames or ask before overwriting existing files.

Risk: The trigger scope may be broader than desired for normal question-answering workflows.

Mitigation: Review the skill before installation and limit activation to requests for generated HTML tutorials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vaintwyt/skills/question-explanation)

## Skill Output:

**Output Type(s):** [text, code, guidance, files]

**Output Format:** [Self-contained HTML with embedded CSS, JavaScript, SVG, and Canvas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a local .html tutorial file and responds once after the file is saved and sent.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
