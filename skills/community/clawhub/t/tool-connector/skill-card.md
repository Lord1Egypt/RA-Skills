## Description:

Connect OpenClaw to tools such as Slack, GitHub, Jira, Confluence, Grafana, Datadog, PagerDuty, Outlook, and Google Drive by helping an agent infer setup details from a tool URL, store local credentials, and use bundled connection recipes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhixiangluo](https://clawhub.ai/user/zhixiangluo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to set up local, user-identity tool access for workplace services, verify existing connection recipes, and draft new integration recipes when a supported recipe does not exist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can grant an agent user-equivalent access to connected workplace tools.

Mitigation: Install only for tools the user actively needs, prefer narrowly scoped tokens, and review access expectations before enabling each connection.

Risk: The skill handles API tokens, SSO cookies, and bearer tokens that may be powerful or long-lived.

Mitigation: Protect local credential files, avoid copying browser-session JWTs where possible, and rotate any token whose prefix may have appeared in logs.

Risk: SSO setup uses Playwright browser automation to capture session material from a headed Chromium session.

Mitigation: Review the SSO helper scripts before use and remove insecure TLS bypasses or replace plaintext storage with a secret store where required.

## Reference(s):

- [Tool Connector ClawHub Page](https://clawhub.ai/zhixiangluo/skills/tool-connector)
- [10xProductivity Methodology](https://github.com/ZhixiangLuo/10xProductivity)
- [Setup Guide](references/setup.md)
- [Add a New Tool](references/add-new-tool.md)
- [Bundled Tool Connection Recipes](references/tool_connections/)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands, code snippets, and local configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update local credential configuration under the user's OpenClaw configuration when connection setup is run.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
