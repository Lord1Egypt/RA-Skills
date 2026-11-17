## Description:

Weekly Review helps an agent turn selected weekly AI usage, prompt quality, project, action, open-session, and automation facts into a structured review report with optional charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[testman2025](https://clawhub.ai/user/testman2025)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to produce weekly AI-usage retrospectives, prompt-improvement notes, inefficiency analysis, action ledgers, open-session cleanup lists, and automation summaries from agent-collected review-input data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to collect AI session data and inspect local workspace folders without clear built-in scope limits.

Mitigation: Use it only for intentionally selected sessions and workspaces, and prefer a user-supplied review-input JSON file.

Risk: The legacy analyzer can read a SQLite session database when explicitly pointed at one.

Mitigation: Use the documented public path where the agent supplies structured review-input data, and avoid scanning arbitrary session history.

Risk: Server-resolved import provenance is unavailable for this release.

Mitigation: Pin or verify the installer source before running npx or other install commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/testman2025/skills/weekly-review)
- [Project homepage](https://github.com/testman2025/weekly-review-skill)
- [Review input schema](schema/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown report with tables and optional SVG chart files; JSON can be returned when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user- or agent-supplied review-input JSON; chart files are generated locally from charts_data.]

## Skill Version(s):

1.2.5 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
