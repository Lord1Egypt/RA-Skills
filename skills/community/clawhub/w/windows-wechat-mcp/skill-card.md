## Description:

Automates Windows desktop WeChat status checks, contact search, screenshots, and message sending through window automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent inspect a local Windows WeChat session and send messages to the current or selected contact. It is intended for workflows where desktop WeChat is already open and the user accepts agent-driven input control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send real WeChat messages from the user's account.

Mitigation: Keep WeChat visible, verify the active recipient before sending, and add confirmation gates for sensitive or high-impact messages.

Risk: The skill can capture WeChat window screenshots that may contain private chat content.

Mitigation: Avoid using it for sensitive chats unless screenshot storage, sharing, and retention are controlled.

Risk: Contact search and detached-window handling can target an unintended chat when names or windows are ambiguous.

Mitigation: Use precise contact names and confirm the selected chat window before allowing send actions.

Risk: Clipboard-based message entry can overwrite user clipboard contents.

Mitigation: Preserve and restore clipboard contents around send operations when integrating this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlark/skills/windows-wechat-mcp)
- [OpenLark publisher profile](https://clawhub.ai/user/openlark)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, Python snippets, JSON-like status objects, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may correspond to real desktop actions in the user's WeChat session.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
