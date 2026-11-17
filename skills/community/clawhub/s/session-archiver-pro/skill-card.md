## Description:

Extract decisions, todos, knowledge, preferences, and risks from AI chat sessions into structured memory. Outputs Markdown, JSON, or Obsidian notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, teams, and AI-assisted workers use this skill to turn one or more AI chat session logs into structured records of decisions, action items, reusable knowledge, preferences, risks, tags, cross-session links, and summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session logs and generated archives may contain sensitive personal, business, or credential-like information.

Mitigation: Process logs locally where appropriate, redact sensitive content, and review outputs before saving or sharing them.

Risk: Memory-inject JSON can promote untrusted or stale session content into an agent's long-term memory.

Mitigation: Require human review, source checks, and deletion or expiration controls before importing memory entries.

## Reference(s):

- [Output formats reference](artifact/references/formats.md)
- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/session-archiver-pro)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown reports, JSON, Obsidian-compatible Markdown, or memory-inject JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-file and directory-based session log processing; memory-inject JSON should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
