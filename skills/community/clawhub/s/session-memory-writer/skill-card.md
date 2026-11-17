## Description:

Write structured task outcome blocks to memory/YYYY-MM-DD.md at session end, enforcing format consistency for Langfuse backfill, Quill journal generation, and QMD search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to append structured session-memory and OUTBOX entries after task completion so downstream observability, journal, and search workflows can parse outcomes consistently.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent session logs and OUTBOX entries may retain workspace details or task outcomes that are not appropriate for every environment.

Mitigation: Confirm the workspace logging policy before use and review entries before committing, syncing, or sharing them.

Risk: The documented daily-log convention assumes AEST and strict markdown formats, which can produce inconsistent records if adopted unchanged in another workflow.

Mitigation: Set the intended timezone convention before adoption and preserve the documented header and field formats for parser compatibility.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nissan/skills/session-memory-writer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown task outcome and session summary templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Append-only daily memory and OUTBOX entry conventions]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
