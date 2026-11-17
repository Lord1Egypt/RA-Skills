## Description:

Adds customizable text watermarks with adjustable opacity and layout to PDFs and images, saving results with a wm_ prefix in the original folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cribug](https://clawhub.ai/user/cribug)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add visible text watermarks to batches of PDFs and common image files for document marking, confidentiality notices, or anti-counterfeiting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically fetches a font from GitHub without an integrity check.

Mitigation: Review before installing, run in an isolated environment where outbound GitHub access is acceptable, and prefer a bundled or hash-pinned font.

Risk: Python dependencies are declared with lower bounds rather than exact reproducible versions.

Mitigation: Pin and hash dependencies before production use.

Risk: Watermarked outputs use a wm_ prefix in the source directory and may conflict with important existing files.

Mitigation: Run on copied inputs or an isolated working directory and add overwrite protection before trusted deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cribug/skills/universal-watermarker)

## Skill Output:

**Output Type(s):** [files, text, guidance]

**Output Format:** [Watermarked PDF or image files plus concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are saved beside the input files with a wm_ filename prefix.]

## Skill Version(s):

2.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
