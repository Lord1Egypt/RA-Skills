## Description:

Helps agents consult locally synced OpenClaw documentation before proposing configuration changes for agents, sessions, channels, cron jobs, notifications, tools, workspaces, gateways, memory, and skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[echoflying](https://clawhub.ai/user/echoflying)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search, read, and sync OpenClaw documentation before designing OpenClaw configuration changes. It supports documentation-grounded guidance with shell commands and cited local document paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports an unsafe document-read path that can escape the docs folder and expose local files.

Mitigation: Review before installing and avoid passing untrusted paths to --read or --list.

Risk: The skill uses shell scripts that fetch OpenClaw docs from GitHub and write under ~/.openclaw.

Mitigation: Use it only if that local write behavior and GitHub access are acceptable for the deployment environment.

Risk: Usage logs and sync notifications can disclose command or sync metadata.

Mitigation: Set DISABLE_USAGE_LOG=true to disable usage logging and keep DOC_NOTIFY_CHANNEL=none unless notification sharing is acceptable.

## Reference(s):

- [Skill README](artifact/SKILL.md)
- [Script Reference](artifact/references/scripts.md)
- [Troubleshooting Guide](artifact/references/troubleshooting.md)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [ClawHub Skill Page](https://clawhub.ai/echoflying/skills/use-openclaw-manual)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local documentation references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include search results, document excerpts, sync status, usage statistics, and configuration steps.]

## Skill Version(s):

2.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
