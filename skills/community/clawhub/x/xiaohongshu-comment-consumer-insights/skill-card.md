## Description:

Retrieves public Xiaohongshu posts and comments to help agents identify consumer questions, purchase concerns, feedback, and sentiment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and analysts use this skill to search public Xiaohongshu content, examine post and creator activity, and summarize comment themes for market research and product feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token and searched keywords or Xiaohongshu links are sent to a third-party data provider.

Mitigation: Use only if sharing those inputs with guaikei.com is acceptable; avoid sensitive queries and protect the API token.

Risk: Returned results are saved in local temporary logs.

Mitigation: Control access to the logs and remove them when they are no longer needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/why20261/skills/xiaohongshu-comment-consumer-insights)
- [Project homepage (listed in skill metadata; import provenance unavailable)](https://github.com/um-why/xiaohongshu-openclaw-skill)
- [Usage and parameters](references/options.md)
- [Troubleshooting](references/troubleshooting.md)
- [Guaikei data provider](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON data, Analysis, Guidance]

**Output Format:** [JSON query results and natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Guaikei API token; supports public Xiaohongshu data only and saves results to local temporary logs.]

## Skill Version(s):

1.1.4 (source: server release, skill frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
