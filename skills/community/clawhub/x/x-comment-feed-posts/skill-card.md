## Description:

Find posts in the user's X feed and leave comments on them one by one. Use when the user wants to comment on N posts from the feed, usually about indie tech launches, new tech, or AI, while keeping comments short, first-person, thread-specific, and manually executed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dishant0406](https://clawhub.ai/user/dishant0406)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to guide an agent through manually selecting recent X feed posts, liking each selected post, posting short first-person comments, and reporting the outcome.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use the user's active X browser session to like posts and publish public comments from the user's account.

Mitigation: Ask the agent to show each selected post and draft comment for approval before posting, and specify the exact topic scope and maximum number of comments.

Risk: The feed may not yield enough fresh, relevant posts for the requested topic scope.

Mitigation: Keep the topic scope explicit and require the agent to report when the feed is weak instead of lowering the quality bar without permission.

Risk: Leaving the X session open after the run may expose an authenticated browser tab longer than needed.

Mitigation: Require confirmation that all x.com tabs were closed at completion.

## Reference(s):

- [Comment Rules](references/comment-rules.md)
- [Feed Workflow](references/feed-workflow.md)
- [Human Voice](references/human-voice.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text, Markdown]

**Output Format:** [Markdown guidance with shell commands and short social comment text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include a completion report with the requested count, actual comments posted, selected topics or posts, final comment text, search-avoidance confirmation, and X tab closure confirmation.]

## Skill Version(s):

1.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
