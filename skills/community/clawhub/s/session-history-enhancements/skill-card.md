## Description:

Adds persistent, browsable, and resumable OpenClaw session history with SQLite indexing, archive and restore workflows, migration support, dashboard pagination, and chat dropdown integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to extend OpenClaw with session archival, browsing, search, resume, rename, delete, migration, pagination, and recent-session dropdown workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unscoped agent IDs could expose or modify sessions outside the intended agent context.

Mitigation: Validate requested agent IDs against configured agents and authorization before listing, archiving, resuming, renaming, or deleting sessions.

Risk: Session history responses could expose internal transcript file paths to dashboard clients.

Mitigation: Return opaque session identifiers and user-facing metadata instead of raw server file paths.

Risk: Archive and restore operations could leave transcript files and SQLite status out of sync when a step fails.

Mitigation: Make file moves and database updates transactional where possible, or fail closed with rollback and reconciliation.

Risk: Deletion prompts can imply permanent transcript deletion even when transcript removal is not actually requested or completed.

Mitigation: Align UI prompts, RPC parameters, and server behavior so transcript deletion is explicit, confirmed, and reported accurately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maverick-software/skills/session-history-enhancements)
- [Skill source](artifact/SKILL.md)
- [Installation guide](artifact/references/INSTALL.md)
- [Backend history database reference](artifact/references/backend-history-db.ts.txt)
- [Backend history migration reference](artifact/references/backend-history-migration.ts.txt)
- [Backend session archive reference](artifact/references/backend-session-archive.ts.txt)
- [Backend protocol schemas reference](artifact/references/backend-protocol-schemas.ts.txt)
- [Backend RPC handlers reference](artifact/references/backend-rpc-handlers.ts.txt)
- [Frontend controllers reference](artifact/references/frontend-controllers-sessions.ts.txt)
- [Frontend views reference](artifact/references/frontend-views-sessions.ts.txt)
- [Frontend state changes reference](artifact/references/frontend-state-changes.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript code references and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires review before applying to OpenClaw deployments that store private chat transcripts.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
