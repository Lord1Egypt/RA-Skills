## Description:

Searches, scans, and monitors student accommodation availability across Yugo and Aparto providers, including room availability, semester options, booking probes, price comparisons, and optional alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gonzalopezgil](https://clawhub.ai/user/gonzalopezgil)

### License/Terms of Use:


## Use Case:

Students, housing searchers, and assisting agents use this skill to find, compare, and monitor student accommodation options across supported Yugo and Aparto cities. It helps users discover properties, scan current availability, probe booking options, and receive alerts for new matches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional notification backends may share room-search details with external services.

Mitigation: Use stdout notifications for the most private mode, and enable webhook, Telegram, or OpenClaw notifications only when external alerts are intended.

Risk: Watch mode and cron-job assistance can create ongoing monitoring or follow-up automation.

Mitigation: Enable watch mode, OpenClaw agent mode, or cron-job assistance only after confirming the desired monitoring scope and automation behavior.

Risk: The skill invokes a separate student_rooms CLI.

Mitigation: Confirm that the installed student_rooms CLI is trusted before using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gonzalopezgil/skills/student-rooms)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, YAML configuration examples, and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce structured JSON from CLI commands and alert messages through stdout, webhook, Telegram, or OpenClaw notification backends.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
