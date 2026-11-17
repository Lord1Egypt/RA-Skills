## Description:

macOS CLI guidance for recording microphone audio, screen video or screenshots, and camera video or photos from the terminal with device listing and output controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atacan](https://clawhub.ai/user/atacan)

### License/Terms of Use:


## Use Case:

Developers, operators, and AI agents on macOS use this skill to install and invoke the record CLI for consented microphone, screen, screenshot, webcam video, and photo capture from terminal workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Microphone, camera, and screen capture can expose sensitive user or workspace information.

Mitigation: Ask for explicit permission before every recording, screenshot, or camera photo, and confirm what will be captured and for how long.

Risk: The skill asks users to install an unpinned third-party recording executable that may receive macOS privacy permissions.

Mitigation: Review the publisher and Homebrew formula before installing, prefer a pinned reviewed release when available, and grant permissions only for the capture feature the user intends to use.

Risk: Using --overwrite can replace an existing output file.

Mitigation: Avoid --overwrite unless the user has explicitly confirmed the exact output path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/atacan/skills/record)
- [Audio command reference](references/audio.md)
- [Screen command reference](references/screen.md)
- [Camera command reference](references/camera.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include commands that produce file paths or JSON output from the underlying CLI when executed.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
