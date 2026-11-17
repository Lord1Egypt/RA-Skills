## Description:

Control a Vector robot via Wirepod's local HTTP API on the same network for movement, head and lift control, speech, camera snapshots, patrols, and exploration from a Pi or Wirepod host.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dbeadle1](https://clawhub.ai/user/dbeadle1)

### License/Terms of Use:


## Use Case:

Developers and robot operators use this skill to control a Vector robot through a local Wirepod host, including motion, speech, audio playback, camera snapshots, patrol routines, and randomized exploration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move a physical Vector robot.

Mitigation: Run movement commands only while supervised, keep the robot in a clear area, and prefer short bounded durations.

Risk: The skill can access camera snapshots and stream data from the robot.

Mitigation: Treat captured images as sensitive and run the skill only on a trusted local Wirepod host.

Risk: The CLI can send audio and network requests to the configured Wirepod base URL.

Mitigation: Avoid untrusted --base URLs and review audio files before playback.

## Reference(s):

- [Wirepod HTTP API](references/wirepod-api.md)
- [Vector Control on ClawHub](https://clawhub.ai/dbeadle1/skills/vector-control)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python CLI usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local MJPG camera snapshot files and converted audio upload requests when the bundled CLI is executed.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
