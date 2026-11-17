## Description:

Video motion analysis assistant that extracts key frames from instructional videos, analyzes motion and posture, and generates stick-figure action diagrams for sports technique review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianheihei002](https://clawhub.ai/user/tianheihei002)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to break down sports teaching videos into key frames, posture analysis, coaching feedback, and visual stick-figure diagrams that highlight correct motion and areas for improvement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes extracted frames and generated images from user-provided videos to local output directories, which may expose private media if retained.

Mitigation: Use the documented output directories, process only videos suitable for local storage, and delete generated output folders after analysis when media is private.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianheihei002/skills/yq-video-motion-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON analysis examples, shell commands, JPEG key frames, and PNG stick-figure diagrams]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes extracted video frames to output/frames/ and generated stick-figure diagrams to output/stickman/.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
