## Description: <br>
A bilingual trading workflow helper for managing daily stock-trading schedules, generating opening, closing, and daily report drafts, monitoring portfolio risk thresholds, and supporting trade review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[horizoncove](https://clawhub.ai/user/horizoncove) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Stock traders and quantitative trading teams use this skill to structure a trading day, draft supervisor-ready reports, monitor configured stop-loss and take-profit thresholds, and maintain a repeatable review workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio configuration and generated reports can contain sensitive account values, positions, symbols, and trade records. <br>
Mitigation: Replace or delete sample portfolio data before use, store generated reports privately, and avoid sharing financial details in broad chats or logs. <br>
Risk: The risk monitor sends stock symbols to Tencent's market-data endpoint over HTTP. <br>
Mitigation: Run the monitor only when that data transfer is acceptable for the user's environment and privacy requirements. <br>
Risk: Stop-loss and take-profit thresholds may be mistaken for automatic trading advice. <br>
Mitigation: Use thresholds as decision-support templates and require trader review before taking financial action. <br>


## Reference(s): <br>
- [Daily Schedule](references_files/daily-schedule.md) <br>
- [Report Templates](references_files/report-templates.md) <br>
- [Risk Management](references_files/risk-management.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/horizoncove/trader-daily) <br>
- [Publisher Profile](https://clawhub.ai/user/horizoncove) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, command examples, JSON configuration guidance, and plain-text risk alerts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports and alerts may include sensitive portfolio holdings, account values, symbols, and trade records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
