## Description:

Analyze agent session logs and generate PDF reports with optional Notion sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to summarize agent session activity, skill usage, failures, and duration from JSONL logs. It can produce a local PDF report and, when configured with scoped Notion credentials, sync a truncated report excerpt to a Notion database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports can contain session IDs, errors, and other log-derived details that may be sent to Notion.

Mitigation: Review the generated PDF before syncing and use a Notion integration token scoped only to the intended database.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/session-log-analyzer)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands; generated PDF report; optional Notion page URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PDF output is saved to pdfs/session_analysis_report.pdf; Notion sync uploads the first 2000 characters of extracted report text when credentials are configured.]

## Skill Version(s):

99.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
