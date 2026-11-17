## Description:

Clean orphan .jsonl files and stale sessions in OpenClaw session storage with safe confirmation flow. 适用于会话列表杂乱、历史会话堆积、需要释放存储空间场景；默认保护 72 小时内会话，删除前必须用户确认。

This skill is ready for commercial/non-commercial use.

## Publisher:

[irideas](https://clawhub.ai/user/irideas)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to scan session storage, identify orphan .jsonl files and stale sessions, and prepare a confirmation-first cleanup plan before removing files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup commands can permanently delete OpenClaw session .jsonl files if applied to the wrong paths.

Mitigation: Review the scan report, confirm exact filenames, and prefer archive or move behavior before hard deletion.

Risk: Blindly pasting an rm command could remove files that are not clearly normal session files under the OpenClaw sessions directory.

Mitigation: Use only paths from the scan output and require explicit confirmation before executing deletion commands.

## Reference(s):

- [Session Cleanup Policy](references/policy.md)
- [ClawHub Skill Page](https://clawhub.ai/irideas/skills/session-cleanup-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown cleanup summaries with inline shell commands and JSON scan output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before cleanup; scan script emits structured JSON.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
