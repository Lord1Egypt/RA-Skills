## Description:

Help people expand their professional networks by discovering relevant peers, collaborators, mentors, and communities, reconnecting with existing contacts, resolving public profiles, and tracking explicitly authorised LinkedIn invitations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to research professional contacts, prepare reviewable shortlists, manage explicitly authorised LinkedIn outreach, and resume networking batches across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can involve professional contact research and explicitly approved LinkedIn actions.

Mitigation: Confirm the exact outreach scope before browser actions, stop on platform warnings or verification challenges, and record only observed states with supporting evidence.

Risk: Project ledgers may contain profile URLs, evidence, relationship states, and approval references, and they are stored locally without encryption.

Mitigation: Keep ledgers outside the installed skill directory, use private project storage with appropriate filesystem permissions, and avoid importing private contact exports without permission.

Risk: Identity matches, relevance scores, and browser observations can be incomplete or wrong.

Mitigation: Review candidate evidence before outreach, preserve uncertainty, and verify live profile state before recording invitations as sent or pending.

## Reference(s):

- [Discovery and identity resolution](references/discovery.md)
- [Authorised LinkedIn work](references/linkedin.md)
- [Start from a networking goal](references/network-plan.md)
- [Private tracking and commands](references/tracking.md)
- [Release notes](docs/release-notes.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON ledger outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The optional helper stores project-local SQLite ledgers and prints JSON; agent-facing guidance may include candidate shortlists, evidence summaries, status reports, and reconciliation notes.]

## Skill Version(s):

0.1.0-rc.2 (source: release evidence, VERSION, and release notes)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
