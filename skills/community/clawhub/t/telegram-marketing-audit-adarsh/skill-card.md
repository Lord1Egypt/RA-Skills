## Description: <br>
Handles the Telegram /marketing_audit command by running a marketing audit for an Instagram handle or website domain and returning the report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AdarshVMore](https://clawhub.ai/user/AdarshVMore) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Telegram bot operators and marketing teams use this skill to trigger a marketing audit from chat and receive the generated report without leaving Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit reports and possible backend error text may be visible in Telegram chats. <br>
Mitigation: Enable the command only in intended chats and review report and error visibility before deployment. <br>
Risk: The skill depends on a separate marketing-orchestrator skill and collector API keys for the actual audit work. <br>
Mitigation: Review the dependent skill and confirm required API keys are configured before enabling the command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AdarshVMore/telegram-marketing-audit-adarsh) <br>
- [Publisher profile](https://clawhub.ai/user/AdarshVMore) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Telegram chat replies with Markdown report content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a separate marketing-orchestrator skill and configured collector API keys to produce the final audit report.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
