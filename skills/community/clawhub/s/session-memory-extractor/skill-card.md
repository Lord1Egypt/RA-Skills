## Description: <br>
Session Memory Extractor scans older OpenClaw session transcripts, extracts durable decisions, preferences, facts, and tasks into memory files, and can clean up successfully processed raw session files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lmqiang-711](https://clawhub.ai/user/lmqiang-711) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to preview and extract long-term memories from older session transcripts before optionally cleaning up raw transcript files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes old session transcripts that may contain secrets, credentials, or sensitive conversations. <br>
Mitigation: Run preview first, use dry-run to inspect extraction behavior, and review generated memory for secrets before normal cleanup. <br>
Risk: Normal runs can permanently delete successfully extracted raw session files after extraction. <br>
Mitigation: Require explicit user confirmation before cleanup, keep backups for sensitive sessions, and rely on the v1.0.6 quarantine behavior for failed or invalid extractions. <br>
Risk: Optional Feishu notifications can send extraction summaries outside the local workspace. <br>
Mitigation: Keep notifications disabled unless needed and only send notifications to trusted targets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lmqiang-711/session-memory-extractor) <br>
- [ClawHub metadata homepage](https://clawhub.ai/hasakyi/session-memory-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; runtime scripts write memory Markdown, JSON reports, and quarantine logs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preview and dry-run modes are available; normal runs can delete successfully extracted raw session files after confirmation.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
