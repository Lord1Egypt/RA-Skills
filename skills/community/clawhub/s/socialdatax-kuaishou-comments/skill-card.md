## Description: <br>
用于快手评论分析、快手评论回复、快手评论洞察、用户反馈、口碑分析、痛点总结和内容讨论分析。覆盖 Kuaishou / Kwai comments and comment replies，来自 SocialDataX 社媒数据助手。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve and analyze Kuaishou first-level comments and replies through SocialDataX. It supports audience feedback review, sentiment themes, objections, pain points, FAQ extraction, and discussion summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The SocialDataX npm package and service receive the SOCIALDATAX_API_KEY and queried Kuaishou URLs or IDs. <br>
Mitigation: Install and run the package only after confirming that SocialDataX and the package source are trusted for the intended workspace. <br>
Risk: Using --all, --pages, or --include-replies may retrieve large volumes of public comment data. <br>
Mitigation: Set page or item limits when broad collection is unnecessary and summarize results by observed themes before drawing conclusions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/devinchen2014/skills/socialdatax-kuaishou-comments) <br>
- [SocialDataX homepage](https://socialdatax.com/?from=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON result handling notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SOCIALDATAX_API_KEY and can process paginated Kuaishou comments and replies, including optional multi-page and reply-inclusive retrieval.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
