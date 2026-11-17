## Description:

Use when the task is to stitch multiple vertically scrolling iPhone screenshots into a single long image with the local screenshot-stitcher CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mate-matt](https://clawhub.ai/user/mate-matt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to combine ordered, vertically scrolling iPhone screenshots into one long local image and choose crop or margin flags when defaults are insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing an unpinned PyPI CLI package.

Mitigation: Install the CLI in a dedicated virtual environment and prefer a pinned, reviewed package version.

Risk: Screenshots may contain sensitive information exposed to local tooling in the active Python environment.

Mitigation: Only process screenshots that are appropriate for that local environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown with inline shell commands and generated image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces local CLI instructions and reports the stitched output path plus low-confidence overlap notes when present.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
