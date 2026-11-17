## Description:

Generates WeChat public-account article drafts by monitoring technology trends, filtering topics, and using an LLM to write review-ready Markdown drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gdp6539](https://clawhub.ai/user/gdp6539)

### License/Terms of Use:

MIT

## Use Case:

External content creators, media operators, and marketing teams use this skill to monitor technology topics and generate draft WeChat articles for manual review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing behavior and credential guidance may be ahead of the implemented and reviewed capability.

Mitigation: Keep auto-publish disabled and do not provide WeChat AppID or AppSecret until the publishing path has been implemented, reviewed, and tested.

Risk: Generated drafts can include injected, misleading, or unsuitable content from external trend sources or LLM output.

Mitigation: Manually review every generated draft before copying or publishing it to WeChat.

Risk: Scheduled runs can create repeated network and LLM calls.

Mitigation: Avoid cron or other scheduled execution unless repeated calls and related costs are intended.

Risk: An auxiliary Zhihu script writes outside the normal skill workspace.

Mitigation: Remove or fix scripts/zhihu-gen.js before running auxiliary scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gdp6539/skills/wechat-auto-publisher)
- [ClawHub publisher profile](https://clawhub.ai/user/gdp6539)
- [Alibaba Cloud Bailian console](https://bailian.console.aliyun.com/)
- [DashScope OpenAI-compatible API endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1)
- [Hacker News API](https://hacker-news.firebaseio.com/v0/topstories.json)
- [GitHub Trending](https://github.com/trending)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown drafts, JSON topic files, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated drafts are intended for human review before publication.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
