## Description: <br>
macOS Spotify control skill for OpenClaw. Supports playback, volume, position, and metadata retrieval via AppleScript. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[copywrite-ai](https://clawhub.ai/user/copywrite-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill on macOS to control Spotify playback, volume, position, shuffle, repeat, and current-track metadata through a Python wrapper around AppleScript. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Volume and seek arguments can be interpreted as AppleScript. <br>
Mitigation: Pass only simple trusted numeric values for volume and seek position; a safer version should parse values as numbers and enforce ranges before invoking AppleScript. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/copywrite-ai/spotify-control) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown with shell command examples and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs one-shot macOS AppleScript commands through scripts/spotify-control.py and may return Spotify status or track metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter, _meta.json, server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
