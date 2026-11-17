## Description:

Generate PowerPoint (.pptx) files from Markdown input. Use when user requests a PPT to be created or exported.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mlnmg2020](https://clawhub.ai/user/mlnmg2020)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert structured Markdown into downloadable PowerPoint (.pptx) presentations when a request asks to create or export a PPT file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Python script on user-selected Markdown and writes a PowerPoint output file.

Mitigation: Use explicit input and output paths, run it only on Markdown files you choose, and install python-pptx from a trusted environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [files, shell commands, guidance]

**Output Format:** [PowerPoint (.pptx) file generated from Markdown input, with shell command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an input Markdown file and an output .pptx path; slide breaks use ---.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
