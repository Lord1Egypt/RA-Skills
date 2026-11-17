## Description:

Guides an agent to help users plan traditional bone or antler tool making by identifying suitable materials, calculating processing schedules, generating templates and reminders, and tracking tests while the human performs all physical work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to convert available animal bones or antlers into awls, needles, scrapers, hooks, or similar hand tools with agent-generated recipes, schedules, logs, and barter or inventory templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command is not version-pinned, creating a generic supply-chain risk.

Mitigation: Install from a trusted ClawHub/npm source, prefer a version-pinned installer when available, and use a dedicated workspace.

Risk: The workflow may store craft photos, progress logs, templates, and reminders in the workspace.

Mitigation: Use a dedicated project directory and review stored files before sharing or publishing the workspace.

Risk: The physical process involves boiling, cutting, drilling, and possible bone dust exposure.

Mitigation: Follow the skill's disclosed safety cautions for ventilation, protective equipment, heat handling, cutting, drilling, and dust control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtousehumans/skills/traditional-bone-tool-making-basics)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands]

**Output Format:** [Markdown with checklists, schedules, templates, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce filesystem-backed craft logs, progress trackers, reminders, and reusable templates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
