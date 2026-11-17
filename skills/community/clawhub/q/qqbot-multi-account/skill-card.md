## Description:

QQBot Multi-Account helps OpenClaw operators manage multi-bot, multi-agent QQBot deployments through account binding checks, duplicate-session diagnosis, proactive send guidance, and local plugin export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naluko](https://clawhub.ai/user/naluko)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure and troubleshoot OpenClaw QQBot deployments with multiple bot accounts and multiple agents. It is especially useful for validating routing bindings, checking appId isolation, diagnosing duplicate sessions, sending through a selected bot account, and exporting a local qqbot plugin archive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The inspection script can print local routing details, appId values, service status, secret file paths, and known-users data.

Mitigation: Run diagnostics only in a trusted terminal and sanitize those fields before sharing output in tickets, chats, or public reports.

Risk: Installing the QQBot plugin with @latest can pull an unreviewed version.

Mitigation: Install a pinned, reviewed QQBot plugin version when using this skill in normal operations.

Risk: Exported qqbot plugin archives may contain local modifications or sensitive files.

Mitigation: Review archive contents before handoff, backup, or release.

## Reference(s):

- [Multi-account routing](artifact/references/multi-account-routing.md)
- [Proactive send and file delivery](artifact/references/proactive-send.md)
- [ClawHub skill page](https://clawhub.ai/naluko/skills/qqbot-multi-account)
- [Publisher profile](https://clawhub.ai/user/naluko)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local OpenClaw configuration, QQBot account identifiers, known-users data, service status, and export archives.]

## Skill Version(s):

1.0.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
