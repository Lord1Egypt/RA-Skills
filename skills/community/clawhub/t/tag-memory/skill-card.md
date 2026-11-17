## Description:

TagMemory gives an agent a local, tag-based long-term memory system for storing, searching, verifying, and summarizing user-confirmed information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckyboybs](https://clawhub.ai/user/luckyboybs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to let an agent retain important user preferences, decisions, project facts, events, and periodic summaries with tag filtering, BM25 search, and human review before memories are treated as reliable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists personal or project details in local plaintext memory storage.

Mitigation: Do not store secrets or confidential data unless local retention is acceptable, and review the local memory database contents regularly.

Risk: Packaged pending summary data may carry stale or unintended memory content into a release.

Mitigation: Remove packaged pending_summary.json before installation or release.

Risk: Weak confirmation defaults can archive summaries or replace memories without sufficiently explicit user approval.

Mitigation: Require explicit confirmation for summary archival and memory replacement, avoid default-confirm behavior, and keep updates recoverable or confirmed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luckyboybs/skills/tag-memory)
- [ClawHub Publisher Profile](https://clawhub.ai/user/luckyboybs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-like tool results with CLI command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local SQLite/FTS5 storage and returns tagged memory records, pending verification prompts, summaries, and statistics.]

## Skill Version(s):

1.0.0 (source: server evidence release.version and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
