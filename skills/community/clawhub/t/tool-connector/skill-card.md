## Description: <br>
Connects OpenClaw agents to external tools such as Slack, GitHub, Jira, Confluence, Grafana, Datadog, PagerDuty, Outlook, and Google Drive with URL-driven setup, local credential storage, and optional Playwright-based SSO token capture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZhixiangLuo](https://clawhub.ai/user/ZhixiangLuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to give an OpenClaw agent access to workplace tools and service APIs, either by configuring bundled connection recipes or by creating a new tool connection pattern. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may allow an agent to act as the logged-in user across chat, email, Drive, CI, ticketing, and observability tools. <br>
Mitigation: Use scoped API tokens or dedicated low-privilege accounts and confirm organizational policy before installation. <br>
Risk: SSO flows capture and persist browser/session credentials for multiple services. <br>
Mitigation: Review the Playwright SSO helper before use, protect local token files, and store tokens only for actively used tools. <br>
Risk: Some bundled examples weaken transport security checks. <br>
Mitigation: Avoid using insecure TLS examples as-is and adapt them to the target organization's certificate and transport requirements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ZhixiangLuo/tool-connector) <br>
- [Setup Guide](references/setup.md) <br>
- [Add a New Tool](references/add-new-tool.md) <br>
- [10xProductivity Methodology](https://github.com/ZhixiangLuo/10xProductivity) <br>
- [OpenClaw Sync Script](scripts/openclaw_sync.py) <br>
- [Playwright SSO Helper](scripts/shared_utils/playwright_sso.py) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May result in local environment variables and credential files for configured tools.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
