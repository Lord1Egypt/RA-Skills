## Description:

Capture and manage TIL (Today I Learned) entries on OpenTIL from the CLI, including creating, publishing, editing, searching, deleting, syncing, and organizing entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biao29](https://clawhub.ai/user/biao29)

### License/Terms of Use:

MIT

## Use Case:

Developers and CLI users use this skill to turn technical learnings into OpenTIL entries, publish or save drafts, and manage existing entries without leaving the agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish, edit, or delete OpenTIL entries using a persistent token with write and delete authority.

Mitigation: Install only when comfortable granting those scopes, prefer profile-based credentials over broad shell-profile exports when possible, and review generated content before publishing or destructive actions.

Risk: A broad affirmative response to a proactive TIL suggestion can send conversation-derived content to OpenTIL.

Mitigation: Treat proactive captures as publication events, review the generated entry for sensitive or proprietary details, and decline suggestions that should remain private.

Risk: Incorrect active profile selection can publish content to the wrong OpenTIL account.

Mitigation: Check the active account shown by the skill when multiple profiles are configured and switch profiles before publishing or syncing.

## Reference(s):

- [OpenTIL](https://opentil.ai)
- [OpenTIL Skill on ClawHub](https://clawhub.ai/biao29/skills/til)
- [OpenTIL Publisher Profile](https://clawhub.ai/user/biao29)
- [API Reference](references/api.md)
- [Management Subcommands Reference](references/management.md)
- [Auto-Detection Guide](references/auto-detection.md)
- [Local Drafts & Sync Protocol](references/local-drafts.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text responses with optional shell commands and API-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local draft files under ~/.til/drafts and credential profiles under ~/.til/credentials when the user authorizes those flows.]

## Skill Version(s):

1.11.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
