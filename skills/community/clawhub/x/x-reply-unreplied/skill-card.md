## Description:

Check X notifications, mentions, or reply threads and answer posts that still need a response from the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dishant0406](https://clawhub.ai/user/dishant0406)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to review X notifications, mentions, or requested reply threads and respond to suitable unreplied posts in a concise first-person style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can like and publish replies from the user's logged-in X account.

Mitigation: Use a narrow scope and count limit, and ask to review drafts before posting when automatic posting is not desired.

Risk: Replies could be inaccurate when the right answer requires facts that cannot be verified quickly.

Mitigation: Skip those threads or verify the needed facts before drafting a reply.

Risk: High-volume or enforcement-avoidant use could conflict with platform expectations.

Mitigation: Use the skill only for manual reply handling, keep the default cap of up to 5 suitable opportunities, and do not use it for mass replies or enforcement evasion.

## Reference(s):

- [X Reply Unreplied on ClawHub](https://clawhub.ai/dishant0406/skills/x-reply-unreplied)
- [Human Voice](artifact/references/human-voice.md)
- [Inbox Workflow](artifact/references/inbox-workflow.md)
- [Reply Rules](artifact/references/reply-rules.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown completion report with posted reply text and skipped-item reasons]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May operate a browser session to like posts and publish short replies from the user's logged-in X account.]

## Skill Version(s):

1.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
