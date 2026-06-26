## Description: <br>
Export Slack thread messages from a logged-in Slack web tab into CSV using an attached Chrome Browser Relay tab. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Devdha](https://clawhub.ai/user/Devdha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and workspace operators use this skill to export authorized Slack thread conversations by user, channel, and date range into reusable CSV and JSONL datasets. It is best suited for operator-led archival, review, or analysis workflows rather than unattended compliance export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exports workplace Slack messages through a logged-in browser session and can expose sensitive or unauthorized data. <br>
Mitigation: Use it only when authorized, keep runs limited to specific users, channels, and dates, store CSV and JSONL outputs securely, and delete exports when they are no longer needed. <br>
Risk: Broad exports or fast request loops may hit Slack rate limits, time out browser evaluation, or leave a partial export. <br>
Mitigation: Run preflight checks, split work into small channel and date batches, use backoff on rate limits, save raw JSONL progress, and retry only failed channels. <br>
Risk: CSV exports may contain message text that is risky to open directly in spreadsheet software. <br>
Mitigation: Review CSV handling before opening exports in spreadsheets and sanitize formula-like cell content when spreadsheet review is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Devdha/slack-thread-export) <br>
- [Slack thread export notes](references/notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with bash command examples; generated exports are CSV, JSONL, summary JSON, and failed-channel text files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an attached logged-in Slack web tab and explicit user, team, channel, date, and output-path settings.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
