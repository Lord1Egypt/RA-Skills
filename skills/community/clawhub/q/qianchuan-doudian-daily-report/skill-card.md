## Description: <br>
自动抓取巨量千川、抖店经营数据，写入飞书表格，并生成每日经营日报。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhitaog500-prog](https://clawhub.ai/user/zhitaog500-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Store operators, ad buyers, and live-commerce teams use this skill to collect OceanEngine and Douyin shop operating metrics, update Feishu spreadsheets, and prepare daily business reports. It reduces repetitive copying, pagination mistakes, and manual field matching in daily reporting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses authenticated OceanEngine session data to read business metrics. <br>
Mitigation: Provide session state only in a controlled environment, prefer STORAGE_STATE_BASE64, and keep storage_state.json private if local storage state is explicitly enabled. <br>
Risk: Feishu writes can modify the configured spreadsheet, worksheet, and cell ranges. <br>
Mitigation: Verify spreadsheet tokens, sheet IDs, and ranges before running, and require CONFIRM_WRITE_FEISHU=1 for explicit write confirmation. <br>
Risk: Optional local CSV and Markdown reports may contain sensitive operating data. <br>
Mitigation: Leave generateReports disabled unless retained local copies are needed, and protect generated report files when enabled. <br>
Risk: OceanEngine page changes or stale selectors can produce missing or misaligned report data. <br>
Mitigation: Review scraped row counts and key totals after page or template changes, then update selectors and field mappings as needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhitaog500-prog/skills/qianchuan-doudian-daily-report) <br>
- [Publisher profile](https://clawhub.ai/user/zhitaog500-prog) <br>
- [Artifact usage guide](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration; runtime output updates Feishu sheets and can optionally write CSV and Markdown reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided OceanEngine session state and Feishu credentials. Local report files are opt-in.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
