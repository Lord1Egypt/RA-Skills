## Description:

Compresses and converts local image batches with ImageMagick, reducing file size while preserving practical visual quality for uploads and web delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need an agent to propose local commands for shrinking image files, converting JPG/PNG assets to WebP, enforcing upload-size limits, or batch-optimizing images for faster web delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may propose local ImageMagick commands and package-manager installation commands.

Mitigation: Review commands before execution and approve installation only when ImageMagick is expected in the environment.

Risk: Bulk compression can process unintended images if the input folder or output path is too broad.

Mitigation: Confirm the input folder, target file patterns, and output directory before running batch commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-image-compress)
- [@iqinghu/qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include target quality, resize bounds, target file-size limit, output directory, and before/after size comparisons.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
