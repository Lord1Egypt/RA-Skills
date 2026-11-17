## Description:

Guides a five-minute conversational WOOP practice that helps users turn a wish into a concrete outcome, inner obstacle, and if-then action plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reffwu](https://clawhub.ai/user/reffwu)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill in an agent chat to work through daily, weekly, habit-building, review, reminder, or story-guided WOOP sessions for personal goal follow-through.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can silently self-update during startup.

Mitigation: Pin or review the installed version before use, and remove silent self-update behavior in environments that require change control.

Risk: The skill stores personal WOOP reflections in plaintext files under the user's home directory.

Mitigation: Treat session logs as sensitive, avoid entering highly sensitive information, and provide clear opt-in, retention, and deletion practices before deployment.

Risk: The skill uses Bash for logging and can create OpenClaw cron reminders.

Mitigation: Review commands before execution and grant shell or cron access only in trusted local environments.

## Reference(s):

- [Woop Daily Homepage](https://github.com/ReffWu/woop-daily)
- [ClawHub Skill Page](https://clawhub.ai/reffwu/skills/woop-daily)
- [WOOP Official Practice Resource](https://woopmylife.org)
- [WOOP / MCII Science Background](references/science.md)
- [Conversation Craft](references/conversation-craft.md)
- [Parable: The Boy Who Built Bridges](references/parable-fog-river.md)
- [Skill Design Principles](references/skill-design-principles.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Conversational Markdown with occasional inline shell commands for reminders and local session logging]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local plaintext WOOP history and optional cron reminders when the user enables those flows.]

## Skill Version(s):

2.2.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
