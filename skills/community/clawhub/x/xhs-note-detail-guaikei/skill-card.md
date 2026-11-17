## Description:

Retrieves public Xiaohongshu (RedNote/XHS) note search results, note details, comments, and creator post data for agent-assisted analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content, marketing, and data-analysis teams use this skill to retrieve public Xiaohongshu notes, comments, and creator posts for trend research, competitive monitoring, KOL screening, and content planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu links, query terms, xsec_token-bearing URLs, API credentials, and returned results may be sent to Guaikei or stored locally.

Mitigation: Use only authorized public data, treat GUAIKEI_API_TOKEN and xsec_token URLs as sensitive, avoid shared workspaces, and clean the logs directory when results contain sensitive business context.

Risk: The authoritative security summary marks the skill suspicious because token handling and saved full results need review before installation.

Mitigation: Review credential handling before regular use, consider redacting tokens from inputs and logs, and prefer passing API credentials in headers where supported.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-note-detail-guaikei)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON command output with optional Markdown summaries and locally saved JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; command results may be written under logs/.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter and package.json report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
