## Description: <br>
通过 openclaw browser 在雪球网执行互动与创作类操作，包括点赞、收藏、评论、回复、转发、发布观点、发布长文。当用户要求"点个赞""收藏一下""评论""转发""发个观点""发个长文"时使用此技能。默认通过 openclaw browser 执行。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gumailianxin](https://clawhub.ai/user/gumailianxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to guide browser-based interaction with a Xueqiu account, including liking, favoriting, commenting, reposting, publishing short posts, and publishing long-form articles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit public actions through a Xueqiu account, including likes, favorites, comments, reposts, short posts, and long-form articles. <br>
Mitigation: Require explicit confirmation of the platform, target post or page, action type, and final text before any publish, repost, comment, like, or favorite is submitted. <br>
Risk: Broad natural-language triggers can cause an agent to act on the wrong Xueqiu content if the target is ambiguous. <br>
Mitigation: Use browser snapshots to verify the exact target and closest matching control before clicking or entering text, and stop for user clarification when multiple plausible targets are present. <br>


## Reference(s): <br>
- [Xueqiu](https://xueqiu.com) <br>
- [Xueqiu Search](https://xueqiu.com/search) <br>
- [Xueqiu Long-form Editor](https://mp.xueqiu.com/write/) <br>
- [Xueqiu Creator Center](https://mp.xueqiu.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text] <br>
**Output Format:** [Markdown or plain text with browser command guidance and a concise status report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports the action attempted, success or failure, where it stopped if unsuccessful, and any resulting URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
