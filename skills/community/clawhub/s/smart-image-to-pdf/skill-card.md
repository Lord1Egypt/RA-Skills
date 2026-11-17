## Description:

Combine multiple image screenshots into a paginated A4 PDF. Intelligently handles page breaks to avoid cutting through text. Use when the user wants to combine, merge, or stitch images/screenshots into a PDF, especially exam papers or documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wxttt](https://clawhub.ai/user/wxttt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to combine screenshots, scanned document images, or exam paper images into a printable A4 PDF with automatic trimming and page splitting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime dependency resolution may download Pillow and numpy when they are not already available.

Mitigation: Use a trusted or pinned Python package environment when stronger supply-chain control is required.

Risk: The script reads local image inputs and writes a PDF to the requested output path.

Mitigation: Run it only on intended image-to-PDF tasks and review the output path before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Markdown or plain text status with an executable shell command and generated PDF file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill runs locally on user-provided image files and produces a PDF at the selected output path.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
