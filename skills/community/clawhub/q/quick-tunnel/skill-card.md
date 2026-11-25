## Description:

Creates temporary public Cloudflare Quick Tunnels for configured local services and helps manage their status, shutdown, and recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theoflemesoficial-ship-it](https://clawhub.ai/user/theoflemesoficial-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when they explicitly ask to make a configured local demo or chat service reachable from another device, check or close a tunnel, or recover a previously requested tunnel. It provides the commands and status information needed to manage those temporary connections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A public tunnel URL can be used by anyone who obtains it, and chat messages may be accessed or changed through that URL.

Mitigation: Expose only non-sensitive content, share the URL carefully, and close the tunnel when it is no longer needed.

Risk: A tunnel may restart across sessions, leaving a local service publicly reachable longer than expected.

Mitigation: Check tunnel status after session changes and stop any tunnel that is no longer needed.

Risk: The supplied security review reports partial scanner coverage, so it does not establish that every referenced component was reviewed.

Mitigation: Review the referenced components before installation and use.

## Reference(s):

- [Quick Tunnel skill instructions](artifact/SKILL.md)
- [Safety rules](artifact/references/safety-rules.md)
- [Tunnel commands](artifact/references/commands.md)
- [Recovery guidance](artifact/references/recovery.md)
- [Chat service API](artifact/references/chat-service.md)
- [ClawHub release page](https://clawhub.ai/theoflemesoficial-ship-it/skills/quick-tunnel)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Text]

**Output Format:** [Markdown guidance with shell command examples and plain-text status or tunnel URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tunnel URLs are temporary and are reported only after service validation.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
