## Description:

Automates sending messages to contacts through the Windows desktop WeChat client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[529279917](https://clawhub.ai/user/529279917)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers on Windows use this skill to let an agent check WeChat status and send requested messages to a visible or searched WeChat chat in the desktop client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send a message from the active WeChat chat without enforced confirmation.

Mitigation: Require manual review of the recipient and message before allowing the send tool call, and use it only with a verified chat visible.

Risk: Screenshots may contain contact or message data and are written to disk during verification, input, search, and send flows.

Mitigation: Remove or redesign screenshot-writing behavior before sensitive use, and delete generated screenshots after each run.

Risk: Desktop automation can target the wrong window or contact if WeChat focus or search selection is incorrect.

Mitigation: Keep WeChat visible, verify the active chat or search result before sending, and invoke the skill only for explicit WeChat requests.

## Reference(s):

- [wechat-skill ClawHub release page](https://clawhub.ai/529279917/skills/wechat-skill)
- [Referenced wechat-mcp ClawHub skill](https://clawhub.ai/dragon015/wechat-mcp)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text MCP responses and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send messages through the active local WeChat UI when invoked.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
