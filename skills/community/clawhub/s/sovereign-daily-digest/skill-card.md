## Description:

Compile and summarize configured news, weather, calendar, tasks, quotes, and optional email sources into a structured daily personal intelligence briefing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryudi84](https://clawhub.ai/user/ryudi84)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to generate daily personal briefings from configured calendar, task, news, weather, quote, GitHub Issues, and optional email sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured sources may expose private calendar, task, GitHub, email, or local-file data beyond the user's intended scope.

Mitigation: Review the configuration before running, use explicit source opt-in, and avoid sensitive calendars, task files, or authenticated GitHub accounts until source selection is tightened.

Risk: HTML output may include unsafe feed or local content.

Mitigation: Prefer Markdown or plain text, or inspect and sanitize HTML output before opening or sharing until HTML escaping is fixed.

Risk: Scheduling, email sending, and archive cleanup can create persistent actions or delete digest files.

Mitigation: Require clear confirmation before cron or scheduled-task setup, email sends, or archive cleanup, and review output_dir and max_archive_days settings.

Risk: Python path interpolation in the shell helper can mishandle crafted paths.

Mitigation: Run from trusted install paths and review path handling before using custom paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryudi84/skills/sovereign-daily-digest)
- [Publisher profile](https://clawhub.ai/user/ryudi84)

## Skill Output:

**Output Type(s):** [text, markdown, HTML, configuration, shell commands]

**Output Format:** [Markdown, HTML, or plain-text digest with saved report files and a concise run summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or uses a local daily-digest configuration file and can save dated digest files under the configured output directory.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
