## Description:

Collects multi-channel Weibo hot search data, stores results in SQLite, and generates queryable text output and an HTML visualization report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noah-1106](https://clawhub.ai/user/noah-1106)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to collect Weibo hot-search rankings across hot, social, entertainment, and life channels, preserve historical results locally, query trends, and generate an HTML report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security scan reports exploitable command and HTML injection risks.

Mitigation: Review before installation; the publisher should remove shell=True, strictly validate Weibo URLs, and avoid innerHTML for remote values before users run --with-content or open generated reports from new scraped data.

Risk: The skill uses the user's OpenClaw browser profile and writes local SQLite, JSON, and HTML output.

Mitigation: Run it only with a profile and workspace intended for Weibo scraping, and confirm the expected network targets and file-write locations before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noah-1106/skills/weibo-trending)
- [Publisher profile](https://clawhub.ai/user/noah-1106)
- [Weibo](https://weibo.com)
- [Weibo hot search](https://weibo.com/hot/search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON data, SQLite records, terminal query output, and generated HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local OpenClaw browser profile, writes local SQLite data under data/weibo.db, can write JSON files, and can generate data/index.html.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
