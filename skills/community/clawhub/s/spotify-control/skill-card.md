## Description:

macOS Spotify control skill for OpenClaw. Supports playback, volume, position, and metadata retrieval via AppleScript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[copywrite-ai](https://clawhub.ai/user/copywrite-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent control Spotify on macOS through a Python wrapper for playback, volume, seeking, shuffle, repeat, and track metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that unvalidated volume or seek values can lead to unintended AppleScript execution.

Mitigation: Validate volume as an integer from 0 to 100 and position as a non-negative finite number before invoking osascript; use only where the agent and wrapper inputs are trusted until fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/copywrite-ai/skills/spotify-control)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one-shot Spotify control commands and command output from the macOS AppleScript wrapper.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
