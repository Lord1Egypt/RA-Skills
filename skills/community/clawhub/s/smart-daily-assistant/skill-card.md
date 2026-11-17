## Description:

Smart Daily Assistant helps users manage reminders, notes, daily briefings, message drafts, quick replies, translations, planning, habits, birthdays, expenses, links, contacts, and related personal-assistant tasks while keeping data local.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkpareek0315](https://clawhub.ai/user/mkpareek0315)

### License/Terms of Use:


## Use Case:

External users use this personal-assistant skill to save local reminders, notes, contacts, expenses, habits, links, and quick-reply templates, and to generate draft messages, translations, briefings, and plans through chat commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores personal reminders, notes, contacts, expenses, habits, links, and usage history locally.

Mitigation: Use explicit commands for saved data, periodically review ~/.openclaw/smart-daily-assistant/, and delete records or the folder when local retention is no longer wanted.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown-style chat responses with local JSON record descriptions and occasional shell setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for local personal-assistant workflows; generated message drafts and templates are copied or acted on manually by the user.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
