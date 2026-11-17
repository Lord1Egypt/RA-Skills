## Description:

Roadmap helps agents use a local command-line planner for timelines, milestones, feature tracking, priority scoring, dependency mapping, and progress reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other command-line users use Roadmap to capture roadmap items, plan and track milestones, review progress, export planning notes, and inspect local status from a terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Roadmap entries are saved locally and may include sensitive planning information.

Mitigation: Avoid storing highly sensitive business plans unless you manage the data directory, file permissions, and retention yourself.

Risk: CSV and JSON exports may not safely escape all values for spreadsheet or machine-readable use.

Mitigation: Review and sanitize exports before opening them in spreadsheets, importing them into other systems, or sharing them.

## Reference(s):

- [Roadmap skill page](https://clawhub.ai/bytesagain1/skills/roadmap)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Terminal text and local log/export files in JSON, CSV, or TXT]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores roadmap data under ~/.local/share/roadmap by default; ROADMAP_DIR can change the data directory.]

## Skill Version(s):

2.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
