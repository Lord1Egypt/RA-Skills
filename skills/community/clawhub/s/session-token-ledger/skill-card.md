## Description:

Analyze local OpenClaw session token usage from a generated SQLite ledger and markdown summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zgjq](https://clawhub.ai/user/zgjq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit local OpenClaw session token usage, diagnose context bloat, review daily trends, identify large or inefficient sessions, and generate markdown reports from a local SQLite ledger.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads completed local OpenClaw session transcripts and stores derived token ledgers, which may expose sensitive session metadata or content-derived summaries.

Mitigation: Install only when local transcript analysis is intended, keep generated ledgers in a controlled workspace, and remove generated artifacts when the audit is complete.

Risk: Automatic hook setup can cause ongoing scans of session transcripts after command or gateway events.

Mitigation: Prefer manual rebuilds unless continuous ledger updates are needed, and disable the hook when the token audit workflow is no longer required.

Risk: Security evidence reports a path-handling issue that may write outside the intended folder.

Mitigation: Prefer manual rebuilds and avoid untrusted output paths until timestamp filename validation and output-path containment are fixed.

## Reference(s):

- [Session Token Ledger Overview](references/overview.md)
- [Session Token Ledger Query Templates](references/queries.sql)
- [Hook Setup](references/hook-setup.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, SQLite queries, generated report files, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce a local SQLite ledger, JSON session index, aggregate token summary, anomaly notes, and per-session markdown reports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
