## Description:

Workcrm is a local-first CRM skill that drafts contact, activity, and task changes and requires explicit user confirmation before saving them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[extraterrest](https://clawhub.ai/user/extraterrest)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use Workcrm to capture CRM notes, follow-up tasks, participants, assignees, and project activity into a local SQLite database after reviewing a draft and confirming the write.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local SQLite storage retains CRM records and draft content, including rejected drafts.

Mitigation: Use a deliberate local database path, apply local access controls and retention practices, and avoid entering sensitive CRM data unless local persistence is acceptable.

Risk: The exact confirmation words and family or personal prefixes can affect whether and where records are saved.

Mitigation: Review each draft before confirming with `记`, use `不记` to reject unintended drafts, and verify the intended profile or database path when using family or personal prefixes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/extraterrest/skills/workcrm)
- [Artifact Skill Instructions](artifact/SKILL.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, JSON, guidance, configuration]

**Output Format:** [Human-facing messages with JSON payloads and local SQLite records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafts are retained for auditability; confirmed writes are stored locally in SQLite.]

## Skill Version(s):

0.1.0-alpha.4 (source: server release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
