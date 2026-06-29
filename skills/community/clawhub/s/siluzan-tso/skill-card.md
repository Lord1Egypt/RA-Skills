## Description: <br>
Routes agents through Siluzan TSO advertising workflows for account management, campaign operations, diagnostics, reporting, finance tasks, alerts, and platform-specific ad work across Google, Bing, Yandex, TikTok, Kwai, and Meta. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sigedev01-bit](https://clawhub.ai/user/sigedev01-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External advertising operators and agents use this skill to select the correct Siluzan TSO workflow, run CLI-backed advertising account tasks, prepare campaign configurations, and generate account, market, website, and platform reports. Write actions affect advertising, finance, permissions, or account-linking workflows and should be confirmed before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide workflows with broad authority over advertising accounts, finance/account-management actions, permissions, and account links. <br>
Mitigation: Install only when this access is intended, use short-lived credentials where possible, and require explicit confirmation before create, update, publish, delete, transfer, invoice, permission, or account-linking actions. <br>
Risk: Installer behavior may change local agent environments through global npm installation, npm registry changes, dependency installation, and registration into multiple assistant skill directories. <br>
Mitigation: Review the installer before use and verify the target assistant directories, registry settings, and installed dependencies before deploying broadly. <br>
Risk: Generated campaign configurations, optimization guidance, and report outputs can influence ad spend, targeting, and business decisions. <br>
Mitigation: Validate JSON templates and CLI outputs, review recommendations against account data and platform policy, and keep write operations gated behind human approval. <br>


## Reference(s): <br>
- [Siluzan TSO ClawHub skill page](https://clawhub.ai/sigedev01-bit/skills/siluzan-tso) <br>
- [Publisher profile](https://clawhub.ai/user/sigedev01-bit) <br>
- [Core intent routing](references/core/intent-routing.md) <br>
- [Agent conventions](references/core/agent-conventions.md) <br>
- [Playbooks](references/core/playbooks.md) <br>
- [Workflows](references/core/workflows.md) <br>
- [Setup](references/core/setup.md) <br>
- [Accounts](references/accounts/accounts.md) <br>
- [Google Ads](references/google-ads/google-ads.md) <br>
- [Reporting](references/analytics/reporting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration templates, and report-oriented deliverables such as HTML, Excel, Markdown, or JSON when a workflow renders them.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, siluzan-tso-cli, and authenticated Siluzan credentials; write workflows require user confirmation before execution.] <br>

## Skill Version(s): <br>
1.1.30 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
