## Description:

AI-powered short video script generator that turns a topic into viral titles, opening hooks, interactive comments, and hashtag recommendations using local templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sysxccl092](https://clawhub.ai/user/sysxccl092)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and social media operators use this skill to quickly draft Chinese-language short-video packages for platforms such as Douyin, Kuaishou, WeChat Channels, Bilibili, TikTok, and YouTube Shorts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated short-video copy can sound persuasive or factual even though it is template-based and not fact-checked.

Mitigation: Review and edit generated titles, hooks, comments, and hashtags before publishing, especially for factual, medical, legal, financial, or reputational claims.

Risk: The artifact imports child_process even though the security evidence reports no subprocess execution, which may confuse reviewers.

Mitigation: Remove the unused import or confirm the packaged release still has no subprocess behavior before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain text short-video copy package, with optional JSON output when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Template-randomized Chinese-language titles, hooks, comments, and hashtags; no network access, file access, persistence, or subprocess execution observed in security evidence.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
