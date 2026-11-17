## Description:

Guides an agent through drafting, confirming, and executing Reddit posts, comments, and upvotes using Reddit interaction playbooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvinperson](https://clawhub.ai/user/alvinperson)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to prepare Reddit-ready post or comment text, confirm high-visibility actions, and guide browser-based posting, commenting, or upvoting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish posts, comments, and votes from a Reddit account.

Mitigation: Verify every post, comment, target, and vote before submission, and avoid pre-authorized immediate sending unless the user explicitly accepts the risk.

Risk: The skill includes guidance for making AI-generated Reddit content appear human-authored.

Mitigation: Use the skill only where automated Reddit activity is acceptable, disclose automation when required, and reject deceptive or policy-violating engagement requests.

Risk: The skill may store persona usage history in PERSONA.md.

Mitigation: Keep persona logging explicit, minimal, and deletable, and do not record unnecessary personal information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvinperson/skills/reddit-engagement)
- [Publisher profile](https://clawhub.ai/user/alvinperson)
- [Post Strategy](references/post-strategy.md)
- [Comment Strategy](references/comment-strategy.md)
- [Reddit Interaction Patterns](references/interaction-patterns.md)
- [Subreddit Archives](references/sub-archives.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text with action summaries and user-confirmed Reddit content drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Reddit post or comment text, target summaries, UI outcome evidence, diagnostics, and recovery guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
