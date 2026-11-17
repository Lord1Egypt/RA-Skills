## Description:

Orchestrates Excel and CSV data analysis workflows, including multi-sheet reading, large-file handling, data cleaning, filtering, aggregation, visualization, and Excel or CSV export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to guide agents through structured spreadsheet workflows, from inspecting Excel or CSV inputs through cleaning, statistics, visualization, and report export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports over-activation for spreadsheet tasks.

Mitigation: Use the skill only when the request is specifically about Excel or CSV analysis, cleaning, statistics, visualization, or export.

Risk: The security evidence reports that sensitive spreadsheet-derived data may be written to predictable local files.

Mitigation: Run the skill in an isolated workspace and review generated file paths before handling confidential spreadsheets.

Risk: The security guidance warns that multilingual cleaning can remove non-Chinese text.

Mitigation: Apply multilingual or Chinese-only text cleaning only when that behavior is explicitly intended for the dataset.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sensenova-skills/skills/sn-da-excel-workflow)
- [Publisher profile](https://clawhub.ai/user/sensenova-skills)
- [Artifact root skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python code snippets, shell-style file paths, and generated spreadsheet or report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Excel, CSV, chart, and report outputs from user-provided spreadsheet data.]

## Skill Version(s):

2026.8.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
