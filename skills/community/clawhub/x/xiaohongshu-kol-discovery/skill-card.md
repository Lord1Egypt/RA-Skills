## Description:

Searches public Xiaohongshu posts, creator activity, post details, and comments to help identify and evaluate potential creator partners.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and analysts use the skill to find Xiaohongshu creators, compare public post engagement, research trends, and summarize audience comments for campaign planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and the API token are sent to the third-party data provider.

Mitigation: Use only if comfortable with guaikei.com receiving Xiaohongshu keywords or URLs and the token; keep the token confidential.

Risk: Returned public-data results are archived in local temp logs.

Mitigation: Restrict local log access and avoid processing private, login-only, or regulated data.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/why20261/skills/xiaohongshu-kol-discovery)
- [Publisher-declared skill homepage](https://github.com/um-why/xiaohongshu-openclaw-skill)
- [Data provider and token access](https://www.guaikei.com)
- [Input options](artifact/references/options.md)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON results with optional concise Markdown analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public-data queries require GUAIKEI_API_TOKEN; returned results are archived in local temp logs.]

## Skill Version(s):

1.1.4 (source: ClawHub release, frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
