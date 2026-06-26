## Description: <br>
每15分钟扫描 OpenClaw 会话记录，识别任务、决策、教训和配置变更，并将遗漏的重要信息写入每日 memory 文件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a1003916989-blip](https://clawhub.ai/user/a1003916989-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to set up scheduled memory scans that capture important conversation outcomes into daily and weekly memory files. It helps preserve completed tasks, decisions, lessons, configuration changes, and pending items without relying on manual note taking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scheduled task reads private conversation transcripts and may store selected details long-term. <br>
Mitigation: Use it only for chats appropriate for persistent memory, and add redaction, review, deletion, and retention rules before using it with sensitive content. <br>
Risk: The artifact does not define clear cleanup limits for generated memory files. <br>
Mitigation: Define retention and deletion procedures for daily memory files, weekly summaries, scan state, and last-write metadata. <br>
Risk: Feishu delivery can send memory merge notifications outside the local workspace if enabled. <br>
Mitigation: Keep delivery disabled unless the destination user ID and notification contents are known and approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a1003916989-blip/xiazun-memory-auto) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown] <br>
**Output Format:** [Markdown with shell commands, JSON examples, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installs a Python scanner and OpenClaw cron configuration that can create and update memory files.] <br>

## Skill Version(s): <br>
1.0.0 (source: target metadata, release evidence, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
