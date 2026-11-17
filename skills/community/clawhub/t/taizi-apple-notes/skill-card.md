## Description:

Manage Apple Notes via the `memo` CLI on macOS (create, view, edit, delete, search, move, and export notes). Use when a user asks Clawdbot to add a note, list notes, search notes, or manage note folders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fresh3](https://clawhub.ai/user/fresh3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate Apple Notes from an agent through the `memo` CLI, including creating, listing, searching, editing, moving, deleting, and exporting notes on macOS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned third-party CLI that can access and modify private Apple Notes.

Mitigation: Install only after reviewing and trusting the memo project, and prefer a pinned, verified release.

Risk: Delete and export actions can expose or remove private notes.

Mitigation: Confirm the exact note before delete or export actions and treat those operations as sensitive.

Risk: Apple Notes Automation access grants the CLI ongoing access to Notes.app.

Mitigation: Grant Automation permission only when needed and revoke it when the integration is no longer in use.

## Reference(s):

- [Apple Notes Skill on ClawHub](https://clawhub.ai/fresh3/skills/taizi-apple-notes)
- [memo CLI homepage](https://github.com/antoniorodr/memo)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require interactive terminal access and Apple Notes Automation permission on macOS.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
