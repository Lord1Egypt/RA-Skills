## Description: <br>
Provides agent-facing guidance for controlling Sonos speakers from the command line, including playback, volume, room grouping, status checks, playlists, alarms, and sleep timers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through Sonos speaker control on a local network they own or administer. It is intended for home Sonos workflows such as playback control, volume changes, room grouping, status checks, and scheduled playback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to discover and control Sonos devices on a local network. <br>
Mitigation: Use it only on networks and Sonos rooms or devices that the user owns or administers, and confirm the target room or device before running discovery or playback commands. <br>
Risk: The security review flags broad trigger wording for a local-network device-control skill. <br>
Mitigation: Invoke the skill only when the user request explicitly involves Sonos, speakers, playback, volume, grouping, or related home-audio control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/sonos-cli-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Sonos CLI commands, local device configuration examples, and structured command-response guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
