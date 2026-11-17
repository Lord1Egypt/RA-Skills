## Description:

Generates whiteboard-style hand-drawing animation videos from images, converting color images into two-stage line-drawing and coloring animations with an optional hand overlay and H.264 MP4 output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangagent](https://clawhub.ai/user/yangagent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to turn one or more local image files into whiteboard-style MP4 animation videos and receive generated file paths or batch status summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup workflow creates a local .venv and installs unpinned Python media packages.

Mitigation: Run the skill in an isolated environment and review or pin opencv-python, numpy, and av before installation when supply-chain control matters.

Risk: Batch generation acts on user-provided image paths and output locations.

Mitigation: Confirm image paths, durations, and output directories before execution, especially for batch jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangagent/skills/whiteboard-animation)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Markdown-style instructions with shell command examples; generated artifacts are H.264 MP4 files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-image mode returns a final video path; batch mode returns success and failure counts, output directory, and failed image paths.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
