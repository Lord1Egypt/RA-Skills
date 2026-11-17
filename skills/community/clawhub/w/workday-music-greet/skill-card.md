## Description:

Auto-switch music scenes by workday schedule and send matching GIF greeting emails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to configure weekday music-scene changes and matching greeting emails for a personal workday routine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires SMTP credentials and can send recurring emails.

Mitigation: Use a dedicated app password or scoped credential, keep the .env file readable only by trusted users, and review recipients before enabling scheduled sends.

Risk: The skill can create persistent cron-based scheduled actions.

Mitigation: Review every generated cron entry before registration and remove entries when the routine is no longer needed.

Risk: Editable configuration is used to construct local shell commands.

Mitigation: Keep scripts/config.json writable only by trusted users and replace shell-string execution with argument-array execution before enabling scheduled jobs.

Risk: The server security verdict is suspicious and recommends dependency review.

Mitigation: Inspect the skill before installation, update nodemailer, and run the skill only from a trusted, non-shared directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/workday-music-greet)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May configure scheduled local actions and SMTP-based email delivery.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
