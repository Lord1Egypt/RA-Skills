## Description: <br>
TPM Copilot helps Technical Program Managers and Project Managers turn Jira, Linear, GitHub, and calendar signals into status reports, risk tracking, meeting prep, dependency maps, and stakeholder dashboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reighlan](https://clawhub.ai/user/reighlan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Technical Program Managers and Project Managers use TPM Copilot to summarize program health, prepare meetings, track actions, monitor risks and blockers, map dependencies, and deliver stakeholder updates from configured work-management systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive project-management, source-control, Slack, and email systems through configured credentials. <br>
Mitigation: Use least-privileged tokens, keep config files out of repositories, and install only where this level of system access is acceptable. <br>
Risk: The skill can send reports to external destinations such as Slack or email. <br>
Mitigation: Verify webhook and email destinations before each send and review report content for confidential information. <br>
Risk: The action tracker can create Jira tickets from stored action items with limited safeguards. <br>
Mitigation: Review the stored action list before using ticket-creation options. <br>
Risk: Untrusted program names or configuration values may affect generated workspace paths and automation behavior. <br>
Mitigation: Use trusted program names and review configuration files before running automation. <br>


## Reference(s): <br>
- [TPM Copilot ClawHub page](https://clawhub.ai/reighlan/tpm-copilot) <br>
- [Jira API Setup](references/jira-setup.md) <br>
- [Linear API Setup](references/linear-setup.md) <br>
- [Report Templates & Customization](references/report-templates.md) <br>
- [Risk Categories & Severity](references/risk-categories.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, terminal summaries, JSON state files, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write reports, risk snapshots, dependency maps, action trackers, and workspace state under the configured TPM workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
