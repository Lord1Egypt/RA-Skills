## Description: <br>
Guides agents through an interactive pre-launch website audit covering DNS, analytics, legal compliance, security headers, SEO/GEO, copy quality, social previews, favicons, quality gates, and weekly SEO maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, site owners, and launch teams use this skill to run an interactive pre-launch audit for marketing, documentation, SaaS, course, and portfolio sites. It helps verify launch readiness and organize blockers, recommended fixes, and optional follow-ups before and after release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags the skill as suspicious because it can involve persistent automation, credential-backed fallbacks, external posting, and permission-bypassing scheduled runs. <br>
Mitigation: Require explicit confirmation for third-party installs, tracking tools, credential-based API calls, Slack delivery, and scheduled agents; avoid permission-bypass cron runs unless the environment is tightly sandboxed. <br>
Risk: The skill may set up analytics, SEO, and monitoring services that handle site traffic, search data, or service credentials. <br>
Mitigation: Review data flows and consent requirements before enabling integrations, keep credentials in a secrets manager, and use least-privilege service accounts where possible. <br>
Risk: Generated launch, SEO, and security recommendations can affect production site behavior if applied without review. <br>
Mitigation: Review proposed changes before execution, test configuration changes in staging when practical, and verify results with the provided command checks before launch. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samber/site-launch-checklist) <br>
- [Publisher homepage](https://github.com/samber/cc-skills) <br>
- [Decisions and matrices](references/decisions.md) <br>
- [Templates](references/templates.md) <br>
- [Weekly SEO maintenance sub-agent](references/weekly-seo-agent.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Interactive Markdown guidance with command snippets and generated configuration or file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Asks for user confirmation before third-party installs, tracking setup, credential-backed API calls, Slack delivery, or scheduled agents.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
