## Description: <br>
Find posts in the user's X feed and leave comments on them one by one. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dishant0406](https://clawhub.ai/user/dishant0406) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to have an agent browse their X For You feed, select relevant recent posts, like them, and post short first-person comments on a requested topic set. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can like posts and publish visible X comments from the user's account. <br>
Mitigation: Require user review and approval of each comment before posting, keep the requested count small, and stop if the feed does not provide suitable candidates. <br>
Risk: First-person or experience-based comments may imply feelings, work history, or product use that are not true for the user. <br>
Mitigation: Allow first-person claims only when they accurately reflect the user's real views or experience; otherwise rewrite comments as narrower observations or questions. <br>
Risk: Public engagement on sensitive or political topics can create reputational or policy risk. <br>
Mitigation: Avoid sensitive, political, or high-risk topics unless the user explicitly approves the topic and the exact comment text. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dishant0406/x-comment-feed-posts) <br>
- [Comment Rules](references/comment-rules.md) <br>
- [Feed Workflow](references/feed-workflow.md) <br>
- [Human Voice](references/human-voice.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown completion report with comment text and run details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports requested and actual comment counts, chosen topics or posts, final comments, search avoidance, and x.com tab closure.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
