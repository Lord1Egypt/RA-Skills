## Description:

Guides an agent through a fixed Xiaohongshu publishing workflow designed to reduce posting failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuchenggong19851114-design](https://clawhub.ai/user/zhuchenggong19851114-design)

### License/Terms of Use:

MIT-0

## Use Case:

External creators or agents assisting them use this skill to publish Xiaohongshu image-text or long-form posts from approved copy and prepared images, then report the success link or failure reason.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish content publicly from a logged-in Xiaohongshu creator account.

Mitigation: Require the agent to show the final post content, destination account, and publish action for explicit user approval before posting.

Risk: The workflow records results to a Feishu content library without clearly scoped confirmation in the artifact.

Mitigation: Approve the Feishu workspace, library, fields, and data to be recorded before allowing that step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuchenggong19851114-design/skills/xiaohongshu-create)
- [Xiaohongshu image publishing page](https://creator.xiaohongshu.com/publish/publish?target=image)
- [Xiaohongshu long-form publishing page](https://creator.xiaohongshu.com/publish/publish?target=text)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown or plain text status with a post link or retry guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a logged-in Xiaohongshu creator session, approved copy, and prepared images.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
