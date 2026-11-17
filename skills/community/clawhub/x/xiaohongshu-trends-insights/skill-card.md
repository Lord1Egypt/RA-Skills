## Description:

Analyzes public Xiaohongshu content by searching posts, reading post details and comments, and retrieving creator profiles and public works to support trend and topic research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Xiaohongshu creators, social media operators, brand researchers, and marketing teams use the skill to identify trends, develop content topics, monitor competitors, screen creators, and summarize public audience discussions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and supplied links, including query parameters, are sent to Guaikei; results may also be saved in local temporary logs, and the remote service was not audited.

Mitigation: Use a dedicated API token, review Guaikei privacy and billing terms, and set `XHS_GUAIKEI_DISABLE_LOG=1` to disable local result logs.

Risk: Queries may be subject to token-plan billing and per-plan result limits.

Mitigation: Check the plan’s terms and set query limits within its allowances.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/why20261/skills/xiaohongshu-trends-insights)
- [Guaikei service and token access](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Troubleshooting reference](references/troubleshooting.md)
- [Changelog](references/changelog.md)
- [GitHub Issues support](https://github.com/um-why/xiaohongshu-openclaw-skill/issues)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured JSON data with natural-language summaries and analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public Xiaohongshu content and supports read-only research; no account login or write actions.]

## Skill Version(s):

1.2.1 (source: artifact frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
