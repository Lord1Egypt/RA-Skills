## Description:

Automates publishing prepared long-form Xiaohongshu notes by filling a title and body in the creator platform and completing the posting workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzh999](https://clawhub.ai/user/wangzh999)

### License/Terms of Use:

MIT

## Use Case:

Creators, marketers, and agent operators use this skill to publish already prepared Xiaohongshu long-form posts through browser automation. It is intended for workflows where the title, body, and optional tags are supplied before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can click the final publish button on a live logged-in Xiaohongshu creator account.

Mitigation: Use it only with prepared content that has been reviewed by the account owner, and avoid broad publish requests unless a final confirmation gate is added.

Risk: Published content may differ from the operator's intent if title, body, tags, or account context are incorrect.

Mitigation: Verify the exact title, content, destination account, and platform preview before allowing the publishing step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangzh999/skills/xiaohongshu-publish-wangzh)
- [Xiaohongshu creator platform](https://creator.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with command examples and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May operate a logged-in browser session and return a publish success status.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
