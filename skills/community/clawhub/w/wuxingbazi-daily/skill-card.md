## Description:

Wuxingbazi Daily helps agents produce Chinese five-elements and Bazi-style astrology reports, daily fortune guidance, almanac-style auspicious and inauspicious suggestions, and lunar calendar conversions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timyljob2011-sudo](https://clawhub.ai/user/timyljob2011-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate entertainment-oriented Chinese almanac and Bazi reports from birth-date inputs, convert between solar and lunar dates, and prepare daily fortune summaries or reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent reminder setup may create a cron or scheduled task without sufficiently clear confirmation, containment, or removal instructions.

Mitigation: Require explicit user approval of the command, path, schedule, and removal method before creating any scheduled task.

Risk: Astrology, health, investment, and decision-related suggestions may be mistaken for professional advice.

Mitigation: Frame fortune, health, and investment-style guidance as entertainment and avoid presenting it as a basis for important decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/timyljob2011-sudo/skills/wuxingbazi-daily)
- [README](artifact/README.md)
- [Sixty Jiazi Nayin Five Elements Table](artifact/nayin_table.md)
- [Five Elements Daily Correspondence Table](artifact/wuxing_daily.md)
- [Zi Wei Dou Shu Major Stars Reference](artifact/ziwei_stars.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with command snippets and formatted astrology reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scheduled reminder setup guidance; users should approve any persistent scheduling command before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
