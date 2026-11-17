## Description:

WordPal is a Chinese-language English vocabulary tutor embedded in chat that personalizes word selection from recent OpenClaw memory, guides learn and report flows, uses FSRS-style review scheduling, and can add scheduled study reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lymon-srad](https://clawhub.ai/user/lymon-srad)

### License/Terms of Use:

MIT-0

## Use Case:

Learners use WordPal through OpenClaw chat to set an English study goal, practice new and due vocabulary, receive hints after wrong answers, and review learning reports. The skill is intended for agents that can run its Node.js scripts to maintain local study state and optional reminder schedules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores vocabulary profile data and study history locally.

Mitigation: Install it only in a workspace where local learner state is appropriate, and keep that workspace access scoped to trusted users.

Risk: Recent OpenClaw memory summaries are used as personalization context.

Mitigation: Keep untrusted or instruction-like text out of memory summaries where possible, and review personalized word choices before relying on them.

Risk: Scheduled study reminders can be added when push times are enabled.

Mitigation: Enable push times only when reminders are desired, and review the generated OpenClaw cron registrations.

## Reference(s):

- [README](README.md)
- [Learn Flow](references/learn.md)
- [Onboarding Flow](references/onboarding.md)
- [Report Flow](references/report.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese-language Markdown chat responses backed by JSON results from local Node.js scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May register OpenClaw cron reminders only when the learner explicitly enables push times.]

## Skill Version(s):

3.1.0 (source: server release metadata, released 2026-03-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
