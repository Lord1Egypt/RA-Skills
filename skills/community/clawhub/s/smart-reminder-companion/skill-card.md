## Description:

智能提醒小管家，支持定时提醒、情绪联动提醒、场景化提醒。

This skill is ready for commercial/non-commercial use.

## Publisher:

[786793119](https://clawhub.ai/user/786793119)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to manage personal reminders, including timed reminders, enable or disable states, emotion-linked suggestions, and weather-related reminder prompts. It stores reminder entries locally for later access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reminder entries are stored locally under ~/.memory/reminders/reminders.json and delete operations may remove entries from that file.

Mitigation: Keep backups of important reminder data before using delete or bulk-management workflows.

Risk: The skill content is mainly in Chinese, which may make review harder for users who do not read Chinese.

Mitigation: Have a Chinese-reading reviewer confirm reminder behavior, prompts, and local file effects before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/786793119/skills/smart-reminder-companion)
- [Project homepage](https://github.com/786793119/miya-skills)
- [Publisher profile](https://clawhub.ai/user/786793119)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify local reminder data under ~/.memory/reminders/reminders.json when used with the referenced reminder script.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
