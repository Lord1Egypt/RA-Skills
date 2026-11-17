## Description:

xhs-content-scan helps agents retrieve public Xiaohongshu notes, comments, and creator posts for content research, competitor monitoring, trend analysis, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, marketers, content operators, and analysts use this skill to collect public Xiaohongshu search results, note details, comments, and creator post lists for competitive research, topic discovery, KOL screening, and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu queries, target links, retrieved public data, and the GUAIKEI_API_TOKEN to the third-party Guaikei service.

Mitigation: Install only when that data sharing is acceptable, and prefer a disposable or scoped GUAIKEI_API_TOKEN.

Risk: User-supplied Xiaohongshu links are accepted as command input and security guidance calls for caution until URL validation is hardened.

Mitigation: Avoid running links from untrusted users, and review the target URL before executing detail or post commands.

Risk: Successful runs may write retrieved data and request details to local JSON logs.

Mitigation: Review the logs directory after use and delete or restrict log files that contain sensitive business research.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-content-scan)
- [Guaikei API service](https://www.guaikei.com)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The command-line tools print status, request metadata, and results as JSON and may save run logs under logs/.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
