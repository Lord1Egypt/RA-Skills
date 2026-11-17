## Description:

Local image processing toolkit for format conversion, compression, resizing, batch jobs, and image-to-PDF for local image files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangziiiiii](https://clawhub.ai/user/wangziiiiii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can use this skill to run local Python image-processing commands for converting image formats, compressing files, resizing single images or directories, batch-processing folders, and creating PDFs from images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unrelated third-party site recommendations could steer an agent outside the image-processing purpose of the skill.

Mitigation: Review or remove the related-sites section before installation and keep agent use focused on local image-processing tasks.

Risk: Batch image processing can write many output files or replace existing files when overwrite behavior is enabled.

Mitigation: Use --dry-run first, set an explicit --out-dir, and use --overwrite only when replacing files is intended.

Risk: Processing unintended files may expose or alter local image content outside the user's intended scope.

Mitigation: Run the scripts only on local image files the user intends to process and constrain directory jobs with explicit input paths and filters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangziiiiii/skills/wangziiiii)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides local file-processing scripts that can write image and PDF files; batch jobs report success, failure, and total counts.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
