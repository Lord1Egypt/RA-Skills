## Description:

Read-only local archive and full-text search of macOS WhatsApp Desktop chats that snapshots WhatsApp's SQLite databases into ~/.wacrawl/wacrawl.db without modifying the app container.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chasewebb](https://clawhub.ai/user/chasewebb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and search a local macOS WhatsApp Desktop archive through the wacrawl command-line tool. It supports read-only chat import, status checks, full-text search, JSON listings, and local SQL queries against the generated archive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Full Disk Access and creates a second local database of WhatsApp chat history.

Mitigation: Grant access only when the local archive is needed, protect ~/.wacrawl with strict local permissions, account for backups, and remove the archive and any schedule when finished.

Risk: The skill directs users to run an unpinned third-party wacrawl binary.

Mitigation: Prefer a pinned or auditable wacrawl release before installation or scheduled use.

## Reference(s):

- [Wacrawl GitHub repository](https://github.com/steipete/wacrawl)
- [ClawHub skill page](https://clawhub.ai/chasewebb/skills/wacrawl)
- [ClawHub publisher profile](https://clawhub.ai/user/chasewebb)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs guide an agent to run the local wacrawl CLI and interpret JSON, SQL, and status results.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
