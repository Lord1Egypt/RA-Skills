## Description: <br>
Smart auto-updater with AI-powered impact assessment that checks OpenClaw and ClawHub skill updates, analyzes impact, and decides whether to auto-update or report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor OpenClaw and ClawHub skill updates, assess update impact, and either apply low-risk updates or produce review reports for manual action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring unattended updates can change OpenClaw or installed skills without manual review. <br>
Mitigation: Start in report-only mode with SMART_UPDATER_AUTO_UPDATE=NONE, test manually, and add scheduled runs only after confirming the target agent and update policy. <br>
Risk: The documented risk gate may not reliably block high-risk changes. <br>
Mitigation: Use conservative thresholds, review generated reports before applying changes, and do not rely on the HIGH-risk gate until the scoring threshold is fixed. <br>
Risk: Webhook URLs used for report delivery can expose notification channels if handled as plain text. <br>
Mitigation: Store webhook URLs as protected environment secrets and avoid committing or sharing configured values. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/litiao1224/smart-auto-updater-litiao) <br>
- [Publisher profile](https://clawhub.ai/user/litiao1224) <br>
- [Risk Assessment Methodology](references/risk-assessment.md) <br>
- [Report Templates](references/report-templates.md) <br>
- [Integration Guide](references/integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with shell commands and environment-variable configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include risk classifications, update decisions, changelogs, and recommendations; may trigger update commands when configured to auto-update.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
