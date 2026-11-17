## Description:

Archives session prompts and responses before token compaction and restores the latest archived context at the start of a new session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[syedateebulislam](https://clawhub.ai/user/syedateebulislam)

### License/Terms of Use:


## Use Case:

ClawHub users and developers use this skill to preserve conversation continuity across compaction by exporting recent session history and making the latest archive available for later ingestion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist sensitive chats, credentials, and prior instructions in plaintext archives.

Mitigation: Install only when durable local transcript memory is desired, apply strict file permissions, and add redaction plus retention or deletion controls before storing sensitive sessions.

Risk: Archived prior instructions may be replayed into later sessions and influence future agent behavior.

Mitigation: Review archived content before ingestion and remove stale, sensitive, or untrusted instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/syedateebulislam/skills/remember-all-prompts-daily)
- [ClawHub publisher profile](https://clawhub.ai/user/syedateebulislam)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown archive entries, terminal status text, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local memory files under ~/.clawd/memory; export formatting truncates long message text in archived entries.]

## Skill Version(s):

1.0.1 (source: server release metadata, created 2026-01-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
