## Description:

Executes common Windows system commands such as ipconfig, tasklist, netstat, systeminfo, and configured aliases, then returns formatted command output for system inspection and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ljr287404428](https://clawhub.ai/user/ljr287404428)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, system administrators, and support operators use this skill to inspect Windows host state, collect network and process information, and run troubleshooting commands from an OpenClaw session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run Windows shell commands with the same permissions as the hosting agent.

Mitigation: Install only when host command execution is intended, restrict who can invoke it, and run the agent under a low-privilege account.

Risk: Command output can expose host, network, process, account, and system details.

Mitigation: Use it only in trusted sessions and review output before sharing logs or transcripts.

Risk: Custom and confirmed high-risk commands may change system state despite blacklist and confirmation checks.

Mitigation: Prefer predefined read-only commands, inspect custom command strings carefully, and require explicit confirmation before high-risk execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ljr287404428/skills/system-cmd)
- [Command reference](artifact/references/commands.md)
- [Usage examples](artifact/references/usage_examples.md)
- [Quick start](artifact/QUICK_START.md)
- [Windows command reference](https://docs.microsoft.com/windows-server/administration/windows-commands/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Formatted text and Markdown-style help with command output, status messages, and warnings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output is truncated for long command results; custom commands use shorter timeouts than confirmed high-risk commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
