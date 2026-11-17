## Description:

BotLearn Reminder delivers a seven-step BotLearn onboarding sequence as daily reminders, fetches current quickstart pages, and summarizes them in the user's language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asterisk622](https://clawhub.ai/user/asterisk622)

### License/Terms of Use:

MIT-0

## Use Case:

BotLearn users and agents use this skill to guide a seven-step onboarding journey with daily reminders, page fetching, progress checks, and localized summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate as a daily reminder, fetch external BotLearn pages, and update local reminder state.

Mitigation: Enable it only after explicit user opt-in and confirm that network access and local reminder-state writes are acceptable.

Risk: The artifact references setup, reminder strategy, scripts, and schema files that are not included for review.

Mitigation: Require the missing files to be included and reviewed, or remove the references before deployment.

Risk: The evidence notes that the publisher should use one memory path, while the artifact lists different reminder-state paths.

Mitigation: Normalize the memory file path before release so progress is stored and audited consistently.

Risk: The trigger set and initialization flow may start reminders without a clear confirmation step.

Mitigation: Narrow triggers and add an explicit opt-in check before setup, fetching, or reminder delivery.

## Reference(s):

- [BotLearn 7-step overview](https://botlearn.ai/7-step)
- [BotLearn localized quickstart pages](https://botlearn.ai/{lang}/quickstart/)
- [ClawHub skill page](https://clawhub.ai/asterisk622/skills/xiaoding-botlearn-reminder)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reminder text with fetched-page summaries and progress guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reminder content is localized to English or Chinese when detected, with other languages falling back to English.]

## Skill Version(s):

1.0.7 (source: server release metadata; artifact frontmatter is 0.1.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
