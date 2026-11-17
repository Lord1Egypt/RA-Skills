## Description:

Automatically collects Ocean Engine Qianchuan and Douyin Shop operating metrics, writes them to Feishu Sheets, and prepares daily operations reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhitaog500-prog](https://clawhub.ai/user/zhitaog500-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Operations, advertising, and live-commerce teams use this skill to refresh daily Qianchuan and Douyin Shop metrics, write the results into Feishu Sheets, and archive CSV or Markdown reports when enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an authenticated Ocean Engine browser session and can expose sensitive business account data if session state or reports are shared.

Mitigation: Keep storage_state.json, STORAGE_STATE_BASE64, config.json, generated reports, and Feishu secrets private; prefer STORAGE_STATE_BASE64 over local session files.

Risk: Feishu writes modify the configured spreadsheet and could affect the wrong workbook, sheet, or cell range if configuration is incorrect.

Mitigation: Review spreadsheetToken, sheet IDs, and ranges before running, and require CONFIRM_WRITE_FEISHU=1 before writes are allowed.

Risk: Exported table values may carry untrusted spreadsheet content before formula escaping is added.

Mitigation: Avoid exporting untrusted table values and keep local CSV or Markdown report generation disabled unless a private archive is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhitaog500-prog/skills/qianchuan-doudian-daily-report)
- [Publisher profile](https://clawhub.ai/user/zhitaog500-prog)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands; optional CSV and Markdown report files; Feishu Sheet updates when enabled.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, Playwright browser dependencies, an authenticated Ocean Engine session, and Feishu credentials supplied through environment variables.]

## Skill Version(s):

1.0.4 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
