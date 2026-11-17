## Description:

Control XiaoPai media player over LAN via HTTP/TCP. Use when asked to play videos, send remote-control keys, adjust volume, or query playback status on a XiaoPai player.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kuangxinyi](https://clawhub.ai/user/kuangxinyi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users use this skill to control a XiaoPai media player on a trusted local network, including playback, remote-control keys, volume adjustment, discovery, and status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act as a local-network remote control and may disrupt a XiaoPai player if powerful commands are sent.

Mitigation: Use only on trusted local networks, confirm the target device or IP, and require explicit user confirmation before power, reboot, delete, or other disruptive commands.

## Reference(s):

- [XiaoPai Player TCP/IP Protocol Reference](references/protocol.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and HTTP/TCP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include mDNS discovery steps and commands targeting a user-confirmed LAN player IP.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
