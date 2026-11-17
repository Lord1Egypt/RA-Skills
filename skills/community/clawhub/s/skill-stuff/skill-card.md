## Description:

Recaps a user's day in the style of a selected TV show and can deliver a recurring creative summary with episode title, narrative arc, plot points, cliffhanger, and a shareable card.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rednix](https://clawhub.ai/user/rednix)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn calendar, email, chat, and other connected-source activity into a playful daily recap. It supports setup, on-demand recaps, scheduled delivery, memory-based season continuity, and shareable Markdown or HTML output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is presented as Skill Stuff while the primary artifact describes Main Character Recap and includes many unrelated skill documents.

Mitigation: Review the package contents before installation and require the publisher to ship a focused package or clearly document the bundle and permissions.

Risk: Scheduled recaps can pull from connected accounts such as calendar, email, Slack, GitHub, Notion, Linear, and Todoist.

Mitigation: Enable only the specific data sources needed for the recap and review the permissions before turning on recurring delivery.

Risk: The skill can keep running memory and daily history files that may contain personal activity summaries.

Mitigation: Keep delivery private and periodically review, redact, or disable retained memory and history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rednix/skills/skill-stuff)
- [ClawHub homepage metadata](https://clawhub.com/skills/main-character-recap)
- [Publisher profile](https://clawhub.ai/user/rednix)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown recap text with optional HTML shareable card and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write memory and history Markdown files and schedule recurring delivery when enabled by the user.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
