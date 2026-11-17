## Description:

Searches public Xiaohongshu notes, retrieves note details and comments, and lists public creator posts as structured data for trend research, competitor analysis, KOL screening, and content planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Content operators, marketers, analysts, and agents use this skill to collect public Xiaohongshu search results, note details, comments, and creator post lists for downstream analysis and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, URLs, and GUAIKEI_API_TOKEN to the Guaikei service, including token use in URL query strings.

Mitigation: Install only if the Guaikei service is trusted, scope and rotate the token, and run in an environment where URLs and command logs are not broadly collected.

Risk: Fetched datasets are saved locally by default and may contain sensitive research, competitor, or campaign data.

Mitigation: Treat saved logs as sensitive, restrict workspace access, and delete local outputs when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-find-notes-guaikei)
- [Guaikei service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON data, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI execution returns structured JSON data and saved local log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; supports keyword, URL, limit, content type, sort, and time filters.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
