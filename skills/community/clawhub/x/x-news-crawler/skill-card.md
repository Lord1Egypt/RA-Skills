## Description:

Crawl X (Twitter) search results through a local CLI that wraps `abs` (agent-browser).

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeguooooo](https://clawhub.ai/user/leeguooooo)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to crawl X search results by keyword, combine Top and Latest results, deduplicate posts, and summarize the resulting feed for news or signal monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a local Chrome CDP session and requests broader browser access than the crawl task may need.

Mitigation: Use a dedicated Chrome profile or separate low-privilege browser account, bind CDP to localhost, and close the debugging browser after use.

Risk: The setup asks for global package installation and build approval.

Mitigation: Review and trust the package source and version before running global installs or broad build approvals.

Risk: X posts can include rumors, spam, or misleading claims even when engagement is high.

Mitigation: Treat unverified posts as low confidence and summarize signal versus noise instead of presenting posts as confirmed facts.

## Reference(s):

- [x-news-crawler flags](references/cli.md)
- [ClawHub skill page](https://clawhub.ai/leeguooooo/skills/x-news-crawler)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON output from the crawler]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The crawler JSON includes fetched_at, query, mode, count, warnings, failed_sources, and rows with source, datetime, status_url, user, text, replies, reposts, and likes.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
