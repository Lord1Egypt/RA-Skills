## Description:

Performs a comprehensive SEO audit of a website across technical, content, architecture, and link factors, then returns prioritized, actionable optimization recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External site owners, marketers, and developers use this skill to audit websites for organic search issues across Google, Baidu, and related webmaster workflows. It helps produce prioritized SEO reports, implementation checklists, configuration examples, and recovery guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples may involve webmaster API tokens and outbound URL submissions.

Mitigation: Store tokens outside source files, treat them as secrets, and enable automatic URL submission only when each destination and trigger is intended.

Risk: Some examples or generated recommendations may use non-HTTPS endpoints or third-party webmaster services.

Mitigation: Prefer HTTPS endpoints and review each external service interaction before use.

Risk: The skill can propose shell commands and configuration changes for SEO tooling or site infrastructure.

Mitigation: Review generated commands and configuration snippets in a sandbox or staging environment before applying them to a production site.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/seo-audit-master)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [Schema.org](https://schema.org/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with checklists, tables, and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prioritized Critical, Important, and Suggested recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
