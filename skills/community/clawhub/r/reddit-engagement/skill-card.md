## Description: <br>
Create and execute Reddit posting, commenting, and upvoting workflows using browser accessibility-tree semantics instead of brittle DOM ids or CSS selectors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Alvinperson](https://clawhub.ai/user/Alvinperson) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to draft, review, and perform Reddit posts, comments, and upvotes through an authenticated browser. It is intended for semantic UI targeting, subreddit-aware content preparation, and status reporting after each Reddit action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make AI-written public Reddit posts and comments through a logged-in account. <br>
Mitigation: Keep immediate posting disabled unless explicitly authorized, preview every generated post or comment, and verify the target, account, and content before submission. <br>
Risk: The skill reuses local persona data, which could expose sensitive facts or create inconsistent public identity claims. <br>
Mitigation: Keep PERSONA.md free of sensitive facts, use only documented non-sensitive facts, and log used content to avoid contradictions. <br>
Risk: AI-assisted or automated engagement may violate Reddit or subreddit rules. <br>
Mitigation: Check Reddit and subreddit rules before use, avoid communities that prohibit AI-generated or automated engagement, and stop when rules or moderation signals are unclear. <br>


## Reference(s): <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Post Strategy](artifact/references/post-strategy.md) <br>
- [Comment Strategy](artifact/references/comment-strategy.md) <br>
- [Interaction Patterns](artifact/references/interaction-patterns.md) <br>
- [Subreddit Archives](artifact/references/sub-archives.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Alvinperson/reddit-engagement) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown status report with generated Reddit content previews when applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns action performed, target, result status, UI evidence, and recovery guidance when actions fail; may create or submit public Reddit content when explicitly authorized.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
