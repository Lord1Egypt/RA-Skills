## Description: <br>
RSS Fetcher helps agents collect and manage RSS articles with incremental fetching, URL deduplication, auto-tagging, source health checks, SQLite storage, query tools, and HTML report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noah-1106](https://clawhub.ai/user/noah-1106) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to maintain local RSS source lists, fetch and deduplicate articles into SQLite, query recent items, and generate a static HTML reading report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched RSS content may be untrusted, and the local HTML report can run unsafe browser code from feed-derived content. <br>
Mitigation: Use curated feeds, avoid opening generated reports from untrusted sources, and prefer or require escaping and sanitization of all feed-derived fields before HTML or JavaScript embedding. <br>
Risk: The release has a suspicious security verdict and should be reviewed before installation. <br>
Mitigation: Review the security summary, inspect report generation behavior, and scan the skill before deploying it in a shared or sensitive environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/noah-1106/rss-fetcher) <br>
- [Database schema reference](artifact/references/schema.sql) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, SQL examples, and generated local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or updates local SQLite data, JSON feed configuration, terminal query output, and a static HTML report.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
