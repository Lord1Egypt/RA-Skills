## Description:

Agent自进化Skill helps an agent identify valuable lessons from completed sessions, ask for user confirmation, and save concise experience or profile updates for future work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckystar513](https://clawhub.ai/user/luckystar513)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to convert repeated fixes, non-obvious pitfalls, reusable design decisions, and explicit preferences into reviewed Markdown memory entries. It supports maintaining personal, project, domain, and user-profile knowledge so future agent sessions can reuse confirmed lessons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist conversation-derived rules into long-lived personal, project, domain, or profile files that may influence future sessions.

Mitigation: Approve only concrete, accurate entries that should affect future work, and reject broad rules, hidden prompt language, or tool-use directives.

Risk: The skill may propose updates to global user-profile files, project CLAUDE.md files, domain skill folders, or its own skill files.

Mitigation: Review every proposed destination and diff before approving a write, with extra scrutiny for global or self-modifying changes.

## Reference(s):

- [Skill source](artifact/SKILL.md)
- [Experience entry and user profile templates](artifact/references/templates.md)
- [ClawHub skill page](https://clawhub.ai/luckystar513/skills/wdp-auto-skills)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown drafts, concise review prompts, and proposed file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Proposes long-lived memory and instruction-file updates only after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
