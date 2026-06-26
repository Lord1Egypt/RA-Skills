## Description: <br>
Safer Spotify playback for OpenClaw on setups where direct spogo play is unreliable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[surdragon-design](https://clawhub.ai/user/surdragon-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to search Spotify and control playback through spogo when direct spogo playback is unreliable. It guides the agent toward safer queue-and-skip playback flows for tracks, albums, and playlists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill references a spotify-safe-play wrapper script that was not included in the reviewed package. <br>
Mitigation: Verify the wrapper script source and behavior before relying on it, or use only the documented spogo commands that are present in the reviewed skill instructions. <br>
Risk: The skill can direct an agent to use an authenticated Spotify setup to queue, skip, pause, resume, and select playback devices. <br>
Mitigation: Install and use it only where agent-driven Spotify playback control is acceptable for the authenticated account and active Spotify Connect devices. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/surdragon-design/spotify-safe-play) <br>
- [Skill metadata homepage](https://github.com/surdragon-design/spotify-safe-player) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Spotify Premium, authenticated spogo, Bash, curl, grep, awk, and an active Spotify Connect target.] <br>

## Skill Version(s): <br>
v0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
