## Description:

Cross-session memory sync protocol. Ensures memory consistency across Feishu, webchat, and any other channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdt328606](https://clawhub.ai/user/sdt328606)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users and developers use this skill to keep conversation memory and active task state consistent across Feishu, webchat, and other agent sessions by reading and updating shared Markdown memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly persists and reuses cross-session conversation context, which can retain sensitive or irrelevant information without enough scoping or consent.

Mitigation: Use it only in a trusted single-user workspace, review and redact memory entries before long-term retention, and avoid using it for credentials, private personal data, confidential business material, or untrusted participant input.

Risk: The cleanup helper archives daily memory logs, which can affect retained records if run without review.

Mitigation: Require explicit confirmation before cleanup and verify that valuable entries have been summarized into long-term memory before archiving logs.

## Reference(s):

- [Session Sync ClawHub skill page](https://clawhub.ai/sdt328606/skills/stitch-session-sync)
- [sdt328606 publisher profile](https://clawhub.ai/user/sdt328606)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown memory updates with optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, update, append, or archive workspace memory files when the agent follows the skill instructions.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
