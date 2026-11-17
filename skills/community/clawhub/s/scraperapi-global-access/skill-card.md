## Description:

Guides agents in using ScraperAPI-backed country proxies, JavaScript rendering, user journey simulation, performance monitoring, resumable runs, and JSON or CSV reporting for global website access checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[126shitou](https://clawhub.ai/user/126shitou)

### License/Terms of Use:

MIT

## Use Case:

Developers, QA teams, SEO operators, and site reliability teams use this skill to check website availability, analytics behavior, and performance across multiple countries through ScraperAPI. It is intended for authorized testing of sites and services where proxy access and JavaScript rendering are appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ClawHub security summary reports that shipped scripts hardcode a ScraperAPI key and target faceswap.cool rather than a user-provided URL.

Mitigation: Remove embedded credentials, load the API key from a private environment variable, and make the target URL explicitly user-controlled before running the scripts.

Risk: The security guidance notes that scripts may send requests through ScraperAPI and trigger analytics or tracking systems.

Mitigation: Use the skill only for authorized sites, avoid sensitive targets, prefer HTTPS for ScraperAPI requests, and document or disable analytics-triggering behavior when it is not required.

Risk: The authoritative security verdict is suspicious because the published instructions overstate generic use compared with the shipped scripts.

Mitigation: Review the bundled scripts before installation or execution and verify that their actual target, credentials, and side effects match the intended use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/126shitou/skills/scraperapi-global-access)
- [ScraperAPI documentation](https://www.scraperapi.com/documentation/)
- [ScraperAPI dashboard](https://dashboard.scraperapi.com/)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash and configuration snippets; bundled scripts produce JSON and CSV report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Script outputs can include progress.json, exploration_report.json, exploration_results.csv, and performance_data.csv.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
