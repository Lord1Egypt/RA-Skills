## Description:

Posts user-provided content to Sina Weibo through browser automation when the user asks to publish a Weibo post.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinazkk](https://clawhub.ai/user/chinazkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to publish prepared text, emoji, and correctly formatted topic tags to Sina Weibo from an existing logged-in browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish directly to a user's Weibo account from a logged-in browser session.

Mitigation: Verify the active Weibo account and full post text, then require explicit final confirmation before the agent clicks send.

Risk: The published post may not match the user's intent if content, emoji, or topic tags are malformed.

Mitigation: Review the final composed post before sending, including the required #tag# format for each topic tag.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chinazkk/skills/weibo-post)
- [Sina Weibo](https://weibo.com)

## Skill Output:

**Output Type(s):** [text, guidance, browser automation commands]

**Output Format:** [Plain text instructions with browser automation command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a logged-in Weibo browser session and explicit final confirmation before clicking send.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
