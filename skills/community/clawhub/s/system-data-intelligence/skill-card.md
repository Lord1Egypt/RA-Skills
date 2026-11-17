## Description:

System Data Intelligence helps agents read common office and data files, connect to databases and REST APIs, analyze datasets, mask selected sensitive values, and generate charts or reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaojie911272507](https://clawhub.ai/user/zhaojie911272507)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to process spreadsheets, documents, CSV/JSON data, SQL query results, and API responses, then produce analysis summaries, structured outputs, and visual reports. It is intended for broad data work where file access, database/API access, and report generation are explicitly desired.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner judged this a suspicious broad data-processing skill because it can expand simple requests into file reading, data analysis, network or database access, and persistent report output without clear user control.

Mitigation: Review the skill before installing, run it only where broad data processing is intended, and require explicit user approval before reading sensitive files, querying databases, calling APIs, or writing reports.

Risk: The skill includes masking utilities for sensitive values, but the security guidance says not to rely on masking as complete privacy protection.

Mitigation: Use a contained environment for sensitive work, minimize input data, validate masking results, and clean temporary outputs after use.

Risk: The security guidance warns against opening untrusted Office or WPS documents through desktop automation.

Mitigation: Avoid desktop automation for untrusted documents; prefer contained parsing or conversion workflows and inspect files before opening them with office applications.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhaojie911272507/skills/system-data-intelligence)
- [File Formats Reference](references/file-formats.md)
- [Windows API Reference](references/windows-api.md)
- [macOS API Reference](references/macos-api.md)
- [Linux API Reference](references/linux-api.md)
- [Visualization Patterns Reference](references/viz-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; generated artifacts may include HTML, PNG, JSON, CSV, and Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce persistent report files and structured analysis outputs under an outputs directory.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
