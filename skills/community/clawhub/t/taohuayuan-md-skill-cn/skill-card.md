## Description:

Provides Chinese-language guidance and Python helpers for creating a local, physical-anchor persistent memory structure for autonomous agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to initialize and manage a local file-based memory anchor for autonomous agents, including root identity records, short-term interaction logs, and consolidated long-term memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory may record broad interaction or environmental details without clear consent, retention, deletion, or isolation controls.

Mitigation: Use explicit opt-in, review and redaction, retention limits, deletion controls, and isolation before connecting the skill to private chats, sensors, agent memory retrieval, or other agents.

Risk: Stored memories can influence later agent behavior even when the stored content is stale, sensitive, or untrusted.

Mitigation: Treat stored memories as untrusted data, review consolidated files before reuse, and restrict downstream retrieval to approved, relevant records.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/spacesq/skills/taohuayuan-md-skill-cn)
- [Taohuayuan.md V2.0 Whitepaper](artifact/taohuayuan_md_whitepaper.md)
- [Developer README](artifact/readme.md)
- [Skill Prompt and Guide](artifact/skill.md)
- [Sample Taohuayuan Record](artifact/samples/taohuayuan.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and JSON-backed local memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local taohuayuan.md, hippocampus_logs.json, and memory_files/ when the Python helper is run.]

## Skill Version(s):

2.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
