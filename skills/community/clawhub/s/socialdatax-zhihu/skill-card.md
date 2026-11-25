## Description:

用于知乎数据助手、知乎热榜、内容搜索、回答文章视频详情、评论分析、创作者资料和文章列表。覆盖 Zhihu content research，来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

Zhihu users and researchers can use the skill to review hot lists, search questions and content, inspect answers, articles, videos and comments, and look up creator profiles and posts. Its documented actions are read-only.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill repeatedly runs an automatically installed, unpinned latest CLI package; a compromised future release could expose credentials or the local environment. Scanner coverage was incomplete because three local references could not be resolved.

Mitigation: Review the CLI package before installing, and use the skill only in an environment with appropriately limited credentials and local access.

## Reference(s):


## Skill Output:

**Output Type(s):** [API data, JSON, Analysis, Guidance, Shell commands]

**Output Format:** [Structured JSON results and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Zhihu research results; no account actions.]

## Skill Version(s):

0.1.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
