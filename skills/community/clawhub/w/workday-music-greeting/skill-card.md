## Description:

Auto-switch music scenes by workday time slot and send matching greeting emails with scene-specific GIFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

People running personal or workspace automation use this skill to trigger time-based music scenes and send matching greeting emails during the workday.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured music command can execute arbitrary shell commands if MUSIC_CMD is set from untrusted input.

Mitigation: Use a fixed allowlisted executable with non-shell arguments, and avoid accepting MUSIC_CMD from untrusted sources.

Risk: Scheduled runs can perform real side effects by changing music scenes and sending email automatically.

Mitigation: Review cron schedules and run with --dry-run before enabling recurring execution.

Risk: SMTP credentials in .env can be exposed or misused if the skill runs with broad account privileges.

Mitigation: Keep .env protected, use a low-privilege account, and update the mail dependency before using real SMTP credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/workday-music-greeting)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, and Node.js execution details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and npm, plus the home-music and imap-smtp-email skills. May execute local music-control commands and send SMTP email when run outside dry-run mode.]

## Skill Version(s):

1.2.0 (source: server release metadata; artifact frontmatter and package.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
