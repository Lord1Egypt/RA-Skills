## Description:

Touch The Grass helps users plan and complete offline wellness activities, schedule reminders in Google Calendar, track scores and streaks, and optionally verify completion with photos or social posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alannetwork](https://clawhub.ai/user/alannetwork)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill when they feel stressed, burned out, or disconnected from non-work routines and want an agent to suggest offline activities, schedule them, and track completion over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Daily proactive reminders and Calendar event creation may be unwanted if enabled without explicit user consent.

Mitigation: Confirm opt-in before configuring cron, heartbeat reminders, or Calendar events, and avoid or remove the setup if the user declines.

Risk: The skill tracks score, streak, activity history, mood check-ins, and optional photo or social-post confirmations.

Mitigation: Explain what will be stored or analyzed before use, offer text-only confirmation, and avoid detailed commentary on personal photo contents.

Risk: The default reminder schedule assumes America/Mexico_City.

Mitigation: Confirm the user's timezone before creating reminders or Calendar events and adjust the cron timezone when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alannetwork/skills/touch-the-grass)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Conversational text and Markdown with optional inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create Google Calendar event instructions, daily reminder setup commands, progress summaries, and agent-memory state descriptions.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
