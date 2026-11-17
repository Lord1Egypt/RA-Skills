## Description:

Manage Sun-Panel navigation by adding websites, creating and editing shortcut groups, and getting icon recommendations for bookmarks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meichuanyi](https://clawhub.ai/user/meichuanyi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent configure Sun-Panel navigation entries, groups, icons, and favicon-based bookmark shortcuts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a reusable Sun-Panel password in plaintext and may send it over unencrypted HTTP.

Mitigation: Use a dedicated low-privilege Sun-Panel account, prefer HTTPS, avoid shared machines, and restrict config-file permissions manually if used.

Risk: The skill can make authenticated changes to Sun-Panel navigation groups and shortcuts.

Mitigation: Confirm every add or edit operation before allowing the agent to change the panel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meichuanyi/skills/sun-panel)
- [ClawHub publisher profile](https://clawhub.ai/user/meichuanyi)
- [Iconify icon sets](https://icon-sets.iconify.design/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local configuration, authenticated Sun-Panel API calls, group management, bookmark creation, favicon retrieval, and icon selection.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
