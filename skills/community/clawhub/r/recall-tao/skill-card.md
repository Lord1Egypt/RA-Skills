## Description: <br>
抖音自动回复技能，通过浏览器自动化连接抖音创作者中心，监控评论，并基于关键词、敏感词过滤、评论分类和可配置 AI 辅助生成回复。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hexiuqian](https://clawhub.ai/user/hexiuqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and operators use this skill to monitor Douyin Creator Center comments, classify incoming comments, apply keyword and sensitive-word rules, and prepare or send account replies with rate limits and logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post replies from a logged-in Douyin account. <br>
Mitigation: Use manual approval or draft-only operation where possible, and confirm that automated replies comply with Douyin rules and the account owner's risk tolerance. <br>
Risk: The skill can retain session and activity data through browser state, monitor state, and logs. <br>
Mitigation: Restrict where session files, state files, and logs are stored; review retention settings and remove sensitive data when it is no longer needed. <br>
Risk: The skill includes stealth and human-mimicry behavior such as browser flags and randomized delays. <br>
Mitigation: Review and disable stealth browser flags or human-mimicry behavior before deployment unless it is explicitly permitted by platform rules. <br>


## Reference(s): <br>
- [抖音自动回复监控助手](artifact/references/monitoring_guide.md) <br>
- [Douyin Creator Center comment management](https://creator.douyin.com/creator-micro/interactive/comment) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript snippets, shell-style commands, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces browser automation guidance and configuration for monitoring comments, filtering content, rate limiting replies, and maintaining logs.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
