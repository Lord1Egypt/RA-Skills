## Description:

Skill Combinator helps an agent identify, evaluate, log, and periodically report useful combinations of installed skills for complex multi-domain tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georges91560](https://clawhub.ai/user/georges91560)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to help agents plan across multiple installed skills, preserve observed combination outcomes, and run a weekly distillation report. It is intended for agents with at least two other skills and an OpenClaw workspace that supports the documented learning files and scheduled reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads agent and workspace context and keeps long-lived combination history.

Mitigation: Review the requested read paths before installation, limit or remove MEMORY.md access where possible, and inspect COMBINATIONS.md and .learnings entries regularly.

Risk: Scheduled reports may send operational summaries through the configured Telegram channel.

Mitigation: Keep Telegram reports free of sensitive project details and store TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID only in environment configuration.

Risk: Multi-skill plans may propose side-effecting actions when paired with other skills.

Mitigation: Require operator review for macro-level or unapproved actions and review generated proposals before adding them to long-lived agent guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/georges91560/skills/skill-combinator)
- [README](artifact/README.md)
- [Configuration guide](artifact/CONFIGURATION.md)
- [Weekly cron prompt](artifact/cron-message.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, configuration snippets, and structured report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent combination records, learning entries, feature-request notes, memory summaries, and weekly operational reports when used in its intended OpenClaw environment.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
