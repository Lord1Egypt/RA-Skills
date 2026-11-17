## Description:

Wuxing Daily helps agents provide Chinese-language five-elements astrology readings, Ba Zi-style profile summaries, daily fortune guidance, lunar date conversion, and optional daily reminder setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timyljob2011-sudo](https://clawhub.ai/user/timyljob2011-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to generate cultural or entertainment-focused five-elements readings, daily fortune summaries, and lunar calendar conversions from birth date information. Operators may also use it to propose local shell commands for running the bundled scripts or setting a daily reminder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The daily reminder workflow can create a persistent cron task.

Mitigation: Require explicit approval before enabling reminders, show the exact cron command, and provide removal steps before scheduling anything.

Risk: The skill may request birth date and birth hour information.

Mitigation: Collect only the date and time details needed for the requested reading and avoid retaining them after the session.

Risk: Fortune, health, finance, or major life-decision suggestions could be mistaken for professional advice.

Mitigation: Present outputs as entertainment or cultural reference and direct users to qualified professionals for medical, financial, legal, or other consequential decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/timyljob2011-sudo/skills/wuxing-daily)
- [README](artifact/README.md)
- [Six-Cycle Nayin Table](artifact/nayin_table.md)
- [Wuxing Daily Correspondence Table](artifact/wuxing_daily.md)
- [Zi Wei Dou Shu Main Stars](artifact/ziwei_stars.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with optional inline shell commands and formatted console-style reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language astrology and almanac content; no external API output format is documented.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
