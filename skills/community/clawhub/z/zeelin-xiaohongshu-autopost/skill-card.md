## Description:

ZeeLin 小红书自动发布 helps agents plan trend-driven social content, generate Xiaohongshu copy, and publish posts through browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelcey2023](https://clawhub.ai/user/kelcey2023)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators, social media teams, and agent users can use this skill to identify relevant trends, shape topics into Xiaohongshu-style copy, prepare content calendars, and optionally drive a logged-in Xiaohongshu creator browser session to publish a post.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish through a logged-in Xiaohongshu creator account without a clear final approval step.

Mitigation: Use an isolated browser profile, manually review titles, body text, and tags before posting, and enable draft-only controls where available.

Risk: Generated marketing copy may contain inaccurate claims, unsuitable positioning, or platform-policy issues.

Mitigation: Treat generated copy as a draft and have a responsible reviewer check factual claims, promotional language, and brand fit before publication.

Risk: The documented XHS_AUTO_PUBLISH safety claim may not match all included publishing scripts.

Mitigation: Do not rely on that safety claim unless the scripts are fixed and verified in the target environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kelcey2023/skills/zeelin-xiaohongshu-autopost)
- [Publisher profile](https://clawhub.ai/user/kelcey2023)
- [Auto Content Ops full documentation](references/auto-content-ops-skill-完整文档.md)
- [Methodology](references/methodology.md)
- [Xiaohongshu Creator Center](https://creator.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports and post drafts, with optional shell-driven publishing actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local draft files and operate an authenticated browser session when publishing scripts are run.]

## Skill Version(s):

1.0.100 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
