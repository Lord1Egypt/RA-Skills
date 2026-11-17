## Description:

Daily Stoic companion for personal growth and virtue tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stoklemariano](https://clawhub.ai/user/stoklemariano)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to receive daily Stoic affirmations, evening virtue check-ins, weekly progress summaries, and on-demand support during anxiety or impulse moments. It helps an agent configure scheduled messages, maintain reflection notes, and tailor guidance to the user's language, relationships, and goals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist sensitive personal reflections, relationship details, phone numbers, or chat IDs in local memory files.

Mitigation: Use it only in a private workspace, avoid saving identifying details unless needed, and confirm where memory files are stored before use.

Risk: The skill creates scheduled messaging jobs for recurring affirmations, check-ins, and summaries.

Mitigation: Set a clear stop or delete process for cron jobs and verify delivery channels, targets, and schedules before enabling them.

Risk: The skill offers companionship and impulse support but is not therapy.

Mitigation: Use the built-in boundary to suggest professional support when the user shows signs of deep distress.

## Reference(s):

- [Stoic Companion configuration template](references/config-template.md)
- [Stoic Companion ClawHub release](https://clawhub.ai/stoklemariano/skills/stoic-companion)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain-language guidance with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local memory notes and scheduled messaging configuration for daily and weekly routines.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
