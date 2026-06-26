## Description: <br>
Control XiaoPai media player over LAN via HTTP/TCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kuangxinyi](https://clawhub.ai/user/kuangxinyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to discover and control a XiaoPai media player on a trusted local network, including playback, volume, remote-control key presses, and status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send disruptive remote-control actions to a XiaoPai player on a local network. <br>
Mitigation: Require explicit user approval before rebooting, powering off, deleting, taking screenshots, changing settings, or sending rapid key sequences. <br>
Risk: mDNS discovery and status queries can expose device identifiers and playback state. <br>
Mitigation: Use the skill only on a trusted LAN, verify that the discovered IP or MAC belongs to the user's device, and avoid logging or sharing identifiers or playback status unnecessarily. <br>


## Reference(s): <br>
- [XiaoPai Player TCP/IP Protocol Reference](references/protocol.md) <br>
- [XiaoPai Player Control on ClawHub](https://clawhub.ai/kuangxinyi/xiaopai-player-control) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands, HTTP examples, and TCP status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include LAN discovery commands, URL-encoded playback requests, remote-control key commands, and JSON status interpretation.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
