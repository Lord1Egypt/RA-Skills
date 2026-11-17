## Description:

X Daily Report monitors a curated set of AI organizations and influencers on X/Twitter and produces a structured daily intelligence report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kongxiaodan20001201-alt](https://clawhub.ai/user/kongxiaodan20001201-alt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect recent X/Twitter activity from AI companies, labs, and public figures, then summarize the most important updates, account activity, and follow-up priorities in a daily report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free scraper can reuse Chrome login cookies through a third-party scraping dependency.

Mitigation: Run it only with a dedicated browser profile or test X account, and avoid exposing a primary logged-in browser session.

Risk: The official API path is described as higher reliability, but evidence indicates it still uses mock tweet data for report generation.

Mitigation: Do not rely on official API mode for operational reports until mock-data behavior is replaced and verified.

Risk: Credential-like values and service identifiers appear in script configuration.

Mitigation: Move credentials and service tokens to environment variables or secret storage before operational use.

## Reference(s):

- [Account list](references/account-list.md)
- [ClawHub skill page](https://clawhub.ai/kongxiaodan20001201-alt/skills/x-daily-report)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with account summary tables, prioritized updates, and follow-up recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a dated Markdown report file when the bundled scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
