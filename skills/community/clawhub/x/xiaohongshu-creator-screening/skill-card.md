## Description:

Searches public Xiaohongshu posts, creator profiles and comments to support creator screening, content research and evidence-based KOL recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing and research teams use public Xiaohongshu posts, creator activity and comments to compare candidate creators, assess engagement and prepare KOL shortlists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send Xiaohongshu keywords or public URLs to the third-party GUAIKEI API and require an API token.

Mitigation: Use a dedicated token, avoid sensitive query terms and approve third-party data sharing before use.

Risk: Saved result logs may contain data sensitive to the team.

Mitigation: Restrict access to local logs and remove them when no longer needed; analyze public content only.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/why20261/skills/xiaohongshu-creator-screening)
- [GUAIKEI API and token information](https://www.guaikei.com)
- [Usage options](references/options.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [JSON data, Analysis, Guidance]

**Output Format:** [Structured JSON results with optional Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers public posts, creator activity and comments; results are saved to local logs.]

## Skill Version(s):

1.1.4 (source: server release, skill frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
