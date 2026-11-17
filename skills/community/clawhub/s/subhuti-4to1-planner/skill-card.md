## Description:

AI planning coach using the 4To1 Method™ that turns a 4-year vision into daily action across Notion, Todoist, Google Calendar, or local Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dorjenorbulim](https://clawhub.ai/user/dorjenorbulim)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal-productivity agents use this skill to set up a structured 4To1 planning system, run weekly and quarterly reviews, choose daily priorities, and sync planning data with a selected backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud API tokens may be stored unsafely in local configuration.

Mitigation: Use the local backend or tightly scoped integrations where possible, protect configuration files with secure permissions, and prefer a secret manager for tokens.

Risk: The bundled status script may execute config-file contents as shell code.

Mitigation: Do not run the status script against any config file you do not fully trust; parse configuration inertly before execution.

Risk: Sensitive goals, reflections, or productivity data may be sent to connected cloud services.

Mitigation: Avoid placing sensitive planning content in Notion, Todoist, or Google services unless that sharing is intended.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/dorjenorbulim/skills/subhuti-4to1-planner)
- [4To1 Planner homepage](https://4to1planner.com)
- [4To1 Planner free starter kit](https://4to1planner.com/free-download.html)
- [4To1 Planner templates and premium](https://4to1planner.com/shop.html)
- [Weekly review template](artifact/scripts/weekly_review.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, API examples, planning prompts, and local file templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or write planning state through Notion, Todoist, Google Calendar, or local Markdown depending on user-selected backend.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact _meta.json lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
