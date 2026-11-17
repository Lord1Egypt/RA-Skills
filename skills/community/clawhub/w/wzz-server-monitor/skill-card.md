## Description:

Monitors Linux server CPU, memory, and disk utilization and helps configure SMTP email alerts with thresholds, quiet windows, rate limits, and message templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiuyiwzz](https://clawhub.ai/user/xiuyiwzz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and server administrators use this skill to set up and operate resource monitoring for Linux hosts, including threshold checks, status inspection, test alerts, and SMTP-based alarm or recovery emails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a user-level cron job that runs the monitor every five minutes.

Mitigation: Inspect the exact crontab entry before installation and install only if recurring local execution is expected.

Risk: The monitor handles SMTP credentials and supports an unencrypted SMTP mode.

Mitigation: Store the SMTP secret in a separate chmod 600 file, prefer SSL or STARTTLS, and avoid smtp.security: none with credentials.

Risk: Setup may install Python dependencies before the monitor runs.

Mitigation: Use a virtual environment with pinned dependencies and a trusted package index.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiuyiwzz/skills/wzz-server-monitor)
- [Publisher profile](https://clawhub.ai/user/xiuyiwzz)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [Example configuration](assets/config.example.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local setup, validation, status checks, SMTP test messages, and cron installation.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; SKILL.md frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
