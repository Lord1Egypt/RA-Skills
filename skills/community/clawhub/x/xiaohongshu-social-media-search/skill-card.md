## Description:

Searches public XiaoHongShu posts, creator content, and comments to support social media research and engagement analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Marketers, researchers, and content teams use the skill to search public XiaoHongShu posts, inspect note and creator engagement, and analyze comments for topic research, competitor monitoring, and creator selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms or links and the configured API token are sent to guaikei.com.

Mitigation: Use only if this data transfer is acceptable, and keep the API token private.

Risk: Returned results may be saved in local temporary logs during large pulls.

Mitigation: Avoid large pulls on shared machines unless local temporary storage is acceptable.

Risk: The skill is intended for public content analysis, not private or restricted data.

Mitigation: Limit use to publicly available content and respect applicable data-use rules.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/why20261/skills/xiaohongshu-social-media-search)
- [Skill homepage (listed in metadata)](https://github.com/um-why/xiaohongshu-openclaw-skill)
- [Options and usage](references/options.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Analysis, JSON]

**Output Format:** [Structured JSON results with optional plain-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns public post, creator, and comment data; large result sets may be saved to local temporary files.]

## Skill Version(s):

1.1.4 (source: release metadata, frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
