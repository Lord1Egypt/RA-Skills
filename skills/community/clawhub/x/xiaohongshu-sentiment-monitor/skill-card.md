## Description:

Fetches public Xiaohongshu/RedNote notes, profile posts, note details, and comments so an agent can support sentiment monitoring, market research, KOL screening, competitor analysis, and risk reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External users, content operators, marketers, and analysts use this skill to retrieve public Xiaohongshu data by keyword, note URL, or profile URL, then turn the structured results into market research, sentiment summaries, competitor monitoring, content planning, and KOL screening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, Xiaohongshu links, and the provider API token are sent to guaikei.com.

Mitigation: Use the skill only when that third-party API path is acceptable; avoid sensitive queries and rotate or revoke the token if exposure is suspected.

Risk: Returned results are saved to local temporary JSON logs that may contain sensitive topics or public-content analysis.

Mitigation: Review and delete temp logs after sensitive work, especially on shared machines or managed environments.

Risk: The package metadata mentions batch download behavior that the security guidance flags as stale or overbroad relative to the inspected code.

Mitigation: Base user-facing expectations on the current SKILL.md, references, and inspected CLI behavior for public-data lookup and analysis.

Risk: Public-data lookups can fail, return empty results, or reflect deleted, unavailable, or rate-limited content.

Mitigation: Treat empty or error responses as inconclusive, verify important findings against source links, and avoid unsupported sentiment or market conclusions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/why20261/skills/xiaohongshu-sentiment-monitor)
- [Project Homepage](https://github.com/um-why/xiaohongshu-openclaw-skill)
- [Options and Invocation Guide](references/options.md)
- [Troubleshooting](references/troubleshooting.md)
- [Changelog](references/changelog.md)
- [Guaikei API Token Provider](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and structured JSON CLI outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16 and GUAIKEI_API_TOKEN; CLI results are also saved as local JSON logs under the OS temp directory.]

## Skill Version(s):

1.1.4 (source: SKILL.md frontmatter, package.json, release metadata, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
