## Description: <br>
Siluzan TSO routes agents through advertising account operations, campaign creation, analytics, reporting, finance, lead, and automation workflows using the siluzan-tso CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sigedev01-bit](https://clawhub.ai/user/sigedev01-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External advertising operations teams and agents use this skill to manage TSO ad accounts, create Search and PMax campaigns, run analytics and reports, and handle finance, lead, and alert workflows through documented CLI procedures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide actions against live advertising accounts, billing, access control, delinking, automation, and lead-data workflows. <br>
Mitigation: Require explicit human confirmation before any live spend, billing, access-control, delink, or automation action, and keep write operations auditable. <br>
Risk: The installer and CLI configuration can affect the local host and store credentials. <br>
Mitigation: Review installer scripts before running them, avoid one-line remote execution, and protect ~/.siluzan/config.json and related environment secrets. <br>
Risk: Lead, identity, or banking data may be exposed if pasted into chat or reports unnecessarily. <br>
Mitigation: Minimize sensitive data disclosure, redact raw lead and identity/banking details unless required, and limit sharing to trusted workspaces. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sigedev01-bit/skills/siluzan-tso) <br>
- [Core Agent Conventions](artifact/references/core/agent-conventions.md) <br>
- [Core Workflows](artifact/references/core/workflows.md) <br>
- [Core Playbooks](artifact/references/core/playbooks.md) <br>
- [Setup](artifact/references/core/setup.md) <br>
- [Accounts](artifact/references/accounts/accounts.md) <br>
- [Google Ads](artifact/references/google-ads/google-ads.md) <br>
- [Google Ads Campaign Plan](artifact/references/google-ads/google-ads-campaign-plan.md) <br>
- [PMax API](artifact/references/google-ads/pmax-api.md) <br>
- [Account Analytics](artifact/references/analytics/account-analytics.md) <br>
- [Report Templates](artifact/report-templates/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, HTML reports, CLI command guidance, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce account, campaign, billing, lead, and report artifacts from live advertising workflows when connected to authenticated services.] <br>

## Skill Version(s): <br>
1.1.29 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
