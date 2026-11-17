## Description:

Operate Weibo via browser automation for composing posts, publishing content, replying to comments, checking mentions, and monitoring basic account metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yikailucas](https://clawhub.ai/user/yikailucas)

### License/Terms of Use:


## Use Case:

External users and social media operators use this skill to manage Weibo posts, replies, mentions, account metrics, and pin/delete moderation through a logged-in browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish, reply, pin, unpin, or delete Weibo content through a logged-in browser session.

Mitigation: Confirm the account, target post, exact text, and media before approving any final publish, moderation, or deletion action.

Risk: Login, secondary verification, CAPTCHA, or invalid sessions can interrupt browser automation.

Mitigation: Pause for user action when authentication or CAPTCHA appears and do not attempt anti-bot bypass.

Risk: Visible creator-page metrics may be partial or unavailable depending on account access and page state.

Mitigation: Report only visible account metrics and mark the operation result as partial or failed when data cannot be confirmed.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown operation report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports action, account, result, details, and next step; publish and delete actions require explicit user confirmation.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
