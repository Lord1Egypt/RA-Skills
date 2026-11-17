## Description:

Analyzes public Xiaohongshu accounts, posts, and comments to support content planning, competitor research, and account teardowns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and analysts use this skill to examine public Xiaohongshu account activity, search posts, review engagement and comments, and develop content or competitor insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms or Xiaohongshu links and the API token are sent to a third-party service.

Mitigation: Use only with an approved token and queries you are comfortable sharing with guaikei.com; treat the token as sensitive.

Risk: Local result logs may retain sensitive research or public user content.

Mitigation: Review and manage local logs, and limit analysis to public data consistent with privacy and platform rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/xiaohongshu-account-teardown)
- [Project homepage](https://github.com/um-why/xiaohongshu-openclaw-skill)
- [API token and service](https://www.guaikei.com)
- [Options and parameters](references/options.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured JSON results with optional short Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a GUAIKEI_API_TOKEN and saves local result logs.]

## Skill Version(s):

1.1.4 (source: release metadata, frontmatter, changelog, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
