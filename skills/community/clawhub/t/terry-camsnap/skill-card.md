## Description:

Take camera snapshots and save them to disk. Use when the user asks to take a photo, capture an image from webcam, or take a snapshot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to capture a snapshot from the default webcam and report where the image was saved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw Bash argument interpolation may allow command injection if untrusted filenames or options are passed.

Mitigation: Avoid untrusted arguments and prefer structured, validated argument handling before broad deployment.

Risk: The referenced `camsnap.py` implementation is not included in the artifact, so its behavior cannot be fully reviewed from this release package.

Mitigation: Review the installed local script before use and grant webcam and local file-write access only in trusted environments.

Risk: The skill captures webcam images and writes files to disk.

Mitigation: Use only where camera access and destination directories are authorized; avoid preview mode on headless systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/terry-camsnap)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Text]

**Output Format:** [Text status with the saved image file path; the skill also writes an image file to disk.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an optional output path, output directory, and preview flag.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
