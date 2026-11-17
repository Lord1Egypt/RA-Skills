## Description:

按关键词、点赞、类目和市场筛选TikTok带货达人，结合达人互动数据、作品表现数据和带货效果给出合作优先级，找到真正和品类、受众及目标匹配的TikTok达人候选。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External creators, brands, marketers, analysts, and agent developers use this skill to retrieve public TikTok search, creator-post, and video-comment data for creator screening, competitor monitoring, content research, social listening, and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends TikTok search terms, profile or video URLs or IDs, and the GUAIKEI_API_TOKEN to www.guaikei.com.

Mitigation: Use only when that data transfer is acceptable for the user's workflow and organization, and avoid submitting sensitive research targets unless approved.

Risk: Result JSON files may be saved under the system temp directory and can include public comments and creator identifiers.

Mitigation: Review and clean up local result logs when they contain sensitive research context, and de-identify creator or commenter data before external sharing.

Risk: The skill retrieves public TikTok data for analysis, which can still raise platform-terms and privacy obligations.

Mitigation: Confirm use complies with TikTok terms and applicable privacy rules before commercial publication or downstream use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/tiktok-creator-match)
- [Guaikei API token and service information](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search request schema](assets/search_cli_req.schema.json)
- [Search response schema](assets/search_cli_resp.schema.json)
- [Post request schema](assets/post_cli_req.schema.json)
- [Post response schema](assets/post_cli_resp.schema.json)
- [Comment request schema](assets/comment_cli_req.schema.json)
- [Comment response schema](assets/comment_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON result envelopes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI stdout is structured JSON; stderr carries logs and progress; result logs may be written under the system temp directory.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
