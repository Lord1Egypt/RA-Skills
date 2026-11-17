## Description:

小红书定制化创作技能 - 固定操作流程，提高发布成功率

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuchenggong19851114-design](https://clawhub.ai/user/zhuchenggong19851114-design)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators, social media managers, and agents assisting them use this skill to publish confirmed copy and prepared image materials to Xiaohongshu through a fixed browser workflow. It also guides common publishing failure handling and returns a success link or retry recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish live content from a logged-in Xiaohongshu account.

Mitigation: Confirm the target account, title, body, images, and topics with the user before allowing publication.

Risk: The skill directs the agent to record published content in Feishu without clear consent, destination, or data limits.

Mitigation: Do not perform the Feishu logging step unless the destination workspace, repository, copied fields, retention, and audience are explicit and acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuchenggong19851114-design/skills/zhuchenggong-xiaohongshu-create)
- [Xiaohongshu creator image publishing page](https://creator.xiaohongshu.com/publish/publish?target=image)
- [Xiaohongshu creator text publishing page](https://creator.xiaohongshu.com/publish/publish?target=text)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text status with a publication link, error reason, and retry recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are tied to browser publishing actions and should reflect whether publication succeeded or failed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
