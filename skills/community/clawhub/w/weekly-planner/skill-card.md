## Description:

File-based weekly planning system (TOML) with inbox capture, time-block scheduling, weekly review, and optional calendar publishing (Google Calendar via gogcli or .ics export).

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanmanchester](https://clawhub.ai/user/tristanmanchester)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to maintain a lightweight weekly planner in plain files: capture inbox tasks, create or roll over week plans, schedule time blocks, run weekly reviews, and optionally publish scheduled blocks to a calendar.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initialization with --force can delete the resolved target planner directory.

Mitigation: Run initialization without --force unless the target is a verified disposable planner directory.

Risk: Optional Google Calendar sync depends on an unpinned third-party gogcli installation and can modify managed calendar events.

Mitigation: Prefer .ics export when possible; for Google Calendar sync, use a dedicated calendar, review dry-run output, and keep calendar.write_enabled false until explicitly applying changes.

## Reference(s):

- [Weekly Planner Skill Page](https://clawhub.ai/tristanmanchester/skills/weekly-planner)
- [PLANNER_SCHEMA.md](references/PLANNER_SCHEMA.md)
- [CALENDAR_SYNC.md](references/CALENDAR_SYNC.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with TOML and bash snippets; planner artifacts as TOML, Markdown, and optional .ics files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local workspace files and Python scripts; optional Google Calendar sync requires gogcli and explicit write enablement]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter metadata.version is 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
