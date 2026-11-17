## Description:

记忆自动主动管理：每15分钟自动扫描对话，发现重要信息自动写入每日 memory，解决主动记录经常遗漏的问题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[a1003916989-blip](https://clawhub.ai/user/a1003916989-blip)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to run scheduled memory checks that scan new conversation transcript messages, compare them with existing memory files, and record missed tasks, decisions, lessons, configuration changes, or blockers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled runs read conversation transcripts and expose selected transcript text to a tool-enabled agent.

Mitigation: Enable the skill only for workspaces where transcript scanning is acceptable; configure an explicit transcript path and review/redact sensitive content before memory writes.

Risk: The cron workflow requests exec, read, and write authority and can write to memory files automatically.

Mitigation: Limit permissions to the narrowest workspace paths possible and review the cron commands, generated memory entries, and scan-state files after installation.

Risk: Optional Feishu delivery can send memory-derived data outside the local environment.

Mitigation: Do not enable Feishu delivery unless external delivery is intended and the recipient user ID, channel, and content handling are approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a1003916989-blip/skills/xiazun-memory-auto)
- [Publisher profile](https://clawhub.ai/user/a1003916989-blip)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and operating guidance for OpenClaw cron jobs and memory files; the bundled scan script prints transcript excerpts and current memory content for agent review.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
