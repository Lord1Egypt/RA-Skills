## Description:

Take camera snapshots and save them to disk. Use when the user asks to take a photo, capture an image from webcam, or take a snapshot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can ask an agent to capture a snapshot from the default webcam and save the image locally, optionally choosing an output path or previewing the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate the default webcam and retain captured snapshots on disk.

Mitigation: Use it only when webcam capture is intended, verify the saved file path after use, and delete snapshots that should not be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/terrycarter-camsnap)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and saved image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local image file in jpg, jpeg, png, bmp, or webp format.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
