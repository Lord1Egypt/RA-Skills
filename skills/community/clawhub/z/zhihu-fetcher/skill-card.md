## Description:

Fetches Zhihu hot-list data with browser-profile, file-cookie, or unauthenticated fallback sources, then saves results to JSON, SQLite, or HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noah-1106](https://clawhub.ai/user/noah-1106)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data analysts use this skill to collect Zhihu hot-list items for reporting, trend monitoring, and local analysis with fallback options when authenticated access is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships sensitive Zhihu cookie material in configuration and scripts can print partial cookie values.

Mitigation: Remove bundled cookie values before installation, store personal cookies outside shared source control, and avoid logging or sharing authentication material.

Risk: Anti-crawl and browser-research snippets inspect cookies, headers, network responses, and rate-limit behavior.

Mitigation: Run those diagnostics only in a controlled environment after reviewing the scripts and confirming the account, site terms, and logging exposure are acceptable.

Risk: Generated HTML reports may render fetched titles and links from external or fallback data sources.

Mitigation: Treat generated reports as untrusted content when data sources are not controlled, and sanitize or review fetched content before sharing reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noah-1106/skills/zhihu-fetcher)
- [Zhihu home](https://www.zhihu.com)
- [Zhihu hot list](https://www.zhihu.com/hot)
- [Configured fallback source](https://raw.githubusercontent.com/SnailDev/zhihu-hot-hub/master/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, HTML, SQLite data]

**Output Format:** [Markdown instructions with shell and JavaScript snippets; runtime outputs include JSON records, SQLite tables, console text, and generated HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configurable item limits, rate limiting, authentication priority, timeout settings, and fallback sources.]

## Skill Version(s):

1.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
