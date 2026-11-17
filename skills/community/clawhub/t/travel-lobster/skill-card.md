## Description:

Travel Lobster lets an agent autonomously explore public web content, send illustrated postcard-style letters with source links to chat, and maintain a persistent travel journal for future trips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangwenyu2](https://clawhub.ai/user/yangwenyu2)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to run a recurring autonomous web exploration workflow that sends postcard-style chat updates with generated illustrations and source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to run as a recurring autonomous agent that browses public sites, spends API credits, sends chat messages, and keeps a persistent journal.

Mitigation: Install only when this behavior is intended, start with a one-shot or manual run, monitor scheduled jobs, and remove the travel-next cron job when stopping autonomous operation.

Risk: The security evidence flags unsafe shell-based handling of .travel-config.

Mitigation: Review or fix .travel-config sourcing before use, and inspect generated configuration after setup.

Risk: The optional watchdog can restart the recurring loop after failures.

Mitigation: Avoid adding the watchdog until the behavior is trusted, and remove any watchdog crontab entry when disabling the skill.

## Reference(s):

- [Travel prompt template](references/travel-prompt.md)
- [OpenRouter chat completions API](https://openrouter.ai/api/v1/chat/completions)
- [ClawHub skill page](https://clawhub.ai/yangwenyu2/skills/travel-lobster)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands, chat messages, generated image files, and source URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw, OpenRouter API credentials, and user-provided chat routing.]

## Skill Version(s):

1.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
